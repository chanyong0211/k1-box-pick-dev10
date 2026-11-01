"""gym 등록. 반복문 없이 그대로(dev9 기록 8.bh: 등록이 import 실패를 삼키지 않게)."""

import gymnasium as gym

gym.register(id="Dev10-Pick-K1-v0", entry_point="isaaclab.envs:ManagerBasedRLEnv", disable_env_checker=True,
             kwargs={"env_cfg_entry_point": "pick.env_cfg:K1PickEnvCfg"})
gym.register(id="Dev10-Pick-K1-Eval-v0", entry_point="isaaclab.envs:ManagerBasedRLEnv", disable_env_checker=True,
             kwargs={"env_cfg_entry_point": "pick.env_cfg:K1PickEnvCfg_EVAL"})
