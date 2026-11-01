"""Isaac 항 (설계 §3–6): dev12 명령을 상위 정책이 내게 바꾼 명령 항, 17 출력 행동(동결 하체 포함), 관측·보상·종료·리셋."""

from __future__ import annotations

import math
import pathlib
from typing import TYPE_CHECKING

import numpy as np
import torch
from isaaclab.managers import ActionTerm, ActionTermCfg
from isaaclab.utils import configclass
from isaaclab.utils.math import euler_xyz_from_quat, matrix_from_quat, quat_from_euler_xyz

from k1_pelvis import feasibility as F
from k1_pelvis.joints import JOINT_NAMES, LEG_JOINTS, UPPER_JOINTS
from k1_pelvis.tasks.mdp import actions as acts12
from k1_pelvis.tasks.mdp import commands as cmds12
from pick import frozen, layout as L, pure as P

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

ASSETS = pathlib.Path(__file__).resolve().parent / "assets"
BUNDLE = ASSETS.parents[3] / "dev12/deploy/pelvis_34750avg/exported/policy.npz"
SNAP = ASSETS / "reset_snapshots.npz"
ARM_RATE, WAIST_RATE = 2.5, 1.0            # rad/s (델타 출력)
SQUEEZE_ROOM = 0.6                         # 어깨 roll 안쪽 여유 (조임용, floor_lift 시험)
STAND_AFTER_S = 0.5                        # 속도 출력이 0 인 채 이만큼 지나야 서기로 (0.1 경계 떨림 방지)
TOE_FROM_FEET = 0.112                      # 발 중앙 → 발끝 [m], make_snapshots 값
BOX_FLIP = math.radians(75.0)
MASS_RANGE = (0.5, 1.0)                    # 설계 §6, 2 kg 은 뒤로
MU_HAND_RANGE, MU_BOX_RANGE = (0.5, 0.9), (0.3, 0.5)
FEET_MU_RANGE = (0.4, 1.2)                 # dev12 d6


# ---------------------------------------------------------------- 명령
class PickPelvisCommand(cmds12.PelvisCommand):
    """무작위 목표 대신 상위 정책 출력. 변화 속도 제한·가능 영역·지연·표본 유지·걸음 시계는 dev12 그대로."""

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.z_stand_min, self.z_walk_min, self.lean_margin_deg, self.roll_cap_deg = F.Z_STAND_MIN, F.Z_WALK_MIN, 45.0, 10.0
        self.goal = self.post_cur.clone()
        self.idle_s = torch.zeros(self.num_envs, device=self.device)

    def _resample_command(self, env_ids):
        super()._resample_command(env_ids)
        ids = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
        self.vel_timer[ids] = self.post_timer[ids] = 1.0e9
        self.goal[ids] = self.post_cur[ids]
        self.idle_s[ids] = 0.0

    def apply_high_level(self, u: torch.Tensor, d_post: torch.Tensor) -> None:
        """u (E,3) ∈ [−1,1] 속도 비율, d_post (E,3) ∈ [−1,1] 자세 변화 비율."""
        dt = self._env.step_dt
        s = F.speed_scale(self.goal[:, 0])
        vmax = torch.tensor(cmds12.V_MAX, device=self.device)[None] * s[:, None]
        v = u * vmax
        v = torch.where(v.abs() < self.cfg.zero_below, torch.zeros_like(v), v)
        moving = (v != 0).any(-1)
        self.idle_s = torch.where(moving, torch.zeros_like(self.idle_s), self.idle_s + dt)
        to_walk = moving & self.is_standing
        self.vel_blocked |= to_walk
        self.is_standing = (self.is_standing & ~moving) | (~moving & (self.idle_s >= STAND_AFTER_S))
        walking = ~self.is_standing
        rates = torch.tensor(cmds12.RATE, device=self.device)[None]
        g = self.goal + d_post * rates * dt
        z = torch.maximum(torch.clamp(g[:, 0], F.Z_STAND_MIN, F.Z_MAX), torch.where(walking, torch.full_like(g[:, 0], F.Z_WALK_MIN), torch.zeros_like(g[:, 0])))
        lo = F.pitch_min_deg(z, walking)
        hi = torch.where(walking, torch.minimum(F.walk_pitch_max_deg(z), torch.full_like(z, F.PITCH_MAX_DEG)), torch.full_like(z, F.PITCH_MAX_DEG))
        p = torch.minimum(torch.maximum(g[:, 1], lo), hi)
        cap = torch.minimum(F.roll_max_deg(z, p), torch.full_like(p, self.roll_cap_deg))
        r = torch.where(walking, torch.zeros_like(p), torch.clamp(g[:, 2], -cap, cap))
        self.goal = torch.stack([z, p, r], -1)
        self.post_tgt = self.goal.clone()
        new_u = v / vmax
        self.u_from = self.u_cur.clone()
        self.u_to = new_u
        self.ramp = torch.where(self.vel_blocked, self.ramp, torch.zeros_like(self.ramp))


