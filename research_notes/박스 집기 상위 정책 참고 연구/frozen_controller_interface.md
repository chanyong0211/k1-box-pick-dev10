# 고정(frozen) 저수준 제어기 위에서 상위 정책을 잘 학습시키는 법: 인터페이스 설계와 학습 기법 (2018 – 2026-10)

작성: 2026-10-23. 범위: 인터페이스 선택(명시 명령 / 관절·키포인트 목표 / 잠재 기술 공간), 저수준이 따라갈 수 있는 명령 유지, 유계 행동 매개화, 저수준 미세조정 여부, 지연 처리, 탐색 잡음, 체크포인트 선택.
겹치는 주제(다른 조사자 담당): (a) HOMIE·AMO·FALCON·ULC·HOVER 같은 명령 인터페이스 계층 시스템, (b) 시각 teacher→student 증류(VIRAL 등), (c) 휴머노이드 상자 집기·들기·나르기. 여기서는 "인터페이스·학습 기법" 관점만 다룬다.
표기: [PR] = 동료 심사 학회/저널, [pre] = arXiv 사전 공개(2026-10-23 기준 심사 venue 미확인).
다운로드 위치 기준: `/home/robotis-ai/Projects2/dev10/pelvis_pick/reference/<short_id>/` (paper.pdf, code/). 내가 받은 총량 약 1.0 GB. Omnigrasp 코드는 GitHub API 크기 600 MB 였지만 실제 클론이 1.4 GB 여서 예산 때문에 지웠다(링크만). 받은 코드는 실행·빌드·설치하지 않았다.

### 카탈로그 표

