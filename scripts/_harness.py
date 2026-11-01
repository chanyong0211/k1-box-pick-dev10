"""MuJoCo dev12 하네스 불러오기: dev12/reports/2026-10-30_throw_catch/floor_lift/fl.py (쪼그린 실제 자세 IK·처짐 보정). 읽기만 한다."""
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS = ROOT.parents[1]
FL = PROJECTS / "dev12/reports/2026-10-30_throw_catch/floor_lift"
sys.path.insert(0, str(ROOT))


def load() -> dict:
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    ns = {"__name__": "fl_harness", "__file__": str(FL / "fl.py")}
    exec(compile((FL / "fl.py").read_text(), str(FL / "fl.py"), "exec"), ns)
    return ns


def calib(h: dict, z: float = 0.335, dist: float = 0.10, squeeze: float = 0.6) -> dict:
    """fl.episode2 앞부분: 상자 없이 쪼그린 실제 자세에서 IK + 처짐 보정. 팔 목표(벌림·조임)를 돌려준다."""
    sim, d, np = h["sim"], h["d"], h["np"]
    I = h["ik"](z, 0.10, "far")
    h["set_contact"]("grasp")
    h["set_kp"](1.0)
    sim.place(np.array([3.0, 0.0, h["H"] / 2]), 0.0, 0.0, 1.0, 0.8)
    zc, pc = h["cmd"](z, 45.0)
    u0 = sim.up_t.copy()
    upre = h["_U"](I["xp"])
    for i in range(250):
        sim._tick(zc, pc, u0 + (upre - u0) * min((i + 1) / 60, 1.0))
    comp = np.zeros(10)
    for _ in range(2):
        base, qv, toe = d.qpos.copy(), d.qvel.copy(), h["toes"]()
        cx = toe + dist + h["A"] / 2
        _, x0, *_ = h["solve"](base, cx, "far", x0s=[I["x0"]])
        _, xp, *_ = h["solve"](base, cx, "far", off=0.06, x0s=[x0])
        d.qpos[:] = base
        d.qvel[:] = qv
        h["set_box"](3.0)
        h["mujoco"].mj_forward(h["m"], d)
        for _ in range(30):
            sim._tick(zc, pc, h["_U"](xp + comp))
        comp = comp + (xp - d.qpos[h["Q"]])
        for _ in range(70):
            sim._tick(zc, pc, h["_U"](xp + comp))
    xg = x0 + comp
    for i, s in h["SIGN"].items():
        xg[i] += s * squeeze
    return dict(xp=xp + comp, xg=xg, toe=float(toe))
