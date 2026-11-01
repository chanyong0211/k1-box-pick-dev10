"""C안 환경: dev12 K1PelvisEnvCfg 를 상속해 박스·명령·행동·관측·보상·이벤트를 바꾼다 (설계 §3–6). dev12 코드는 안 고친다."""

from __future__ import annotations

import isaaclab.sim as sim_utils
from isaaclab.assets import RigidObjectCfg
from isaaclab.envs import mdp as base_mdp
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg  # noqa: F401
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.sensors import ContactSensorCfg
from isaaclab.utils import configclass

from k1_pelvis.tasks import env_cfg as env12
from pick import mdp, pure as P

EPISODE_S = 12.0


def _dev12_groups(cfg) -> None:
    """동결 하체 입력 그룹: dev12 학습과 같은 항·잡음, p_act 만 다리 12 로."""
    policy = env12._terms(noisy=True, rate=True)
    policy["c_clock"] = ObsTerm(func=env12.obs.gait_clock)
    hist = env12._terms(noisy=True, rate=False)
    for t in (policy, hist):
        t["p_act"] = ObsTerm(func=mdp.leg_last_action)
    cfg.observations = type(cfg.observations)()
    for name in list(vars(cfg.observations)):
        setattr(cfg.observations, name, None)
    cfg.observations.dev12_policy = env12._group(policy)
    cfg.observations.dev12_hist = env12._group(hist, history=5)
    cfg.observations.policy = env12._group({"actor": ObsTerm(func=mdp.actor_obs)}, corruption=False)
    cfg.observations.critic = env12._group({"critic": ObsTerm(func=mdp.critic_obs)}, corruption=False)


@configclass
class K1PickEnvCfg(env12.K1PelvisEnvCfg):
    pick_start_level: int = 0

    def __post_init__(self):
        super().__post_init__()
        self.episode_length_s = EPISODE_S
        solver = env12.make_newton_cfg(njmax=400, nconmax=160)
        solver.solver_cfg.cone = "elliptic"
        solver.solver_cfg.impratio = 10.0
        solver.default_shape_cfg.margin = env12.CONTACT_MARGIN
        self.sim.physics = solver
        self.scene.box = RigidObjectCfg(
            prim_path="{ENV_REGEX_NS}/Box",
            init_state=RigidObjectCfg.InitialStateCfg(pos=(0.6, 0.0, P.H / 2 + 0.001)),
            spawn=sim_utils.CuboidCfg(size=P.BOX, rigid_props=sim_utils.RigidBodyPropertiesCfg(), mass_props=sim_utils.MassPropertiesCfg(mass=1.0),
                                      collision_props=sim_utils.CollisionPropertiesCfg(), visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.8, 0.55, 0.3))))
        self.scene.box_contact = ContactSensorCfg(prim_path="{ENV_REGEX_NS}/Robot/.*(rubber_hand|knee_link)", filter_prim_paths_expr=["{ENV_REGEX_NS}/Box"], history_length=1)
        self.scene.box_contact.update_period = self.sim.dt
        self.commands.pelvis = mdp.PickPelvisCommandCfg()
        self.commands.upper_body = mdp.PickUpperCommandCfg()
        self.actions.joint_pos = None
        self.actions.pick = mdp.PickActionCfg()
        _dev12_groups(self)
        for name in list(vars(self.rewards)):
            setattr(self.rewards, name, None)
        self.rewards.pick = RewTerm(func=mdp.pick_reward, weight=1.0)
        self.rewards.termination = RewTerm(func=base_mdp.is_terminated, weight=P.TERMINATION_WEIGHT)
        self.terminations.box_flipped = DoneTerm(func=mdp.box_flipped)
        for name in list(vars(self.curriculum)):
            setattr(self.curriculum, name, None)
        e = self.events
        for name in ("reset_base", "reset_posture", "reset_window", "reset_amp_history", "push_robot", "reset_dev12_state", "dev12_step", "curriculum_step", "physics_material"):
            setattr(e, name, None)
        e.pick_properties = EventTerm(func=mdp.randomize_pick_properties, mode="startup")
        e.reset_pick = EventTerm(func=mdp.reset_pick, mode="reset")
        step = (self.sim.dt * self.decimation,) * 2
        e.pick_step = EventTerm(func=mdp.pick_step, mode="interval", interval_range_s=step, is_global_time=True)


@configclass
class K1PickEnvCfg_EVAL(K1PickEnvCfg):
    def __post_init__(self):
        super().__post_init__()
        self.observations.dev12_policy.enable_corruption = False
        self.observations.dev12_hist.enable_corruption = False