| short_id | title | venue/year | arXiv | code | license(코드) | 관련도(1–5) | downloaded path (또는 "링크만") |
|---|---|---|---|---|---|---|---|
| resmimic | ResMimic: From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learning | [pre] 2025-10 | [2510.05070](https://arxiv.org/abs/2510.05070) | [amazon-far/ResMimic](https://github.com/amazon-far/ResMimic) | Apache-2.0 | 5 | reference/resmimic/ (paper.pdf, code/) |
| visualmimic | VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation | [pre] 2025-09 (v2 2025-11) | [2509.20322](https://arxiv.org/abs/2509.20322) | [visualmimic/VisualMimic](https://github.com/visualmimic/VisualMimic) (sim2sim·체크포인트만, 학습 코드 없음) | 명시 없음 | 5 | reference/visualmimic/ (paper.pdf, code/) |
| diplo | DiPLO: Self-distilled Diffusion Planning for Loco-manipulation | [pre] 2026-10 | [2610.24847](https://arxiv.org/abs/2610.24847) | 링크 없음 | – | 4 | 링크만 |
| omniinteract | OmniInteract: Towards Unified Whole-Body Interaction Control for Dual Humanoids | [pre] 2026-10 | [2610.26043](https://arxiv.org/abs/2610.26043) | 확인 못함 | – | 4 | 링크만 |
| catchcarry | Catch & Carry: Reusable Neural Controllers for Vision-Guided Whole-Body Tasks | [PR] SIGGRAPH 2020 (TOG) | [1911.06636](https://arxiv.org/abs/1911.06636) | 공개 코드 확인 못함 | – | 4 | reference/catchcarry/paper.pdf |
| pulse | PULSE: Universal Humanoid Motion Representations for Physics-Based Control | [PR] ICLR 2024 | [2310.04582](https://arxiv.org/abs/2310.04582) | [ZhengyiLuo/PULSE](https://github.com/ZhengyiLuo/PULSE) | 명시 없음(LICENSE 파일 없음) | 4 | reference/pulse/ (paper.pdf, code/) |
| omnigrasp | Omnigrasp: Grasping Diverse Objects with Simulated Humanoids | [PR] NeurIPS 2024 | [2407.11385](https://arxiv.org/abs/2407.11385) | [ZhengyiLuo/Omnigrasp](https://github.com/ZhengyiLuo/Omnigrasp) | 명시 없음 | 4 | reference/omnigrasp/paper.pdf (코드는 링크만) |
| ase | ASE: Large-Scale Reusable Adversarial Skill Embeddings | [PR] SIGGRAPH 2022 (TOG) | [2205.01906](https://arxiv.org/abs/2205.01906) | [nv-tlabs/ASE](https://github.com/nv-tlabs/ASE) | NVIDIA License(비상업) | 4 | reference/ase/ (paper.pdf, code/) |
| closd | CLoSD: Closing the Loop between Simulation and Diffusion | [PR] ICLR 2025 | [2410.03441](https://arxiv.org/abs/2410.03441) | [GuyTevet/CLoSD](https://github.com/GuyTevet/CLoSD) | MIT | 4 | reference/closd/ (paper.pdf, code/) |
| sonic | SONIC: Supersizing Motion Tracking for Natural Humanoid Whole-Body Control | [pre] 2025-11 | [2511.07820](https://arxiv.org/abs/2511.07820) | [NVlabs/GR00T-WholeBodyControl](https://github.com/NVlabs/GR00T-WholeBodyControl) (GEAR-SONIC) | Apache-2.0(README 배지) | 4 | 링크만(팀 내 이미 사용) |
| whatmatters | What Matters In On-Policy RL? A Large-Scale Empirical Study | [PR] ICLR 2021 | [2006.05990](https://arxiv.org/abs/2006.05990) | – | – | 4 | reference/whatmatters/paper.pdf |
| rslrl_beta | rsl_rl `BetaDistribution` (PR #202) | 코드 2026-05-07 | – | [leggedrobotics/rsl_rl](https://github.com/leggedrobotics/rsl_rl/blob/main/rsl_rl/modules/distribution.py) | GitHub 표시 NOASSERTION | 4 | 링크만 |
| hilmares | HiLMa-Res: A General Hierarchical Framework via Residual RL for Combining Quadrupedal Locomotion and Manipulation | [PR] IROS 2024 | [2407.06584](https://arxiv.org/abs/2407.06584) | 확인 못함 | – | 3 | reference/hilmares/paper.pdf |
| maskedmimic | MaskedMimic: Unified Physics-Based Character Control Through Masked Motion Inpainting | [PR] SIGGRAPH Asia 2024 (TOG) | [2409.14393](https://arxiv.org/abs/2409.14393) | [NVlabs/ProtoMotions](https://github.com/NVlabs/ProtoMotions) | Apache-2.0 | 3 | reference/maskedmimic/ (paper.pdf, code/) |
| puppeteer | Hierarchical World Models as Visual Whole-Body Humanoid Controllers (Puppeteer) | [PR] ICLR 2025 | [2405.18418](https://arxiv.org/abs/2405.18418) | [nicklashansen/puppeteer](https://github.com/nicklashansen/puppeteer) | MIT | 3 | reference/puppeteer/ (paper.pdf, code/) |
| tennis | Learning Physically Simulated Tennis Skills from Broadcast Videos (Vid2Player3D) | [PR] SIGGRAPH 2023 (TOG) | 없음 | [프로젝트](https://research.nvidia.com/labs/toronto-ai/vid2player3d) | – | 3 | 링크만 |
| humanoidarena | HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning | [pre] 2026-06 | [2606.17833](https://arxiv.org/abs/2606.17833) | [humanoidarena.github.io](https://humanoidarena.github.io) | 코드 라이선스 미기재 | 3 | 링크만 |
| swap | SWAP: Test-Time Steerable Humanoid Whole-Body Collision Avoidance | [pre] 2026-10 | [2610.25711](https://arxiv.org/abs/2610.25711) | 미기재 | – | 3 | 링크만 |
| refinedp | REFINE-DP (diffusion planner + RL controller 동시 갱신) | RA-L 2026 채택(PDF 머리말), abs 페이지엔 venue 없음 | [2603.13707](https://arxiv.org/abs/2603.13707) | [프로젝트](https://refine-dp.github.io/REFINE-DP/) | – | 3 | 링크만 |
| humanoidbench | HumanoidBench | [PR] RSS 2024 | [2403.10506](https://arxiv.org/abs/2403.10506) | – | – | 3 | 링크만 |
| bangbang | Is Bang-Bang Control All You Need? | [PR] NeurIPS 2021 | [2111.02552](https://arxiv.org/abs/2111.02552) | – | – | 3 | 링크만 |
| capg | Clipped Action Policy Gradient | [PR] ICML 2018 | [1802.07564](https://arxiv.org/abs/1802.07564) | – | – | 3 | 링크만 |
| caps | Regularizing Action Policies for Smooth Control with RL (CAPS) | [PR] ICRA 2021 | [2012.06644](https://arxiv.org/abs/2012.06644) | – | – | 3 | 링크만 |
| chou_beta | Improving Stochastic Policy Gradients ... using the Beta Distribution | [PR] ICML 2017 | – | [PMLR](http://proceedings.mlr.press/v70/chou17a.html) | – | 3 | 링크만 |
| calm | CALM: Conditional Adversarial Latent Models | [PR] SIGGRAPH 2023 | [2305.02195](https://arxiv.org/abs/2305.02195) | [NVlabs/CALM](https://github.com/NVlabs/CALM) | NOASSERTION | 2 | 링크만 |
| beyondmimic | BeyondMimic | [pre] 2025-08 | [2508.08241](https://arxiv.org/abs/2508.08241) | [HybridRobotics/whole_body_tracking](https://github.com/HybridRobotics/whole_body_tracking) (추적 부분) | MIT | 2 | 링크만 |
| pdp | PDP: Physics-Based Character Animation via Diffusion Policy | [PR] SIGGRAPH Asia 2024 | [2406.00960](https://arxiv.org/abs/2406.00960) | – | – | 2 | 링크만 |
| unihsi | UniHSI: Unified Human-Scene Interaction via Prompted Chain-of-Contacts | [PR] ICLR 2024 | [2309.07918](https://arxiv.org/abs/2309.07918) | – | – | 2 | 링크만 |
| lucid | LUCID: Latent-Skill Unified Control via Imagined Dynamics | [pre] 2026-08 | [2608.07746](https://arxiv.org/abs/2608.07746) | 없음 | – | 2 | 링크만 |
| hiwet | HiWET: Hierarchical World-Frame End-Effector Tracking | [pre] 2026-02 | [2602.06341](https://arxiv.org/abs/2602.06341) | 없음 | – | 2 | 링크만 |
| imagine2real | Imagine2Real | [pre] 2026 | [2605.22272](https://arxiv.org/abs/2605.22272) | – | – | 2 | 링크만 |
| asc | ASC: Adaptive Skill Coordination for Robotic Mobile Manipulation | [pre→?] 2023 | [2304.00410](https://arxiv.org/abs/2304.00410) | – | – | 2 | 링크만 |
| hippo | Sub-policy Adaptation for Hierarchical RL (HiPPO) | [PR] ICLR 2020 | [1906.05862](https://arxiv.org/abs/1906.05862) | – | – | 2 | 링크만 |
| vbc | Visual Whole-Body Control for Legged Loco-Manipulation | [PR] CoRL 2024 | [2403.16967](https://arxiv.org/abs/2403.16967) | – | – | 2 | 링크만 |
| ctrlz / reliability / rlmatters | Ctrl-Z; Measuring the Reliability of RL Algorithms; Deep RL that Matters | [pre] 2019 / [PR] ICLR 2020 / [PR] AAAI 2018 | [1910.03732](https://arxiv.org/abs/1910.03732), [1912.05663](https://arxiv.org/abs/1912.05663), [1709.06560](https://arxiv.org/abs/1709.06560) | – | – | 2 | 링크만 |

### 방법별 요약 (무엇 · 숫자 · 관련도 · 가져올 것)

- **ResMimic (5)** — 사람 동작만으로 학습한 GMT 추적기를 고정 기저로 두고, 물체·접촉 정보를 보는 잔차 정책이 `a = a_gmt + Δa_res`(29차원)를 더한다. 마지막 층을 작은 gain 의 Xavier 로 초기화해 처음 잔차가 0 근처에서 시작. 가상 물체 PD 힘(kp, kd 를 점점 줄임) 커리큘럼, 점군 물체 추적 보상, 몸–물체 접촉 보상(발 제외 몸통·엉덩이·팔). MuJoCo sim2sim 평균 성공률: 기저 GMT 10 %, 처음부터 학습 0 %, **GMT 미세조정 7.5 %, ResMimic 92.5 %**; 수렴 반복 수 평균 처음부터 4500, 미세조정 2400, ResMimic 1300. G1 실기 4.5 kg 상자. 공개 코드에서 기저 정책은 TorchScript 로 불러 `detach()` 하고 `final_actions = actions + base_actions` (고정 확인). [논문](https://arxiv.org/html/2510.05070v1), 코드 `reference/resmimic/code/rsl_rl/rsl_rl/runners/on_policy_dagger_runner.py`. → **가져올 것: 저수준을 건드리지 말고(또는 다리 잔차만 작게) 가상 상자 보조 힘 커리큘럼으로 초기 학습을 안정화.**
- **VisualMimic (5)** — 저수준 = 6개 키포인트(루트·머리·양손·양발) 명령을 따르는 추적기(teacher-student 증류), 상위 = 키포인트 명령을 내는 PPO teacher → 깊이 student(DAgger). 상위 행동을 **저수준 학습 때 기록한 정규화기 통계로 μ±1.64σ(약 90 %)에 자름**; 저수준 학습 때 명령에 **곱셈 잡음 λ∈U(0.5, 1.5)** 주입. 제거 실험(상태 기반, Forward): 자르기 없음 → Kick Ball 189±3 → 12±12, Kick Box 78±3 → 3±4, "학습 후반 return 붕괴"; 잡음 없음 → Push Box 151±29 → 2±1; **키포인트 대신 23-DoF 관절 인터페이스** → Push Box 152→10, Kick Box 78→40, Kick Ball 189→0. 실기 상자 들기·밀기·차기 전이(실기 성공률 수치 없음). [논문](https://arxiv.org/html/2509.20322v1) → **가져올 것: 상위 행동 범위를 저수준 학습 명령 분포의 분위수로 정하고, 저수준 재학습 시 명령 잡음을 넣을 것.**
- **DiPLO (4)** — 확산 플래너가 로봇+물체 동작 묶음을 내고, 고정된 범용 RL 추적기(50 Hz, 계획 관절 기준에 잔차 보정)가 따른다. 실측 상태에서 다시 계획. 집기-나르기-놓기에서 사전학습 플래너 생존 약 45 % → SD:DPO + DA:PPO 후 생존 99.5 %·성공 98.8 %. **추적기 미세조정 최대 89.3 % vs 플래너 미세조정 96.5 %.** G1 실기 10/10, 5/5. [논문](https://arxiv.org/html/2610.24847v1) → **가져올 것: 성능을 올릴 곳은 상위; 저수준 미세조정은 이득이 작다.**
- **OmniInteract (4)** — 고정 SONIC 출력에 `α_res·tanh(π_res)` 잔차를 더하고 잔차 정규화 보상. 성공률: SONIC 단독 63.32 %, 처음부터 RL 68.49 %, 잔차 MLP 80.68 %, 흐름 매칭 잔차 84.32 %. [논문](https://arxiv.org/html/2610.26043) → **가져올 것: 잔차는 tanh 로 크기를 묶고 보상으로 정규화.**
- **Catch & Carry (4)** — NPMP 류 저수준(미래 5 단계 상태 → 잠재 의도 z → 행동)을 감독 학습 후 고정, 상위 시각 정책이 z 를 출력해 공 받기·상자 나르기. **"저수준이 본 값과 맞추려고 상위 행동을 (−2, 2)로 제한"**(잠재는 0 근처로 정규화돼 있음). [논문](https://arxiv.org/abs/1911.06636) → **가져올 것: 상자 나르기에서 "고정 저수준 + 범위 제한 상위"의 원형.**
- **PULSE (4)** — PHC+ 를 온라인 증류해 인코더·디코더·학습된 prior 를 만들고, 하위 과제에서는 디코더·prior 고정. **상위 행동 = prior 평균에 대한 잔차** `a = D(π_task + μ_prior)`, 탐색 분산은 prior σ 가 너무 작아 **고정값 0.22** 사용. 제거 실험: prior 잔차 행동이 없으면 "잠재 공간을 샘플하기 너무 어렵다"(R5 vs R6), 연속 잠재 차이 벌점 L_regu 가 탐색에 유리. ASE·CALM(64-d 초구면) 및 처음부터 학습보다 하위 과제 성능 우수, 처음부터 학습은 비자연스러운 동작. [논문](https://arxiv.org/abs/2310.04582) → **가져올 것: 상위 행동을 "명목 동작에 대한 잔차"로 정의(우리 경우: 단계별 명목 골반 높이·피치·팔 자세 + 잔차).**
- **Omnigrasp (4)** — PULSE-X(손가락 포함) 디코더·prior 고정, 같은 prior-잔차 행동으로 잡기·궤적 따르기. PULSE-X 없이 PPO 로 약 100억 샘플(한 달) 학습한 PPO-10B 가 "크게 뒤처짐", 같은 보상·상태로 PULSE-X 행동 공간을 빼면 성공률 크게 하락·비자연스러운 동작. 모방기에 정답 동작을 그대로 넣는 PHC 방식은 평균 30 mm 추적 오차 때문에 잡기 실패. [논문](https://arxiv.org/abs/2407.11385) → **가져올 것: "참조 동작을 추적기에 넣는" 인터페이스는 정밀 접촉에 오차가 너무 크다 → 접촉 단계엔 보정 채널이 필요.**
- **ASE (4)** — 적대적 기술 임베딩. 상위 행동은 정규화 전 잠재 z̄ 이고 **초구면으로 정규화(z = z̄/‖z̄‖)**, 이유: "제한 없는 Z 는 원점에서 먼 잠재를 골라 비자연스러운 동작". 저수준 30 Hz, **상위 6 Hz**. 상위 보상 = 0.9 과제 + **0.1 고정 판별기 스타일 보상**(없으면 잠재가 매 스텝 바뀌며 "떨리는 비자연스러운 동작"). 처음부터 학습은 return 이 더 높지만 비자연스러운 행동으로 얻은 것. [논문](https://arxiv.org/abs/2205.01906) → **가져올 것: 상위 주기 낮추기(6 Hz)와 "저수준 분포 안에 있음"을 재는 고정 판별기형 보상.**
- **CLoSD (4)** — 실시간 확산 플래너(40 프레임, 3,500 fps)가 계획, PHC 추적기가 실행, 실현된 프레임을 플래너 접두로 되먹임. **추적기를 플래너를 고정한 채 PPO 로 미세조정하되 원래 PHC 추적 보상·리셋을 그대로 사용**(과제 보상 아님), 여러 과제 동시. 미세조정 없는 추적기는 상호작용 과제에서 "크게 저하", 개루프는 앉기·일어서기에서 실패. [논문](https://arxiv.org/abs/2410.03441) → **가져올 것: 저수준을 고칠 땐 과제 보상이 아니라 "원래 추적 보상 + 상위가 실제로 내는 명령 분포"로.**
- **SONIC (4)** — 범용 토큰(FSQ) 공간과 로봇·사람·혼합(머리·손 키포인트 + 하체 로봇 동작) 인코더. 운동학 플래너 10 Hz·정책 50 Hz. **VLA(GR00T N1.5)는 토큰이 아니라 텔레옵 형식의 명시 명령(상체 자세 3, 허리 높이, 루트 선·각속도)**을 내며 사과 집기 20회 중 95 %. 못 따라갈 명령(예: 6.0 → −6.0 m/s 반전)은 임계 감쇠 스프링으로 완화. 응용들은 "플래너·추적 정책 재학습 없이" 구성. [논문](https://arxiv.org/html/2511.07820v2) → **가져올 것: 상위 → 저수준 사이에 2차 스프링(속도·가속 한계) 필터를 "환경 쪽"에 고정해 두기.**
- **What Matters In On-Policy RL (4)** — 250k 에이전트 대규모 실험. 권고: 마지막 정책 층 가중치 100배 작게(Humanoid +66 %), softplus 로 std 변환 + 음의 offset, **초기 std 0.5** 가 대부분 최적, 행동 변환은 clip 보다 tanh 가 약간 우수(HalfCheetah +30 %), tanh 는 엔트로피 정규화에서 log-det 항이 극단 행동을 벌하고 엔트로피 상한을 준다. [논문](https://arxiv.org/abs/2006.05990) (`reference/whatmatters/paper.pdf` 3.2절·B.8) → **가져올 것: 상위 정책 초기화·std 기본값.**
- **rsl_rl BetaDistribution (4, 실무)** — 2026-05-07 PR #202 로 `BetaDistribution` 추가: MLP 가 α, β 원값을 내고 `Softplus + 1` 로 α, β > 1(단봉) 보장, [0,1] 샘플을 `action_range`(기본 (−1, 1))로 선형 변환. 2026-04-23 PR #201 로 Gaussian 에 std clamp(`std_range`, 기본 (1e-6, 1e6))와 상수 std 기능 추가. [distribution.py](https://github.com/leggedrobotics/rsl_rl/blob/main/rsl_rl/modules/distribution.py), [커밋 이력](https://github.com/leggedrobotics/rsl_rl/commits/main/rsl_rl/modules/distribution.py) → **가져올 것: 환경 자르기 없이 유계 분포로 바로 교체 가능(우리 rsl_rl 버전 확인 필요).**
- **HiLMa-Res (3)** — 사족 보행기의 발끝(작업 공간) 궤적 추적 저수준(CPG 명목 + Bézier 잔차) 위에 상위 계획기가 Bézier 제어점·CPG 명령(기저 속도·회전)을 출력. 저수준은 명령 범위(Table I)를 무작위로 10초마다 바꿔 학습. 실기 검증된 저수준 재사용이 "동역학적으로 불가능한 행동 학습을 막고" 종단 학습 대비 "표본 효율이 크게 높다". [논문](https://arxiv.org/abs/2407.06584) → **가져올 것: 상위는 저수준 학습 때와 같은 매개(같은 범위)로만 명령.**
- **MaskedMimic (3)** — 부분 목표(관절·물체·텍스트)로 전신 동작을 inpainting 하는 단일 제어기; 새 과제는 학습 없이 FSM "goal-engineering". PULSE 보다 테스트 일반화 우수. ProtoMotions 에 ASE·CALM·PULSE·MaskedMimic 구현이 함께 있다. [논문](https://arxiv.org/abs/2409.14393) → 우리 저수준 재설계 때 "가려진 목표" 학습 개념만 참고.
- **Puppeteer (3)** — 저수준 추적 월드모델(TD-MPC2)이 손·발·머리 끝점 위치 명령을 추적, 상위 시각 puppeteer 가 같은 주기(k=1)로 명령. 저수준 고정(가중치 갱신 없음). 사람 선호 51명 중 97.8 % 가 계층 쪽 선택. [논문](https://arxiv.org/abs/2405.18418) → 끝점 명령 인터페이스의 자연스러움 근거.
- **Tennis / Vid2Player3D (3)** — 상위가 동작 임베딩 잠재를 고르고, 임베딩이 틀린 부분(손목)은 **상위가 직접 관절 보정값으로 덮어쓰는 혼합 제어**. [프로젝트](https://research.nvidia.com/labs/toronto-ai/vid2player3d) → **우리 구조(골반 명령 + 상체 관절 직접 목표)와 같은 "혼합 인터페이스"의 선례.**
- **HumanoidArena (3)** — 상위가 40-D 표준 행동(루트 xy 차이 2, 루트 z 1, rot6d 6, 관절 29, 손 개폐 2)을 내고 추적기별 어댑터가 변환. SONIC 쪽 최고 평균 성공률이 TWIST2 보다 HOI 16.11 %p 높음; 추적기를 바꾸면 평균 36.0–39.9 % 하락 → "성능은 정책–추적기 쌍의 성질". [논문](https://arxiv.org/html/2606.17833v1) → 상위는 특정 저수준의 지연·보정 습관에 특화된다.
- **SWAP (3)** — 고정 저수준에 무작위 명령을 넣어 실제로 실행된 궤적을 기준으로 데이터를 만듦(쓸고 간 부피 밖에만 장애물 배치). 넘어짐·큰 추적 오차 롤아웃 약 3 % 제거. 성공률 88.3 %(조향 없이 72.4 %, 종단 확산 17.4 %). [논문](https://arxiv.org/html/2610.25711v1) → "실행된 것"으로 레이블.
- **REFINE-DP (3)** — 확산 계획기를 PPO 기반 정책경사로 미세조정하면서 RL 제어기도 동시에 갱신해 변하는 명령 분포를 따르게 함. 시뮬 90 % 이상. 고정 제어기 대비 수치는 초록에 없음. [초록](https://arxiv.org/abs/2603.13707)
- **HumanoidBench (3)** — 한손·양손 도달 정책(MJX PPO 20억·40억 스텝)을 고정하고 상위(DreamerV3, TD-MPC2)가 3D 목표점을 출력; **목표 범위를 로봇 작업 공간으로 제한**. push 는 평면 학습을 크게 앞섬, package 는 들기를 저수준이 배운 적 없어 이득 작음. [논문](https://arxiv.org/html/2403.10506v2) → 저수준이 못 배운 동작(들기)은 상위로 못 만든다.
- **2(참고)** — CALM: 잠재 + 스타일 보상(PULSE 비교에서 스타일 보상 없이는 탐색이 막힘) [2305.02195](https://arxiv.org/abs/2305.02195); BeyondMimic: 잠재 확산 + 분류기 유도로 시험 시 새 목적(조이스틱·장애물) [2508.08241](https://arxiv.org/abs/2508.08241); PDP: 확산 정책 문자 제어 [2406.00960](https://arxiv.org/abs/2406.00960); UniHSI: 접촉 사슬 명령 [2309.07918](https://arxiv.org/abs/2309.07918); LUCID: 적대적 모방 잠재 저수준 고정 + 상위와 거시 월드모델 공동 학습 [2608.07746](https://arxiv.org/abs/2608.07746); HiWET: 세계 좌표 끝점 부목표 + 운동학 매니폴드 잔차 prior [2602.06341](https://arxiv.org/abs/2602.06341); Imagine2Real: 키포인트 추적기 출력에 관절 잔차 [2605.22272](https://arxiv.org/abs/2605.22272); ASC: 사전학습 기술 + 보정(corrective) 정책 [2304.00410](https://arxiv.org/abs/2304.00410); HiPPO: 하위 정책 공동 적응 [1906.05862](https://arxiv.org/abs/1906.05862); VBC: 속도·끝점 명령 계층 [2403.16967](https://arxiv.org/abs/2403.16967).

## Q1. 명시적 명령 인터페이스 vs 잠재 기술 공간: 조작 과제에서 표본 효율·sim2real·동작 품질 근거

### Takeaway
같은 조건에서 "명시 명령 vs 잠재"를 직접 비교한 조작 연구는 찾지 못했다. 근거는 (i) 잠재·prior 행동 공간이 **관절 공간 처음부터 학습**보다 자연스럽고 성공률이 높다(캐릭터 애니메이션, 전부 시뮬), (ii) 실기 휴머노이드 조작(2025–2026)은 거의 전부 **명시적·저차원·작업 공간 명령(키포인트, 끝점, 골반/루트 명령)**을 쓰고, 관절(DoF) 인터페이스는 키포인트보다 나빴다(VisualMimic). 실기 전이 근거는 명시 명령 쪽에만 있다.

### Cited Findings
- 잠재(PULSE) 행동 공간 위 상위 정책은 ASE·CALM 잠재와 처음부터 학습을 하위 과제(속도·도달·타격·지형)에서 앞서고, 처음부터 학습은 정규화 return 은 가깝지만 비자연스러운 동작 — [PULSE](https://arxiv.org/abs/2310.04582)
- Omnigrasp: 같은 보상·상태에서 PULSE-X 행동 공간을 빼면 성공률 크게 하락·비자연스러운 동작; PULSE-X 없이 약 100억 샘플 PPO 도 크게 뒤처짐 — [Omnigrasp](https://arxiv.org/abs/2407.11385)
- ASE: 처음부터 학습한 정책이 대부분 과제에서 return 은 더 높지만 비자연스러운 행동을 이용; 잠재 위 상위는 더 자연스럽고 표본도 적게 든다 — [ASE](https://arxiv.org/abs/2205.01906)
- VisualMimic(실기 상자 들기·밀기): 상위 인터페이스를 6-키포인트 대신 23-DoF 관절로 바꾸면 Push Box 152±36 → 10±9, Kick Box 78±3 → 40±34, Kick Ball 189±3 → 0±0(상태 기반) — [VisualMimic](https://arxiv.org/html/2509.20322v1)
- SONIC 의 VLA 연동은 범용 토큰이 아니라 텔레옵 형식 명시 명령(상체 자세 3개, 허리 높이, 루트 선·각속도)으로 했고 사과 집기 95 %(20회) — [SONIC](https://arxiv.org/html/2511.07820v2)
- HumanoidArena 는 SMPL 같은 고차원 행동 대신 40-D 표준 행동을 택함: 고차원 행동 공간이 "학습 복잡도를 크게 올림" — [HumanoidArena](https://arxiv.org/html/2606.17833v1)
- Puppeteer: 끝점 위치 명령 계층이 평면 TD-MPC2 대비 사람 선호 97.8 % — [Puppeteer](https://arxiv.org/abs/2405.18418)
- HiLMa-Res: 작업 공간(발끝 궤적 + 기저 속도) 명령 계층이 종단 학습보다 표본 효율이 "크게 높고", 실기 검증된 저수준 재사용이 sim2real 부담을 덜어 준다 — [HiLMa-Res](https://arxiv.org/abs/2407.06584)
- HumanoidBench: 고정 도달 정책 위 상위(3D 목표점)는 push 에서 평면 학습을 크게 앞서지만, 저수준이 배운 적 없는 들기가 필요한 package 에선 이득 작음 — [HumanoidBench](https://arxiv.org/html/2403.10506v2)
- 정밀 접촉: 정답 운동학 동작을 모방기에 넣어도 평균 30 mm 오차로 잡기 실패(PHC 기준선) — [Omnigrasp](https://arxiv.org/abs/2407.11385); 잔차 없이 GMT 만 쓰면 상자 나르기 0 %(ResMimic 표 I) — [ResMimic](https://arxiv.org/html/2510.05070v1)
- 혼합 인터페이스 선례: 잠재(동작 임베딩)로 전신을 고르고 틀린 관절(손목)은 상위가 직접 관절 보정으로 덮어씀 — [Vid2Player3D](https://research.nvidia.com/labs/toronto-ai/vid2player3d)
- 속도 명령 인터페이스가 저수준의 능력을 제한한다는 문제 제기로 위치 목표 종단 학습을 제안(사족) — [Rudin et al. IROS 2022](https://arxiv.org/abs/2209.12827)

### Inferences
- 우리 구조(골반 명시 명령 + 상체 11 관절 직접 목표)는 문헌상 "명시 명령 + 관절 보정" 혼합형(테니스의 손목 덮어쓰기, SONIC 혼합 인코더, [HEX](https://arxiv.org/abs/2604.07993) 의 VLA 팔·손 행동 + 하체 명령)과 같은 계열이다. 잠재 공간으로 바꿀 근거는 약하다: 잠재의 이점은 "관절 공간 처음부터"와 비교한 것이고, 우리 상위는 이미 저차원 명시 명령으로 하체를 다룬다.
- 약점은 상체 11 관절 직접 목표 쪽이다(VisualMimic 의 DoF 인터페이스가 키포인트보다 나빴던 것과 같은 축). 팔을 "손 목표점(작업 공간) + 저수준 IK/추적"으로 바꾸는 것은 저수준 재학습이 필요하므로, 당장은 "단계별 명목 팔 자세 + 작은 잔차"(PULSE prior-잔차, HiLMa-Res 명목 + 잔차)로 탐색 공간을 줄이는 쪽이 비용이 작다.
- 이전 버전(SONIC 에 관절 기준 전달)의 "명령은 ±17°, 실제 ±11°" 문제는 문헌에서 "참조 추적 인터페이스는 정밀 접촉에 오차가 크다"(Omnigrasp 30 mm, ResMimic GMT 단독 0 %)와 같은 현상이다.

### Gaps
- 같은 과제·같은 저수준에서 명시 명령 vs 잠재 공간을 표본 효율·sim2real 로 직접 비교한 연구는 찾지 못함.
- 잠재 인터페이스 쪽 실기 휴머노이드 조작 근거는 확인하지 못함(Omnigrasp·PULSE 는 시뮬 전용; Omnigrasp 는 "실기 준비됐다고 주장하지 않음").
- Omnigrasp 표 4 의 정확한 수치는 PDF 표 추출이 깨져 확인 못함.

## Q2. PPO 유계 행동 매개화(tanh 가우시안, Beta, clip + 벌점)와 bang-bang

### Takeaway
"환경에서 자르기만 하고 벌점 없음"이 가장 나쁜 조합이다: 경계 밖 행동이 모두 같은 효과라 평균이 밖으로 표류하고 std 를 붙잡는 힘이 없다. 해법은 (1) 분포 자체를 유계로(tanh-가우시안 + log-det 엔트로피, 또는 Beta α,β>1), (2) 가우시안을 유지하면 std 상한 + 원 행동의 범위 밖 L2 벌점, (3) 초기 std 작게(0.5)와 마지막 층 축소. bang-bang 은 행동 비용이 없으면 가우시안 PPO 에서도 자연히 생기는 현상이라 매개화만으로는 안 없어지고 행동 비용·평활화 정규화가 필요하다.

### Cited Findings
- 대규모 실험: tanh 변환이 clip 보다 약간 우수(HalfCheetah +30 %), 차이는 초기 행동 크기 감소 때문일 수 있음; 초기 std 0.5 가 대부분 최적; 마지막 정책 층 100배 작게(Humanoid +66 %); softplus + 음의 offset 권고; tanh 의 엔트로피에 log tanh′(x) 항을 넣으면 "극단 행동을 벌해 tanh 포화와 기울기 소실을 막고 엔트로피가 무한히 커지지 않게 함"; PPO 비율·KL 에서는 이 항이 상쇄 — [What Matters (ICLR 2021)](https://arxiv.org/abs/2006.05990)
- Brax PPO 기본 행동 분포는 `tanh_normal`(softplus + min_std 0.001), 엔트로피에 log-det-Jacobian 포함 — [brax ppo/networks.py](https://github.com/google/brax/blob/main/brax/training/agents/ppo/networks.py), [brax distribution.py](https://github.com/google/brax/blob/main/brax/training/distribution.py)
- rsl_rl 은 2026-05 부터 `BetaDistribution`(Softplus+1 로 α,β>1 단봉, [0,1] → action_range 선형) 제공, 2026-04 부터 Gaussian std clamp(`std_range`)·상수 std 제공 — [rsl_rl distribution.py](https://github.com/leggedrobotics/rsl_rl/blob/main/rsl_rl/modules/distribution.py)
- Isaac Lab 의 `clip_actions` 는 정책 밖 `RslRlVecEnvWrapper` 안에서 적용(기본 None) — [Isaac Lab rsl_rl cfg 문서](https://isaac-sim.github.io/IsaacLab/v2.3.2/_modules/isaaclab_rl/rsl_rl/rl_cfg.html)
- 유계 행동에 가우시안을 쓰고 자르면 경계에서 정책경사가 편향, Beta 는 유한 지지로 이를 없앰 — [Chou et al. ICML 2017](http://proceedings.mlr.press/v70/chou17a.html); 잘린 행동의 log-prob 를 꼬리 누적확률로 바꾼 CAPG 가 불편·저분산 추정량 — [CAPG (ICML 2018)](https://arxiv.org/abs/1802.07564)
- Beta PPO 가 Gym 과제에서 가우시안보다 최종 보상·안정성·수렴 우수(사전 공개) — [2111.02202](https://arxiv.org/abs/2111.02202); 로봇에서 Beta 사용 예: 바퀴-다리 로봇 상위 정책 행동 공간을 Beta 로 제한 — [Science Robotics 2024](https://arxiv.org/abs/2405.01792); 보행-스케이트보드 하이브리드 자동자 학습이 Beta 정책 사용 — [2503.01842](https://arxiv.org/abs/2503.01842). 실기 전이 효과를 분리한 비교는 찾지 못함.
- 학습된 연속 제어 정책은 행동 공간 경계를 선호(bang-bang); Bernoulli(양 끝만) 정책이 여러 벤치마크에서 최고 수준; 로봇에선 에너지·유지 비용 때문에 다름 — [Seyde et al. NeurIPS 2021](https://arxiv.org/abs/2111.02552)
- 시간·공간 평활성 정규화(CAPS) — [ICRA 2021](https://arxiv.org/abs/2012.06644); 휴머노이드 보행에서 평활 보상·저역 필터 대신 Lipschitz(기울기 벌점) 제약 — [LCP](https://arxiv.org/abs/2410.11825)
- 탐색 분산: PULSE 는 prior σ 가 너무 작아 상위 탐색 분산을 고정값 0.22 로 둠 — [PULSE](https://arxiv.org/abs/2310.04582); ASE 상위 분포는 정규화 전 잠재의 원점 중심에서 시작해 초구면 위를 고르게 탐색 — [ASE](https://arxiv.org/abs/2205.01906)
- OmniInteract 잔차는 `α_res·tanh(·)` 로 크기 제한 + 잔차 정규화 보상 — [OmniInteract](https://arxiv.org/html/2610.26043)
- 내부 교훈: 환경 안에서 잘리거나 버려지는 행동에는 원 행동 L2 벌점이 없으면 PPO std 가 발산 — 내부 메모리 `rl-env-action-clip-std-explosion.md`(dev10/dev9 경험, 외부 출처 아님)

### Inferences
- std 폭발 메커니즘(추론): 환경에서 자른 뒤에는 경계 밖 행동이 보상에 아무 차이를 안 만들어 평균이 밖으로 흘러도 비용이 없고, 엔트로피 보너스는 std 를 키우는 방향으로만 작용한다. 큰 std 는 잘린 뒤엔 "양 끝 값"이 되므로 bang-bang 이 같이 나타난다. 이전 버전의 (2)(3) 문제는 같은 원인일 가능성이 높다.
- 권고 순서(추론): ① 상위 행동 전체를 rsl_rl `BetaDistribution`(action_range = 저수준 학습 명령 범위)로 바꾸거나, ② 가우시안 유지 시 tanh 를 정책 쪽 분포 변환으로 넣고(PPO 비율은 그대로, 엔트로피는 log-det 포함) std_range 상한(예: 정규화 행동 단위 1.0 이하) + 원 행동의 범위 밖 L2 벌점. 환경 쪽 clip 은 안전용으로만 남긴다.
- Beta(α,β>1)는 경계에서 밀도가 0 이라 정확히 경계 값을 고를 수 없어 bang-bang 을 약하게 억제하지만, 평균을 경계 근처로 몰 수는 있다. bang-bang 자체는 Seyde 결과대로 "행동 비용이 없어서" 생기므로, 원 행동 변화율 벌점(CAPS 시간 항)이나 Lipschitz 벌점을 상위에 넣어야 한다.
- LPF 0.2 와 bang-bang(추론): 상위의 원 출력이 저역 필터를 통과하면, 필터된 목표를 빨리 움직이려고 원 출력을 끝까지 미는 것이 최적이 된다. 필터를 "환경의 고정 동역학"으로 두려면 상위 행동을 "목표 변화율(델타)"로 정의하고 변화율 한계를 저수준 학습 때의 목표 변화율 분위수로 맞추는 편이 낫다(SONIC 의 스프링 필터와 같은 발상). 그러면 포화 = 최대 변화율이라 무해하고 벌점으로 다루기 쉽다.

### Gaps
- 상위(계층) 정책에서 tanh vs Beta vs clip+벌점을 같은 과제로 비교한 연구는 찾지 못함.
- rsl_rl/Isaac Lab 이슈 트래커에서 "clip_actions 로 std 발산" 논의 원문은 검색으로 찾지 못함(인증 없는 GitHub 코드 검색 불가).
- Seyde 논문의 수치 결과는 초록만 확인.

## Q3. 상위가 저수준의 분포 밖(OOD) 동작을 악용하지 못하게 하는 방법 (저수준 지연·추종 지연 처리 포함)

### Takeaway
문헌의 표준 도구는 다섯 가지다: (1) 상위 행동을 저수준 학습 분포로 묶기(범위 자르기·초구면 정규화·prior 잔차), (2) 저수준 학습 때 명령에 잡음·교란을 넣어 분포를 넓히기, (3) 상위 보상에 "저수준 분포 안"을 재는 항(고정 판별기 스타일 보상, 잔차 정규화), (4) 실제 실행 상태를 상위에 되먹이고 실측에서 다시 계획, (5) 명령과 저수준 사이에 속도·가속 한계 필터. 지연은 별도 기법보다 "고정 저수준을 루프 안에 넣고 같은 주기·같은 필터로 학습"해 상위가 흡수하게 하는 것이 일반적이다.

### Cited Findings
- 범위 자르기: 상위 키포인트 행동을 저수준 정규화기 통계의 μ±1.64σ 로 자름, 없으면 학습 후반 return 붕괴(Kick Ball 189 → 12) — [VisualMimic](https://arxiv.org/html/2509.20322v1)
- 범위 자르기: "저수준 감독 학습 때 본 값과 맞추고 OOD 를 막으려" 상위 행동을 (−2, 2)로 제한 — [Catch & Carry](https://arxiv.org/abs/1911.06636)
- 작업 공간 제한: 상위 도달 목표를 로봇 작업 공간으로 제한 — [HumanoidBench](https://arxiv.org/html/2403.10506v2)
- 초구면 정규화: 제한 없는 잠재는 원점에서 먼 값을 골라 비자연스러운 동작 → z = z̄/‖z̄‖ — [ASE](https://arxiv.org/abs/2205.01906)
- prior 잔차: 상위 행동을 학습된 prior 평균에 대한 잔차로; 없으면 "샘플하기 너무 어려움" — [PULSE](https://arxiv.org/abs/2310.04582)
- 저수준 학습 시 명령 잡음: 키포인트 명령에 λ∈U(0.5, 1.5) 곱셈 잡음, 없으면 Push Box 151 → 2 — [VisualMimic](https://arxiv.org/html/2509.20322v1); SONIC 은 목표 동작 명령에 교란을 주어 학습 — [SONIC](https://arxiv.org/html/2511.07820v2); HiLMa-Res 는 저수준 명령 매개를 표 I 범위에서 10초마다 무작위로 바꿔 학습 — [HiLMa-Res](https://arxiv.org/abs/2407.06584)
- 분포 안 보상: 고정 판별기 스타일 보상(w_G 0.9, w_S 0.1); 없으면 매 스텝 기술 전환으로 떨림 — [ASE](https://arxiv.org/abs/2205.01906); 잔차 정규화 보상 — [OmniInteract](https://arxiv.org/html/2610.26043). 고정 판별기에 대고 학습하면 판별기의 특이점을 악용할 수 있다는 지적도 ASE 본문에 있음 — [ASE](https://arxiv.org/abs/2205.01906)
- 실행 결과로 되먹임: 실현된 프레임을 플래너 접두로 넣는 폐루프; 개루프는 앉기·일어서기 실패 — [CLoSD](https://arxiv.org/abs/2410.03441); 실측 상태에서 다시 계획해 추적 오차가 다음 계획에 반영 — [DiPLO](https://arxiv.org/html/2610.24847v1)
- 실행된 것으로 레이블: 고정 저수준에 무작위 명령을 넣어 실제 궤적 기준으로 데이터 생성, 넘어짐·큰 추적 오차 약 3 % 제거 — [SWAP](https://arxiv.org/html/2610.25711v1)
- 명령 평활: 한 구간 안에 못 따라갈 명령(6.0 → −6.0 m/s)은 임계 감쇠 스프링으로 완화(감쇠 계수엔 둔감, 종종 생략 가능) — [SONIC](https://arxiv.org/html/2511.07820v2)
- 주기: 저수준 30 Hz·상위 6 Hz — [ASE](https://arxiv.org/abs/2205.01906); 같은 주기 k=1 — [Puppeteer](https://arxiv.org/abs/2405.18418); 플래너 10 Hz·정책 50 Hz — [SONIC](https://arxiv.org/html/2511.07820v2); 상위 20 Hz·5스텝 묶음, 저수준 50 Hz — [SWAP](https://arxiv.org/html/2610.25711v1)
- 잔차 관측에 행동 이력 t−10…t 와 참조 창 t−10…t+10 포함 — [ResMimic](https://arxiv.org/html/2510.05070v1)
- 상위는 학습 때 쓴 추적기의 동역학·보정 습관에 특화: 추적기를 바꾸면 평균 36.0–39.9 % 하락 — [HumanoidArena](https://arxiv.org/html/2606.17833v1)
- 상위가 실행 불가능한 명령을 보내면 부분 자율성 없이 로봇이 불안정해지고 학습 실패 — [Nature MI 2023 계층 생성 모델](https://www.nature.com/articles/s42256-023-00752-z)

### Inferences
- 우리 (1)번 문제(허리 명령 ±17° vs 실제 ±11°)에 대한 처방(추론): 상위 행동 범위를 "저수준 명령 샘플러 범위"가 아니라 "고정 저수준이 실제로 도달한 범위"로 정한다. SWAP 식으로 고정 저수준에 명령 격자(높이 × 피치 × 상체 자세)를 넣어 정상 상태 도달값·오차를 재고, 그 결과로 높이별 피치 한계 같은 결합 범위를 만들 수 있다. 측정은 별도 단계 없이 상위 환경 스모크 안에서 하면 된다.
- 차이(참조 − 실제)는 벌점만이 아니라 관측으로도 넣는다(CLoSD·DiPLO 의 실측 되먹임과 같은 역할). 상위 관측에 저수준의 실현 골반 상태(높이·피치·속도), 필터된 상체 목표, 직전 상위 행동 이력(ResMimic 은 10 스텝)을 넣으면 지연을 정책이 흡수할 수 있다.
- 저수준이 "필터된 현재 목표 + 변화율"을 관측하므로 상위가 빠른 상체 목표를 내면 저수준 입력의 변화율 채널이 학습 분포 밖으로 간다. 상위 행동을 변화율로 정의하고 그 한계를 저수준 학습 때의 변화율 분위수(예: μ±1.64σ, VisualMimic 방식)로 두면 둘 다 막힌다.
- 판별기형 "분포 안" 보상(ASE)은 우리 저수준에 판별기가 없으므로 대신 저수준 critic 값이나 추적 오차를 보상 항으로 쓰는 변형이 가능하다(문헌 직접 근거 없음, 추론).
- 상위 주기: 상자 접근·쪼그림은 6–10 Hz 상위로도 충분할 가능성이 있다(ASE·SONIC). 주기를 낮추면 bang-bang 떨림과 저수준 OOD 변화율이 함께 줄어든다(추론).

### Gaps
- "저수준 능력에서 명령 경계를 학습"하는 전용 방법(능력 지도·가능성 예측기)을 정량 비교한 논문은 찾지 못함. Skill-Nav 등이 능력 모델에 기대지만 원문 확인 못함.
- 지연을 상위 관측에 명시적으로 모델링(예: 추정 추종 지연 입력)한 비교 실험은 찾지 못함.

## Q4. 저수준과 상위를 함께 미세조정한 사례와 결과 (잔차 저수준 적응 포함)

### Takeaway
현재 근거는 일관되게 "저수준은 고정하고, 필요하면 작은 잔차를 더한다"를 지지한다. 저수준 자체를 과제 보상으로 미세조정한 경우는 잔차보다 나빴고(ResMimic 7.5 % vs 92.5 %, DiPLO 89.3 % vs 96.5 %), 저수준을 고친 성공 사례(CLoSD)는 과제 보상이 아니라 원래 추적 보상을 상위가 내는 명령 분포 위에서 다시 최적화한 경우다. 동시 갱신(REFINE-DP)은 90 % 이상을 보고했지만 고정 대비 수치는 없다.

### Cited Findings
- ResMimic(MuJoCo sim2sim, 4 과제 평균): 기저 GMT 10 %, 처음부터 0 %, **GMT 미세조정 7.5 %**, 고정 기저 + 잔차 **92.5 %**; 수렴 반복 수 처음부터 4500, 미세조정 2400, 잔차 1300; 물체 추적 오차 0.76 / 0.46 / 0.12 — [ResMimic](https://arxiv.org/html/2510.05070v1)
- DiPLO: 추적기 미세조정 최대 89.3 % vs 플래너(DA:PPO) 미세조정 96.5 %, 미세조정 중 추적기 고정 — [DiPLO](https://arxiv.org/html/2610.24847v1)
- CLoSD: 플래너 고정 후 추적기를 PPO 로 미세조정, 원래 PHC 추적 보상·리셋 그대로, 여러 과제 동시; 미세조정 없는 추적기는 상호작용 과제에서 크게 저하 — [CLoSD](https://arxiv.org/abs/2410.03441)
- OmniInteract: 고정 SONIC + tanh 잔차 84.32 % vs SONIC 단독 63.32 % vs 처음부터 68.49 %(SONIC 미세조정 직접 비교는 없음) — [OmniInteract](https://arxiv.org/html/2610.26043)
- REFINE-DP: 확산 계획기를 PPO 정책경사로 미세조정하면서 제어기도 동시에 갱신, 시뮬 90 % 이상(고정 제어기 비교 수치 없음) — [REFINE-DP](https://arxiv.org/abs/2603.13707)
- Imagine2Real: 키포인트 추적기 출력에 관절 잔차를 더하는 상호작용 어댑터 — [Imagine2Real](https://arxiv.org/abs/2605.22272)
- ASC(Spot 실기): 사전학습 기술 + OOD 상태에서 기술을 고치는 보정 정책, 60회 중 59(98 %) vs 순차 실행 44(73 %) — [ASC](https://arxiv.org/abs/2304.00410)
- HiPPO: 상위와 하위 정책을 함께 적응시키는 계층 정책경사 — [HiPPO (ICLR 2020)](https://arxiv.org/abs/1906.05862)
- PULSE: RL 목표와 온라인 감독 증류를 섞으면(저수준 표현 학습 중) 성능이 나빠짐(표 3 R4 vs R6) — [PULSE](https://arxiv.org/abs/2310.04582)
- 저수준 고정 + 잔차는 초기에 0 근처 출력(작은 gain Xavier) — [ResMimic](https://arxiv.org/html/2510.05070v1)

### Inferences
- 우리 경우(추론): 1순위는 저수준 고정. 상자 무게·반력 때문에 다리가 못 버티는 증상이 분명해지면 2순위로 "다리 12 관절에 α·tanh 잔차"를 상위와 같은 PPO 로 학습(초기 0, 잔차 L2 벌점, α 는 작게). 3순위로 저수준 자체를 고친다면 과제 보상이 아니라 원래 골반 명령 추적 보상을 그대로 쓰고, 명령 샘플러에 상위가 실제로 내는 명령 분포(+상자 무게 외력)를 섞어 CLoSD 식으로 다시 학습한다.
- 저수준을 PPO 로 다시 만질 때는 critic 을 새로 만들지 말 것: 내부 메모리 "RL resume: expand widened critic input — random critic destroys the actor in one update"와 같은 위험이 있다(내부 경험, 외부 출처 아님).

### Gaps
- 휴머노이드 조작에서 "저수준 미세조정 시 망가짐(망각)"을 KL·행동 복제 정규화로 막은 정량 비교는 찾지 못함.
- REFINE-DP 의 제어기 동시 갱신 정규화 방식과 고정 대비 수치는 초록에 없어 확인 못함.

## Q5. 탐색 잡음·엔트로피(유계 명령 공간)와 비단조 성공률에서의 체크포인트 선택

### Takeaway
탐색은 "작게 시작"이 공통이다(초기 std 0.5, 마지막 층 축소, 잔차 0 초기화, 고정 탐색 분산). 체크포인트 선택에 대해 계층 RL 전용 연구는 없고, 일반 RL 신뢰도 문헌은 "학습 중 성능 붕괴는 흔하며, 여러 시드·고정 평가셋·분산 지표로 골라야 한다"는 쪽이다.

### Cited Findings
- 초기 std 0.5 최적, 마지막 층 100배 축소; 엔트로피·KL 정규화는 HalfCheetah 외엔 도움이 없었고, 저자들은 "신중한 초기화가 탐색을 보장해 엔트로피 보너스를 불필요하게 만든다"고 추정 — [What Matters](https://arxiv.org/abs/2006.05990)
- 고정 탐색 분산 0.22(prior σ 대신) — [PULSE](https://arxiv.org/abs/2310.04582); 잔차 0 초기화 — [ResMimic](https://arxiv.org/html/2510.05070v1)
- 학습이 성능 붕괴를 보이면 통계 검정(Mann-Whitney U)으로 개선이 멈췄는지 보고 이전 최상 체크포인트로 되돌림 — [Ctrl-Z](https://arxiv.org/abs/1910.03732)
- 학습 중 시간에 따른 분산(dispersion across time)·하방 위험(CVaR) 같은 신뢰도 지표 제안 — [Chan et al. ICLR 2020](https://arxiv.org/abs/1912.05663)
- 시드·구현 차이만으로도 결과가 크게 달라짐 → 여러 시드·통계 보고 필요 — [Henderson et al. AAAI 2018](https://arxiv.org/abs/1709.06560)
- 자르기 없으면 return 이 학습 후반에 붕괴 — [VisualMimic](https://arxiv.org/html/2509.20322v1)
- 내부 교훈: 고른 체크포인트의 개선은 선택 효과일 수 있으니 이웃 저장본과 같은 지표로 먼저 비교 — 내부 메모리 `selected-checkpoint-improvement-is-selection.md`(외부 출처 아님)

### Inferences
- 우리 (4)번(성공률 비단조)은 (2)(3)과 묶여 있을 가능성이 크다: std 가 커지는 구간에서 결정적(평균) 평가와 확률적 평가가 갈리고, 잘린 행동이 경계로 몰리며 성공률이 출렁인다. 유계 분포 + std 상한으로 바꾼 뒤 다시 보는 것이 먼저다(추론).
- 선택 절차(추론): 저장 간격마다 고정 시드 평가셋(상자 위치·높이·무게 격자, 수천 에피소드)으로 결정적 평가, 성공률과 함께 하위 10 % 에피소드 지표(CVaR 류)를 기록, 최고점 하나가 아니라 이웃 3–5개 평균이 높은 구간에서 고르고, 같은 지표로 sim2sim(MuJoCo)에서 재확인.

### Gaps
- PPO 정책 가중치 EMA·평균으로 체크포인트 출렁임을 줄인 로봇 RL 연구는 이번 검색에서 확인 못함.
- 계층(고정 저수준) 설정에서 비단조 성공률 원인을 분석한 논문은 찾지 못함.
