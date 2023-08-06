import torch
from torch import nn
import torch.nn.functional as F

from local_attention import LocalAttention
from relay_transformer.reversible import ReversibleSequence, SequentialSequence

# helper fns

def default(val, d):
    return d if val is None else val

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
        _, _, t, d = q.shape
        dots = torch.einsum('bhid,bhjd->bhij', q, k) * (d ** -0.5)
        if self.causal:
            mask = torch.ones((t, t), device=q.device).triu_(1).bool()
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
        self.attn = FullAttention(causal = causal) if full_attention else LocalAttention(window_size, causal = causal, rel_pos_emb_config = (dim // heads, heads))

    def forward(self, x):
        b, t, d, h = *x.shape, self.heads
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        merge_heads = lambda t: t.reshape(*t.shape[:2], h, -1).transpose(1, 2)
        q, k, v = map(merge_heads, (q, k, v))
        out = self.attn(q, k, v)
        out = out.transpose(1, 2).reshape_as(x)
        out = self.to_out(out)
        return out

class AttentionLayer(nn.Module):
    def __init__(self, dim, heads = 8, causal = False, window_size = 256, relay_tokens_per_window = 2, global_attention = False):
        super().__init__()
        self.heads = heads
        self.global_attn = SelfAttention(dim, causal = causal, heads = heads, full_attention = True) if global_attention else None

        self.ws_with_relays = window_size + relay_tokens_per_window
        self.seq_per_relay = window_size // relay_tokens_per_window
        self.local_attn = SelfAttention(dim, causal = causal, heads = heads, window_size = self.ws_with_relays)

    def forward(self, x, **kwargs):
        b, _, d = x.shape

        if self.global_attn is not None:
            # slice out relay tokens
            x = x.reshape(b, -1, self.seq_per_relay + 1, d)
            relay_tokens = x[:, :, 0]

            # have relay tokens attend to each other, passing information from afar

            relay_tokens = self.global_attn(relay_tokens) + relay_tokens
            relay_tokens = relay_tokens.unsqueeze(2)

            # concat relay tokens back to sequence for local attention to extract

            x = torch.cat((relay_tokens, x[:, :, 1:].clone()), dim=2)
            x = x.reshape(b, -1, d)

        x = self.local_attn(x)
        return x

class RelayTransformer(nn.Module):
    def __init__(self, dim, max_seq_len, depth, causal = False, heads = 8, window_size = 256, relay_tokens_per_window = 2, depth_start_relay_attn = None, reversible = False):
        super().__init__()
        depth_start_relay_attn = default(depth_start_relay_attn, depth // 2)
        assert depth_start_relay_attn > 1 and depth_start_relay_attn <= depth, 'invalid depth for which to start relay attention'

        self.relay_token_emb = nn.Parameter(torch.zeros(1, dim))

        self.window_size = window_size
        self.relay_tokens_per_window = relay_tokens_per_window

        layers = nn.ModuleList([])
        for ind in range(depth):
            layer_num = ind + 1
            relay_attends = layer_num >= depth_start_relay_attn

            attn = PreNorm(dim, AttentionLayer(dim, heads = heads, causal = causal, window_size = window_size, relay_tokens_per_window = relay_tokens_per_window, global_attention = relay_attends))
            feedforward = PreNorm(dim, FeedForward(dim))

            layers.append(nn.ModuleList([attn, feedforward]))

        execute_type = ReversibleSequence if reversible else SequentialSequence
        self.layers = ReversibleSequence(layers)
        self.pad_to_multiple = window_size

    def forward(self, x, **kwargs):
        b, t, d = x.shape
        relay_token_every = self.window_size // self.relay_tokens_per_window

        # concat relay tokens to input, interspersed evenly throughout sequence

        x = x.reshape(b, -1, relay_token_every, d)
        relay_tokens = self.relay_token_emb[None, None, ...].expand(b, x.shape[1], -1, -1)
        x = torch.cat((relay_tokens, x), dim = 2)
        inp_with_relay_shape = x.shape
        x = x.reshape(b, -1, d)

        # attention and feedforward

        x = self.layers(x)

        # remove relay tokens

        x = x.reshape(*inp_with_relay_shape)
        out = x[:, :, 1:].reshape(b, -1, d)
        return out

class RelayTransformerLM(nn.Module):
    def __init__(self, num_tokens, dim, max_seq_len, depth, causal = False, heads = 8, window_size = 256, relay_tokens_per_window = 2, depth_start_relay_attn = None, reversible = False):
        super().__init__()
        assert (window_size % relay_tokens_per_window) == 0, 'window size must be divisible by the relay tokens to be interspersed in it'
        self.max_seq_len = max_seq_len

        self.token_emb = nn.Embedding(num_tokens, dim)
        self.transformer = RelayTransformer(dim, max_seq_len, depth, causal = causal, heads = heads, window_size = window_size, relay_tokens_per_window = relay_tokens_per_window, depth_start_relay_attn = depth_start_relay_attn, reversible = reversible)
        self.to_logits = nn.Linear(dim, num_tokens)
    def forward(self, x, **kwargs):
        x = self.token_emb(x)
        x = self.transformer(x, **kwargs)
        return self.to_logits(x)
