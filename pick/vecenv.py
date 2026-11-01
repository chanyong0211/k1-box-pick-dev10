"""벤더링 rsl_rl 2.3.1 러너 계약. isaaclab 을 import 하지 않는다."""

from __future__ import annotations

import torch


class PickVecEnv:
    def __init__(self, env):
        self.env = env
        self.cfg = env.cfg
        self.num_envs = env.num_envs
        self.num_actions = int(env.action_manager.total_action_dim)
        self.max_episode_length = env.max_episode_length
        self.device = env.device

    @property
    def unwrapped(self):
        return self.env

    @property
    def episode_length_buf(self):
        return self.env.episode_length_buf

    @episode_length_buf.setter
    def episode_length_buf(self, value):
        self.env.episode_length_buf = value

    def _extras(self, extras: dict) -> dict:
        return {"observations": {"critic": self._obs["critic"]}, "time_outs": extras.get("time_outs"), "log": extras.get("log", {})}

    def get_observations(self):
        if not hasattr(self, "_obs"):
            self._obs = self.env.reset()[0]
        return self._obs["policy"], {"observations": {"critic": self._obs["critic"]}}

    def reset(self):
        self._obs = self.env.reset()[0]
        return self._obs["policy"], {"observations": {"critic": self._obs["critic"]}}

    def step(self, actions: torch.Tensor):
        self._obs, rew, term, trunc, extras = self.env.step(actions)
        rew = torch.nan_to_num(rew)
        infos = self._extras(extras)
        if infos["time_outs"] is None:
            infos["time_outs"] = trunc
        rt = self.env.pick_rt
        infos["log"] = {**infos["log"], **rt.log, "Pick/gate_level": float(rt.gate.level)}
        if hasattr(rt, "log_ep"):
            infos["log"].update({f"Pick/ep_{k}": v for k, v in rt.log_ep.items()})
        return self._obs["policy"], rew, (term | trunc).long(), infos
