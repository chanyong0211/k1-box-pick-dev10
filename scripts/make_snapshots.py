"""리셋 스냅숏 4 개 (설계 §6): MuJoCo 에서 dev12 번들로 자리 잡은 실제 상태. CPU. 출력 pick/assets/reset_snapshots.npz."""
import importlib.util

import _harness
import numpy as np

h = _harness.load()
sim, d, m = h["sim"], h["d"], h["m"]
spec = importlib.util.spec_from_file_location("joints12", _harness.PROJECTS / "dev12/source/k1_pelvis/joints.py")
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)
names = h["names"]
order = [names.index(n) for n in J.JOINT_NAMES]
up_order = [names.index(n) for n in J.UPPER_JOINTS]
C = _harness.calib(h)
default = np.asarray(h["c"].default_joint_pos, float)


def target(x):
    q = default.copy()
    if x is not None:
        q[h["ARM"]] = x
    return q


foot = [m.body(n).id for n in ("left_ankle_roll_link", "right_ankle_roll_link")]
rows = {k: [] for k in ("q", "root_pos", "root_quat", "z_cmd", "pitch_cmd", "toe", "up_target")}
for label, z, p, arms in (("서기", 0.765, 0.0, None), ("서기+벌림", 0.765, 0.0, C["xp"]), ("0.50 m", 0.50, 37.0, C["xp"]), ("쪼그림", 0.335, 45.0, C["xp"])):
    sim.place(np.array([3.0, 0.0, h["H"] / 2]), 0.0, 0.0, 1.0, 0.8)
    zc, pc = (z, p) if z > 0.7 else h["cmd"](z, p)
    u0, up = sim.up_t.copy(), target(arms)[sim.up_c]
    for i in range(400):
        sim._tick(zc, pc, u0 + (up - u0) * min((i + 1) / 60, 1.0))
    h["mujoco"].mj_forward(m, d)
    mid = d.xpos[foot].mean(0)
    q = np.zeros(len(names))
    q[:] = d.qpos[sim._qpos]
    root = d.qpos[:3].copy()
    root[:2] -= mid[:2]                                  # 발 중앙을 env 원점에
    rows["q"].append(q[order])
    rows["root_pos"].append(root)
    rows["root_quat"].append(d.qpos[3:7].copy())
    rows["z_cmd"].append(zc)
    rows["pitch_cmd"].append(pc)
    rows["toe"].append(h["toes"]() - mid[0])
    rows["up_target"].append(target(arms)[up_order])
    print(f"{label}: 골반 z {d.qpos[2]:.3f} pitch {sim._pitch():.1f} 발끝(발 중앙 기준) {rows['toe'][-1]:.3f} 골반 x {root[0]:+.3f}", flush=True)
out = _harness.ROOT / "pick/assets/reset_snapshots.npz"
np.savez(out, joint_names=np.array(J.JOINT_NAMES), up_grip=np.array(target(C["xg"])[up_order], np.float32), **{k: np.array(v, np.float32) for k, v in rows.items()})
print("저장", out, flush=True)
