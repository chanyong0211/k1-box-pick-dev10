"""박스 기하·보상·게이트·박스 추정 (설계 §4–6). torch 만 쓴다: 호스트 시험, MuJoCo 점검, Isaac 환경이 같은 코드.

틀: "h" = 골반 heading 틀(원점 골반, x = 골반 yaw, z 위), 박스 틀 = 박스 중심, x 깊이, y 폭, z 위.
손 지수 0 = 왼손(박스 +y 면), 1 = 오른손(−y 면)."""

from __future__ import annotations

import math

import torch

BOX = (0.371, 0.405, 0.292)            # 실측 상자 (v2 scene)
A, W, H = BOX
G = 9.81
CONTACT_N = 5.0                        # 접촉 판정 (v2)
# 고무 손 패드 평면 (dev10 v2 pure, MuJoCo 메시 hull): 왼손 링크 틀, 오른손은 y 반대. 패드 중심 = 표본 평균.
PAD_N = (-0.052, -0.997, -0.049)
PAD_D = 0.028
TARGET = (-0.03, 0.10)                 # 손 목표: 박스 중심 3 cm 뒤·10 cm 위 (dev12 floor_lift 시험, 기울기 ≈ atan(3/10))
TOE_TARGET = 0.10                      # 발끝–박스 (floor_lift·descend 시험: 10 cm 에서만 들림)
ARM_CONT_NM = 10.6                     # QC060 연속 토크
SUCCESS_Z, SUCCESS_TILT, SUCCESS_HOLD_S = 0.15, math.radians(20.0), 1.0
LIFT_FULL = 0.20

# 렌즈(IR1) 장착: dev10/source/k1_boxlift/depth_spec.py (실측, 다시 재지 않음)
CAM_POS = (0.039, 0.0175, 0.482)
CAM_QUAT_WXYZ = (0.498716, 0.506874, -0.507635, -0.486485)   # MuJoCo 카메라 규약 (−z 앞, +y 위)
FX, PPX, PPY, IMG_W, IMG_H = 386.5288391113281, 318.2183837890625, 240.0052032470703, 640, 480

WEIGHTS = {"reach": 1.0, "align": 0.5, "grip": 2.0, "cone": 1.0, "lift": 6.0, "hold": 6.0, "push": -2.0, "tilt": -1.0,
           "arm_torque": -0.02, "action_rate": -0.01, "overflow": -0.1, "limit": -1.0, "waist": -0.1, "body_box": -0.5}
TERMINATION_WEIGHT = -100.0


def pad_center_local() -> torch.Tensor:
    """(2, 3) 손 링크 틀 패드 중심. 표본 격자 평균 (v2 pad_local 과 같은 범위: x 0.07–0.27)."""
    x = torch.linspace(0.07, 0.27, 6)
    t = (x - 0.07) / 0.20
    z_lo, z_hi = -0.015 - 0.022 * t, 0.010 + 0.019 * t
    z = z_lo[:, None] + (z_hi - z_lo)[:, None] * torch.linspace(0.0, 1.0, 4)[None, :]
    xx = x[:, None].expand(6, 4)
    nx, ny, nz = PAD_N
    y = (PAD_D - nx * xx - nz * z) / ny
    left = torch.stack([xx, y, z], -1).reshape(-1, 3).mean(0)
    return torch.stack([left, left * torch.tensor([1.0, -1.0, 1.0])])