@configclass
class PickPelvisCommandCfg(cmds12.PelvisCommandCfg):
    class_type: type = PickPelvisCommand


class PickUpperCommand(cmds12.UpperBodyCommand):
    """무작위 목표 대신 상위 정책 출력 + dev12 저역 필터 0.2. 어깨 roll 은 조임 여유만큼 안쪽으로 더."""

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.goal_lo, self.goal_hi = self.lo.clone(), self.hi.clone()
        names = UPPER_JOINTS
        self.goal_lo[:, names.index("left_shoulder_roll_joint")] -= SQUEEZE_ROOM
        self.goal_hi[:, names.index("right_shoulder_roll_joint")] += SQUEEZE_ROOM

    def _resample_command(self, env_ids):
        ids = torch.as_tensor(env_ids, device=self.device, dtype=torch.long)
        snap = getattr(self._env, "pick_reset_upper", None)
        q = self.default[ids] if snap is None else snap[ids]
        self.goal[ids] = self.target[ids] = q
        self.rate[ids] = 0.0

    def _update_command(self):
        prev = self.target
        self.target = self.low_pass(self.target, self.goal)
        self.rate = self.target - prev


@configclass
class PickUpperCommandCfg(cmds12.UpperBodyCommandCfg):
    class_type: type = PickUpperCommand


# ---------------------------------------------------------------- 행동
class PickAction(ActionTerm):
    """17 출력 → dev12 명령, 동결 하체 → 다리 12 + 상체 11 (안쪽 LegsExternalUpperAction: env 마다 0/1 스텝 지연)."""

    cfg: PickActionCfg

    def __init__(self, cfg, env):
        super().__init__(cfg, env)
        self.inner = acts12.LegsExternalUpperAction(acts12.LegsExternalUpperActionCfg(), env)
        self.lower = frozen.FrozenLower(BUNDLE).to(self.device)
        self._raw = torch.zeros(self.num_envs, L.N_ACT, device=self.device)
        self._prev = self._raw.clone()
        self.code = torch.zeros(self.num_envs, 8, device=self.device)
        self.scripted = None                                          # 스모크 전용: dict(z, p, upper, v)

    @property
    def action_dim(self) -> int:
        return L.N_ACT

    @property
    def raw_actions(self) -> torch.Tensor:
        return self._raw

    @property
    def processed_actions(self) -> torch.Tensor:
        return self.inner.processed_actions

    def process_actions(self, actions: torch.Tensor):
        self._prev = self._raw.clone()
        self._raw[:] = actions
        pelvis = self._env.command_manager.get_term("pelvis")
        upper = self._env.command_manager.get_term("upper_body")
        if self.scripted is None:
            a = actions.clamp(-1.0, 1.0)
            lvl = P.LEVELS[PickRuntime.get(self._env).gate.level]
            on = torch.tensor([lvl[3], lvl[4], lvl[4], 1.0, 1.0, lvl[5], lvl[5]], device=self.device, dtype=a.dtype)
            body = a[:, :7] * on
            pelvis.apply_high_level(body[:, :3], body[:, 3:6])
            dt = self._env.step_dt
            d = torch.cat([body[:, 6:7] * WAIST_RATE, a[:, 7:] * ARM_RATE], -1) * dt
            upper.goal = torch.minimum(torch.maximum(upper.goal + d, upper.goal_lo), upper.goal_hi)
        else:
            s = self.scripted
            n = self.num_envs
            pelvis.goal = torch.stack([torch.full((n,), float(s["z"]), device=self.device), torch.full((n,), float(s["p"]), device=self.device), torch.zeros(n, device=self.device)], -1)
            pelvis.apply_high_level(torch.tensor(s.get("v", (0.0, 0.0, 0.0)), device=self.device, dtype=torch.float32)[None].expand(n, -1), torch.zeros(n, 3, device=self.device))
            upper.goal = torch.as_tensor(s["upper"], device=self.device, dtype=torch.float32)[None].expand(n, -1).clone()
        legs, self.code = self.lower(self._env.obs_buf["dev12_policy"], self._env.obs_buf["dev12_hist"])
        self.inner.process_actions(legs)

    def apply_actions(self):
        self.inner.apply_actions()

    def reset(self, env_ids=None):
        ids = slice(None) if env_ids is None else env_ids
        self._raw[ids] = 0.0
        self._prev[ids] = 0.0
        self.code[ids] = 0.0
        self.inner.reset(env_ids)
        snap = getattr(self._env, "pick_reset_upper", None)
        if snap is not None:
            self.inner._hist[:, ids, 12:] = snap[ids]


