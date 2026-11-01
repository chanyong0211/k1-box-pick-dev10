"""actor 입력 256 배치와 머리별 슬라이스·거울 (설계 §4). 벡터 하나를 세 머리가 나눠 본다."""

from __future__ import annotations

import torch

ARM_SIGN = (1.0, -1.0, -1.0, 1.0, -1.0)   # 어깨 pitch, roll, yaw, 팔꿈치, 손목 roll: dev12 symmetry 규칙(roll·yaw 반대)
HIST = 5                                  # 관절 이력 스텝

SHARED = {"box_pos": 3, "box_yaw": 1, "box_vis": 1, "box_age": 1, "code": 8, "grav": 3, "angvel": 3, "post": 3, "vel": 3, "clock": 2}
HAND = {"palm": 3, "normal": 3, "plane": 1, "on_face": 2, "line_angle": 1, "line_dist": 1}
ARM_STEP = 15                             # 위치·속도·토크 각 5
N_SHARED, N_HAND = sum(SHARED.values()), sum(HAND.values())
N_ARM = ARM_STEP * HIST + 5               # 이력 + 지난 목표 5
N_WAIST, N_LEGS, N_BODY_LAST = 3 * HIST + 1, 24, 6
N_OBS = N_SHARED + 2 * N_HAND + 2 * N_ARM + N_WAIST + N_LEGS + N_BODY_LAST
N_BODY_OUT, N_ARM_OUT, N_ACT = 7, 5, 17   # vx vy wz, z pitch roll, 허리 / 왼팔 / 오른팔

S0 = 0
HL0 = S0 + N_SHARED
HR0 = HL0 + N_HAND
AL0 = HR0 + N_HAND
AR0 = AL0 + N_ARM
W0 = AR0 + N_ARM
LEG0 = W0 + N_WAIST
BL0 = LEG0 + N_LEGS
assert BL0 + N_BODY_LAST == N_OBS == 256


def _shared_sign() -> list[float]:
    s = [1.0] * N_SHARED
    for i in (1, 3):                        # 박스 y, yaw
        s[i] = -1.0
    code = 6                                # 속도 3·높이 1·무게중심 3·총 무게 1
    s[code + 1] = -1.0
    s[code + 5] = -1.0
    g = code + 8
    s[g + 1] = -1.0                         # 중력 y
    s[g + 3], s[g + 5] = -1.0, -1.0         # 각속도 x·z
    p = g + 6
    s[p + 2] = -1.0                         # 자세 roll
    s[p + 4], s[p + 5] = -1.0, -1.0         # 속도 vy·wz
    s[p + 6], s[p + 7] = -1.0, -1.0         # 걸음 시계: 거울 = 반주기 이동
    return s


def _hand_sign() -> list[float]:
    return [1.0, -1.0, 1.0, 1.0, -1.0, 1.0] + [1.0] * 5   # 손바닥·법선 y 반대, 나머지는 박스 틀 크기


def _arm_sign() -> list[float]:
    return list(ARM_SIGN) * (3 * HIST + 1)


SUMMARY = list(range(3)) + list(range(6, 9))    # 상대 손 요약: 손바닥 3, 면까지 1, 면 위 2
TAU_LAST = [ARM_STEP * (HIST - 1) + 10 + j for j in range(5)]   # 팔 블록 안 최신 토크


def arm_indices(side: int) -> tuple[torch.Tensor, torch.Tensor]:
    """머리 입력 만드는 (지수, 부호): side 0 왼팔 그대로, 1 오른팔을 왼팔 꼴로 거울. 공유 28 + 자기 손 11 + 자기 팔 80 + 상대 손 6 + 상대 토크 5 + 허리 위치 1."""
    me_h, ot_h, me_a, ot_a = (HL0, HR0, AL0, AR0) if side == 0 else (HR0, HL0, AR0, AL0)
    flip = side == 1
    idx, sign = [], []

    def add(start, ids, signs):
        idx.extend(start + i for i in ids)
        sign.extend(signs[i] if flip else 1.0 for i in ids)

    add(S0, range(N_SHARED), _shared_sign())
    add(me_h, range(N_HAND), _hand_sign())
    add(me_a, range(N_ARM), _arm_sign())
    add(ot_h, SUMMARY, _hand_sign())
    add(ot_a, TAU_LAST, _arm_sign())
    add(W0 + 3 * (HIST - 1), [0], [-1.0])       # 최신 허리 위치
    return torch.tensor(idx, dtype=torch.long), torch.tensor(sign)


N_ARM_IN = N_SHARED + N_HAND + N_ARM + len(SUMMARY) + len(TAU_LAST) + 1


def obs_mirror() -> tuple[torch.Tensor, torch.Tensor]:
    """전체 입력의 좌우 거울 (시험용): 왼·오 블록 교환 + 부호."""
    idx, sign = [], []

    def add(start, n, s):
        idx.extend(range(start, start + n))
        sign.extend(s)

    add(S0, N_SHARED, _shared_sign())
    add(HR0, N_HAND, _hand_sign())
    add(HL0, N_HAND, _hand_sign())
    add(AR0, N_ARM, _arm_sign())
    add(AL0, N_ARM, _arm_sign())
    add(W0, N_WAIST, [-1.0] * N_WAIST)
    leg_sign = [1.0, -1.0, -1.0, 1.0, 1.0, -1.0]
    for block in (0, 12):                        # 다리 위치·속도, 왼·오 6 씩 교환
        idx.extend(range(LEG0 + block + 6, LEG0 + block + 12))
        idx.extend(range(LEG0 + block, LEG0 + block + 6))
        sign.extend(leg_sign * 2)
    add(BL0, N_BODY_LAST, [1.0, -1.0, -1.0, 1.0, 1.0, -1.0])
    return torch.tensor(idx, dtype=torch.long), torch.tensor(sign)
