"""C안 actor(세 머리)·대조군(한 머리) (설계 §2). 입력 정규화 없음: 거울이 정확히 성립해야 한다."""

from __future__ import annotations

import torch
import torch.nn as nn

from pick import layout as L


def mlp(n_in: int, hidden, n_out: int) -> nn.Sequential:
    layers: list[nn.Module] = []
    for h in hidden:
        layers += [nn.Linear(n_in, h), nn.ELU()]
        n_in = h
    last = nn.Linear(n_in, n_out)
    nn.init.zeros_(last.bias)
    last.weight.data *= 0.01                   # 처음 행동이 거의 0: 델타 출력이라 제자리에서 시작
    return nn.Sequential(*layers, last)


class ThreeHeadActor(nn.Module):
    """몸통 = 전체 입력, 왼팔 = 슬라이스, 오른팔 = 같은 왼팔 망에 거울 입력 → 출력 거울."""

    def __init__(self, body_hidden=(512, 256, 128), arm_hidden=(256, 128, 64)):
        super().__init__()
        self.body = mlp(L.N_OBS, body_hidden, L.N_BODY_OUT)
        self.arm = mlp(L.N_ARM_IN, arm_hidden, L.N_ARM_OUT)
        for name, side in (("left", 0), ("right", 1)):
            i, s = L.arm_indices(side)
            self.register_buffer(f"{name}_i", i, persistent=False)
            self.register_buffer(f"{name}_s", s, persistent=False)
        self.register_buffer("arm_sign", torch.tensor(L.ARM_SIGN), persistent=False)

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        left = self.arm(obs[..., self.left_i])
        right = self.arm(obs[..., self.right_i] * self.right_s) * self.arm_sign
        return torch.cat([self.body(obs), left, right], -1)


class OneHeadActor(nn.Module):
    """대조군 ①: 같은 입력 → 한 망 → 17."""

    def __init__(self, hidden=(512, 256, 128)):
        super().__init__()
        self.net = mlp(L.N_OBS, hidden, L.N_ACT)

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        return self.net(obs)


# 시작 탐색 폭: 걸음, 자세, 허리, 팔 (설계 §3)
INIT_STD = [0.2, 0.2, 0.2] + [0.5, 0.5, 0.3] + [0.1] + [0.5] * 10


def make_actor_critic_class():
    """벤더링 rsl_rl 을 import 한 뒤에 부른다(러너가 클래스 이름으로 찾는다)."""
    from rsl_rl.modules import ActorCritic

    class ActorCriticPick(ActorCritic):
        def __init__(self, num_actor_obs, num_critic_obs, num_actions, head: str = "three", critic_hidden=(512, 256, 128), **kw):
            assert num_actor_obs == L.N_OBS and num_actions == L.N_ACT, (num_actor_obs, num_actions)
            super().__init__(num_actor_obs, num_critic_obs, num_actions, actor_hidden_dims=[32], critic_hidden_dims=list(critic_hidden),
                             activation="elu", init_noise_std=1.0, noise_std_type="scalar", **kw)
            self.actor = ThreeHeadActor() if head == "three" else OneHeadActor()
            self.std = nn.Parameter(torch.tensor(INIT_STD))

    return ActorCriticPick
