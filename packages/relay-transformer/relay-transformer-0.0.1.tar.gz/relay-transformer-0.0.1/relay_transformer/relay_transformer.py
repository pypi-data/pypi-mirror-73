import torch
from torch import nn
import torch.nn.functional as F

from local_attention import LocalAttention

# helper functions

flat_map = (lambda arr: [sub_el for el in arr for sub_el in el])

# classes

class Residual(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn
    def forward(self, x):
        return x + self.fn(x)

class PreNorm(nn.Module):
    def __init__(self, dim, fn):
        super().__init__()
        self.norm = nn.LayerNorm(dim)
        self.fn = fn
    def forward(self, x, **kwargs):
        x = self.norm(x)
        return self.fn(x, **kwargs)

class FeedForward(nn.Module):
    def __init__(self, dim, mult = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(dim, dim * mult),
            nn.LeakyReLU(inplace = True),
            nn.Linear(dim * mult, dim)
        )
    def forward(self, x, **kwargs):
        return self.net(x)

class FullAttention(nn.Module):
    def __init__(self, causal = False):
        super().__init__()
        self.causal = causal

    def forward(self, q, k, v):
        dots = torch.einsum('bhid,bhjd->bhij', q, k)
        if self.causal:
            mask = torch.ones(*dots.shape[-2:], device=q.device).triu_(diagonal = 1 + dots.shape[-1]).bool()
            dots.masked_fill_(mask, float('-inf'))
            del mask
        attn = dots.softmax(dim=-1)
        return torch.einsum('bhjd,bhij->bhid', v, attn)

class SelfAttention(nn.Module):
    def __init__(self, dim, heads = 8, causal = False, window_size = 256, full_attention = True):
        super().__init__()
        self.heads = heads
        self.to_qkv = nn.Linear(dim, dim * 3, bias = False)
        self.to_out = nn.Linear(dim, dim)
        self.attn = FullAttention(causal = causal) if full_attention else LocalAttention(window_size, causal = causal)

    def forward(self, x):
        b, t, d, h = *x.shape, self.heads
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        merge_heads = lambda t: t.reshape(*t.shape[:2], h, -1).transpose(1, 2)
        q, k, v = map(merge_heads, (q, k, v))
        out = self.attn(q, k, v)
        out = out.transpose(1, 2).reshape_as(x)
        out = self.to_out(out)
        return out

class RelayTransformer(nn.Module):
    def __init__(self, dim, max_seq_len, depth, causal = False, heads = 8, window_size = 256, relay_tokens_per_window = 2):
        super().__init__()
        self.relay_token_emb = nn.Parameter(torch.zeros(1, dim))

        self.window_size = window_size
        self.relay_tokens_per_window = relay_tokens_per_window

        self.relay_attns = nn.ModuleList([Residual(PreNorm(dim, SelfAttention(dim, heads = heads, causal = causal, window_size = window_size, full_attention = True))) for _ in range(depth)])
        self.local_attns = nn.ModuleList([Residual(PreNorm(dim, SelfAttention(dim, heads = heads, causal = causal, window_size = (window_size + relay_tokens_per_window)))) for _ in range(depth)])
        self.feedforwards = nn.ModuleList([Residual(PreNorm(dim, FeedForward(dim))) for _ in range(depth)])

    def forward(self, x):
        b, t, d = x.shape
        relay_token_every = self.window_size // self.relay_tokens_per_window

        # concat relay tokens to input, interspersed evenly throughout sequence

        x = x.reshape(b, -1, relay_token_every, d)
        relay_tokens = self.relay_token_emb[None, None, ...].expand(b, x.shape[1], -1, -1)
        x = torch.cat((relay_tokens, x), dim = 2)
        inp_with_relay_shape = x.shape
        x = x.reshape(b, -1, d)

        # layers of self reflection

        for attn, ff, global_attn in zip(self.local_attns, self.feedforwards, self.relay_attns):

            # slice out relay tokens

            x = x.reshape(*inp_with_relay_shape)
            relay_tokens = x[:, :, 0]

            # have relay tokens attend to each other, passing information from afar

            relay_tokens = global_attn(relay_tokens)
            relay_tokens = relay_tokens.unsqueeze(2)

            # concat relay tokens back to sequence for local attention to extract

            x = torch.cat((relay_tokens, x[:, :, 1:].clone()), dim=2)
            x = x.reshape(b, -1, d)

            # usual self attention for both relay tokens and target sequence

            x = attn(x)
            x = ff(x)

        # remove relay tokens

        x = x.reshape(*inp_with_relay_shape)
        out = x[:, :, 1:].reshape(b, -1, d)
        return out

class RelayTransformerLM(nn.Module):
    def __init__(self, num_tokens, dim, max_seq_len, depth, causal = False, heads = 8, window_size = 256, relay_tokens_per_window = 2):
        super().__init__()
        self.token_emb = nn.Embedding(num_tokens, dim)
        self.transformer = RelayTransformer(dim, max_seq_len, depth, causal = causal, heads = heads, window_size = window_size, relay_tokens_per_window = relay_tokens_per_window)
        self.to_logits = nn.Linear(dim, num_tokens)
    def forward(self, x):
        x = self.token_emb(x)
        x = self.transformer(x)
        return self.to_logits(x)