@configclass
class PickActionCfg(ActionTermCfg):
    class_type: type = PickAction
    asset_name: str = "robot"


# ---------------------------------------------------------------- 실행 상태
class PickRuntime:
    """관절 이력, 박스 추정, 성공 판정, 게이트, 로그. 환경마다 하나."""

    def __init__(self, env: ManagerBasedRLEnv):
        self.env = env
        E, dev = env.num_envs, env.device
        self.robot, self.box = env.scene["robot"], env.scene["box"]
        names = self.robot.joint_names
        self.ids_all = [names.index(n) for n in JOINT_NAMES]
        self.ids_up = [names.index(n) for n in UPPER_JOINTS]
        self.ids_legs = [names.index(n) for n in LEG_JOINTS]
        self.ids_arms = self.ids_up[1:]
        self.hands = [self.robot.body_names.index(n) for n in ("left_wrist_roll_rubber_hand", "right_wrist_roll_rubber_hand")]
        self.feet = [self.robot.body_names.index(n) for n in ("left_ankle_roll_link", "right_ankle_roll_link")]
        self.torso = self.robot.body_names.index("torso_link")
        self.gate = P.Gate(int(getattr(env.cfg, "pick_start_level", 0)))
        self.hist = torch.zeros(L.HIST, E, 33, device=dev)              # 팔 10 + 허리 1 의 위치·속도·토크, [−1] = 최신
        self.est = P.BoxEstimator(E, env.step_dt, dev)
        self.hold_s = torch.zeros(E, device=dev)
        self.success = torch.zeros(E, dtype=torch.bool, device=dev)
        self.lifted = torch.zeros(E, dtype=torch.bool, device=dev)
        self.both_steps = torch.zeros(E, device=dev)
        self.box0 = torch.zeros(E, 2, device=dev)
        self.mass = torch.ones(E, device=dev)
        self.mu = torch.full((E,), 0.7, device=dev)
        self.log = {}
        self.act = None
        snap = np.load(SNAP)
        assert list(snap["joint_names"]) == JOINT_NAMES
        self.snap = {k: torch.tensor(snap[k], device=dev, dtype=torch.float32) for k in ("q", "root_pos", "root_quat", "z_cmd", "pitch_cmd", "up_target")}
        w, x, y, z = self.snap["root_quat"].unbind(-1)                  # MuJoCo wxyz → 오일러 → 이 Isaac Lab 사본의 규약은 라이브러리에 맡김
        self.snap["rpy"] = torch.stack([torch.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)), torch.asin((2 * (w * y - z * x)).clamp(-1, 1)),
                                        torch.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))], -1)
        self.upper_order = [JOINT_NAMES.index(n) for n in UPPER_JOINTS]

    @staticmethod
    def get(env) -> PickRuntime:
        if not hasattr(env, "pick_rt"):
            env.pick_rt = PickRuntime(env)
        return env.pick_rt

    @property
    def action(self) -> PickAction:
        return self.env.action_manager.get_term("pick")

    def _joint_frame(self) -> torch.Tensor:
        r = self.robot.data
        return torch.cat([r.joint_pos.torch[:, self.ids_up] - r.default_joint_pos.torch[:, self.ids_up], r.joint_vel.torch[:, self.ids_up] * 0.1,
                          r.computed_torque.torch[:, self.ids_up] * 0.05], -1)

    def poses(self) -> dict:
        r = self.robot.data
        root, quat = r.root_link_pos_w.torch, r.root_link_quat_w.torch
        yaw = euler_xyz_from_quat(quat)[2]
        Rh = P.rot_z(yaw)
        hp = r.body_link_pos_w.torch[:, self.hands]
        hq = r.body_link_quat_w.torch[:, self.hands]
        hR = matrix_from_quat(hq.reshape(-1, 4)).reshape(-1, 2, 3, 3)
        b = self.box.data
        bp, bq = b.root_link_pos_w.torch, b.root_link_quat_w.torch
        return dict(root=root, yaw=yaw, Rh=Rh, hp=hp, hR=hR, bp=bp, bR=matrix_from_quat(bq), byaw=euler_xyz_from_quat(bq)[2])

    def hand_force(self) -> tuple[torch.Tensor, torch.Tensor]:
        """손마다 박스가 민 힘 (E,2,3), 무릎 힘 크기 최댓값 (E,). 센서 = 손 2 + 무릎 2, 상대 = 박스."""
        s = self.env.scene["box_contact"]
        f = s.data.force_matrix_w.torch[:, :, 0]
        ids = getattr(self, "_sensor_ids", None)
        if ids is None:
            names = s.sensor_names
            ids = self._sensor_ids = ([names.index("left_wrist_roll_rubber_hand"), names.index("right_wrist_roll_rubber_hand")], [names.index("left_knee_link"), names.index("right_knee_link")])
        return f[:, ids[0]], f[:, ids[1]].norm(dim=-1).max(-1).values

    # --- 리셋·스텝 ---
    def reset(self, ids: torch.Tensor) -> None:
        pose = torch.cat([self.box.data.root_link_pos_w.torch[ids], euler_xyz_from_quat(self.box.data.root_link_quat_w.torch[ids])[2][:, None]], -1)
        self.est.reset(ids, pose)
        self.box0[ids] = pose[:, :2]
        self.hold_s[ids] = 0.0
        self.success[ids] = False
        self.lifted[ids] = False
        self.both_steps[ids] = 0.0
        self.hist[:, ids] = self._joint_frame()[ids]

    def step(self) -> None:
        self.hist = torch.roll(self.hist, -1, dims=0)
        self.hist[-1] = self._joint_frame()
        p = self.poses()
        pose = torch.cat([p["bp"], p["byaw"][:, None]], -1)
        r = self.robot.data
        vis = P.box_visible(p["bp"], r.body_link_pos_w.torch[:, self.torso], matrix_from_quat(r.body_link_quat_w.torch[:, self.torso]))
        self.est_out = self.est.step(pose, vis)

    # --- 관측 ---
    def actor_obs(self) -> torch.Tensor:
        E, dev = self.env.num_envs, self.env.device
        p = self.poses()
        est, vis, age = getattr(self, "est_out", (torch.cat([p["bp"], p["byaw"][:, None]], -1), torch.ones(E, dtype=torch.bool, device=dev), torch.zeros(E, device=dev)))
        Rt = p["Rh"].transpose(-1, -2)
        box_h = torch.einsum("eij,ej->ei", Rt, est[:, :3] - p["root"])
        yaw_h = torch.atan2(torch.sin(est[:, 3] - p["yaw"]), torch.cos(est[:, 3] - p["yaw"]))
        yaw_q = (yaw_h + math.pi / 4) % (math.pi / 2) - math.pi / 4     # 검출기 규약: 90° 주기
        hp_h = torch.einsum("eij,ehj->ehi", Rt, p["hp"] - p["root"][:, None])
        hR_h = torch.einsum("eij,ehjk->ehik", Rt, p["hR"])
        palm_h, normal_h = P.palm(hp_h, hR_h)
        hf = P.hand_features(palm_h, normal_h, box_h, yaw_q)
        r = self.robot.data
        cmd = self.env.command_manager.get_term("pelvis")
        pc = cmd.post_cur / torch.tensor([1.0, 45.0, 45.0], device=dev)
        v = cmd.cmd_true[:, :3]
        shared = torch.cat([box_h, yaw_q[:, None], vis.float()[:, None], age[:, None].clamp(max=2.0), self.action.code, r.projected_gravity_b.torch,
                            r.root_link_ang_vel_b.torch * 0.25, pc, v, cmd.clock_obs], -1)
        h = self.hist.permute(1, 0, 2)                                   # (E, 5, 33): 위치 11, 속도 11, 토크 11; 순서 허리, 왼 5, 오 5
        up = self.env.command_manager.get_term("upper_body")
        last = up.goal - up.default
        def arm(a0):
            return torch.cat([torch.cat([h[:, t, a0:a0 + 5], h[:, t, 11 + a0:11 + a0 + 5], h[:, t, 22 + a0:22 + a0 + 5]], -1) for t in range(L.HIST)] + [last[:, a0:a0 + 5]], -1)
        waist = torch.cat([torch.cat([h[:, t, 0:1], h[:, t, 11:12], h[:, t, 22:23]], -1) for t in range(L.HIST)] + [last[:, :1]], -1)
        legs = torch.cat([r.joint_pos.torch[:, self.ids_legs] - r.default_joint_pos.torch[:, self.ids_legs], r.joint_vel.torch[:, self.ids_legs] * 0.1], -1)
        body_last = self.action.raw_actions[:, :6].clamp(-1.0, 1.0)
        obs = torch.cat([shared, hf[:, 0], hf[:, 1], arm(1), arm(6), waist, legs, body_last], -1)
        return torch.nan_to_num(obs)

    def reward_state(self) -> dict:
        p = self.poses()
        fh, knee = self.hand_force()
        n = P.side_normal(fh, p["bR"])
        palm_w, _ = P.palm(p["hp"], p["hR"])
        pad_box = P.to_box(palm_w, p["bp"], p["bR"])
        r = self.robot.data
        feet = r.body_link_pos_w.torch[:, self.feet]
        mid = feet.mean(1)
        fq = euler_xyz_from_quat(r.body_link_quat_w.torch[:, self.feet[0]])[2]
        fq2 = euler_xyz_from_quat(r.body_link_quat_w.torch[:, self.feet[1]])[2]
        fy = torch.atan2(torch.sin(fq) + torch.sin(fq2), torch.cos(fq) + torch.cos(fq2))
        d = p["bp"][:, :2] - mid[:, :2]
        c, s_ = torch.cos(fy), torch.sin(fy)
        bx, by = c * d[:, 0] + s_ * d[:, 1], -s_ * d[:, 0] + c * d[:, 1]
        eyaw = (p["byaw"] - fy + math.pi / 4) % (math.pi / 2) - math.pi / 4
        q_arm = r.joint_pos.torch[:, self.ids_arms]
        lim = r.soft_joint_pos_limits.torch[:, self.ids_arms]
        over = (q_arm - lim[..., 1]).clamp(min=0.0) + (lim[..., 0] - q_arm).clamp(min=0.0)
        act = self.action
        return dict(pad_box=pad_box, n_side=n, mass=self.mass, mu=self.mu, min_z=P.box_corners_min_z(p["bp"], p["bR"]) - self.env.scene.env_origins[:, 2], tilt=P.tilt(p["bR"]),
                    disp=(p["bp"][:, :2] - self.box0).norm(dim=-1), ex=bx - (TOE_FROM_FEET + P.TOE_TARGET + P.A / 2), ey=by, eyaw=eyaw, tau_arm=r.computed_torque.torch[:, self.ids_arms],
                    act=act.raw_actions, act_prev=act._prev, limit=over.sum(-1), waist=r.joint_pos.torch[:, self.ids_up[0]], body_box=knee)

    def critic_extra(self) -> torch.Tensor:
        s = self.reward_state()
        p = self.poses()
        Rt = p["Rh"].transpose(-1, -2)
        b = self.box.data
        vel = torch.cat([torch.einsum("eij,ej->ei", Rt, b.root_link_lin_vel_w.torch), torch.einsum("eij,ej->ei", Rt, b.root_link_ang_vel_w.torch) * 0.25], -1)
        cmd = self.env.command_manager.get_term("pelvis")
        return torch.cat([torch.einsum("eij,ej->ei", Rt, p["bp"] - p["root"]), torch.einsum("eij,ejk->eik", Rt, p["bR"])[:, :, :2].reshape(-1, 6), vel, self.mass[:, None], self.mu[:, None],
                          s["n_side"] * 0.05, (s["n_side"] > P.CONTACT_N).float(), s["min_z"][:, None], s["tilt"][:, None], s["disp"][:, None], s["ex"][:, None], s["ey"][:, None], s["eyaw"][:, None],
                          (self.env.episode_length_buf.float() / self.env.max_episode_length)[:, None], torch.full((self.env.num_envs, 1), self.gate.level / 4.0, device=self.env.device),
                          cmd.vel_blocked.float()[:, None], self.hold_s[:, None]], -1)


