"""동결 dev12 번들 (policy.npz) 의 배치 torch 판: 행동 = (π(o) + M_a π(M_o o, M_h h)) / 2. 하네스 sim2sim_pelvis.Policy 와 같다."""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn


def _mlp(d, prefix: str) -> nn.Sequential:
    ids = sorted({int(k.split(".")[1]) for k in d.files if k.startswith(prefix + ".")})
    layers: list[nn.Module] = []
    for n, i in enumerate(ids):
        w, b = d[f"{prefix}.{i}.weight"], d[f"{prefix}.{i}.bias"]
        lin = nn.Linear(w.shape[1], w.shape[0])
        lin.weight.data, lin.bias.data = torch.tensor(w, dtype=torch.float32), torch.tensor(b, dtype=torch.float32)
        layers.append(lin)
        if n < len(ids) - 1:
            layers.append(nn.ELU())
    return nn.Sequential(*layers)


class FrozenLower(nn.Module):
    def __init__(self, npz_path):
        super().__init__()
        d = np.load(npz_path)
        self.encoder, self.actor = _mlp(d, "encoder"), _mlp(d, "actor")
        assert "mirror.act_perm" in d.files and "fast_clock" not in d.files, "거울 평균 판, 빠른 재학습 전 번들만"
        for k in ("obs", "hist", "act"):
            self.register_buffer(f"{k}_p", torch.tensor(d[f"mirror.{k}_perm"], dtype=torch.long))
            self.register_buffer(f"{k}_s", torch.tensor(d[f"mirror.{k}_sign"], dtype=torch.float32))
        self.requires_grad_(False)
        self.eval()

    @torch.no_grad()
    def forward(self, obs: torch.Tensor, hist: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        code = self.encoder(hist)
        a = self.actor(torch.cat([code, obs], -1))
        code_m = self.encoder(hist[..., self.hist_p] * self.hist_s)
        am = self.actor(torch.cat([code_m, obs[..., self.obs_p] * self.obs_s], -1))
        return 0.5 * (a + am[..., self.act_p] * self.act_s), code
