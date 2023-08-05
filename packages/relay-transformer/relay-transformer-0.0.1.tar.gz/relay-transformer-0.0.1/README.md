## Relay Transformer (wip)

My attempt at a Transformer capable of long-range language modeling. The idea is to intersperse within the sequence relay tokens dedicated to passing global information at an extra step where they are all excised and attend to one another only. For even longer sequences, one can imagine restricting relay token attention to be within a fixed window size, and then doing relays of relays.

Will also investigate using cheap linear attention for the relay token attention step.

## Install

```bash
$ pip install relay_transformer
```

## Usage

```python
import torch
from relay_transformer import RelayTransformerLM

lm = RelayTransformerLM(
    num_tokens = 20000,
    dim = 512,
    max_seq_len = 4096,
    depth = 6,
    causal = True,
    window_size = 256,            # local attention window size
    relay_tokens_per_window = 2   # how many relay tokens to intersperse within each local attention window
).cuda()

x = torch.randint(0, 20000, (1, 1024)).cuda()
lm(x) # (1, 1024, 20000)
```