def palm(hand_pos: torch.Tensor, hand_R: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """패드 중심 (E,2,3), 손바닥 법선 (E,2,3). hand_pos·hand_R = 어떤 틀 <- 손 링크."""
    c = pad_center_local().to(hand_pos.device, hand_pos.dtype)
    n = torch.tensor([PAD_N, (PAD_N[0], -PAD_N[1], PAD_N[2])], device=hand_pos.device, dtype=hand_pos.dtype)
    return hand_pos + torch.einsum("ehij,hj->ehi", hand_R, c), torch.einsum("ehij,hj->ehi", hand_R, n)


def rot_z(yaw: torch.Tensor) -> torch.Tensor:
    c, s = torch.cos(yaw), torch.sin(yaw)
    o, i = torch.zeros_like(c), torch.ones_like(c)
    return torch.stack([c, -s, o, s, c, o, o, o, i], -1).reshape(*yaw.shape, 3, 3)


def to_box(p: torch.Tensor, box_pos: torch.Tensor, box_R: torch.Tensor) -> torch.Tensor:
    """점 (E,K,3) → 박스 틀. box_R = 같은 틀 <- 박스."""
    return torch.einsum("eji,ekj->eki", box_R, p - box_pos[:, None, :])


def line_features(pad_box: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """접촉선(패드를 옆면에 투영한 두 점)의 면 법선과의 각 [rad], 박스 중심과의 거리 [m]. (E,)."""
    pl = pad_box[:, 0] * torch.tensor([1.0, 0.0, 1.0], device=pad_box.device) + torch.tensor([0.0, W / 2, 0.0], device=pad_box.device)
    pr = pad_box[:, 1] * torch.tensor([1.0, 0.0, 1.0], device=pad_box.device) + torch.tensor([0.0, -W / 2, 0.0], device=pad_box.device)
    v = pl - pr
    u = v / v.norm(dim=-1, keepdim=True).clamp(min=1e-6)
    angle = torch.acos(u[:, 1].clamp(-1.0, 1.0))
    dist = torch.cross(pl, u, dim=-1).norm(dim=-1)
    return angle, dist


def hand_features(palm_h: torch.Tensor, normal_h: torch.Tensor, box_pos_h: torch.Tensor, box_yaw_h: torch.Tensor) -> torch.Tensor:
    """손마다 11 (E,2,11): 손바닥 3, 법선 3, 면까지 부호 거리, 면 위 위치 2(정규화), 접촉선 각, 접촉선 거리. 박스는 추정값."""
    R = rot_z(box_yaw_h)
    b = to_box(palm_h, box_pos_h, R)
    side = torch.tensor([1.0, -1.0], device=b.device, dtype=b.dtype)
    plane = b[..., 1] * side - W / 2
    on_face = torch.stack([b[..., 0] / (A / 2), b[..., 2] / (H / 2)], -1)
    angle, dist = line_features(b)
    n = angle.shape[0]
    return torch.cat([palm_h, normal_h, plane[..., None], on_face, angle[:, None, None].expand(n, 2, 1), dist[:, None, None].expand(n, 2, 1)], -1)


def side_normal(force_on_hand: torch.Tensor, box_R: torch.Tensor) -> torch.Tensor:
    """손마다 옆면 수직 힘 (E,2) ≥ 0: 박스가 손을 바깥으로 미는 성분."""
    lat = box_R[:, :, 1]
    along = (force_on_hand * lat[:, None, :]).sum(-1)
    return torch.stack([along[:, 0], -along[:, 1]], -1).clamp(min=0.0)


def box_corners_min_z(box_pos: torch.Tensor, box_R: torch.Tensor) -> torch.Tensor:
    s = torch.tensor([[a * A / 2, b * W / 2, c * H / 2] for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)], device=box_pos.device, dtype=box_pos.dtype)
    return (box_pos[:, None] + torch.einsum("eij,kj->eki", box_R, s))[..., 2].min(1).values


def tilt(box_R: torch.Tensor) -> torch.Tensor:
    return torch.acos(box_R[:, 2, 2].clamp(-1.0, 1.0))


def required_squeeze(mass: torch.Tensor, mu: torch.Tensor) -> torch.Tensor:
    return mass * G / (2.0 * mu)


def is_success_state(min_z, tlt, n_side) -> torch.Tensor:
    return (min_z >= SUCCESS_Z) & (tlt <= SUCCESS_TILT) & (n_side > CONTACT_N).all(-1)


def rewards(s: dict) -> dict:
    """항별 값 (E,). 입력 s: pad_box (E,2,3) 참 박스 틀, n_side (E,2), mass, mu, min_z, tilt, disp (박스 수평 이동 m), ex, ey, eyaw (발끝 목표 오차),
    tau_arm (E,10), act (E,17), act_prev (E,17), limit (E,) 소프트 한계 넘음 합, waist (E,), body_box (E,) 무릎·몸 힘 N."""
    pb, n = s["pad_box"], s["n_side"]
    side = torch.tensor([1.0, -1.0], device=pb.device, dtype=pb.dtype)
    tgt = torch.stack([torch.full_like(side, TARGET[0]), side * W / 2, torch.full_like(side, TARGET[1])], -1)
    d = (pb - tgt).norm(dim=-1)
    near = 0.5 * torch.exp(-d.square() / 0.5**2) + 0.5 * torch.exp(-d.square() / 0.1**2)
    both = (n > CONTACT_N).all(-1)
    need = 1.5 * required_squeeze(s["mass"], s["mu"])
    angle, ldist = line_features(pb)
    cone = ((torch.atan(s["mu"]) - angle) / 0.2).clamp(0.0, 1.0) * torch.exp(-(ldist / 0.1).square())
    low = (s["min_z"] < 0.03).float()
    lifted = (s["min_z"] >= 0.03).float()
    excess = (s["tau_arm"].abs() - ARM_CONT_NM).clamp(min=0.0)
    over = (s["act"].abs() - 1.0).clamp(min=0.0)
    return {
        "reach": 0.5 * (near.mean(-1) + near.min(-1).values),
        "align": torch.exp(-(s["ex"] / 0.05).square() - (s["ey"] / 0.05).square() - (s["eyaw"] / 0.15).square()),
        "grip": (n.min(-1).values / need.clamp(min=1.0)).clamp(max=1.5) / 1.5,
        "cone": both.float() * cone,
        "lift": both.float() * (s["min_z"] / LIFT_FULL).clamp(0.0, 1.0) * torch.exp(-(s["tilt"] / 0.35).square()),
        "hold": is_success_state(s["min_z"], s["tilt"], n).float(),
        "push": low * (s["disp"] - 0.05).clamp(min=0.0),
        "tilt": lifted * s["tilt"].square(),
        "arm_torque": excess.square().sum(-1),
        "action_rate": (s["act"] - s["act_prev"]).square().sum(-1),
        "overflow": over.square().sum(-1),
        "limit": s["limit"],
        "waist": s["waist"].square(),
        "body_box": (s["body_box"] > 20.0).float(),
    }


def total(parts: dict) -> torch.Tensor:
    return sum(WEIGHTS[k] * v for k, v in parts.items())


# ---------------------------------------------------------------- 게이트 (설계 §6)
LEVELS = (  # 앞(발끝) m, 옆 m, yaw °, 앞뒤 걸음, 옆·회전 걸음, 허리·roll
    ((0.08, 0.12), 0.03, 3.0, False, False, False),
    ((0.08, 0.20), 0.05, 5.0, True, False, False),
    ((0.08, 0.30), 0.05, 10.0, True, True, False),
    ((0.08, 0.40), 0.10, 20.0, True, True, False),
    ((0.08, 0.40), 0.10, 20.0, True, True, True),
)
GATE_MIN_EPISODES, GATE_SUCCESS = 8192, 0.60


class Gate:
    """지난 수준에서 끝난 에피소드 수·성공률로 한 단계씩 올린다. 내림 없음. 수준 하나 = 전역."""

    def __init__(self, level: int = 0):
        self.level, self.episodes, self.successes = level, 0, 0

    def update(self, n_done: int, n_success: int) -> bool:
        self.episodes += n_done
        self.successes += n_success
        if self.level < len(LEVELS) - 1 and self.episodes >= GATE_MIN_EPISODES:
            up = self.successes / self.episodes >= GATE_SUCCESS
            self.episodes, self.successes = 0, 0
            if up:
                self.level += 1
                return True
        return False

    def sample_box(self, n: int, device) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """발끝–가까운 모서리 거리, 옆, yaw [rad]."""
        (lo, hi), lat, yaw_deg = LEVELS[self.level][:3]
        r = torch.rand(n, 3, device=device)
        return lo + (hi - lo) * r[:, 0], lat * (2 * r[:, 1] - 1), math.radians(yaw_deg) * (2 * r[:, 2] - 1)


def box_centre_ahead(dist: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
    """발끝에서 가까운 모서리까지 dist 일 때 박스 중심 앞 거리 (v2 gates.box_centre_ahead)."""
    a = yaw.abs()
    return dist + A / 2 * torch.cos(a) + W / 2 * torch.sin(a)


# ---------------------------------------------------------------- 박스 추정: teacher 입력 = 참값 + student 수준 오차 (10-26)
class BoxEstimator:
    """세계 틀 박스 (x, y, z, yaw). 에피소드 편향 ±5 cm·±10°, 깊이 나이 20–100 ms(1–5 스텝), 안 보이면 마지막 값 유지."""

    def __init__(self, n: int, dt: float, device, max_delay: int = 5, pos_bias: float = 0.05, yaw_bias_deg: float = 10.0):
        self.dt, self.device, self.max_delay = dt, device, max_delay
        self.pos_bias, self.yaw_bias = pos_bias, math.radians(yaw_bias_deg)
        self.buf = torch.zeros(max_delay + 1, n, 5, device=device)      # 값 4 + 보임 1, [0] = 지금
        self.bias = torch.zeros(n, 4, device=device)
        self.delay = torch.ones(n, dtype=torch.long, device=device)
        self.last = torch.zeros(n, 4, device=device)
        self.age = torch.zeros(n, device=device)
        self.seen = torch.zeros(n, dtype=torch.bool, device=device)

    def reset(self, ids: torch.Tensor, pose_w: torch.Tensor) -> None:
        m = len(ids)
        r = 2 * torch.rand(m, 4, device=self.device) - 1
        self.bias[ids] = r * torch.tensor([self.pos_bias, self.pos_bias, self.pos_bias, self.yaw_bias], device=self.device)
        self.delay[ids] = torch.randint(1, self.max_delay + 1, (m,), device=self.device)
        self.buf[:, ids] = torch.cat([pose_w, torch.zeros(m, 1, device=self.device)], -1)
        self.last[ids] = pose_w + self.bias[ids]                         # 처음 값은 앞 단계(보고 이동)가 준 추정
        self.age[ids] = 0.0
        self.seen[ids] = True

    def step(self, pose_w: torch.Tensor, visible: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        self.buf = torch.roll(self.buf, 1, dims=0)
        self.buf[0] = torch.cat([pose_w, visible.float()[:, None]], -1)
        d = self.buf[self.delay, torch.arange(pose_w.shape[0], device=self.device)]
        vis = d[:, 4] > 0.5
        self.last = torch.where(vis[:, None], d[:, :4] + self.bias, self.last)
        self.age = torch.where(vis, self.delay.float() * self.dt, self.age + self.dt)
        return self.last, vis, self.age


def box_visible(box_pos_w: torch.Tensor, torso_pos_w: torch.Tensor, torso_R_w: torch.Tensor) -> torch.Tensor:
    """박스 중심이 깊이 화면 안인가 (설계 §4 내 판단). 카메라 = 몸통 고정."""
    w, x, y, z = CAM_QUAT_WXYZ
    R = torch.tensor([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                      [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                      [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]], device=box_pos_w.device, dtype=box_pos_w.dtype)
    cam_p = torch.tensor(CAM_POS, device=box_pos_w.device, dtype=box_pos_w.dtype)
    p_t = torch.einsum("eji,ej->ei", torso_R_w, box_pos_w - torso_pos_w) - cam_p
    p_c = p_t @ R                                                       # 카메라 틀(OpenGL): x 오른쪽, y 위, −z 앞
    depth = -p_c[:, 2]
    u = PPX + FX * p_c[:, 0] / depth.clamp(min=1e-3)
    v = PPY - FX * p_c[:, 1] / depth.clamp(min=1e-3)
    return (depth > 0.1) & (u >= 0) & (u < IMG_W) & (v >= 0) & (v < IMG_H)
