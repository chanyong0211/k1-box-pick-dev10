import pathlib
import sys

import numpy as np
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pick import frozen, layout as L, net  # noqa: E402


def test_sizes():
    assert L.N_OBS == 256 and L.N_ARM_IN == 28 + 11 + 80 + 6 + 5 + 1


def test_obs_mirror_is_involution():
    p, s = L.obs_mirror()
    x = torch.randn(3, L.N_OBS)
    m = x[..., p] * s
    assert torch.allclose(m[..., p] * s, x)


def test_three_head_output_shape_and_arm_equivariance():
    torch.manual_seed(0)
    a = net.ThreeHeadActor()
    for m in a.arm.modules():                    # 끝층 작게 시작한 것과 무관하게 시험
        if isinstance(m, torch.nn.Linear):
            torch.nn.init.normal_(m.weight, std=0.3)
    x = torch.randn(4, L.N_OBS)
    y = a(x)
    assert y.shape == (4, 17)
    p, s = L.obs_mirror()
    ym = a(x[..., p] * s)
    sign = torch.tensor(L.ARM_SIGN)
    assert torch.allclose(ym[:, 7:12], y[:, 12:17] * sign, atol=1e-5)    # 거울 입력의 왼팔 = 원래 오른팔의 거울
    assert torch.allclose(ym[:, 12:17], y[:, 7:12] * sign, atol=1e-5)


def test_left_head_ignores_right_arm_history_but_sees_summary():
    a = net.ThreeHeadActor()
    for m in a.arm.modules():
        if isinstance(m, torch.nn.Linear):
            torch.nn.init.normal_(m.weight, std=0.3)
    x = torch.randn(2, L.N_OBS)
    z = x.clone()
    z[:, L.AR0] += 1.0                           # 오른팔 가장 오래된 위치: 왼팔 머리 입력 아님
    assert torch.allclose(a(z)[:, 7:12], a(x)[:, 7:12])
    z = x.clone()
    z[:, L.HR0] += 1.0                           # 오른손 위치: 요약에 있음
    assert not torch.allclose(a(z)[:, 7:12], a(x)[:, 7:12])


def test_one_head_shape():
    assert net.OneHeadActor()(torch.zeros(2, L.N_OBS)).shape == (2, 17)


def test_init_std_length():
    assert len(net.INIT_STD) == L.N_ACT


def test_frozen_matches_numpy_harness():
    bundle = ROOT.parents[1] / "dev12/deploy/pelvis_34750avg/exported/policy.npz"
    d = np.load(bundle)

    def run(prefix, x):
        ids = sorted({int(k.split(".")[1]) for k in d.files if k.startswith(prefix + ".")})
        for n, i in enumerate(ids):
            x = x @ d[f"{prefix}.{i}.weight"].astype(np.float64).T + d[f"{prefix}.{i}.bias"].astype(np.float64)
            if n < len(ids) - 1:
                x = np.where(x > 0, x, np.expm1(np.minimum(x, 0)))
        return x

    f = frozen.FrozenLower(bundle)
    rng = np.random.default_rng(0)
    o, h = rng.normal(size=(5, 94)) * 0.3, rng.normal(size=(5, 405)) * 0.3
    co = run("encoder", h)
    a = run("actor", np.concatenate([co, o], -1))
    cm = run("encoder", h[:, d["mirror.hist_perm"]] * d["mirror.hist_sign"])
    am = run("actor", np.concatenate([cm, o[:, d["mirror.obs_perm"]] * d["mirror.obs_sign"]], -1))
    want = 0.5 * (a + am[:, d["mirror.act_perm"]] * d["mirror.act_sign"])
    got, code = f(torch.tensor(o, dtype=torch.float32), torch.tensor(h, dtype=torch.float32))
    assert np.abs(got.numpy() - want).max() < 1e-4
    assert np.abs(code.numpy() - co).max() < 1e-4
