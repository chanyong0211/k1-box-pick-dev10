"""보상 점검 (`reward-design-stillness-check`): MuJoCo 스크립트 궤적을 Isaac 과 같은 순수 보상에 넣어 12 s 합을 비교한다. CPU, 학습 없음."""
import _harness
import numpy as np
import torch

from pick import pure as P

h = _harness.load()
sim, d, m, mj = h["sim"], h["d"], h["m"], h["mujoco"]
C = _harness.calib(h)
DT, T = 0.02, 600
MASS, MU = 1.0, 0.7
foot = [m.body(n).id for n in ("left_ankle_roll_link", "right_ankle_roll_link")]
ARM = h["ARM"]
U = h["_U"]
tensor = lambda x: torch.tensor(x, dtype=torch.float32)[None]  # noqa: E731


def box_R():
    return d.xmat[sim.box].reshape(3, 3).copy()


def sample(cx0):
    R, bp = tensor(box_R()), tensor(d.xpos[sim.box].copy())
    hp = tensor(np.stack([d.xpos[b] for b in sim.hands]))
    hR = tensor(np.stack([d.xmat[b].reshape(3, 3) for b in sim.hands]))
    pc, _ = P.palm(hp, hR)
    pad_box = P.to_box(pc, bp, R)
    n = P.side_normal(tensor(sim.force_on_hands_w().copy()), R)
    mid = d.xpos[foot].mean(0)
    return dict(pad_box=pad_box, n_side=n, mass=tensor(MASS), mu=tensor(MU), min_z=P.box_corners_min_z(bp, R), tilt=P.tilt(R),
                disp=torch.tensor([float(np.hypot(d.xpos[sim.box][0] - cx0, d.xpos[sim.box][1]))]),
                ex=torch.tensor([float(d.xpos[sim.box][0] - mid[0] - (h["toes"]() - mid[0] + P.TOE_TARGET + P.A / 2))]), ey=torch.tensor([float(d.xpos[sim.box][1] - mid[1])]), eyaw=torch.zeros(1),
                tau_arm=tensor(d.actuator_force[sim._actuators][ARM].copy()), act=torch.zeros(1, 17), act_prev=torch.zeros(1, 17), limit=torch.zeros(1), waist=torch.zeros(1), body_box=torch.zeros(1))


def run(label, script, walk=None):
    h["set_contact"]("grasp")
    h["set_kp"](1.0)
    cx = C["toe"] + P.TOE_TARGET + P.A / 2
    sim.place(np.array([cx, 0.0, P.H / 2]), 0.0, 0.0, MASS, MU)
    if walk is not None:
        orig = sim.cmd.set
        sim.cmd.set = lambda stand, v=(0, 0, 0), z=.765, pitch=0., roll=0.: orig(False, walk, z, pitch, roll)
    tot = {k: 0.0 for k in P.WEIGHTS}
    best, fell = 0.0, False
    for t in range(T):
        z, p, up = script(t)
        sim._tick(z, p, up)
        if d.qpos[2] < 0.25 or d.xmat[sim.pelvis][8] < 0.3:
            fell = True
        parts = P.rewards(sample(cx))
        for k, v in parts.items():
            tot[k] += P.WEIGHTS[k] * float(v) * DT
        best = max(best, float(parts["hold"]))
    r = sum(tot.values())
    print(f"{label:22s} | 합 {r:7.1f} | " + " ".join(f"{k} {v:.1f}" for k, v in tot.items() if abs(v) > 0.05) + f" | 넘어짐 {fell} 성공상태 {best:.0f}", flush=True)


u0 = np.asarray(sim.up_t, float).copy()
zc, pc = h["cmd"](0.335, 45.0)
up, ug = U(C["xp"]), U(C["xg"])
ug_left = up.copy()
L = [i for i, n in enumerate(h["names"][j] for j in sim.up_c) if n.startswith("left")]
ug_left[L] = ug[L]
ramp = lambda a, b, t, n: a + (b - a) * min(t / n, 1.0)  # noqa: E731


def lift(t):
    if t < 80:
        return 0.765, 0.0, ramp(u0, up, t, 60)
    if t < 330:
        return zc, pc, up
    if t < 405:
        return zc, pc, ramp(up, ug, t - 330, 75)
    if t < 455:
        return zc, pc, ug
    k = min((t - 455) / 125, 1.0)
    zt = zc + 0.25 * k
    return zt, float(h["F"].lean_rule_deg(zt, pc + (35.0 - pc) * k, 0.0, False)), ug


def crouch(t):
    return (0.765, 0.0, ramp(u0, up, t, 60)) if t < 80 else (zc, pc, up)


def one_hand(t):
    if t < 80:
        return 0.765, 0.0, ramp(u0, up, t, 60)
    if t < 330:
        return zc, pc, up
    return zc, pc, ramp(up, ug_left, t - 330, 75)


print("시나리오 | 12 s 합 | 항별", flush=True)
run("가만히 서기", lambda t: (0.765, 0.0, u0))
run("쪼그려 팔 벌리고 멈춤", crouch)
run("한 손만 조임", one_hand)
run("앞으로 걸어 밀기", lambda t: (0.765, 0.0, u0), walk=(0.3, 0.0, 0.0))
run("스크립트 들기", lift)
