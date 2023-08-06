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

model = RelayTransformerLM(
    num_tokens = 20000,
    dim = 512,
    max_seq_len = 2048,
    depth = 6,
    causal = True,
    window_size = 256,            # local attention window size
    relay_tokens_per_window = 2,  # how many relay tokens to intersperse within each local attention window
    depth_start_relay_attn = 3,   # the layer at which to begin global attention
    reversible = True,            # use reversible networks, from Reformer paper
).cuda()

x = torch.randint(0, 20000, (1, 2048)).cuda()
model(x) # (1, 2048, 20000)
```

## Citation

```bibtex
@inproceedings{rae-razavi-2020-transformers,
    title = "Do Transformers Need Deep Long-Range Memory?",
    author = "Rae, Jack  and Razavi, Ali",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.672"
}
```

```bibtex
@inproceedings{kitaev2020reformer,
    title       = {Reformer: The Efficient Transformer},
    author      = {Nikita Kitaev and Lukasz Kaiser and Anselm Levskaya},
    booktitle   = {International Conference on Learning Representations},
    year        = {2020},
    url         = {https://openreview.net/forum?id=rkgNKkHtvB}
}
```