# ---------------------------------------------------------------- 관측 항
def leg_last_action(env) -> torch.Tensor:
    """dev12 p_act: 동결 하체 자신의 지난 다리 12 (base last_action 은 여기선 17 출력이라 못 씀)."""
    return env.action_manager.get_term("pick").inner.raw_actions


def actor_obs(env) -> torch.Tensor:
    return PickRuntime.get(env).actor_obs()


def critic_obs(env) -> torch.Tensor:
    rt = PickRuntime.get(env)
    return torch.nan_to_num(torch.cat([rt.actor_obs(), rt.critic_extra()], -1))


# ---------------------------------------------------------------- 보상·종료
def pick_reward(env) -> torch.Tensor:
    rt = PickRuntime.get(env)
    s = rt.reward_state()
    parts = P.rewards(s)
    state = P.is_success_state(s["min_z"], s["tilt"], s["n_side"])
    rt.hold_s = torch.where(state, rt.hold_s + env.step_dt, torch.zeros_like(rt.hold_s))
    rt.success |= rt.hold_s >= P.SUCCESS_HOLD_S
    rt.lifted |= s["min_z"] >= 0.03
    rt.both_steps += (s["n_side"] > P.CONTACT_N).all(-1).float()
    rt.log = {f"Pick/r_{k}": float((P.WEIGHTS[k] * v).mean()) for k, v in parts.items()}
    return torch.nan_to_num(P.total(parts))


