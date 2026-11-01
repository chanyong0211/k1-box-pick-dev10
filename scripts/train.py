"""C안 비교 학습 진입점 (설계 §7). dev12 scripts/train.py 꼴: AppLauncher → 벤더링 rsl_rl 2.3.1 → env → OnPolicyRunner. 시작은 사용자 지시 뒤."""

from __future__ import annotations

import argparse
import pathlib
import sys

from isaaclab.app import AppLauncher

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--head", choices=("three", "one"), required=True)
parser.add_argument("--num_envs", type=int, default=4096)
parser.add_argument("--max_iterations", type=int, default=1000)
parser.add_argument("--save_interval", type=int, default=100)
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--run_name", type=str, required=True)
parser.add_argument("--start_level", type=int, default=0)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

sys.path.insert(0, str(ROOT))

import gymnasium as gym  # noqa: E402
from isaaclab.utils.io import dump_yaml  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from k1_pelvis.vendor import assert_vendored, ensure_vendored_rsl_rl  # noqa: E402

ensure_vendored_rsl_rl()
import rsl_rl  # noqa: E402

assert_vendored(rsl_rl)
import rsl_rl.runners.on_policy_runner as opr  # noqa: E402

import pick.env_register  # noqa: E402,F401
from pick.net import make_actor_critic_class  # noqa: E402
from pick.vecenv import PickVecEnv  # noqa: E402

opr.ActorCriticPick = make_actor_critic_class()
TRAIN = {
    "num_steps_per_env": 24, "save_interval": args.save_interval, "empirical_normalization": False, "logger": "tensorboard",
    "policy": {"class_name": "ActorCriticPick", "head": args.head},
    "algorithm": {"class_name": "PPO", "value_loss_coef": 1.0, "use_clipped_value_loss": True, "clip_param": 0.2, "entropy_coef": 0.005, "num_learning_epochs": 5,
                  "num_mini_batches": 4, "learning_rate": 1.0e-3, "schedule": "adaptive", "gamma": 0.99, "lam": 0.95, "desired_kl": 0.01, "max_grad_norm": 1.0},
}


def main() -> None:
    task = "Dev10-Pick-K1-v0"
    cfg = parse_env_cfg(task, device=args.device, num_envs=args.num_envs)
    cfg.seed = args.seed
    cfg.pick_start_level = args.start_level
    env = gym.make(task, cfg=cfg, render_mode=None)
    env.unwrapped.dev12_nan_guard = True
    log_dir = ROOT / "logs" / args.run_name
    log_dir.mkdir(parents=True, exist_ok=True)
    dump_yaml(str(log_dir / "params/env.yaml"), cfg)
    dump_yaml(str(log_dir / "params/agent.yaml"), {**TRAIN, "cli": vars(args)})
    vec = PickVecEnv(env.unwrapped)
    obs, extras = vec.get_observations()
    print(f"[INFO] actor {obs.shape[-1]} critic {extras['observations']['critic'].shape[-1]} actions {vec.num_actions} envs {vec.num_envs} head {args.head}", flush=True)
    runner = opr.OnPolicyRunner(vec, TRAIN, log_dir=str(log_dir), device=str(vec.device))
    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)
    env.close()


main()
simulation_app.close()
