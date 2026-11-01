# 명시적 명령으로 하위 전신·보행 제어기를 모는 휴머노이드 계층 시스템 (2023–2026-10)

범위: 상위 층이 하위 제어기에 **명시적 명령**(기저 속도 vx·vy·yaw rate, 골반·기저 높이, 몸통 pitch·roll, 상체 관절 목표 또는 손 끝 목표)을 주는 계층형 휴머노이드 loco-manipulation. 무게는 **동결(또는 공동 학습)된 하위 제어기 위에 RL·IL 상위 정책을 학습한 연구**에 두었다. 하위 보행 쪽 자체(FAME·HULK·Thor·HAFO·SoFTA·yahmp 등)는 이미 [dev12 구현 참고 연구와 오픈소스.md](/home/robotis-ai/Projects2/dev12/reports/dev12%20구현%20참고%20연구와%20오픈소스.md)에서 다뤘으므로 여기서는 "위에 무엇을 얹었나"만 본다. HugWBC 는 이미 `/home/robotis-ai/Projects2/dev12/reference/HugWBC`(코드)와 `/home/robotis-ai/Projects2/dev12/reference/hugwbc_paper/HugWBC_2502.03206v3.pdf`(논문)에 있다.

비교 기준(우리 설정): ROBOTIS K1(35.7 kg, 23 DoF, 손가락 없는 공 손 → 두 손 조이기). 하위 = dev12 하체 RL(Isaac Lab + Newton, rsl_rl PPO, 다리만 AMP), 명령 vx·vy·wz·골반 높이 0.335–0.77 m·pitch ±45°·roll(서 있을 때만), 상체 11 관절(허리 yaw + 팔 2×5)은 **외부 PD 목표**이고 하위는 저역 통과된 목표와 그 변화율을 관측, 손 외력 0–5 kg 무작위로 학습. 새 프로젝트: 상위 정책이 상체 11 목표 + 골반 명령을 내 상자(37×40×29 cm, 0.5–2 kg)를 바닥·낮은 받침(0–0.3 m)에서 두 손으로 조여 들고 일어선다. 특권 RL teacher → D436 깊이 student(DAgger). 지난 판(SONIC 추종기 위 joint-space teacher)의 문제: teacher 출력이 추종기 능력 밖, 출력이 켜짐/꺼짐으로 포화, student 가 teacher 보다 약 20 %p 낮음.

다른 연구자 담당과 겹치는 부분: (a) 시각 teacher→student 증류(사족 보행 포함), (b) 휴머노이드 상자 집기·들기·나르기 방법 자체, (c) 동결 제어기 위 정책의 인터페이스 설계·학습 기법(잠재 기술 공간 등). 이 노트는 그 각도는 짧게만 언급한다. reference/ 폴더에는 다른 연구자가 이미 받은 항목(viral, doorman, visualmimic, hulk, splitadapter, resmimic, physhsi, vbc, slim, hilmares, puppeteer, pulse, omnigrasp, maskedmimic 등)이 있어 그 폴더는 건너뛰었다.

## Q1. 우리와 거의 같은 분할(하체 명령 추종 RL + 외부에서 오는 상체) 위에 자율 상위 정책을 학습한 시스템은 무엇인가 (전체 카탈로그 포함)

### Takeaway
우리 구조와 가장 가까운 공개 사례는 NVIDIA GEAR 의 **VIRAL·DoorMan**(동결 HOMIE 하체 RL 위에 특권 RL teacher → RGB student DAgger, Unitree G1 실기)이고, Isaac Lab 에서 "동결 속도·높이 하체 정책을 행동 항으로 감싸고 그 위에 RL 상체 정책을 학습"하는 코드 꼴은 **AGILE**(Apache-2.0)이 가장 직접적인 견본이다. 하위 명령 공간이 우리와 거의 같은 것은 HOMIE·AMO·ULC·HiWET·DemoHLM 이지만, 이 중 상위를 RL 로 학습한 것은 HiWET 뿐이고 나머지는 IL(텔레옵 시연)이다. 상자를 "동결 하위 + RL 상위"로 집은 실기 사례는 R2S2(H1, 잠재 기술 공간, 90 %)·VisualMimic(G1, 키포인트 명령, 0.5 kg)·HuGo 의 RL 기준선(시뮬 0 %)뿐이어서, 우리 조합(골반 명령 + 상체 관절 + 깊이 student + 두 손 조이기)은 공개 선례가 없다.

### Cited Findings

#### 카탈로그 표 (유사도 내림차순)

유사도 5 = 구조·학습 방식·실기까지 거의 같음, 1 = 주변 참고. "받은 경로"는 `/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/` 기준. 이 노트 작성자가 받은 것은 agile, homie, amo, demohlm, hiwet, refine_dp, oil, hugo, r2s2(합 약 551 MB). viral·doorman·visualmimic·hulk·splitadapter 는 다른 연구자가 이미 받아 둔 것을 확인만 했다.