def box_flipped(env) -> torch.Tensor:
    return P.tilt(matrix_from_quat(env.scene["box"].data.root_link_quat_w.torch)) > BOX_FLIP


# ---------------------------------------------------------------- 이벤트
def randomize_pick_properties(env, env_ids) -> None:
    """시작: 발 μ 는 dev12 그대로 env 마다, 손 μ·박스 μ·박스 질량. Newton 은 max 결합 → 손–박스 실효 = max(손, 박스), 박스–바닥 = 박스."""
    import isaaclab_newton.physics.newton_manager as nm
    import warp as wp
    from newton.solvers import SolverNotifyFlags

    from k1_pelvis.tasks.mdp import events as ev12

    ev12.randomize_friction(env, env_ids, FEET_MU_RANGE)
    rt = PickRuntime.get(env)
    E, dev = env.num_envs, env.device
    model = nm.NewtonManager.get_model()
    rv = rt.robot._root_view
    mu_r = wp.to_torch(rv.get_attribute("shape_material_mu", model)[:, 0])
    shapes = sorted({int(s) for b, n in enumerate(rv.body_names) if "rubber_hand" in n for s in rv.body_shapes[b]})
    hand = MU_HAND_RANGE[0] + (MU_HAND_RANGE[1] - MU_HAND_RANGE[0]) * torch.rand(E, device=mu_r.device)
    mu_r[:, shapes] = hand[:, None]
    bv = rt.box.root_view
    mu_b = wp.to_torch(bv.get_attribute("shape_material_mu", model)[:, 0])
    rest_b = wp.to_torch(bv.get_attribute("shape_material_restitution", model)[:, 0])
    box = MU_BOX_RANGE[0] + (MU_BOX_RANGE[1] - MU_BOX_RANGE[0]) * torch.rand(E, device=mu_b.device)
    mu_b[:] = box[:, None]
    rest_b[:] = 0.0
    nm.NewtonManager.add_model_change(SolverNotifyFlags.SHAPE_PROPERTIES)
    rt.mu = torch.maximum(hand, box).to(dev)
    mass = MASS_RANGE[0] + (MASS_RANGE[1] - MASS_RANGE[0]) * torch.rand(E, device=dev)
    rt.mass = mass
    a, b, h = P.BOX
    box_i = torch.stack([mass / 12 * (b * b + h * h), torch.zeros(E, device=dev), torch.zeros(E, device=dev), torch.zeros(E, device=dev), mass / 12 * (a * a + h * h),
                         torch.zeros(E, device=dev), torch.zeros(E, device=dev), torch.zeros(E, device=dev), mass / 12 * (a * a + b * b)], -1)
    all_ids = torch.arange(E, device=dev)
    rt.box.set_masses_index(masses=mass[:, None], body_ids=[0], env_ids=all_ids)
    rt.box.set_inertias_index(inertias=box_i[:, None], body_ids=[0], env_ids=all_ids)


