"""스모크 ①②③ (설계 §8): 크기·NaN, 스크립트 쥠(Newton), 하체 추종. 학습 없음. 예: --cone elliptic --num_envs 64."""

from __future__ import annotations

import argparse
import pathlib
import sys

from isaaclab.app import AppLauncher

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--num_envs", type=int, default=64)
parser.add_argument("--cone", choices=("elliptic", "pyramidal"), default="elliptic")
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()
app_launcher = AppLauncher(args)
simulation_app = app_launcher.app
sys.path.insert(0, str(ROOT))

import gymnasium as gym  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from isaaclab_tasks.utils import parse_env_cfg  # noqa: E402
from k1_pelvis import feasibility as F  # noqa: E402

import pick.env_register  # noqa: E402,F401
from pick import layout as L, mdp, pure as P  # noqa: E402
from pick.vecenv import PickVecEnv  # noqa: E402

task = "Dev10-Pick-K1-v0"
cfg = parse_env_cfg(task, device=args.device, num_envs=args.num_envs)
cfg.seed = 7
if args.cone == "pyramidal":
    cfg.sim.physics.solver_cfg.cone = "pyramidal"
    cfg.sim.physics.solver_cfg.impratio = 1.0
env = gym.make(task, cfg=cfg, render_mode=None)
u = env.unwrapped
vec = PickVecEnv(u)
obs, ex = vec.get_observations()
rt = u.pick_rt
print(f"① actor {obs.shape} (기대 {L.N_OBS}) critic {ex['observations']['critic'].shape} 행동 {vec.num_actions} (기대 {L.N_ACT}) dev12 {u.obs_buf['dev12_policy'].shape} {u.obs_buf['dev12_hist'].shape}", flush=True)
assert obs.shape[-1] == L.N_OBS and vec.num_actions == L.N_ACT and u.obs_buf["dev12_policy"].shape[-1] == 94 and u.obs_buf["dev12_hist"].shape[-1] == 405
print("   박스 질량", rt.box.data.body_mass.torch[:3, 0].tolist(), "손-박스 μ", rt.mu[:3].tolist(), flush=True)
zero = torch.zeros(vec.num_envs, L.N_ACT, device=u.device)
for _ in range(100):
    obs, r, d, _ = vec.step(zero)
    assert torch.isfinite(obs).all() and torch.isfinite(r).all()
print(f"   100 스텝 NaN 없음, 보상 평균 {r.mean():.3f}, 끝남 {int(d.sum())}, 게이트 {rt.gate.level}", flush=True)

act = rt.action
snap = np.load(mdp.SNAP)
stand_up = snap["up_target"][0]
open_up = snap["up_target"][3]
grip_up = snap["up_grip"]                                # 조임 목표 = 처짐 보정 + 어깨 roll 0.6


def run(steps, z, p, up, v=(0.0, 0.0, 0.0)):
    act.scripted = dict(z=z, p=p, upper=up, v=v)
    for _ in range(steps):
        vec.step(zero)


def report(label):
    p = rt.poses()
    s = rt.reward_state()
    fell = u.termination_manager.terminated
    print(f"   {label}: 골반 z {rt.robot.data.root_link_pos_w.torch[:, 2].mean():.3f}, 힘 왼 {s['n_side'][:, 0].mean():.1f} 오 {s['n_side'][:, 1].mean():.1f} N, "
          f"모서리 p50 {100 * s['min_z'].median():.1f} cm, 3 cm 이상 {100 * (s['min_z'] >= 0.03).float().mean():.0f} %, 기울기 p50 {torch.rad2deg(P.tilt(p['bR'])).median():.1f}°, 끝난 env {int(fell.sum())}", flush=True)


# ② 스크립트 쥠: 고정 입력. 시간 초과가 걸리지 않게 처음부터 다시
print(f"② 스크립트 쥠 ({args.cone}), 발끝 10 cm", flush=True)
rt.gate.sample_box = lambda n, device: (torch.full((n,), P.TOE_TARGET, device=device), torch.zeros(n, device=device), torch.zeros(n, device=device))
rt.gate.update = lambda *a: False
u.episode_length_buf[:] = 0
vec.reset()
zc, pc = 0.335, float(F.lean_rule_deg(torch.tensor(0.335), torch.tensor(45.0), torch.tensor(0.0), False))
run(250, zc, pc, open_up)
report("쪼그림")
run(75, zc, pc, grip_up)
run(50, zc, pc, grip_up)
report("조임")
act.scripted = None
for i in range(125):
    t = (i + 1) / 125
    zt = zc + 0.25 * t
    act.scripted = dict(z=zt, p=float(F.lean_rule_deg(torch.tensor(zt), torch.tensor(pc + (35.0 - pc) * t), torch.tensor(0.0), False)), upper=grip_up)
    vec.step(zero)
run(75, zc + 0.25, 35.0, grip_up)
report("들림")

# ③ 하체 추종: 박스를 멀리
print("③ 하체 추종, 박스 멀리", flush=True)
rt.gate.sample_box = lambda n, device: (torch.full((n,), 1.5, device=device), torch.zeros(n, device=device), torch.zeros(n, device=device))
u.episode_length_buf[:] = 0
vec.reset()
r = rt.robot.data
for label, z, p, v, n in (("서기", 0.765, 0.0, (0.0, 0.0, 0.0), 150), ("0.50 m·37°", 0.50, 37.0, (0.0, 0.0, 0.0), 200), ("0.335 m·45°", 0.335, 45.0, (0.0, 0.0, 0.0), 150), ("0.765 m 앞 0.3", 0.765, 0.0, (0.3, 0.0, 0.0), 200)):
    run(n, z, p, stand_up, v=v)
    print(f"   {label}: z {r.root_link_pos_w.torch[:, 2].mean():.3f} 앞 속도 {r.root_link_lin_vel_b.torch[:, 0].mean():.2f} 끝난 env {int(u.termination_manager.terminated.sum())}", flush=True)
env.close()
simulation_app.close()
