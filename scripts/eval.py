"""저장본 평가 (설계 §7): 결정적 행동, 수준 고정, 끝난 에피소드 성공률·3 cm 들림·두 손 접촉률·기울기·넘어짐."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from isaaclab.app import AppLauncher

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--checkpoint", required=True, help="절대 경로")
parser.add_argument("--head", choices=("three", "one"), required=True)
parser.add_argument("--level", type=int, default=0)
parser.add_argument("--num_envs", type=int, default=512)
parser.add_argument("--seed", type=int, default=100)
parser.add_argument("--out", default=None)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app_launcher = AppLauncher(args)
simulation_app = app_launcher.app
sys.path.insert(0, str(ROOT))

import gymnasium as gym  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from k1_pelvis.vendor import ensure_vendored_rsl_rl  # noqa: E402

ensure_vendored_rsl_rl()
import pick.env_register  # noqa: E402,F401
from pick import net, pure as P  # noqa: E402
from pick.vecenv import PickVecEnv  # noqa: E402


def main() -> None:
    task = "Dev10-Pick-K1-Eval-v0"
    cfg = parse_env_cfg(task, device=args.device, num_envs=args.num_envs)
    cfg.seed = args.seed
    cfg.pick_start_level = args.level
    env = gym.make(task, cfg=cfg, render_mode=None)
    env.unwrapped.dev12_nan_guard = True
    vec = PickVecEnv(env.unwrapped)
    actor = net.ThreeHeadActor() if args.head == "three" else net.OneHeadActor()
    sd = torch.load(args.checkpoint, map_location="cpu", weights_only=False)["model_state_dict"]
    actor.load_state_dict({k[len("actor."):]: v for k, v in sd.items() if k.startswith("actor.")})
    actor = actor.to(vec.device).eval()
    rt = env.unwrapped.pick_rt if hasattr(env.unwrapped, "pick_rt") else None
    obs, _ = vec.reset()
    rt = env.unwrapped.pick_rt
    rt.gate.update = lambda *a: False                      # 수준 고정
    E = vec.num_envs
    res = {k: [] for k in ("success", "lift3", "both", "fell", "tilt")}
    tilt_now = torch.zeros(E, device=vec.device)
    prev = {}
    T = int(vec.max_episode_length) * 2 + 10
    with torch.no_grad():
        for _ in range(T):
            prev = dict(success=rt.success.clone(), lifted=rt.lifted.clone(), both=rt.both_steps.clone(), len=env.unwrapped.episode_length_buf.clone().float())
            tilt_now = P.tilt(rt.poses()["bR"])
            obs, _, dones, infos = vec.step(actor(obs))
            done = dones.bool()
            if done.any():
                fell = done & ~infos["time_outs"].bool()
                res["success"] += prev["success"][done].float().tolist()
                res["lift3"] += prev["lifted"][done].float().tolist()
                res["both"] += (prev["both"][done] / prev["len"][done].clamp(min=1)).tolist()
                res["fell"] += fell[done].float().tolist()
                res["tilt"] += torch.rad2deg(tilt_now[done]).tolist()
    out = {"checkpoint": args.checkpoint, "level": args.level, "episodes": len(res["success"]), **{k: float(np.mean(v)) if v else None for k, v in res.items()},
           "tilt_p90": float(np.percentile(res["tilt"], 90)) if res["tilt"] else None}
    print(json.dumps(out, ensure_ascii=False), flush=True)
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(out, ensure_ascii=False))
    env.close()


main()
simulation_app.close()