def reset_pick(env, env_ids) -> None:
    """리셋: 스냅숏 4 개 중 하나 + 게이트 범위 박스. 끝난 에피소드 수·성공을 게이트에 넘긴다."""
    rt = PickRuntime.get(env)
    dev = env.device
    ids = torch.as_tensor(env_ids, device=dev, dtype=torch.long)
    done = ids[env.episode_length_buf[ids] > 0]
    if len(done):
        rate = float(rt.success[done].float().mean())
        rt.log_ep = dict(success=rate, lift3=float(rt.lifted[done].float().mean()), both=float((rt.both_steps[done] / env.episode_length_buf[done].float().clamp(min=1)).mean()))
        rt.gate.update(len(done), int(rt.success[done].sum()))
    n = len(ids)
    k = torch.randint(0, len(rt.snap["q"]), (n,), device=dev)
    origin = env.scene.env_origins[ids]
    rpy = rt.snap["rpy"][k]
    pose = torch.cat([origin + rt.snap["root_pos"][k] + torch.tensor([0.0, 0.0, 0.002], device=dev), quat_from_euler_xyz(rpy[:, 0], rpy[:, 1], rpy[:, 2])], -1)
    rt.robot.write_root_pose_to_sim_index(root_pose=pose, env_ids=ids)
    rt.robot.write_root_velocity_to_sim_index(root_velocity=torch.zeros(n, 6, device=dev), env_ids=ids)
    q = torch.zeros(n, rt.robot.num_joints, device=dev)
    q[:, rt.ids_all] = rt.snap["q"][k]
    rt.robot.write_joint_state_to_sim_index(position=q, velocity=torch.zeros_like(q), env_ids=ids)
    if not hasattr(env, "dev12_reset_posture"):
        env.dev12_reset_posture = torch.zeros(env.num_envs, 2, device=dev)
        env.pick_reset_upper = torch.zeros(env.num_envs, 11, device=dev)
    env.dev12_reset_posture[ids] = torch.stack([rt.snap["z_cmd"][k], rt.snap["pitch_cmd"][k]], -1)
    env.pick_reset_upper[ids] = rt.snap["up_target"][k]
    dist, lat, yaw = rt.gate.sample_box(n, dev)
    bp = origin + torch.stack([TOE_FROM_FEET + P.box_centre_ahead(dist, yaw), lat, torch.full_like(lat, P.H / 2 + 0.001)], -1)
    bq = quat_from_euler_xyz(torch.zeros_like(yaw), torch.zeros_like(yaw), yaw)
    rt.box.write_root_pose_to_sim_index(root_pose=torch.cat([bp, bq], -1), env_ids=ids)
    rt.box.write_root_velocity_to_sim_index(root_velocity=torch.zeros(n, 6, device=dev), env_ids=ids)
    rt.reset(ids)


def pick_step(env, env_ids) -> None:
    PickRuntime.get(env).step()