| short_id | 제목 | 발표처/연도 | arXiv | 코드 | 라이선스 | 유사도 | 받은 경로 |
|---|---|---|---|---|---|---|---|
| viral | VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation | CVPR 2026 포스터, 2025-11 | [2511.15200](https://arxiv.org/abs/2511.15200) | [NVlabs/GR00T-VisualSim2Real](https://github.com/NVlabs/GR00T-VisualSim2Real) main | Apache-2.0 | 5 | `viral/`(다른 연구자) |
| doorman | Opening the Sim-to-Real Door for Humanoid Pixel-to-Action Policy Transfer | CVPR 2026, 2025-11 | [2512.01061](https://arxiv.org/abs/2512.01061) | 같은 저장소 `doorman` 브랜치 | Apache-2.0 | 5 | `doorman/`(다른 연구자) |
| agile | AGILE: A Comprehensive Workflow for Humanoid Loco-Manipulation Learning | 프리프린트, 2026-03 | [2603.20147](https://arxiv.org/abs/2603.20147) | [nvidia-isaac/WBC-AGILE](https://github.com/nvidia-isaac/WBC-AGILE) | Apache-2.0 + BSD-3(RSL_RL 부분) | 4 | `agile/`(paper.pdf, code/) |
| visualmimic | VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation | 프리프린트, 2025-09 (v2 2025-11) | [2509.20322](https://arxiv.org/abs/2509.20322) | [visualmimic/VisualMimic](https://github.com/visualmimic/VisualMimic)(sim2sim·체크포인트만) | 저장소 LICENSE 없음 | 4 | `visualmimic/`(다른 연구자) |
| homie | HOMIE: Humanoid Loco-Manipulation with Isomorphic Exoskeleton Cockpit | RSS 2025 | [2502.13013](https://arxiv.org/abs/2502.13013) | [InternRobotics/OpenHomie](https://github.com/InternRobotics/OpenHomie) | CC BY-NC 4.0(LICENSE 파일) / README 는 BY-NC-SA, 불일치 | 4 | `homie/`(paper.pdf, code/) |
| amo | AMO: Adaptive Motion Optimization for Hyper-Dexterous Humanoid Whole-Body Control | RSS 2025(다른 논문의 인용으로만 확인) | [2505.03738](https://arxiv.org/abs/2505.03738) | [OpenTeleVision/AMO](https://github.com/OpenTeleVision/AMO)(추론 체크포인트만) | Apache-2.0(LICENSE 파일, API 는 NOASSERTION) | 4 | `amo/`(paper.pdf, code/) |
| hiwet | HiWET: Hierarchical World-Frame End-Effector Tracking for Long-Horizon Humanoid Loco-Manipulation | 프리프린트, 2026-02 | [2602.06341](https://arxiv.org/abs/2602.06341) | 없음 | – | 4 | `hiwet/`(paper.pdf) |
| refine_dp | REFINE-DP: Diffusion Policy Fine-tuning for Humanoid Loco-manipulation via Reinforcement Learning | 프리프린트, 2026-03 | [2603.13707](https://arxiv.org/abs/2603.13707) | 없음 | – | 4 | `refine_dp/`(paper.pdf) |
| oil | OIL: An Object Interaction Layer for Humanoid Whole-Body Control | 프리프린트, 2026-10 | [2610.14033](https://arxiv.org/abs/2610.14033) | 없음(하위 MHC 는 [osudrl/masked-humanoid-controller](https://github.com/osudrl/masked-humanoid-controller)) | – | 4 | `oil/`(paper.pdf) |
| hugo | HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation | 프리프린트, 2026-09 | [2609.30594](https://arxiv.org/abs/2609.30594) | 없음 | – | 3 | `hugo/`(paper.pdf) |
| r2s2 | Unleashing Humanoid Reaching Potential via Real-world-Ready Skill Space | IEEE RA-L 2025 | [2505.10918](https://arxiv.org/abs/2505.10918) | [OpenWBT](https://github.com/GalaxyGeneralRobotics/OpenWBT)(텔레옵만, 잠재 기술 공간 미공개) | Apache-2.0 | 3 | `r2s2/`(paper.pdf) |
| demohlm | DemoHLM: From One Demonstration to Generalizable Humanoid Loco-Manipulation | 프리프린트, 2025-10 | [2510.11258](https://arxiv.org/abs/2510.11258) | [BeingBeyond/DemoHLM](https://github.com/BeingBeyond/DemoHLM)(README·그림만, 코드 없음) | MIT 배지 | 3 | `demohlm/`(paper.pdf, code/) |
| ulc | ULC: A Unified and Fine-Grained Controller for Humanoid Loco-Manipulation | 프리프린트, 2025-07 | [2507.06905](https://arxiv.org/abs/2507.06905) | 프로젝트 페이지가 코드 공개를 말함(저장소 확인 못 함) | 미확인 | 3 | 링크만 |
| falcon | FALCON: Learning Force-Adaptive Humanoid Loco-Manipulation | L4DC 2026 (PMLR 331) | [2505.06776](https://arxiv.org/abs/2505.06776) | [LeCAR-Lab/FALCON](https://github.com/LeCAR-Lab/FALCON) | MIT | 3 | 링크만 |
| twist2 | TWIST2: Scalable, Portable, and Holistic Humanoid Data Collection System | 프리프린트, 2025-11 | [2511.02832](https://arxiv.org/abs/2511.02832) | [amazon-far/TWIST2](https://github.com/amazon-far/TWIST2)(상위 정책 코드는 별도 저장소 예정) | MIT | 3 | 링크만 |
| wholebodyvla | WholeBodyVLA: Towards Unified Latent VLA for Whole-Body Loco-Manipulation Control | ICLR 2026 | [2512.11047](https://arxiv.org/abs/2512.11047) | [OpenDriveLab/WholebodyVLA](https://github.com/OpenDriveLab/WholebodyVLA) | MIT | 3 | 링크만 |
| skillblender | SkillBlender: Towards Versatile Humanoid Whole-Body Loco-Manipulation via Skill Blending | 프리프린트, 2025-06 | [2506.09366](https://arxiv.org/abs/2506.09366) | [Humanoid-SkillBlender/SkillBlender](https://github.com/Humanoid-SkillBlender/SkillBlender) | NOASSERTION | 3 | 링크만 |
| anymal_pnp | Collaborative Loco-Manipulation for Pick-and-Place Tasks with Dynamic Reward Curriculum (사족, 참고) | 프리프린트, 2025-09 | [2509.13239](https://arxiv.org/abs/2509.13239) | 없음 | – | 3 | 링크만 |
| humanoidmimicgen | HumanoidMimicGen: Data Generation for Loco-Manipulation via Whole-Body Planning | 프리프린트, 2026-05 | [2605.27724](https://arxiv.org/abs/2605.27724) | 없음 | – | 2 | 링크만 |
| openhlm | OpenHLM: An Empirical Recipe for Whole-Body Humanoid Loco-Manipulation | 프리프린트, 2026-06 | [2606.22174](https://arxiv.org/abs/2606.22174) | [OpenHLM-project/OpenHLM](https://github.com/OpenHLM-project/OpenHLM) + HF 체크포인트 | Apache-2.0 | 2 | 링크만 |
| workhorse | Workhorse: Learning Robust Whole-Body Humanoid Loco-Manipulation from Human Data | 프리프린트, 2026-10 | [2610.09117](https://arxiv.org/abs/2610.09117) | 없음 | – | 2 | 링크만 |
| cwi | CWI: Composite Humanoid Whole-Body Imitation System for Loco-manipulation | 프리프린트, 2026-06(RA-L 여부 미확인) | [2606.27676](https://arxiv.org/abs/2606.27676) | 없음 | – | 2 | 링크만 |
| splitadapter | SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation | 프리프린트, 2026-06 | [2606.03297](https://arxiv.org/abs/2606.03297) | 없음 | – | 2 | `splitadapter/`(다른 연구자) |
| hulk | HULK: Learning Whole-Body Forceful Loco-Manipulation for Humanoids | 프리프린트, 2026-10 | [2610.08970](https://arxiv.org/abs/2610.08970) | 없음 | – | 2 | `hulk/`(다른 연구자) |
| ceer | CEER: Compliant End-Effector and Root Control as a Unified Interface for Hierarchical Humanoid Loco-Manipulation | 프리프린트, 2026-05 | [2605.19981](https://arxiv.org/abs/2605.19981) | 없음 | – | 2 | 링크만 |
| leverb | LeVERB: Humanoid Whole-Body Control with Latent Vision-Language Instruction | 프리프린트, 2025-06 | [2506.13751](https://arxiv.org/abs/2506.13751) | 없음(웹사이트 저장소만) | – | 2 | 링크만 |
| mobile_tv | Mobile-TeleVision: Predictive Motion Priors for Humanoid Whole-Body Control | 프리프린트, 2024-12 | [2412.07773](https://arxiv.org/abs/2412.07773) | 없음 | – | 2 | 링크만 |
| hover | HOVER: Versatile Neural Whole-Body Controller for Humanoid Robots | ICRA 2025 | [2410.21229](https://arxiv.org/abs/2410.21229) | [NVlabs/HOVER](https://github.com/NVlabs/HOVER) | Apache-2.0 | 2 | 링크만 |
| gr00t_wbc | GR00T-WholeBodyControl (Decoupled WBC, GEAR-SONIC) | 저장소 | – | [NVlabs/GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl) | 코드 Apache-2.0, 가중치 NVIDIA Open Model License | 2 | 링크만 |
| hex | HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation | 프리프린트, 2026-04 | [2604.07993](https://arxiv.org/abs/2604.07993) | [Open-X-Humanoid/HEX](https://github.com/Open-X-Humanoid/HEX) | LICENSE 없음 | 2 | 링크만 |
| haf | HAF: Adapting Generalist VLAs to Humanoid Whole-Body Loco-manipulation via Hierarchical Action Flow and Spectral Latent RL | 프리프린트, 2026-08 | [2608.16837](https://arxiv.org/abs/2608.16837) | 없음 | – | 2 | 링크만 |
| resmimic | ResMimic: From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learning | 프리프린트, 2025-10 | [2510.05070](https://arxiv.org/abs/2510.05070) | [amazon-far/ResMimic](https://github.com/amazon-far/ResMimic) | Apache-2.0 | 2 | `resmimic/`(다른 연구자) |
| being0 | Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills | 프리프린트, 2025-03 | [2503.12533](https://arxiv.org/abs/2503.12533) | [BeingBeyond/Being-0](https://github.com/BeingBeyond/Being-0) | LICENSE 없음 | 1 | 링크만 |
| trajbooster | TrajBooster: Boosting Humanoid Whole-Body Manipulation via Trajectory-Centric Learning | 프리프린트, 2025-09 | [2509.11839](https://arxiv.org/abs/2509.11839) | 논문에 저장소 없음(jiachengliu3/TrajBooster 존재, 공식 여부 미확인) | – | 1 | 링크만 |
| omnih2o | OmniH2O: Universal and Dexterous Human-to-Humanoid Whole-Body Teleoperation and Learning | 프리프린트 표기, 2024-06 | [2406.08858](https://arxiv.org/abs/2406.08858) | [LeCAR-Lab/human2humanoid](https://github.com/LeCAR-Lab/human2humanoid) | LICENSE 없음 | 1 | 링크만 |
| halomi | HALOMI: Learning Humanoid Loco-Manipulation with Active Perception from Human Demonstrations | 프리프린트, 2026-06 | [2606.18772](https://arxiv.org/abs/2606.18772) | 없음 | – | 1 | 링크만 |
| humanoidbench | HumanoidBench: Simulated Humanoid Benchmark for Whole-Body Locomotion and Manipulation | 프리프린트, 2024-03 | [2403.10506](https://arxiv.org/abs/2403.10506) | [carlosferrazza/humanoid-bench](https://github.com/carlosferrazza/humanoid-bench) | NOASSERTION | 1 | 링크만 |
| clone | CLONE: Closed-Loop Whole-Body Humanoid Teleoperation for Long-Horizon Tasks | 프리프린트, 2025-06 | [2506.08931](https://arxiv.org/abs/2506.08931) | 없음 | – | 1 | 링크만 |

저장소 크기·라이선스는 GitHub API `size`(KB)·`license` 필드로 확인했다(2026-10-23): GR00T-VisualSim2Real 3,512, WBC-AGILE 1,084, OpenHomie 77,090, AMO 46,709, VisualMimic 159,802, DemoHLM 50,265, FALCON 127,108, TWIST2 36,891, WholebodyVLA 45,934, OpenWBT 158,801, GR00T-WholeBodyControl 412,936, HOVER 5,597, HEX 8,392, OpenHLM 9,856, ResMimic 27,892, MHC 13,431, SkillBlender 47,187 — [GitHub REST API](https://docs.github.com/rest/repos/repos#get-a-repository).

#### 항목별 상세 (유사도 4–5)

**viral (유사도 5)** — 하위 = HOMIE(G1 하체 RL, 사전학습). 논문은 "pre-trained WBC policy" 를 쓴다고만 하고 동결 여부를 명시하지 않는다 — [VIRAL](https://arxiv.org/html/2511.15200v1). 코드는 HOMIE 를 `homie_walk_model_path`·`homie_stand_model_path`(걷기·서기 두 모델)로 불러 행동 항 안에서 돌리며, 학습 대상이 아니다 — [walk_stand_place_grasp_turn_homie.yaml](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/exp/loco_manip/walk_stand_place_grasp_turn_homie.yaml).
- HOMIE 명령 벡터: `loco_vel`(3), `height`(1), `rpy`(3), `left_arm`(7), `right_arm`(7), 손(각 1). 높이 기본값 0.74 m 에 더한다. 이 과제의 teacher 가 실제로 움직이는 것은 `loco_vel`·`right_arm`·`right_hand` 뿐이고 높이·rpy·왼팔은 기본값에 고정 — [obs_walk_stand_place_grasp_turn_homie.yaml](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/obs/loco_manip/obs_walk_stand_place_grasp_turn_homie.yaml).
- HOMIE 명령 자르기: vx·vy ±0.5 m/s, wz ±1.0 rad/s, 높이 0.3–0.75 m, roll·pitch·yaw ±0.5 rad. 잘린 양의 제곱합을 벌점으로 주는 `penalty_homie_action_limit` 과 명령 변화 벌점 `penalty_homie_action_rate` 가 있다 — [walk_stand_place_grasp_turn_homie.yaml (env)](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/env/walk_stand_place_grasp_turn_homie.yaml), [homie_base.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/envs/base_task/homie_base.py).
- 상체 목표를 현재 관절 위치 ±0.5 rad 안으로 자르는 `clip_upper_actions` 옵션이 구현돼 있으나 이 과제 설정에서는 꺼져 있다(`False`) — 같은 파일들.
- teacher 행동 = 델타: 오른팔 7·손가락 1(그리고 설정상 속도 3)의 증분 × 0.1 을 누적해 명령으로 쓴다(`delta_action_scale: 0.1`, `no_delta_vel: True` 로 속도는 델타에서 제외되는 것으로 보임) — 같은 env yaml. 논문: "this delta representation significantly accelerates and stabilizes RL training", 절대 행동은 "fails to reach high success" — [VIRAL](https://arxiv.org/html/2511.15200v1).
- teacher 관측(226 차원/스텝)에는 현재 HOMIE 명령(`b_homie_commands`)과 누적 델타(`delta_actions`)가 들어간다 — obs yaml, 논문 Table 1.
- 시연 상태 초기화(RSI): 시뮬 텔레옵 시연 200 개를 리셋 상태로 쓴다. 없으면 teacher 성공률이 "below 10%" 에서 정체 — [VIRAL](https://arxiv.org/html/2511.15200v1).
- PPO 32,768 env, γ 0.998, MLP [512,256,128], 16 GPU. student 는 RGB 108×192(DINOv3) + 고유감각 + 델타 행동 + HOMIE 명령, DAgger 와 BC 를 α = 0.5 로 섞고 65,535 env. 순수 BC(α = 1)는 "brittle". 시각 무작위화를 끄면 0.649(−35.1 %) — [VIRAL](https://arxiv.org/html/2511.15200v1).
- 실기: 두 탁자 사이 걷기·놓기·집기·돌기 연속 54/59(약 91.5 %), 주기 20.2 s(전문 텔레옵 21.4 s). teacher 시뮬 "nearly 95%". 물체 질량은 다루지 않음 — [VIRAL](https://arxiv.org/html/2511.15200v1).
- 가져올 것: 하위 명령 자르기 + 잘린 양 벌점, 델타 행동(배율 0.1), 현재 명령을 관측에 넣기, 시연 RSI, DAgger/BC 혼합 α.

**doorman (유사도 5)** — 같은 HOMIE 스택, G1 + 3손가락 손, RGB 만(D435i 깊이 미사용). 특권 teacher(문·손잡이 변환, 손 18 몸체 접촉 렌치, 기저 선속도), 50 Hz, 행동 변화 벌점 −0.01 — [DoorMan](https://arxiv.org/html/2512.01061v1).
- 단계 리셋: 단계(0–5)마다 최근 스냅숏 100 개를 굴려 담고 일정 확률로 거기서 리셋. 버퍼 100 이면 약 1,700 iteration 에 모든 단계 도달, 10 이면 4,000 넘게, 없으면 실패 — 같은 출처.
- student(ResNet + 2층 LSTM 512) DAgger 후 **teacher 80–90 % 대비 student 50–70 % 에서 정체**, 이진 성공 보상 + 부드러움 벌점의 GRPO 미세조정 후 80.8–85.8 % — 같은 출처.
- 실기 83 %(전문 텔레옵 80 %, 비전문 60 %), 완료 시간 최대 31.7 % 단축. CVPR 2026 — [NVIDIA Research](https://research.nvidia.com/labs/lpr/publication/xue2026opening/).
- 가져올 것: 우리 student 20 %p 격차와 같은 크기의 격차를 GRPO(희소 성공 보상) 미세조정으로 메운 유일한 휴머노이드 실기 사례. 단계 리셋 버퍼.

**agile (유사도 4)** — G1 + Booster T1, Isaac Lab + RSL-RL. 높이 제어 G1 보행 정책을 동결해 "lower-body API" 로 쓰고, 그 위에서 **오른팔·허리만 RL 로 학습한 상체 전문가**(특권 상태, 레퍼런스 궤적 유도, 20k iteration)가 pick-and-place 시연을 만들어 GR00T N1.5 를 미세조정, 시뮬 100 회 90 % — [AGILE](https://arxiv.org/html/2603.20147v1).
- 하위 학습 시 허리·상체 관절을 사다리꼴 속도 프로파일로 무작위 구동(코드: 최대 속도 5–10 rad/s), 명령 vx −0.5–1.5, vy ±0.5, wz ±1.0, 높이 0.4 m–기본 골반 높이, 걷기 최소 높이 0.5 m, 재표본 7.5–10 s, 기저 질량 −1–+3 kg — [velocity_height_env_cfg.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/tasks/locomotion_height/g1/velocity_height_env_cfg.py).
- 동결 하위를 Isaac Lab `ActionTerm` 로 감싼 `AgileBasedLowerBodyAction`: TorchScript 정책을 불러 상위 행동 4 차원 `[vx, vy, wz, hip_height]` 를 받고, 명령별 `clip` 사전을 지원 — [policy_actions.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/mdp/actions/policy_actions.py). pick-place 과제는 이 행동 항(`unitree_g1_velocity_height_teacher_torchscript.pt`)과 상체 관절 행동(오른팔 배율 0.05)을 함께 쓴다 — [pick_place_tracking_env_cfg.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/tasks/pick_place/pick_place_tracking_env_cfg.py), [g1_pick_place_tracking_env_cfg.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/tasks/pick_place/g1/g1_pick_place_tracking_env_cfg.py).
- 대칭 거울 손실 teacher-student, L2C2, 가상 하네스 등 — [AGILE](https://arxiv.org/html/2603.20147v1). 대상 버전 Isaac Lab 3.0.0-beta2, Isaac Sim 6.0, RSL-RL 5.4.1 — [README](https://github.com/nvidia-isaac/WBC-AGILE).
- 가져올 것: dev12 하체를 Isaac Lab 행동 항으로 감싸는 코드 꼴 그대로(우리 상위는 4 → 6 명령 + 상체 11).

**visualmimic (유사도 4)** — G1 + D435i. 하위 = 사람 동작(AMASS·OMOMO, GMR 리타깃)으로 teacher-student 학습한 **키포인트 추종기**(명령 = 루트 위치 오차 + 머리·두 손·두 발 5 키포인트의 루트 기준 오차). 하위 학습 때 명령 각 차원에 ×U(0.5, 1.5) 곱셈 잡음("relative noise level to 50%"). 상위 = 과제별 RL teacher(특권 물체 상태) → 깊이 student(DAgger) — [VisualMimic](https://arxiv.org/html/2509.20322v2).
- **상위 행동 자르기**: 하위 학습 때 기록한 입력 정규화기의 μ·σ 로 상위 출력 범위를 "μ±1.64σ, which covers approximately 90% of the probability mass" 로 제한 — 같은 출처.
- 상자 들기 시뮬 15″×20″×20″ 0.5 kg, 실기 0.5 kg 상자를 1 m 로. 실기 성공률 수치 없음. 시뮬 Lift Box: student 높이 1 ± 0 m, 떨어뜨림 30 ± 23 %(teacher 34 ± 25 %). Push Box 거리 teacher 152 ± 36 vs student 37 ± 28 — 같은 출처.
- 가져올 것: 상위 출력을 "하위가 학습 때 본 명령 분포" 로 자르는 규칙, 하위의 명령 잡음 내성 학습.

**homie (유사도 4)** — G1(+GR-1). 하체 RL 명령 `C_t = [v_x, ω_yaw, h]`(파라미터 표엔 vy 도 있음), G1 vx −0.80–1.20 m/s, yaw ±0.80 rad/s, 쪼그림 높이 범위 표기 −0.24–0.74 m, 걷기 높이 0.74 m, 4 s 마다 재표본. 허리 명령 없음 — [HOMIE](https://arxiv.org/html/2502.13013).
- 상체: 진폭 ρ_a 를 0 에서 시작해 선속도 보상이 문턱을 넘을 때마다 +0.05, 지수꼴 분포에서 뽑고 1 s 마다 재표본·선형 보간. 하체 관측에는 상체 목표가 없고 상체 관절 위치·속도만(6 스텝 이력) — 같은 출처.
- 자율 상위: Seer 계열 IL(다시점 RGB + q + 상체 명령 + C_t, 10 Hz), 출력은 팔·손·높이 명령. 실기 Squat Pick 73.3 %, Pick & Place 80.0 %(각 15 회). 하위 동결 여부 미기재 — 같은 출처. RSS 2025 — [RSS 프로그램](https://roboticsconference.org/2025/program/papers/70/).
- 가져올 것: 상위가 상체 관절 + 높이 명령을 동시에 내 쪼그려 집기를 한 실기 사례(우리와 같은 출력 꼴, 단 IL).

**amo (유사도 4)** — G1 + Dex3 손 + 3 DoF 능동 머리. 하위 명령 v = [vx, vy, vyaw] + 몸통 rpy + 높이. 학습 범위 높이 0.5–0.8 m, roll ±0.7, pitch −0.52–1.57, yaw ±1.57 rad. 하위 행동 15 = 다리 12 + 허리 3. AMO 모듈(TO 데이터로 학습한 MLP)이 상체 관절·rpy·h → 하체 레퍼런스 관절. 팔 목표는 4,000 스텝까지 기본 자세, 이후 AMASS — [AMO](https://arxiv.org/html/2505.03738).
- 자율 상위: ACT(DINOv2), 관측에 **직전 명령 v, rpy, h** 를 넣고 출력 `[q_head, q_arm, q_hand, v, rpy, h]`. 실기 종이가방 집기 8/10·옮기기 8/10·놓기 9/10 — 같은 출처.
- 추종: 서기 높이 오차 0.0151 m(AMO 없이 0.1168), 학습 밖 높이 0.4 m·yaw ±2 rad 까지 추종 — 같은 출처.
- 가져올 것: 상위 관측에 직전 명령을 넣는 꼴, 몸통 pitch 를 크게 쓰는 하위 설계(우리 pitch ±45° 와 비슷한 축).

**hiwet (유사도 4)** — G1. 1단계 하위 추종기 명령 `u = [vx, vy, ωz, h_des, T_L, T_R(기저 좌표 손 자세), α(허리 정규화 가중)]`, 평가 범위 v ±1 m/s, ωz ±3 rad/s, 높이 0.3–0.78 m. 2단계 **RL(PPO, 비대칭 actor-critic) 상위가 같은 u 를 출력**, 하위는 "frozen". 상위는 고유감각·월드 기저 자세·과제 명령을 보고, critic 만 참 기저 속도를 본다 — [HiWET](https://arxiv.org/html/2602.06341v1).
- 시뮬 손 끝 오차 12.4 ± 2.4 mm, 실기 원 RMSE 0.012 m(LiDAR 위치추정). 상위 시험은 한 팔, 접촉 많은 잡기는 다루지 않음 — 같은 출처.
- 가져올 것: 우리와 같은 꼴(높이 0.3–0.78 + 손 목표 + 속도)의 RL 상위를 동결 하위 위에 PPO 로 학습한 설정.

**refine_dp (유사도 4)** — Booster T1. 하위 = 분리된 하체(발 디딤 명령)·상체(루트 좌표 SE(3) 손 자세) RL, 50 Hz. 상위 = 확산 정책(10 Hz, 상태 기반 모캡 입력)이 기저 속도·손 자세·그리퍼를 출력 — [REFINE-DP](https://arxiv.org/html/2603.13707v2).
- **동결 하위의 문제를 수치로 보인 사례**: 상위 명령이 사전학습 때의 정지 명령과 달라 "distribution mismatch that degrades tracking performance", 상위만 미세조정하면 과제를 위해 "overcommand" 해 추종이 나빠진다. 하위만 최적화해도 장기 pick-and-place 성공 +18 %, 공동 최적화 시 90 % 도달 20 iteration(사전학습 하위는 40) — 같은 출처.
- 상자 집기 과제 포함. 사전학습 50–70 % → DPPO 미세조정 90 % 이상. 실기 상자 운반 50 %, 문 열기 70 % 이상 — 같은 출처.
- 가져올 것: 동결 하위가 상위 학습 중 추종 저하를 일으키는지 재는 지표(추종 오차를 상위 학습 전후로 기록)와, 필요하면 하위를 추종 보상 유지한 채 함께 미세조정하는 선택지.

**oil (유사도 4)** — Digit V3. 하위 = 동결 MHC(Masked Humanoid Controller), 기저 지시(평면 속도·회전·기저 자세, 높이 U(0.36, 1.05) m) + **8 차원 팔 관절 지시**. OIL 층 = 2층 LSTM(64) PPO 정책이 팔 관절 목표 8 개를 출력, 기저 지시는 별도 생성기 — [OIL](https://arxiv.org/html/2610.14033).
- 관측: 관절 위치·속도, 기저 각속도·자세(선속도 제외), 로봇 좌표 물체 자세(실기 10 Hz), 손·물체 목표, 접촉 플래그. 학습 때 물체 상태 갱신율을 U(7, 15) Hz 로 무작위하고 사이에는 값 유지. 행동 변화 L1 벌점 — 같은 출처.
- 물체 질량 U(0.1, 3.0) kg, 크기 0.16–0.25 m. 6.5 kg 에서도 약 80 % 이상. 시뮬 평균 90.4 %, 구성(집기→운반→놓기→밀기) 무미세조정 78.9 % — 같은 출처.
- 가져올 것: 팔 관절 목표만 내는 RL 층을 동결 WBC 위에 얹은 실기 사례, 지각 갱신율 무작위.

#### 항목별 요약 (유사도 1–3)

- **hugo (3)**: G1, 동결 하위 둘(rl_isaac, SONIC 3점 VR)의 10 차원 명령 `[a_base(3), p_ee^L, p_ee^R, z_body]`. **같은 명령 공간의 PPO 상위 기준선(384M 스텝, 과제별 밀집 보상)이 Lift Box 0.0 %**, Push Box 1.67 %. 원인: "reinforcement learning discovers how to act on the object but not the staged structure". LLM 코드 정책은 rl_isaac Lift Box 75.92 %, SONIC 24.91 %(SONIC 은 걷는 중 높이를 못 바꿈). 실기 Lift Box 최고 66.7 %, 상자가 두 하위 모두에서 들 때 미끄러짐 — [HuGo](https://arxiv.org/html/2609.30594v1).
- **r2s2 (3)**: H1. 기본 기술(보행 vx·vy·ω, 높이 h + 몸통 pitch, 6D 손 도달)을 잠재 공간으로 묶고 동결 디코더 위에 PPO 상위. 상자 집기 시뮬 100 %/0.04 m, 실기 90 %(10 회). 잠재 공간 없이(명시 명령) 43.29 %, 바닐라 PPO·HumanoidBench 계층 0 % — [R2S2](https://arxiv.org/html/2505.10918v2). RA-L — [OpenAlex](https://api.openalex.org/works/doi:10.1109%2FLRA.2025.3645662). 잠재 공간 논의는 연구자 (c) 몫.
- **demohlm (3)**: G1 + D435(2 DoF 목) + 그리퍼. 하위 명령 `(vx, vy, ω, h, r, p, y, q_upper)`(AMO 를 따름, 범위 미기재). 상위 = 한 번의 시연에서 생성한 데이터로 IL(ACT·DP 등), 10 Hz, 관측 `[q, q̇, r, p, 카메라 좌표 물체 6D 자세]`. 시뮬 LiftBox 98.83 %, 실기 LiftBox 5/5 — [DemoHLM](https://arxiv.org/html/2510.11258v1).
- **ulc (3)**: G1 단일 통합 제어기. 명령 vx −0.45–0.55, vy ±0.45, wz ±1.2, 골반 높이 0.3–0.75 m, 몸통 yaw ±2.62, roll ±0.52, pitch −0.52–1.57 rad, 팔 관절. 순차 기술 습득, 잔차 팔 행동, **명령 5차 다항 보간 1.0 s**, 관절별 무작위 지연 해제 p = 0.5, 손목 하중 0–2 kg. 2 kg 하중 팔 오차 E_a 0.05(AMO 0.16, HOMIE 0.18, FALCON 0.11). 상위 정책 없음(VR 텔레옵) — [ULC](https://arxiv.org/html/2507.06905).
- **falcon (3)**: G1·T1, 하체 에이전트(루트 선·각속도, stance, 높이, 허리 yaw) + 상체 에이전트(관절 목표) 이중 RL, 3D 손 힘 커리큘럼(X·Y ±50–100 N, Z −60–+5 / −100–+5 N, 토크 한계 인식 표본). 실기 손당 1.2 kg, 과열로 지속 운반 약 2 kg/팔. 자율은 모캡 + FoundationPose + IK + 상태 기계 — [FALCON](https://arxiv.org/html/2505.06776). L4DC 2026 — [PMLR](https://proceedings.mlr.press/v331/zhang26a.html).
- **twist2 (3)**: G1 + 2 DoF 목 ZED Mini. 하위 = 범용 동작 추종기, 명령 p_cmd = 루트 x·y 속도, 루트 높이, roll·pitch, yaw 각속도, 전신 관절 위치. 상위 = 확산 정책, 관측은 RGB + **과거 p_cmd 열만**(로봇 원시 상태 없음), 출력 = 같은 p_cmd 64 스텝 덩어리, 20 Hz 추론. Kick-T 6/7 — [TWIST2](https://arxiv.org/html/2511.02832).
- **wholebodyvla (3)**: AgiBot X2. 하위 LMO RL 명령 = 이산 {−1,0,1}³(전진·옆·회전) + 연속 자세 높이, 상체 관절은 VLA 디코더가 직접. LMO 는 데이터 수집·배포 내내 고정. 하중 무작위 몸통 [−5, 10]·손 [−0.1, 0.3](단위 미기재), AgiBot World 팔 동작 재생 교란. 상자 싣기(쪼그려 잡기 19/25, 일어나 돌기 17/25) — [WholeBodyVLA](https://arxiv.org/html/2512.11047v2). ICLR 2026 — [ICLR](https://iclr.cc/virtual/2026/poster/10009805).
- **skillblender (3)**: H1·G1·H1-2 시뮬. 동결 기본 기술(걷기 속도, 손 도달, 쪼그림 높이, 발 디딤) 위에 PPO 상위가 하위 목표와 관절별 혼합 가중을 출력. PackageLift 오차 0.024(평면 PPO 0.026, HumanoidBench 계층 0.571). 상위 실기 배치 없음 — [SkillBlender](https://arxiv.org/html/2506.09366).
- **anymal_pnp (3, 사족)**: ANYmal D + 팔. 사전학습 보행 정책(동결) + 팔 정책 위에 RL 상위(기저 속도·손 끝 자세·그리퍼), 7 단계 동적 보상 커리큘럼, teacher-student. 실기 1.5 kg 상자 8/9 — [2509.13239](https://arxiv.org/html/2509.13239). 사족·증류 쪽은 연구자 (a) 몫.
- **humanoidmimicgen (2)**: G1, HOMIE 를 하위로 쓰는 API(상체 관절 + 기저 4 벡터 ẋ, ẏ, θ̇, z). "not in a way that perfectly tracks velocity actions" 라서 계획 대신 실제 도달 자세로 갈아끼움. GR00T N1.6 미세조정, 시뮬 Box Lift Floor 0.97 — [HumanoidMimicGen](https://arxiv.org/html/2605.27724).
- **openhlm (2)**: G1, SONIC 기반 관절 추종기 + π0.5 VLA. 인터페이스 비교(관절 32 차원 vs 분리 21 차원 vs VR 3점 24 차원), **미리보기 지연 0.2 s 가 최적(0.6 s 면 진행률 13 %)** — [OpenHLM](https://arxiv.org/html/2606.22174).
- **workhorse (2)**: G1, 하위 = BeyondMimic 계열 RL 이 5 링크(몸통·두 손목·두 발) 목표를 추종, 상위 = 흐름 정합 IL 계획기 5 Hz. 하위 학습 때 **상자 들기 중 손목을 벌리는 스프링 최대 40 N**, 명령 증강(재계획 간격 0.2–1 s, 수평 10 cm·yaw 10° 표류). 명령 증강을 빼면 밀림 하 성공 64 → 52 % — [Workhorse](https://arxiv.org/html/2610.09117).
- **cwi (2)**: LimX Oli, 골반 높이 명령 0.17–0.9 m, VR 텔레옵만. AMO 류 계층은 "the lower-body reference remains near standing" 이라고 비판 — [CWI](https://arxiv.org/html/2606.27676v1).
- **splitadapter (2)**: G1, 동결 PhysHSI 식 AMP 기본 정책 + 하중 적응 모듈(질량 추정 m̂·적재 상태 ℓ̂), 상자 0.5–5.0 kg·높이 0–0.6 m 학습. 실기 전체 26/27(기본 16/27). 계층 상위 없음 — [SplitAdapter](https://arxiv.org/html/2606.03297v1).
- **hulk (2)**: G1 하위 명령 vx·vy ±0.5, wz ±0.5, 높이 0.5–0.8 m, roll ±0.2, pitch ±0.25 rad, 팔 14 관절. 상위 정책 없음. 실기 운반 11 kg(최대 12.25 kg) — [HULK](https://arxiv.org/html/2610.08970).
- **ceer (2)**: 루트 + 손 끝 자세 명령만 받는 하위(범용 추종기에서 증류), 이질적 계획기를 재학습 없이 꽂음, 손 끝 3.3 cm, 시뮬 단일 물체 최대 70 % — [CEER](https://arxiv.org/abs/2605.19981v1).
- **leverb (2)**: G1, 하위가 256 차원 잠재 명령을 5 스텝마다 받음(50 Hz), 상위 VLA 약 10 Hz. 시뮬 58.5 % — [LeVERB](https://arxiv.org/html/2506.13751).
- **mobile_tv (2)**: H1, 하체 RL 명령 = 선속도·rpy·높이, 상체는 IK·리타깃을 PD 로 직접, CVAE 동작 사전(64 차원)을 하체 관측에 넣음. 자율 상위 없음 — [Mobile-TeleVision](https://arxiv.org/html/2412.07773v2).
- **hover (2)**: 루트 속도·상체 관절 각 등 여러 모드를 하나로 증류한 다중 모드 제어기, ICRA 2025 — [HOVER](https://arxiv.org/abs/2410.21229).
- **gr00t_wbc (2)**: Decoupled WBC(하체 RL + 상체 IK)가 GR00T N1.5·N1.6 의 하위, GEAR-SONIC 은 별도. 명령 형식은 README 에 없음 — [GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl).
- **hex (2)**: TienGong 2.0·3.0, VLA 가 상체 행동과 하체 명령(서기·걷기·무릎 꿇기 모드)을 동시 출력, 보간 없이 전달. 장기 상자 운반 53.3 % — [HEX](https://arxiv.org/html/2604.07993).
- **haf (2)**: TienKung, VLA 동결 + 잠재 흐름 잡음 위 스펙트럼 SAC(실기 RL), Box Transfer 93.3 — [HAF](https://arxiv.org/html/2608.16837).
- **resmimic (2)**: 사람 동작으로 학습한 GMT 위에 잔차 정책(점구름 물체 추종 보상, 가상 물체 제어기 커리큘럼) — [ResMimic](https://arxiv.org/abs/2510.05070). 지난 dev10(SONIC 위 teacher)과 같은 계열이며 연구자 (b) 몫.
- **being0·trajbooster·omnih2o·halomi·humanoidbench·clone (1)**: 기초 모델·VLM 연결기 + 기술 라이브러리(Being-0), VLA 가 전신 동작을 내는 데이터 증강(TrajBooster), 운동학 자세를 범용 인터페이스로 쓰는 텔레옵·자율(OmniH2O), 능동 지각 머리-손 추종(HALOMI), 시뮬 벤치마크의 계층 기준선(HumanoidBench), 폐루프 텔레옵(CLONE) — [Being-0](https://arxiv.org/abs/2503.12533), [TrajBooster](https://arxiv.org/abs/2509.11839), [OmniH2O](https://arxiv.org/abs/2406.08858), [HALOMI](https://arxiv.org/abs/2606.18772), [HumanoidBench](https://arxiv.org/abs/2403.10506), [CLONE](https://arxiv.org/abs/2506.08931).

### Inferences
- 우리 분할(하체 = 명령 추종 RL, 상체 = 외부 PD 목표, 상위가 둘 다 냄)은 HOMIE·AMO·VIRAL·DemoHLM·HumanoidMimicGen 이 쓰는 "decoupled WBC" 와 같은 꼴이다. 차이는 (1) 우리 하체가 상체 목표와 그 변화율을 직접 관측한다는 점(HOMIE 는 상체 관절 상태만, Mobile-TeleVision 은 CVAE 잠재), (2) 손 하중 0–5 kg 학습(HOMIE 손 −0.1–0.3 kg 보다 훨씬 큼), (3) 상위를 RL teacher → 깊이 student 로 학습한다는 점이다. (3)을 한 실기 사례는 VIRAL·DoorMan(RGB, HOMIE)과 VisualMimic(깊이, 키포인트 추종기)뿐이다.
- 지난 dev10 의 세 문제에 대응하는 공개 처방이 각각 있다: 추종기 능력 밖 출력 → VIRAL 명령 자르기 + 잘린 양 벌점, VisualMimic μ±1.64σ 자르기, AGILE 행동 항 clip. 켜짐/꺼짐 포화 → VIRAL 델타 행동(배율 0.1 누적, 절대 행동은 실패). student 격차 → DoorMan GRPO(50–70 → 80.8–85.8 %), VIRAL DAgger/BC α 0.5.
- HuGo 의 RL 기준선(Lift Box 0 %)과 VIRAL 의 RSI 없음(<10 %)은 "동결 하위 + 명시 명령 + 밀집 보상 PPO" 만으로는 집기처럼 단계가 있는 과제에서 탐색이 막힌다는 같은 신호다. 단계 리셋(DoorMan), 시연 RSI(VIRAL), 단계 보상 커리큘럼(사족 2509.13239)이 그 해법으로 쓰였다.
- K1(35.7 kg)과 질량이 가장 비슷한 플랫폼은 G1(약 35 kg, [dev12 보고서](/home/robotis-ai/Projects2/dev12/reports/dev12%20구현%20참고%20연구와%20오픈소스.md))이고, 위 실기 사례 대부분이 G1 이다.

### Gaps
- BumbleBee(2506.12779) 초록 조회가 시간 초과로 실패했고, Humanoid-VLA(2502.14795)는 조회하지 않았다. 둘 다 명시 명령 계층의 상위 RL 학습과는 거리가 있다고 보지만 확인하지 못했다.
- HOMIE·AMO·DemoHLM·VIRAL·DoorMan 논문은 상위 학습 중 하위 동결 여부를 명시하지 않는다. VIRAL 은 코드에서 하위가 파일로 불려 학습 대상이 아님을 확인했지만, 나머지는 추정이다.
- ULC 코드 저장소, OIL·HiWET·REFINE-DP·HuGo 코드는 찾지 못했다. VisualMimic 은 하위·상위 학습 코드가 미공개(README 체크리스트).
- FALCON·AMO 의 학회는 각각 PMLR 페이지·2차 인용으로 확인했고, VisualMimic·TWIST2·ULC·HiWET 등은 학회 정보를 찾지 못해 프리프린트로 표기했다.

## Q2. 하위가 동결일 때 상위를 어떻게 학습하는가: 상위가 하위에 대해 무엇을 관측하나, 명령 평활·속도 제한, 지연 처리

### Takeaway
공개 사례 가운데 **하위의 추종 오차를 상위 관측에 명시적으로 넣은 것은 찾지 못했다**. 대신 (1) 현재(잘린) 명령·누적 델타·직전 명령·명령 이력을 관측에 넣고(VIRAL·AMO·TWIST2·HuGo), (2) 상위 출력을 하위 학습 분포 안으로 자르며(VIRAL·VisualMimic·AGILE), (3) 델타·보간·변화 벌점으로 명령을 매끄럽게 하고(VIRAL·OIL·ULC·HOMIE), (4) 지각 갱신율·미리보기 지연을 무작위화하거나 고른다(OIL·OpenHLM). 하위를 끝까지 동결하면 상위가 "overcommand" 해 추종이 나빠진다는 반대 증거(REFINE-DP)도 있다.

### Cited Findings
**상위가 관측하는 것**
- VIRAL teacher actor: 기저 선·각속도, 중력, 직전 행동, 단계, 누적 델타 행동, 관절 위치·속도, 물체·탁자·손 변환, 손가락 끝 힘, **현재 HOMIE 명령(`b_homie_commands`)**. HOMIE 입력용으로 명령 이력 5 스텝도 둔다 — [obs yaml](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/obs/loco_manip/obs_walk_stand_place_grasp_turn_homie.yaml). student 는 RGB + 기저 각속도·중력·행동·다리·팔 관절·델타 행동·HOMIE 명령(기저 선속도 없음) — [VIRAL](https://arxiv.org/html/2511.15200v1).
- AMO 상위 상태 토큰: 상체 고유감각 + 직전 v, rpy, h — [AMO](https://arxiv.org/html/2505.03738).
- TWIST2 상위: RGB + 과거 p_cmd 열(로봇 원시 상태 없이) — [TWIST2](https://arxiv.org/html/2511.02832).
- HuGo: 기저 위치·방향, 기저 속도, 손 끝 위치, 몸 높이, 물체·목표, **직전 명령** — [HuGo](https://arxiv.org/html/2609.30594v1).
- OIL: LSTM 이 실행 이력을 보며 추종 오차 입력은 없음, 기저 선속도는 실기 추정이 어려워 뺌 — [OIL](https://arxiv.org/html/2610.14033).
- HiWET: 고유감각 + 월드 기저 자세 + 과제 명령, critic 만 참 기저 속도·월드 손 자세 — [HiWET](https://arxiv.org/html/2602.06341v1).
- DemoHLM: 관절 위치·속도, 몸통 roll·pitch, 물체 6D 자세. 명령 이력 언급 없음 — [DemoHLM](https://arxiv.org/html/2510.11258v1).
- Workhorse 계획기: 영상 4 장(0.24 s 간격) + 5 링크 이력 9 샘플(0.12 s 간격) — [Workhorse](https://arxiv.org/html/2610.09117).

**명령 자르기·평활·속도 제한**
- VIRAL: HOMIE 명령 자르기(vx·vy ±0.5, wz ±1.0, 높이 0.3–0.75, rpy ±0.5) + 잘린 양 제곱 벌점 + 명령 변화 벌점, 델타 배율 0.1. 논문 보상표의 델타 행동 변화 −0.01, 출력 부드러움 −9.0 — [homie_base.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/envs/base_task/homie_base.py), [env yaml](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/env/walk_stand_place_grasp_turn_homie.yaml), [VIRAL](https://arxiv.org/html/2511.15200v1). 속도 명령 크기가 0.1 미만이면 0 으로 만들어 서기 모델로 넘어가게 한다 — 같은 homie_base.py.
- VisualMimic: 상위 출력을 하위 정규화기 통계의 μ±1.64σ 로 자름, 하위는 명령 ×U(0.5, 1.5) 잡음으로 학습 — [VisualMimic](https://arxiv.org/html/2509.20322v2).
- AGILE: 동결 하체 행동 항이 `[vx, vy, wz, height]` 별 clip 사전을 받음, 상체 행동 배율 0.05 — [policy_actions.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/mdp/actions/policy_actions.py), [g1_pick_place_tracking_env_cfg.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/tasks/pick_place/g1/g1_pick_place_tracking_env_cfg.py).
- OIL: 행동 변화 L1 벌점 — [OIL](https://arxiv.org/html/2610.14033). DoorMan: 행동 변화 −0.01, GRPO 에도 관절 속도·가속·행동 변화 벌점 — [DoorMan](https://arxiv.org/html/2512.01061v1).
- 하위 쪽 평활: HOMIE 상체 목표 1 s 선형 보간 — [HOMIE](https://arxiv.org/html/2502.13013). ULC 명령 5차 다항 보간 1.0 s + 관절별 무작위 지연 해제 — [ULC](https://arxiv.org/html/2507.06905). HEX 는 하체 명령을 보간 없이 전달 — [HEX](https://arxiv.org/html/2604.07993).
- 하위의 상위 오차 내성: Workhorse 는 하위 학습 때 재계획 간격 0.2–1 s, 수평 10 cm·yaw 10° 표류 명령 증강, 빼면 밀림 하 성공 64 → 52 %, 낙상 15 → 23 % — [Workhorse](https://arxiv.org/html/2610.09117).

**주기·지연**
- 상위 10 Hz / 하위 50 Hz: DemoHLM, WholeBodyVLA(디코드 약 10 Hz, LMO 50 Hz), OpenHLM — [DemoHLM](https://arxiv.org/html/2510.11258v1), [WholeBodyVLA](https://arxiv.org/html/2512.11047v2), [OpenHLM](https://arxiv.org/html/2606.22174). LeVERB 잠재 5 스텝마다(50 Hz 하위) — [LeVERB](https://arxiv.org/html/2506.13751). HuGo 상위 50 Hz(rl_isaac)·10 Hz(SONIC) — [HuGo](https://arxiv.org/html/2609.30594v1). DoorMan teacher 50 Hz — [DoorMan](https://arxiv.org/html/2512.01061v1).
- OpenHLM 미리보기 지연 Δt: 0.2 s 에서 진행률 67 %, 0.6 s 에서 13 % — [OpenHLM](https://arxiv.org/html/2606.22174).
- OIL 은 학습 중 물체 상태 갱신율을 U(7, 15) Hz 로 무작위하고 갱신 사이 값을 유지, 실기는 50 스텝 칼만 필터 — [OIL](https://arxiv.org/html/2610.14033). VIRAL 은 센서 지연을 무작위화하고, student 관측 설정 이름에 `rgb_delay` 가 있다 — [VIRAL](https://arxiv.org/html/2511.15200v1), [obs 설정 폴더](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/gr00t/rl/config/obs/loco_manip/).

**탐색·초기화**
- VIRAL: 텔레옵 시연 200 개 RSI, 없으면 <10 % — [VIRAL](https://arxiv.org/html/2511.15200v1). DoorMan: 단계별 스냅숏 100 개 리셋 버퍼 — [DoorMan](https://arxiv.org/html/2512.01061v1). HuGo: 같은 명령 공간 PPO 가 Lift Box 0 % — [HuGo](https://arxiv.org/html/2609.30594v1). R2S2: 명시 명령 대신 잠재를 쓰면 43.29 → 100 %, "the discrete skill indicator hinders RL exploration" — [R2S2](https://arxiv.org/html/2505.10918v2).

**동결 대 공동 학습**
- 동결 유지: HiWET("frozen"), OIL(가중치 고정), WholeBodyVLA(LMO 고정), SkillBlender(기술 고정), R2S2(디코더 고정), SplitAdapter(기본 정책 고정·어댑터만) — [HiWET](https://arxiv.org/html/2602.06341v1), [OIL](https://arxiv.org/html/2610.14033), [WholeBodyVLA](https://arxiv.org/html/2512.11047v2), [SkillBlender](https://arxiv.org/html/2506.09366), [R2S2](https://arxiv.org/html/2505.10918v2), [SplitAdapter](https://arxiv.org/html/2606.03297v1).
- 공동 미세조정: REFINE-DP 는 상위만 미세조정하면 추종이 나빠지고, 하위만 최적화해도 +18 %, 공동이면 90 % 도달이 두 배 빠름 — [REFINE-DP](https://arxiv.org/html/2603.13707v2).

**teacher-student 격차**
- DoorMan 50–70 % → GRPO 후 80.8–85.8 %(teacher 80–90 %) — [DoorMan](https://arxiv.org/html/2512.01061v1). VIRAL 은 시뮬 teacher-student 수치 격차를 보고하지 않음 — [VIRAL](https://arxiv.org/html/2511.15200v1). VisualMimic Push Box 152 → 37, Kick Ball 189 → 135 — [VisualMimic](https://arxiv.org/html/2509.20322v2).

### Inferences
- 우리 하위는 "저역 통과된 상체 목표 + 변화율" 을 보므로, 상위 출력이 급변하면 하위가 학습 때 못 본 변화율을 받는다. VIRAL 식 델타(증분 × 작은 배율 누적)는 상위 출력 ±1 을 "최대 변화율" 로 바꿔, 포화가 곧 극단 자세가 되지 않게 한다. 지난 판의 켜짐/꺼짐 포화를 직접 겨냥한다.
- 상위 출력 범위는 dev12 학습 명령 분포(골반 높이 0.335–0.77, pitch ±45° 등)와 상체 목표 분포에서 뽑아 VisualMimic 처럼 자르고, VIRAL 처럼 잘린 양을 벌점으로 주는 것이 가장 직접적인 선례다. 높이·pitch 의 결합 가능 영역(낮은 높이에서 pitch 제한)은 단순 상자 자르기로 못 담으니 dev12 의 가능 영역 표를 그대로 상위 자르기에 써야 한다(추론).
- 추종 오차를 상위 관측에 넣은 선례는 없지만, VIRAL 이 "현재 명령 + 관절 상태" 를 함께 넣는 것은 사실상 같은 정보를 준다. 우리 teacher 에는 특권으로 하위 추종 오차(명령 높이 − 실제 골반 높이 등)를 넣고 student 에서는 명령 이력 + 고유감각으로 남기는 비대칭 구성이 가능하다(추론).
- HuGo·VIRAL 의 탐색 실패를 보면, 쪼그려 집기에는 RSI(스크립트 또는 dev12 재생으로 만든 쪼그림 자세·손 위치)나 단계 리셋 버퍼가 사실상 필수다.
- 상위 학습 중 하위 추종 오차를 계속 기록해, REFINE-DP 가 말한 "overcommand → 추종 저하" 가 보이면 그때 하위 미세조정(추종 보상 유지)을 고려하는 순서가 근거와 맞는다(추론).

### Gaps
- 상위가 하위 추종 오차를 명시 관측으로 받는 휴머노이드 사례는 찾지 못했다(검색어 "tracking error observation high-level" 등으로 찾았으나 없음).
- VIRAL·DoorMan 상위 정책의 실제 행동 주기(HOMIE 50 Hz 와 같은지)는 논문에 명시돼 있지 않다.
- 동결 하위 위 RL 상위에서 명령 변화율 상한(rate limiter)을 하드 제한으로 둔 사례는 찾지 못했다. 모두 벌점·델타·보간이다.

## Q3. 무거운 물체·손 외력을 하위에서 어떻게 다루나

### Takeaway
"동결 하위 + 상위" 사례들의 하위 하중 범위는 대체로 작다(HOMIE·WholeBodyVLA 손 −0.1–0.3 kg, AGILE 기저 −1–+3 kg, VIRAL 은 물체 질량 언급 없음). 손에 0–2 kg 이상을 명시적으로 학습한 하위는 ULC(손목 0–2 kg), FALCON(3D 힘 커리큘럼), HULK(±40 N·−50 N, 실기 11 kg), SplitAdapter(상자 0.5–5 kg)이고, 상위 쪽에서 물체 질량을 무작위한 것은 OIL(0.1–3 kg)이다. 우리 하위(손 0–5 kg)는 이 계층 사례들보다 하중 쪽이 이미 강하다. 두 손 조이기 상자를 하위 학습에서 모형화한 것은 Workhorse 의 "손목을 벌리는 최대 40 N 스프링" 이 유일하다.

### Cited Findings
- HOMIE: 몸통 하중 −5–10 kg, 손 하중 −0.1–0.3 kg, 4 s 마다 밀기 — [HOMIE](https://arxiv.org/html/2502.13013). 코드 `payload_mass_range = [-5, 10]`, `hand_payload_mass_range = [-0.1, 0.3]` — [g1_29dof_config.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/homie/code/HomieRL/legged_gym/legged_gym/envs/g1/g1_29dof_config.py).
- WholeBodyVLA LMO: 몸통 [−5, 10], 손 [−0.1, 0.3](단위 미기재) + AgiBot World 팔 동작 재생 교란 + 0.5 m/s 밀기 — [WholeBodyVLA](https://arxiv.org/html/2512.11047v2).
- AGILE G1 속도·높이: 기저 질량 −1–+3 kg, 몸체 질량 ×0.95–1.05 — [velocity_height_env_cfg.py](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/rl_env/tasks/locomotion_height/g1/velocity_height_env_cfg.py).
- AMO: 하중·외력은 다루지 않음 — [AMO](https://arxiv.org/html/2505.03738). VIRAL: 물체 질량 무작위 없음(시각·조명·재질·탁자·카메라만) — [VIRAL](https://arxiv.org/html/2511.15200v1).
- ULC: 손목 질량 0–2 kg 리셋마다, 기저 ±5 kg, 질량중심 추종 보상. 실기 0.5·1.0·1.5 kg — [ULC](https://arxiv.org/html/2507.06905).
- FALCON: 토크 한계 인식 3D 힘 표본(자코비안 + 관절 토크 한계로 축별 상한, Dirichlet 비율), 걷는 방향 반대 평면 힘, 저역 필터. 실기 손당 1.2 kg, 지속 운반은 과열로 약 2 kg/팔 — [FALCON](https://arxiv.org/html/2505.06776).
- HULK: 손목 힘 수평 ±40 N, 수직 −50–+5 N(명령 아님, 교란), 중심 MPC 가 보상 유도, 실기 11 kg(최대 12.25 kg) — [HULK](https://arxiv.org/html/2610.08970).
- OIL(상위 쪽): 물체 질량 U(0.1, 3.0) kg, 마찰 U(0.5, 1.5), 6.5 kg 에서 약 80 % 이상 — [OIL](https://arxiv.org/html/2610.14033).
- SplitAdapter: 동결 기본 정책 + 질량 추정 어댑터, 상자 0.5–5.0 kg, 6 kg 시뮬 10/10(기본 5/10), 실기 26/27 — [SplitAdapter](https://arxiv.org/html/2606.03297v1).
- Workhorse: 상자 들기 중 손목에 "It can only push the wrists apart, with up to 40 N" 스프링 — [Workhorse](https://arxiv.org/html/2610.09117).
- 상자 미끄러짐: HuGo 는 두 하위 모두에서 들 때 상자가 미끄러진다고 보고 — [HuGo](https://arxiv.org/html/2609.30594v1). OIL 구성 시험에서도 미끄러짐 언급 — [OIL](https://arxiv.org/html/2610.14033).
- 하위 쪽 손 하중 연구(FAME, Thor, HAFO, yahmp, Kinematics-Aware)는 이미 정리됨: HULK·Thor·HAFO 는 힘을 critic 특권으로만 두고도 실기에서 버팀, 배포 정책이 힘을 직접 추정한 것은 FAME·ADAPT 뿐 — [dev12 구현 참고 연구와 오픈소스.md](/home/robotis-ai/Projects2/dev12/reports/dev12%20구현%20참고%20연구와%20오픈소스.md).

### Inferences
- 우리 하위가 손 하중 0–5 kg 로 학습돼 있으므로, 상자 0.5–2 kg 는 하위 분포 안이다. 상위 teacher 학습에서는 OIL 처럼 상자 질량·마찰을 무작위하고, 6.5 kg 처럼 범위 밖에서도 평가해 하위 여유를 재는 것이 공개 선례와 맞다.
- 공 손 두 손 조이기에서는 조이는 힘이 손목을 "벌리는" 반작용으로 돌아온다. dev12 하위의 손 외력 무작위가 아래 방향 하중 위주라면, Workhorse 식 손목 벌림 힘(최대 40 N)은 하위가 학습 때 못 본 방향일 수 있다. dev12 외력 표본의 방향 분포를 확인할 필요가 있다(추론, dev12 설정은 이 노트에서 확인하지 않음).
- HuGo 의 미끄러짐 보고는 "명령 공간이 조이는 힘을 직접 못 표현하면 상자를 들 때 미끄러진다" 는 신호다. 우리 상위는 팔 관절 목표를 상자 안쪽으로 넘겨 PD 조임을 만드는 방식이 될 것이고, 이는 [쥐기는 조임을 명시적으로](/home/robotis-ai/.claude/projects/-home-robotis-ai-Projects2/memory/grip-needs-explicit-squeeze.md) 메모와도 같은 방향이다(추론).

### Gaps
- VIRAL·DoorMan 의 HOMIE 가 어떤 손 하중으로 학습됐는지는 GR00T-VisualSim2Real 저장소에 학습 코드가 없어 확인 못 했다(HOMIE 원본 기준 −0.1–0.3 kg 으로 추정).
- 두 손 조이기 상자를 하위 학습에서 접촉 물체로 넣은 계층 사례는 찾지 못했다(Workhorse 의 스프링 근사가 유일).

## Q4. 공개 코드(Isaac Lab / Isaac Gym / mjlab / MuJoCo)와 하위 체크포인트 공개 여부

### Takeaway
"동결 하위 + 상위 학습" 을 통째로 재현 가능한 공개 코드는 **GR00T-VisualSim2Real(VIRAL·DoorMan, Isaac Lab, Apache-2.0, HOMIE 걷기·서기 가중치가 Git LFS 로 들어 있음)**과 **WBC-AGILE(Isaac Lab 3.0 beta + RSL-RL 5.4.1, Apache-2.0, G1 속도·높이 teacher TorchScript 가 LFS 로 들어 있음)** 두 개다. 둘 다 Newton 이 아니라 Isaac Sim 물리 기준이다. HOMIE·AMO 는 하위 체크포인트(ONNX/TorchScript)는 공개했지만 상위 학습 코드가 없고, VisualMimic 은 sim2sim 과 실기 과제 체크포인트만 있다. mjlab 기반 계층 상위 코드는 찾지 못했다.

### Cited Findings
- GR00T-VisualSim2Real: Isaac Lab(Isaac Sim 5.1) + TRL + Hydra, teacher PPO·student DAgger·평가·ONNX 내보내기, Apache-2.0. VIRAL 은 main, DoorMan 은 doorman 브랜치 — [README](https://github.com/NVlabs/GR00T-VisualSim2Real). 클론의 `models/` 에 `model_walk.pt`, `model_stand.pt`, `dec_loco_model.onnx`, `decoupled_locomotion_stand_multi_amass_obsnoise_lr-20250601_173154_last.onnx` 등이 있으나 받은 사본은 132 바이트 LFS 포인터라 실제 가중치는 LFS 로 받아야 한다 — [models 폴더](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/viral/code/models).
- WBC-AGILE: Isaac Lab v3.0.0-beta2, Isaac Sim 6.0, Python 3.12, RSL-RL 5.4.1 + 작은 패치, sim-to-MuJoCo 검증, 대부분 Apache-2.0 과 RSL_RL 부분 BSD-3 — [README](https://github.com/nvidia-isaac/WBC-AGILE). `agile/data/policy/velocity_height_g1/` 에 teacher·history 의 TorchScript·state_dict 4 개(LFS 포인터) — [로컬 폴더](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/agile/data/policy/velocity_height_g1). 팀 경험 문서 `LESSONS_LEARNED.md` 동봉 — [LESSONS_LEARNED.md](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/agile/code/LESSONS_LEARNED.md).
- OpenHomie: Isaac Gym Preview 4, legged_gym·rsl_rl·HIMLoco 기반, `HomieDeploy/deploy.onnx` 동봉, 하드웨어(외골격) 설계 포함. LICENSE 파일은 CC BY-NC 4.0, README 는 CC BY-NC-SA 4.0 — [README](https://github.com/InternRobotics/OpenHomie), [LICENSE](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/homie/code/LICENSE).
- AMO: `amo_jit.pt`, `adapter_jit.pt`(AMO 모듈), MuJoCo `play_amo.py` 만, 학습 코드 없음, LICENSE 는 Apache-2.0 — [저장소](https://github.com/OpenTeleVision/AMO), [로컬 code](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/amo/code).
- VisualMimic: sim2sim 파이프라인·실기 과제 체크포인트 공개, 하위 추종기 학습 코드·체크포인트·상위 학습 코드·sim2real 은 미공개 — [README](https://github.com/visualmimic/VisualMimic).
- FALCON: Isaac Gym, 학습·sim2sim·sim2real 코드 공개, MIT — [README](https://github.com/LeCAR-Lab/FALCON).
- TWIST2: Isaac Gym 기반 제어기 학습·텔레옵, 상위 정책(iDP3 변형)은 별도 저장소 예정, MIT — [README](https://github.com/amazon-far/TWIST2).
- GR00T-WholeBodyControl: Decoupled WBC(N1.5·N1.6), GEAR-SONIC 학습 코드 + G1 체크포인트 3 개, Isaac Lab 2.3.2, 코드 Apache-2.0·가중치 NVIDIA Open Model License — [README](https://github.com/NVlabs/GR00T-WholeBodyControl).
- OpenWBT(R2S2 팀): G1 전신 텔레옵(MuJoCo·Isaac Sim 4.5), "Release Latent Skill Space" 는 미완료, Apache-2.0 — [README](https://github.com/GalaxyGeneralRobotics/OpenWBT).
- MHC(OIL 의 하위): Isaac Gym, ASE 기반 — [README](https://github.com/osudrl/masked-humanoid-controller).
- OpenHLM: Apache-2.0, HF 체크포인트, SONIC 의 다운로드 스크립트 참조 — [README](https://github.com/OpenHLM-project/OpenHLM).
- DemoHLM 저장소는 README 와 그림만 있다 — [로컬 code](/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/demohlm/code).
- HugWBC(이미 로컬): LICENSE 없음, Isaac Gym legged_gym — [dev12 보고서](/home/robotis-ai/Projects2/dev12/reports/dev12%20구현%20참고%20연구와%20오픈소스.md).

### Inferences
- 우리 스택(Isaac Lab + Newton + rsl_rl)에 가장 바로 옮길 수 있는 것은 AGILE 의 `AgileBasedLowerBodyAction` 꼴(동결 TorchScript 하체를 Isaac Lab 행동 항으로, 상위 행동 = 명령 + clip)이다. VIRAL 의 `homie_base.py` 는 같은 일을 자체 환경에서 하며, 명령 자르기·잘린 양 벌점·델타 누적·현재 명령 관측을 한 파일에 보여 준다. 둘을 합치면 dev10/pelvis_pick 상위 환경의 뼈대가 된다(추론).
- 두 저장소의 하위 가중치는 LFS 이므로 필요하면 `git lfs pull` 이 따로 필요하다. 이 노트에서는 받지 않았고, 코드는 데이터로만 읽었다(실행·설치 안 함).

### Gaps
- Newton 물리에서 동결 하체 + 상위 RL 을 돌린 공개 사례는 찾지 못했다(AGILE 은 Isaac Lab 3.0 beta 대상이지만 Newton 사용 여부는 README 에서 확인 못 함).
- VIRAL 저장소에 HOMIE 학습 코드는 없어서, 그 HOMIE 가 원본 OpenHomie 와 같은 체크포인트인지(파일 이름상 "decoupled_locomotion ... amass" 계열은 GR00T Decoupled WBC 쪽으로 보임) 확인 못 했다.
- mjlab 기반의 "동결 하위 + 상위 RL" 공개 코드는 찾지 못했다.
