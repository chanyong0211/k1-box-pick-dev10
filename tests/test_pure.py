import math
import pathlib
import sys

import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pick import pure as P  # noqa: E402


def test_pad_centre_matches_v2_pad_local():
    sys.path.insert(0, str(ROOT.parent / "sonic_pick"))
    import importlib.util

    s = importlib.util.spec_from_file_location("v2pure", ROOT.parent / "sonic_pick/env/pure.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    assert torch.allclose(P.pad_center_local(), m.pad_local().mean(1), atol=1e-6)


def _grip(dx=-0.03, dz=0.10):
    return torch.tensor([[[dx, P.W / 2, dz], [dx, -P.W / 2, dz]]])


def test_line_features_level_centre():
    a, d = P.line_features(torch.tensor([[[0.0, P.W / 2, 0.0], [0.0, -P.W / 2, 0.0]]]))
    assert a.item() < 1e-3 and d.item() < 1e-6


def test_line_distance_is_offset():
    a, d = P.line_features(_grip())
    assert a.item() < 1e-3 and abs(d.item() - math.hypot(0.03, 0.10)) < 1e-5


def test_hand_features_shape_and_plane_sign():
    palm = torch.tensor([[[0.5, P.W / 2 + 0.02, 0.1], [0.5, -P.W / 2 - 0.02, 0.1]]])
    n = torch.tensor([[[0.0, -1.0, 0.0], [0.0, 1.0, 0.0]]])
    f = P.hand_features(palm, n, torch.tensor([[0.5, 0.0, 0.0]]), torch.zeros(1))
    assert f.shape == (1, 2, 11)
    assert abs(f[0, 0, 6].item() - 0.02) < 1e-6 and abs(f[0, 1, 6].item() - 0.02) < 1e-6


def test_side_normal_only_outward():
    R = torch.eye(3)[None]
    f = torch.tensor([[[0.0, 10.0, 0.0], [0.0, 10.0, 0.0]]])       # 왼손은 바깥(+y), 오른손은 안쪽(+y)
    n = P.side_normal(f, R)
    assert n[0, 0] == 10.0 and n[0, 1] == 0.0


def test_corners_and_tilt():
    assert abs(P.box_corners_min_z(torch.tensor([[0.0, 0.0, P.H / 2]]), torch.eye(3)[None]).item()) < 1e-6
    th = torch.tensor(0.3)
    Ry = torch.tensor([[[torch.cos(th), 0, torch.sin(th)], [0, 1, 0], [-torch.sin(th), 0, torch.cos(th)]]])
    assert abs(P.tilt(Ry).item() - 0.3) < 1e-5


def _state(**k):
    s = dict(pad_box=_grip(), n_side=torch.tensor([[30.0, 30.0]]), mass=torch.tensor([1.0]), mu=torch.tensor([0.8]), min_z=torch.tensor([0.2]),
             tilt=torch.tensor([0.05]), disp=torch.tensor([0.0]), ex=torch.zeros(1), ey=torch.zeros(1), eyaw=torch.zeros(1), tau_arm=torch.zeros(1, 10),
             act=torch.zeros(1, 17), act_prev=torch.zeros(1, 17), limit=torch.zeros(1), waist=torch.zeros(1), body_box=torch.zeros(1))
    s.update(k)
    return s


def test_full_grip_rewards_are_at_their_top():
    p = P.rewards(_state())
    assert p["reach"].item() > 0.99 and p["grip"].item() == 1.0 and p["hold"].item() == 1.0
    assert p["lift"].item() > 0.97 and p["align"].item() == 1.0


def test_one_hand_earns_no_grip_lift_or_hold():
    p = P.rewards(_state(n_side=torch.tensor([[30.0, 0.0]])))
    assert p["grip"].item() == 0.0 and p["lift"].item() == 0.0 and p["hold"].item() == 0.0 and p["cone"].item() == 0.0


def test_tilted_box_fails_success():
    assert P.rewards(_state(tilt=torch.tensor([math.radians(25.0)])))["hold"].item() == 0.0


def test_push_only_counts_while_low():
    assert P.rewards(_state(min_z=torch.tensor([0.0]), disp=torch.tensor([0.15])))["push"].item() > 0.09
    assert P.rewards(_state(min_z=torch.tensor([0.2]), disp=torch.tensor([0.15])))["push"].item() == 0.0


def test_gate_needs_episodes_and_success():
    g = P.Gate()
    assert not g.update(8000, 8000) and g.level == 0
    assert g.update(500, 500) and g.level == 1
    assert not g.update(9000, 100) and g.level == 1 and g.episodes == 0


def test_gate_sample_in_range():
    g = P.Gate(3)
    d, lat, yaw = g.sample_box(1000, "cpu")
    assert d.min() >= 0.08 and d.max() <= 0.40 and lat.abs().max() <= 0.10 and yaw.abs().max() <= math.radians(20.0)


def test_estimator_holds_when_not_seen():
    e = P.BoxEstimator(2, 0.02, "cpu")
    ids = torch.arange(2)
    pose = torch.tensor([[1.0, 0, 0.146, 0], [1.0, 0, 0.146, 0]])
    e.reset(ids, pose)
    e.delay[:] = 1
    e.bias[:] = 0.0
    e.step(pose, torch.ones(2, dtype=torch.bool))
    v = e.step(pose, torch.ones(2, dtype=torch.bool))
    assert v[1].all() and abs(v[2][0].item() - 0.02) < 1e-6
    moved = pose + torch.tensor([0.5, 0, 0, 0])
    e.step(moved, torch.zeros(2, dtype=torch.bool))
    last, vis, age = e.step(moved, torch.zeros(2, dtype=torch.bool))
    assert not vis.any() and abs(last[0, 0].item() - 1.0) < 1e-6 and age[0].item() > 0.03


def test_camera_sees_ahead_and_down_when_leaning():
    """깊이 레이 측정(11-01): 서면 발끝 앞 0.4 m 안 안 보임, 숙이면 보임. 몸통 틀 근사."""
    torso = torch.tensor([[0.0, 0.0, 1.0]])
    upright = torch.eye(3)[None]
    assert not P.box_visible(torch.tensor([[0.45, 0.0, 0.146]]), torso, upright).item()
    assert P.box_visible(torch.tensor([[3.0, 0.0, 0.146]]), torso, upright).item()
    s, c = math.sin(math.radians(45)), math.cos(math.radians(45))
    lean = torch.tensor([[[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]])
    assert P.box_visible(torch.tensor([[0.60, 0.0, 0.146]]), torch.tensor([[0.0, 0.0, 0.70]]), lean).item()
