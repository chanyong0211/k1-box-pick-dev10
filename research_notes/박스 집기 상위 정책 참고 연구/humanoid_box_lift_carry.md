# 휴머노이드 박스·큰 물체 집기·들기·운반 방법 카탈로그 (2022–2026.10, 손가락 없는 양손·전신 접촉 중심)

> 조사일 2026-10-23. 우리 조건(ROBOTIS K1, 손가락 없는 고무 공 손, 37×40×29 cm·0.5–2 kg 상자를 옆면 두 손바닥으로 조여 바닥·0–0.3 m 받침에서 들기, 하체 RL 정책(vx·vy·wz·골반 높이 0.335–0.77 m·pitch ±45°·roll) 위의 상위 RL 정책)에 비추어 유사도 1–5를 매김.
> 다른 조사자 담당과 겹치는 것: (a) 명령 인터페이스 계층(HULK·FALCON·Thor·SoFTA·AMO), (b) 시각 teacher→student(LessMimic 시각판, VisualMimic, VIRAL), (c) 동결 하위 제어기 위 학습 요령(Humanoid Hanoi 데이터 집계, AdaptManip 잔차). 여기서는 "물체 들기" 관점(보상·접촉·커리큘럼·성공 정의)만 다룸.
> 이미 다른 조사자가 받아 둔 폴더: `reference/resmimic`(논문만), `catchcarry`, `omnigrasp`, `visualmimic`, `ase`, `closd`, `maskedmimic`, `pulse`, `puppeteer`, `hilmares`, `whatmatters` — 이 노트에서는 resmimic 만 다시 다룸(내려받기 건너뜀).

## 1. 카탈로그: 2022–2026 박스/큰 물체 집기·운반 방법 (목표 항목)

### Takeaway
우리 구조(동결된 하체 보행 정책 + 상체 관절 목표·골반 명령을 내는 상위 정책 + 손가락 없는 손으로 옆면 조이기)와 거의 같은 것은 **Humanoid Hanoi**(Digit, 팔 관절 목표+골반 pitch·높이 10차원 지시를 공유 WBC 에 줌)와 **AdaptManip**(G1 고무 손, 동결 보행 정책에 [vx,vy,ω,z] 명령 + 상체 17차원 잔차)이고, 보상 설계 참고로는 **PhysHSI/SplitAdapter**(G1 고무 손, 바닥 0–0.6 m, 실기 0.30×0.43×0.30 m 상자)와 **Digit 박스(Dao et al.)**가 가장 직접적이다. 2026년 신작(OmniContact, LessMimic, HULK, HOTICE, SplitAdapter, I-BFM)은 대부분 G1 실기이며 시뮬 성공률 85–99 %대, 실기는 3–10회 단위 시험만 보고한다.

### Cited Findings

#### 요약 표 (유사도 순)

| short_id | title | venue/year | arXiv | code | license | 유사도 | downloaded path |
|---|---|---|---|---|---|---|---|
| humanoid_hanoi | Humanoid Hanoi: Investigating Shared Whole-Body Control for Skill-Based Box Rearrangement | CoRL 2026 (논문 머리글) | [2602.13850](https://arxiv.org/abs/2602.13850) | [osudrl/Humanoid_Hanoi](https://github.com/osudrl/Humanoid_Hanoi) (MuJoCo 벤치마크 환경) | 라이선스 파일 없음 | 5 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/humanoid_hanoi/ (paper.pdf, code/) |
| adaptmanip | AdaptManip: Learning Adaptive Whole-Body Object Lifting and Delivery with Online Recurrent State Estimation | arXiv 2026 (저장소 파일명상 RA-L 2026, 미확인) | [2602.14363](https://arxiv.org/abs/2602.14363) | 없음 ([morganbyrd03/adaptmanip](https://github.com/morganbyrd03/adaptmanip)는 PDF·영상만 있는 프로젝트 페이지) | — | 5 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/adaptmanip/ (paper.pdf, 링크만) |
| physhsi | PhysHSI: Towards a Real-World Generalizable and Natural Humanoid-Scene Interaction System | arXiv 2025 (preprint) | [2510.11072](https://arxiv.org/abs/2510.11072) | [InternRobotics/PhysHSI](https://github.com/InternRobotics/PhysHSI) (legged_gym, G1 carrybox) | CC BY-NC-SA 4.0 | 4 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/physhsi/ (paper.pdf, code/) |
| splitadapter | SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation | arXiv 2026 (preprint) | [2606.03297](https://arxiv.org/abs/2606.03297) | 없음(프로젝트 페이지만) | — | 4 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/splitadapter/ (paper.pdf, 링크만) |
| digitbox | Sim-to-Real Learning for Humanoid Box Loco-Manipulation (Dao, Duan, Fern) | ICRA 2024 | [2310.03191](https://arxiv.org/abs/2310.03191) | 없음 | — | 4 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/digitbox/ (paper.pdf, 링크만) |
| hdmi | HDMI: Learning Interactive Humanoid Whole-Body Control from Human Videos | arXiv 2025 (preprint) | [2509.16757](https://arxiv.org/abs/2509.16757) | [LeCAR-Lab/HDMI](https://github.com/LeCAR-Lab/HDMI) | 라이선스 파일 없음 | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/hdmi/ (paper.pdf, code/) |
| resmimic | ResMimic: From General Motion Tracking to Humanoid Whole-body Loco-Manipulation via Residual Learning | arXiv 2025 (preprint) | [2510.05070](https://arxiv.org/abs/2510.05070) | [amazon-far/ResMimic](https://github.com/amazon-far/ResMimic) | Apache-2.0 | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/resmimic/ (다른 조사자가 받음, 논문만; 코드는 링크만) |
| hulk | HULK: Learning Whole-Body Forceful Loco-Manipulation for Humanoids | arXiv 2026 (preprint) | [2610.08970](https://arxiv.org/abs/2610.08970) | 없음(www.hulk-forceful-wbc.com) | — | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/hulk/ (paper.pdf, 링크만) |
| lessmimic | LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations | arXiv 2026 (preprint) | [2602.21723](https://arxiv.org/abs/2602.21723) | [Yutang-Lin/LessMimic](https://github.com/Yutang-Lin/LessMimic) (현재 README 만) | 없음 | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/lessmimic/ (paper.pdf, code/=README) |
| omnicontact | OmniContact: Chaining Meta-Skills via Contact Flow for Generalizable Humanoid Loco-Manipulation | CoRL 2026 (저장소 README) | [2606.26201](https://arxiv.org/abs/2606.26201) | [Ingrid789/OmniContact](https://github.com/Ingrid789/OmniContact) (Isaac Lab), [OmniContact_sim2sim](https://github.com/Ingrid789/OmniContact_sim2sim) | 라이선스 파일 없음 | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/omnicontact/ (paper.pdf, code/) |
| hotice | HOTICE: Whole-Body Humanoid Object Transportation in Cluttered Environments | arXiv 2026 (preprint) | [2609.25363](https://arxiv.org/abs/2609.25363) | 없음 | — | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/hotice/ (paper.pdf, 링크만) |
| embrace | Embracing Bulky Objects with Humanoid Robots: Whole-Body Manipulation with RL | arXiv 2025 (preprint) | [2509.13534](https://arxiv.org/abs/2509.13534) | 없음 | — | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/embrace/ (paper.pdf, 링크만) |
| boxlocomanip | Hierarchical Planning and Control for Box Loco-Manipulation (Xie et al.) | Proc. ACM CGIT 2023 (SCA) | [2306.09532](https://arxiv.org/abs/2306.09532) | 없음 | — | 3 | /home/robotis-ai/Projects2/dev10/pelvis_pick/reference/boxlocomanip/ (paper.pdf, 링크만) |
| omniretarget | OmniRetarget (상호작용 보존 리타게팅 + 박스 운반 추종) | arXiv 2025 | [2509.26633](https://arxiv.org/abs/2509.26633) | 미확인(아래 Gaps) | — | 2 | 링크만 |
| dreamcontrol | DreamControl (확산 사전 + RL, 바닥 집기·양손 집기) | arXiv 2025 | [2509.14353](https://arxiv.org/abs/2509.14353) | 미확인 | — | 2 | 링크만 |
| skillblender | SkillBlender (PackageLift/PackageCarry, 동결 기본 기술 섞기) | arXiv 2025 | [2506.09366](https://arxiv.org/abs/2506.09366) | [Humanoid-SkillBlender/SkillBlender](https://github.com/Humanoid-SkillBlender/SkillBlender) | NOASSERTION | 2 | 링크만 |
| coohoi | CooHOI (캐릭터, 혼자/둘이 큰 상자 운반) | NeurIPS 2024 Spotlight | [2406.14558](https://arxiv.org/abs/2406.14558) | [Winston-Gu/CooHOI](https://github.com/Winston-Gu/CooHOI) | 없음 | 2 | 링크만 |
| tokenhsi | TokenHSI (캐릭터, carry 태스크 토큰) | CVPR 2025 Oral | [2503.19901](https://arxiv.org/abs/2503.19901) | [liangpan99/TokenHSI](https://github.com/liangpan99/TokenHSI) | 없음 | 2 | 링크만 |
| ibfm | I-BFM (보상 조건 행동 기반 모델, Carry Box) | arXiv 2026 | [2610.06129](https://arxiv.org/abs/2610.06129) | 없음 | — | 2 | 링크만 |
| contactmimic | ContactMimic (접촉 조건 추종, Pick up box) | arXiv 2026 | [2607.08742](https://arxiv.org/abs/2607.08742) | 없음 | 논문 CC BY 4.0 | 2 | 링크만 |
| recipe_gr1 | Sim-to-Real RL for Vision-Based Dexterous Manipulation on Humanoids (GR-1 양손 상자 들기) | arXiv 2025 | [2502.20396](https://arxiv.org/abs/2502.20396) | 없음 | — | 2 | 링크만 |
| demohlm | DemoHLM (G1 + 평행 그리퍼, 범용 WBC 위 상위 정책) | roboticsproceedings rss22 (RSS 2026로 보임) | [2510.11258](https://arxiv.org/abs/2510.11258) | [BeingBeyond/DemoHLM](https://github.com/BeingBeyond/DemoHLM) | 없음 | 2 | 링크만 |
| opt2skill | Opt2Skill (Digit, 궤적 최적화 참조 + RL, 상자 집기 포함) | arXiv 2024 | [2409.20514](https://arxiv.org/abs/2409.20514) | 미확인 | — | 2 | 링크만 |
| softa | Hold My Beer (SoFTA, 상·하체 두 에이전트) | CoRL 2025 | [2505.24198](https://arxiv.org/abs/2505.24198) | [LeCAR-Lab/SoFTA](https://github.com/LeCAR-Lab/SoFTA) | MIT | 2 (겹침 a) | 링크만 |
| interphys | Synthesizing Physical Character-Scene Interactions (Hassan et al., carry 포함) | arXiv 2023 | [2302.00883](https://arxiv.org/abs/2302.00883) | 없음 | — | 2 | 링크만 |
| intermimic | InterMimic (OMOMO 큰 물체 HOI, teacher→student) | CVPR 2025 | [2502.20390](https://arxiv.org/abs/2502.20390) | [Sirui-Xu/InterMimic](https://github.com/Sirui-Xu/InterMimic) | MIT | 1–2 | 링크만 |
| genhoi / imagine2real / scenebot | 생성 영상·장면 접촉 기반 HOI (상자 집기 예시 포함) | arXiv 2026 | [2606.12995](https://arxiv.org/abs/2606.12995), [2605.22272](https://arxiv.org/abs/2605.22272), [2606.27581](https://arxiv.org/abs/2606.27581) | 없음/예정 | — | 1–2 | 링크만 |

내려받은 총량은 약 1.3 GB(코드 5개 + 논문 12편). 코드는 실행·설치·import 하지 않았고 설정 파일만 텍스트로 읽음.

#### 항목별 상세

**[humanoid_hanoi] Humanoid Hanoi (Oregon State, Digit V3, CoRL 2026) — 유사도 5**
- 구조: 각 기술(GoTo, GoTo-with-Box, Pickup, Place)은 2층 LSTM(은닉 64, 50 Hz) 정책이고, 관절 명령이 아니라 "마스크된 지시(directive)"를 내며, 사전학습된 공유 WBC(Masked Humanoid Controller, MHC)가 이를 20개 관절 PD 목표로 바꾼다 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Pickup 정책 출력은 **팔 관절 목표 + 골반(base) pitch + 높이 명령(a ∈ R^10)**, 관측은 고유감각 + 시작 시 상자 자세(로봇 루트 좌표) + 상자 치수 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Pickup 은 단계 커리큘럼(approach, contact, lift, stand). 접근 시간은 상자 높이에 맞춤: t_approach = 100×(0.9 − box height) + 30 (스텝), contact 25 스텝, lift 35 스텝, stand 는 목표 서기 높이 0.8 m 까지 거리로 결정. **접촉 후 45 스텝에 받침 탁자를 없애 완전히 들도록 강제**. 종료: 시간 초과, 상자 떨어짐, 잘못된 손 접촉. 끝에 120 스텝 서기 연장 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Pickup 보상(Table 3, w·exp(−α·c) 형태): hand contact position 0.5; base pitch/roll 0.2(α 15); **box rotation |θ|+|φ| 는 contact(L∧R) 일 때만 0.1(α 10)**; box acceleration 0.05; **table force F_table/mg 도 contact(L∧R) 일 때만 0.05(α 2.0)**; motor vel 0.05; torque 0.05; foot velocity 0.05; self-collision −1.0. 공유 항: hand traj tracking 0.1(α 5.5), hand roll 0.05, base height error 0.5(α 8), base pitch limit 1(|φ|>0.25) −0.1, CoP 0.15(α 20), stance width 0.05, action smoothness 0.1, low-level cmd 변화 0.05, height cmd 범위 밖 −0.1 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- 무작위화(Table 5): 상자 질량 0.0–3.5 kg, 크기 XYZ 0.15–0.5 m, X 0.3–0.6 m, Y ±0.1 m, **Z 0.085–0.95 m**, yaw ±18°, 미끄럼 마찰 0.1–1.0, 구름 0.01–0.1, 회전 0.001–0.005, 통신 지연 2–4 ms; 몸 질량 ×0.75–1.25, 관절 감쇠 ×0.5–3.5, 마찰 ×0.8–1.2 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- 핵심 발견: "낮은 높이 집기 등 극단 자세는 기술 정책이 그럴듯한 명령을 내도 DR 아래에서 실행 오류를 낸다" → 공유 WBC 가 새 기술이 유도하는 상태·명령 분포를 덮지 못함. 해결: 새 기술 폐루프 실행에서 성공한 지시 시퀀스(Pickup·Place 각 9개, 극단 측면 위치·높이)를 WBC 학습 참조 집합에 더해 원래 목적함수로 계속 학습("Extended") — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- 결과(DR, 10 시드×1000 에피소드): Pickup 성공 Base 89.43 % → Finetune 92.83 % / Residual 93.15 % / **Extended 96.92 %** / Joint 91.39 % / 종단간 E2E(Dao et al.) 81.11 %. 낮은 상자(<0.2 m): Base 85.00 % → Extended 95.03 %, E2E 73.13 %. 실기 7수 하노이 전체: Extended 6/15(40 %), 다른 기준선 0/15 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Place 는 Pickup 성공 롤아웃 60k(어려운 높이 70–90 cm, 크기 15–50 cm 1만 개 포함)를 거꾸로 돌려 참조로 사용, **내릴 때 앞쏠림을 벌하는 base-pitch 제약이 결정적**이었다고 보고 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- 코드: MuJoCo 벤치마크 환경(H1·G1·Digit 그림 포함) — [osudrl/Humanoid_Hanoi](https://github.com/osudrl/Humanoid_Hanoi)
- 가져올 것: 우리와 같은 "팔 목표 + 골반 높이·pitch" 지시 인터페이스, 높이 따라 접근 시간 조절, 접촉 후 받침 제거, 두 손 접촉일 때만 켜지는 상자 자세·탁자 하중 보상, 상위 정책이 만든 명령 시퀀스로 하체 정책 재학습(데이터 집계).

**[adaptmanip] AdaptManip (Georgia Tech, Unitree G1, 2026) — 유사도 5**
- G1 29 DoF, **관절 없는 고무 손이라 마찰만으로 잡음(form closure 없음)**, 양손 파지 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- 구조: PPO 로 학습한 **동결 보행 정책** 위에 잔차 조작 정책. 행동 = 보행 정책 명령 ū_loco = [v̄x, v̄y, ω̄, z̄] ∈ R^4 + 상체(허리·팔) 잔차 PD 목표 17차원. 비대칭 actor-critic(MLP 512-256-128), **PPO + 좌우 대칭 손실**. 상자 상태는 LSTM(128) 추정기가 시각(AprilTag)·고유감각·행동으로 추정, 정책과 함께 학습. 입력은 GT→추정값을 w = min(t/T, 1) 로 섞는 커리큘럼 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- 조작 보상(식 2, λ 값 미공개): 운동학 추종 exp(−|ψ_robot−ψ_box|), exp(−4‖p_hand‖), exp(−1.5‖p_root‖); 상자 안정 exp(−2‖p_box−p_des‖₁ − ‖q_box−q_des‖₁), exp(−‖v_root − v_box‖₂); **접촉력 품질 λ_con·clamp(Σ_h‖f_con,h‖·I_box, 0, 1)**; **미끄럼 벌점 −λ_slip·Σ_h min(0, v_hand,z − v_box,z)**. 본문은 "대칭 양손 접촉력 장려, 손–상자 접촉 방향 보상, 접촉 실패 벌점, 접선 미끄럼 억제"라고 설명 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- DR(Table II): 몸 질량 ±2.5 kg, kp/kd ×0.8–1.2, 지면 정마찰 0.3–1.5·동마찰 0.3–0.9, 탁자·상자 정마찰 0.3–1.3·동마찰 0.3–1.5·반발 0–0.5, **상자 질량 −0.88…+1.5 kg 가산**, 상자 x/y 크기 ×0.75–1.25, 무게중심 변화, 외력 ±4 N·±2 N·m — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- 종료: 20 s, 기울기 60° 초과, 루트 높이 0.15 m 미만, **상자 높이 0.25 m 미만** — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- 결과(135 시행 = 질량 3 × 크기 3 × 마찰 3 × 시드 5): 전체 성공 IsaacLab 0.85 / MuJoCo(미학습 시뮬) 0.75; Oracle 0.91/0.79; Pure RL 0.62/0.37; Pure RL+FK 0.88/0.61; Motion Imitation 0.42/0.00. MuJoCo 에서 재파지 6.32회 — 실패 후 다시 잡는 회복 행동. 원통 82–86 %, 구 51 %. 실기 G1 은 정성 시연만 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- 가져올 것: 우리 구조와 동일한 "동결 보행 명령 4개 + 상체 잔차", 대칭 손실, 미끄럼(손–상자 수직 속도 차) 벌점, 상자-루트 상대 속도 보상, 상자 높이 종료.

**[physhsi] PhysHSI (G1, 2025) — 유사도 4**
- G1 29 DoF, 고무 손 두 손 클램프(전용 파지 제어기 없음), AMP 기반 단일 PPO 정책(+판별기), 참조 데이터는 pickUp/carryWith/putDown 하위 집합으로 나눠 참조 상태 초기화(RSI)에 사용 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 관측: 고유감각 5스텝 이력(108차원/스텝) + 과제 15차원(상자 크기 3, 위치 3, 6D 회전 6, 목표 위치 3) — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 보상(w_G 0.7, w_R 0.7, w_S 0.3): 단계별 거리 게이트(0.7 m). Pick = 2.0·exp(−3|0.75 − box height|), 상자가 0.75 m 넘거나 목표 근처면 2.0; Carry 에 0.7·exp(−3‖box − hand‖²). 정규화(Table VI): dof vel −2e−4, torques −1e−4, dof acc −1e−7, torque limits −0.1, dof pos limits −5.0, action rate −0.03, dof vel limits −1e−3. **스타일 가중치를 초반엔 작게, 점점 키움**(빠르고 거친 지름길 억제) + L2C2 매끄러움 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 공개 코드 값: 상자 기본 0.3×0.3×0.25 m, x·y ×0.7–1.3, z ×0.6–1.4, 밀도 10–100 kg/m³; 손 충돌체 이름 "rubber_hand"; 들기 목표 높이 target_box_height 0.72; carryup = 0.7·exp(−3‖mean(hand_pos) − box_center‖²) + 2.0·(상자 높이 항); 공식 설정에서 hand_contact 가중치는 0.0(안 씀); 손–상자 거리는 상자 표면 최근접점 기준 exp(−0.5·d) 함수도 있음; 기술 초기화 확률 [loco 0.8, pickUp 0.2, carryWith 0.2, putDown 0] — [PhysHSI carrybox_config.py](https://github.com/InternRobotics/PhysHSI/blob/main/legged_gym/legged_gym/envs/g1/carrybox_config.py), [carrybox.py](https://github.com/InternRobotics/PhysHSI/blob/main/legged_gym/legged_gym/envs/g1/carrybox.py)
- 무작위화: 상자·받침 마찰 0.5–1.2, 반발 0–0.2, payload ±2 kg(논문) / 코드 payload_mass_range [−2, 5], 시뮬 상자 폭 0.2–0.5 m·높이 0.15–0.35 m, 상자·목표 높이 0.0–0.6 m — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072), [carrybox_config.py](https://github.com/InternRobotics/PhysHSI/blob/main/legged_gym/legged_gym/envs/g1/carrybox_config.py)
- 결과: 시뮬 91.34 %(분포 안) / 84.60 %(전체) — 본문 81.34 %, Table II 79.34 % 와 서로 다름(논문 내부 불일치). 실기 집기 8/10, 전체 6/10. 한계 분석: **높이 0–60 cm, 0.6–3.6 kg, 최대 크기 20–45 cm 까지 안정, 4.5 kg 0/3. 더 무겁거나 넓은 상자는 고무 손·팔 길이(도달) 한계로 실패** — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 가져올 것: G1 고무 손이라는 거의 같은 손 조건, 양손 평균 위치를 상자 중심에 두는 보상, 단계 게이트, 스타일 가중치 점증.

**[splitadapter] SplitAdapter (Samsung, G1, 2026) — 유사도 4**
- PhysHSI 식 AMP 기본 정책을 동결하고 물체/하중·동역학 두 문맥 인코더(50스텝 이력, FiLM)를 붙임. 학습 상자 x·y 0.25–0.45 m, z 0.25–0.35 m, **질량 0.5–5.0 kg**, 높이 0–0.6 m; 평가 2·4·6 kg × 0·30·60 cm — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- 보상(PhysHSI 대비 추가): carryup = 0.7·r_hand_pos + **0.7·r_hand_contact** + 2.0·r_box_height + 0.3·r_pelvis_box. r_hand_pos = exp(−3‖p_hand,avg − p_box‖²), r_box_height = exp(−3·max(h* − h_box, 0)), **r_hand_contact = min(min_k f_hand,k / 20, 1)·𝟙[∃k, f_wrist,k > 1.0]** (두 손 중 약한 쪽 힘 기준, 20 N 에서 포화). hold* = exp(−0.3·e_stand) − 0.05‖ω_pelvis,xy‖² − 0.02‖ω_torso,xy‖². 추가 정규화: 발목 간격이 좁으면 벌(ankle roll close), **상자 근처에서 상자가 너무 낮은 채 2.0 s 넘게 머물면 벌(low box time penalty)**. 놓은 뒤 hand_free(두 손 다 떼면 1, 한 손 0.5, 둘 다 붙어 있으면 0) — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- DR: 상자 마찰 0.5–1.0, 반발 0.05–0.2, 받침 마찰 0.5–2.0, 무게중심 ±0.1 m, 링크 질량 ×0.8–1.2, Kp/Kd ×0.9–1.1, 8 스텝마다 ±50 외란 — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- 결과: MuJoCo 90 시행 전체 성공 Base(PhysHSI) 71/90 → SplitAdapter 86/90, 들기 86/90 → 90/90. **6 kg·0 cm(바닥)이 가장 어려움**: Base 5/10 → 10/10. 실기 G1(고마찰 장갑, 모캡, **검증 상자 0.30×0.43×0.30 m**) 전체 16/27 → 26/27, 들기 22/27 → 27/27; 6 kg 0/30/60 cm 에서 Base 1·1·0 → 2·3·3 — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- 가져올 것: min-힘 접촉 보상(한 손 밀기 차단), 바닥에서 머뭇거림 벌점, hold 보상, 실기 상자가 우리 것(37×40×29)과 거의 같은 크기.

**[digitbox] Dao, Duan, Fern — Digit 박스 (ICRA 2024) — 유사도 4**
- Digit(손가락 없음), 5개 기술(Walk, Stand, StandBox, PickUp, WalkBox)을 따로 학습하고 이전 기술 종료 상태를 다음 기술 초기 분포로 사용, 전환 시 10 스텝 행동 보간 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- PickUp: 상자 0.35–0.5 m 앞, ±0.3 m 옆, **바닥에서 1.3 m 높이까지**, yaw ±22.5°, 각 변 20–45 cm, 1–10 kg. 명령 = 상자 치수·질량·시작 자세 + 목표 위치 + 두 위상 지시자(p_contact, p_lift). 행동은 **현재 모터 위치에 더함(고정 기준보다 빨리 학습)** — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- 보상 R = R_traj + R_box + R_stand + R_reg (가중치 Table III: Hand Position 0.15, Hand Roll 0.05, Box Position 0.15, Box Orientation 0.05, Table force 0.05, CoP 0.1, Base Orientation 0.05, Foot Orientation 0.1, Motor Velocity 0.05, Foot Velocity 0.05, Hand Force 0.05, Box Acceleration 0.05, Action Change 0.05, Torque 0.05). 손 궤적: 1.5 s 에 상자 옆 10 cm, **2 s 에 옆면에 닿고**, 3.5 s 에 목표 위치 양옆. **r_contact 는 t ≥ t_contact 일 때만 켜짐(너무 이른 접촉 방지)**, 양손 접촉 지시자에 대한 로그형 식(추출 텍스트가 깨져 정확한 식은 불확실). 손 힘 ‖F_hand,box‖ 벌점으로 "부드러운 손 상호작용". 자가 충돌·손 속도 > 1.0 m/s 에 −0.1 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- 종료(탐색 유도): 몸통 높이 < 40 cm, 몸통 pitch > 35°, 발 접촉 상실, 탁자에 몸이 닿음, 상자가 땅에, **접촉 마감 0.5 s 뒤에도 손이 상자에 안 닿음, 들기 마감 0.5 s 뒤에도 상자가 탁자에 닿아 있음** — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- StandBox/WalkBox: 상자를 쥔 채 시작, **손이 상자 접촉을 잃으면 종료**; 상자 높이 명령 h_cmd 추종, 상자 질량(±0.5 kg)·치수(±5 cm) 입력에 잡음 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- 결과(MuJoCo 1만 에피소드): PickUp 96.15 %(오차 7.93 cm), StandBox 95.25 %, WalkBox 100 %. 분포 밖 한계: 질량 22.9 kg, 크기 64 cm, Z 130 cm. **손 궤적 보상을 빼면 표본이 약 2배 필요하고 실기 성공도 낮음**. 실기 1–8 kg 성공, 단 실기에서 한쪽으로 기울어 "무게중심 trim" 필요, 8 kg 에서는 앞으로 기울어 trim 증가 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- 가져올 것: 시간 게이트 접촉 보상, 접촉·들기 마감 종료, 손 힘 벌점, 상자를 쥔 서기·걷기 정책의 접촉 상실 종료.

**[hdmi] HDMI (CMU LeCAR, G1, 2025) — 유사도 3**
- 사람 영상에서 뽑은 로봇·물체 궤적을 함께 추종, 행동 = 참조 관절 + 잔차(θ_target = θ_ref + a_t) — [arXiv 2509.16757](https://arxiv.org/abs/2509.16757)
- 보상 가중치(Table I): body local pose 2.0, root global pose 1.0, body global vel 1.0, joint 1.0, **object pose 2.0, contact 5.0**, action rate 0.1, joint pos limits 10.0, joint vel 5e−4, torque limits 0.01, feet impact 1.0, feet slip 0.5, feet air time 5.0. 접촉 보상 R_contact,i = exp(−‖p_eef,i − p_target,i‖/σ_pos)·min(exp((‖F_i‖ − F_thres)/σ_frc), 1), 원하는 접촉 끝단 평균 — [arXiv 2509.16757](https://arxiv.org/abs/2509.16757)
- 공개 설정 값: eef_contact_exp pos_sigma 0.3, frc_sigma 40, **frc_thres 10 N**; bread box 접촉 목표 = 상자 기준 좌우 ±0.17 m(높이 0.14 m) 옆면; 상자 질량 1.2–1.8 kg, 동마찰 0.3–0.8, 정/동 비 1.0–2.0, 크기 ×0.9–1.1; 접촉 상실 종료 pos > 0.2 m 이고 힘 < 1.0 N 이 25 스텝 — [hdmi-base.yaml](https://github.com/LeCAR-Lab/HDMI/blob/main/cfg/task/base/hdmi-base.yaml), [carry_and_place_bread_box.yaml](https://github.com/LeCAR-Lab/HDMI/blob/main/cfg/task/G1/hdmi/carry_and_place_bread_box.yaml)
- 종료: 루트·몸·물체 자세 오차 > 0.5 m 또는 1.2 rad(최소 25 스텝), 접촉 상실. 실기: 여행가방 연속 7회, 빵 상자 2회 완주 — [arXiv 2509.16757](https://arxiv.org/abs/2509.16757)

**[resmimic] ResMimic (Amazon FAR, G1, 2025) — 유사도 3**
- 사람 동작만으로 학습한 GMT 정책 위에 잔차 Δa ∈ R^29, a = a_gmt + Δa, 잔차 마지막 층은 작은 이득 Xavier 초기화 — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)
- 보상: 물체 점구름 추종 exp(−λ_o Σ‖P_i − P̂_i‖), 접촉 보상 Σ ĉ_i·exp(−λ/f_i)(몸통·엉덩이·팔, 발 제외). **가상 물체 제어기**: 초기 학습 안정화를 위해 물체를 참조 쪽으로 PD 힘·토크로 당기고 이득을 점차 줄임. 종료: 물체 메시 편차 > σ_o, **필요 접촉이 10 프레임 넘게 끊기면 종료** — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)
- 시뮬(MuJoCo) 성공: Kneel 90 %, Carry 100 %, **Squat(팔·몸통으로 들기) 80 %**, Chair 100 %; 기본 GMT 는 Squat 40 %, 처음부터 학습 0 %. 실기 4.5 kg 상자(손목 한계 약 2.5 kg)를 전신 접촉으로 운반 — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)

**[hulk] HULK (Amazon·UMich·Caltech, G1, 2026) — 유사도 3 (겹침 a)**
- 명령 인터페이스: 평면 속도, yaw rate, **base height 0.5–0.8 m, 몸통 roll/pitch, 팔 관절 목표** — 우리 하체 명령과 매우 비슷. 손목 하중 teacher + 전신 파지(몸통·팔뚝으로 안기) teacher → DAgger 학생 — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970)
- 물체 유지 보상: grasp-wrench 추종 [1 + E_g/(25 N)²]⁻¹ 가중 8; **grasp-force 정규화 e/(e+50 N), e = max(F − 30 N, 0), 가중 −0.5(과도한 조임 벌)**; 물체 떨어짐 −250; 몸통 기준 물체 미끄럼 속도 −2 — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970)
- 커리큘럼: **파지 질량 상한 b_e 0.5–5 kg, 완주 시 ×1.1, 실패 종료 시 ÷1.1**; 손목 힘 계수 0.02씩 증감; 지연 20 ms 까지 점증. 종료: 기울기 70°, 발 외 지면 접촉, 물체 상대 이동 > 0.15 m, **물체 높이 < 0.30 m** — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970)
- 실기: 냉장고 4/4(최대 7.0 kg), 통 4/4(6.1 kg, 기준선 모두 0/4), 물건 운반 4/4(12.25 kg) — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970)

**[lessmimic] LessMimic (PKU/BIGAI, 2026) — 유사도 3 (겹침 b)**
- 거리장(DF) 특징 VAE 잠재 + 상호작용 판별기 보상(최소제곱 GAN 꼴) + 스타일; 추종 보상·수작업 성형 항은 일부러 뺌. teacher(π_mimic)로 ResMimic 사용 — [arXiv 2602.21723](https://arxiv.org/abs/2602.21723)
- PickUp = 다양한 크기 상자를 **바닥에서 두 손으로** 들어 유지. 성공: **상자가 지면 0.3 m 위로, 3 s 이상 안정 유지**. 실기(모캡) 22 cm 상자 10/10, 60 cm 8/10; 시각판 8/10, 7/10. 로봇 이름은 본문 가시 부분에 없음(G1 로 보이나 미확인) — [arXiv 2602.21723](https://arxiv.org/abs/2602.21723)

**[omnicontact] OmniContact (Noitom·HKUST, G1, CoRL 2026) — 유사도 3**
- 규칙 기반 CF-Gen(단계 템플릿·제약 IK 키프레임) + 단일 RL 추적기 CF-Track(희소 미래 목표 + 4차원 이진 접촉 상태). Carry Box 6단계(접근·쪼그려 잡기·들기·운반·쪼그려 놓기·서기) — [arXiv 2606.26201](https://arxiv.org/abs/2606.26201)
- 보상(Table 12): 몸통·몸 추종 각 0.2, **손목(고무 손) 위치·방향 0.4**, 물체 위치·방향 1.0, 손–물체 상대 위치·방향 0.4, 접촉 일치 1.0; 추적:AMP = 0.85:0.15. 마찰 DR 정 0.3–1.6·동 0.3–1.2, 물체 질량 ×0.5–1.5 — [arXiv 2606.26201](https://arxiv.org/abs/2606.26201)
- 시뮬 Carry Box: OmniContact 98.70 %, PhysHSI 87.00 %, LessMimic 34.00 %(xy 만), HDMI 0 %, SONIC 3.38 %(저자 측정). 실기 G1 + Noitom 모캡 — [arXiv 2606.26201](https://arxiv.org/abs/2606.26201)

**[hotice] HOTICE (USC, G1, 2026) — 유사도 3**
- 하체 12 + 팔 8 관절 두 에이전트(허리·손목 제외), 각자 critic; 안내장(guidance field) 벡터 관측. 상자 최대 40×40×40 cm, 최대 3.5 kg. 종료: 넘어짐·떨어뜨림·장애물 충돌. 성공: 5 s 안에 목표 0.1 m 이내 — [arXiv 2609.25363](https://arxiv.org/abs/2609.25363)
- 시뮬 88.5 %(2만 시행), 실기 장애물 유형별 6/6·5/6·5/6 — [arXiv 2609.25363](https://arxiv.org/abs/2609.25363)

**[embrace] Embracing Bulky Objects (HKUST-GZ, H1-2, 2025) — 유사도 3 (구조만)**
- PHC teacher → PULSE 식 VAE 모션 사전(디코더·prior 동결) → 상위 정책이 잠재 z 출력. NSDF(상자 중심→상체 링크 거리장) 15차원 특징이 핵심: NSDF 없으면 MuJoCo 3 kg 성공 0 %, 있으면 100 %; 7 kg 원통 93 %, 직육면체 80 % — [arXiv 2509.13534](https://arxiv.org/abs/2509.13534)
- 초기화 세 가지 무작위 선택: 멀리서 접근 / 안기 직전 자세 / 이미 안은 자세 — [arXiv 2509.13534](https://arxiv.org/abs/2509.13534)

**[boxlocomanip] Xie et al. 2023 (캐릭터, Proc. ACM CGIT) — 유사도 3**
- 웅크리기→일어서기 단일 참조(팔은 쉼 자세→운반 자세 선형 보간) + RL. 보상: 모방 곱(r_joint·r_translation·r_orientation) + r_box-hand = exp(−‖p_lhand − p_lbox‖² − ‖p_rhand − p_rbox‖²)(**상자 반대 옆면의 미리 정한 점**), 상자 직립 exp(−10‖·‖²), 상자 높이를 받침 높이→몸통 높이(1.2 m)로 보간한 목표 추종 exp(−10·…) — [arXiv 2306.09532](https://arxiv.org/abs/2306.09532)
- 학습 받침 높이 0.3–0.7 m, 폭 0.3–0.5 m, 1 kg 인데 상자 1개 기준 **0.05–1.00 m 높이**, 8 kg, 폭 0.12–0.79 m 까지 일반화 — [arXiv 2306.09532](https://arxiv.org/abs/2306.09532)

**유사도 2 이하 (요점만)**
- CooHOI: 손 두 개의 중점을 물체 양 끝 중심("held points")에 두는 보상 exp(−5‖x_hand − h‖²), 보상 0.2·walk + 0.4·held + 0.4·target, AMP 0.5:0.5; 혼자 5–25 kg 학습, 13 kg 넘으면 성공 급감; 종료: 물체 높이 < 0.3 m 이고 수평 속도 > 1 m/s(차기 방지); 성공 = 최종 거리 < 0.2 m, 혼자 96.48 % — [arXiv 2406.14558](https://arxiv.org/abs/2406.14558)
- TokenHSI carry: 성공 = 상자 중심이 목표 20 cm 구 안; 조합 시 상자 최저점이 지면 20 cm 미만이면 운반 실패; 전문 정책 83.1 %, TokenHSI 92.2 % — [arXiv 2503.19901](https://arxiv.org/abs/2503.19901)
- SkillBlender(H1·G1·H1-2, 손목·손 고정, **팔뚝으로** 들기): PackageLift 보상 5·exp(−4‖h_pkg − ĥ‖) + 5·exp(−4‖p_wrist − p_pkg‖), 동결 기본 기술(Reaching+Squatting)을 관절별 softmax 가중으로 섞음 — [arXiv 2506.09366](https://arxiv.org/abs/2506.09366)
- DreamControl(G1, 손 이진 개폐): 바닥 집기(옆 잡기 손목 목표 0.1 m, 위 잡기 0.2 m)·양손 집기(0.65 m) 시뮬 100 %; 들어 올리면 주는 희소 보상 — [arXiv 2509.14353](https://arxiv.org/abs/2509.14353)
- OmniRetarget(G1): 보상 5개(몸 추종, 물체 추종, action rate, 소프트 관절 한계, 자가 충돌)만으로 상자 운반 다중 정책; 물체 질량 0.1–2 kg·무게중심 ±0.08 m·관성 50–150 %·형상 ±10 % DR; 물체가 1.0 m·45° 벗어나면 종료 — [arXiv 2509.26633](https://arxiv.org/abs/2509.26633)
- I-BFM(G1): Carry Box 시뮬 94.3 %, 실기 상자 0.35 m 정육면체 0.7 kg(정성); 성공 = 3D 거리 < 0.2 m 를 100 스텝 유지 — [arXiv 2610.06129](https://arxiv.org/abs/2610.06129)
- ContactMimic(G1): 접촉 라벨 일치 보상 ½(TPR+TNR) 가중 4.0, 접촉 거리 보상 σ 0.2 m 가중 3.0 + 불필요 접촉 벌점; "Pick up box" 포함, 실기 성공은 기대기·앉기 동작만 보고 — [arXiv 2607.08742](https://arxiv.org/abs/2607.08742)
- GR-1 양손 상자 들기(덱스 손): 손끝–물체 "스티커"(접촉 표식) 거리 1/(1+α·d) 합 + 목표 보상, 실기 80 % — [arXiv 2502.20396](https://arxiv.org/abs/2502.20396)
- DemoHLM: 하위 범용 WBC + 상위 조작 정책 계층, 단 G1 고무 손을 3D 프린트 평행 그리퍼로 교체("고무 손은 정밀 조작에 부족") — [arXiv 2510.11258](https://arxiv.org/abs/2510.11258)
- Opt2Skill(Digit): DDP 궤적 최적화 참조 + RL 잔차, 상자 집기 포함 — [arXiv 2409.20514](https://arxiv.org/abs/2409.20514), [Georgia Tech lab page](https://lab-idar.gatech.edu/opt2skill-achieving-versatile-humanoid-loco-manipulation-through-model-based-trajectory-optimization-and-reinforcement-learning/)
- Hold My Beer / SoFTA: 상체 100 Hz·하체 50 Hz 두 에이전트, 끝단 가속 2–5배 감소(CoRL 2025) — [arXiv 2505.24198](https://arxiv.org/abs/2505.24198)
- 산업: Agility Digit "motor cortex" WBC 기초 모델(LSTM < 100만 파라미터, Isaac Sim 학습, 팔·몸통 자유공간 목표로 무거운 물체 집기·놓기) — [Agility blog](https://www.agilityrobotics.com/content/training-a-whole-body-control-foundation-model); Boston Dynamics·TRI Atlas LBM(2025-08, 걷기·쪼그리기·들기 섞인 포장·분류, 단일 모델, 회사 발표만) — [TRI news](https://tri.global/news/ai-powered-robot-boston-dynamics-and-toyota-research-institute-takes-key-step-towards-general)

### Inferences
- 손가락 없는 손 + 옆면 조이기 조건에서 실기까지 간 사례는 Digit(Dao, Hanoi)과 G1 고무 손(PhysHSI, SplitAdapter, AdaptManip, OmniContact)이 전부이며, 이들 모두 손가락 대신 "양손 위치 목표 + 접촉/힘 항 + 상자 높이 항"의 세 묶음 보상을 쓴다.
- 동결 하위 제어기 위 상위 정책 구조(Hanoi, AdaptManip, Embrace, SkillBlender, DemoHLM)에서 반복되는 실패 원인은 "상위 정책이 하위 제어기 학습 분포 밖 명령(특히 낮은 집기)을 낸다"는 것이다. 우리 하체 정책이 0.335 m 근처·pitch 큰 영역을 얼마나 학습했는지가 바닥 상자 성공률을 가를 가능성이 크다(Hanoi 의 데이터 집계가 직접 대응책).
- 우리 상자(37×40×29 cm)는 PhysHSI 실기 최대 폭(45 cm) 안이지만 기본 학습 상자(0.3 m)보다 크다. SplitAdapter 실기 상자(0.30×0.43×0.30)가 가장 비슷하다.

### Gaps
- AdaptManip·HDMI·ResMimic·PhysHSI 의 실기 성공률은 시행 수가 적거나(2–10회) 정성 시연뿐이다.
- 2026년 HULK·HOTICE·SplitAdapter·I-BFM·Embrace 는 코드가 없다(2026-10-23 기준 확인).
- HumanoidBench 상자 과제, PhysHOI, SkillMimic-V2, InterPhys(Hassan 2023)의 carry 보상 세부, FALCON·Thor 는 이번에 원문을 확인하지 못했다(겹침 a 조사 범위).
- "Load-Aware Locomotion Control for Humanoid Robots in Industrial Transportation Tasks"([2603.14308](https://arxiv.org/pdf/2603.14308)), "Whole-Body Dexterity"([2610.22184](https://arxiv.org/abs/2610.22184)), WT-UMI([2606.13232](https://arxiv.org/pdf/2606.13232)), CompliantWBC([2609.33310](https://arxiv.org/abs/2609.33310))는 검색 제목만 봤다.
- OmniRetarget 공개 코드 위치: [amazon-far/holosoma](https://github.com/amazon-far/holosoma)(Apache-2.0, 약 125 MB)가 있으나 이번에 내용을 확인하지 않았다.

## 2. 한 손 밀기 대신 두 손 조이기(squeeze)를 안정적으로 만드는 보상·접촉 정식화는?

### Takeaway
가장 직접적인 장치는 (1) **두 손 중 약한 쪽 힘으로 주는 접촉 보상**(SplitAdapter: min_k f_hand,k/20), (2) **두 손 접촉(L∧R)일 때만 켜지는 하류 보상**(Hanoi: 상자 자세·탁자 하중 보상)과 **접촉 마감 뒤 미접촉 종료**(Digit), (3) **상자 반대 옆면에 정한 손 목표점 또는 양손 중점=상자 중심 보상**(Xie, CooHOI, PhysHSI, HDMI ±0.17 m), (4) **좌우 대칭 손실**(AdaptManip)이다. "평균·합" 형태의 손별 보상은 한 손만 닿아도 절반을 주므로 한 손 국소 최적을 막지 못한다.

### Cited Findings
- SplitAdapter 의 손 접촉 보상은 r = min(min_k f_hand,k / 20, 1)·𝟙[∃k, f_wrist,k > 1 N] 로 두 손 중 작은 힘만 셈하며 carryup 안에서 가중 0.7 — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- Humanoid Hanoi Pickup 은 상자 회전 보상과 탁자 하중(F_table/mg) 보상을 contact(L∧R) 일 때만 적용하고, 잘못된 손 접촉이면 종료, 접촉 45 스텝 뒤 받침 탁자를 제거해 완전히 들게 함 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Digit 박스: 손 목표 궤적이 "상자 옆 10 cm(1.5 s) → 옆면 접촉(2 s) → 목표 양옆(3.5 s)", 접촉 보상은 t_contact 이후에만 켜져 이른 접촉을 막고, 접촉 마감 0.5 s 뒤에도 손이 안 닿았거나 들기 마감 0.5 s 뒤에도 상자가 탁자에 닿아 있으면 종료. 손 궤적 보상을 빼고 "좌우 옆면 중심" 고정 목표만 쓰면 표본이 약 2배 들고 실기 성공이 낮음 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- PhysHSI 는 양손 평균 위치와 상자 중심 거리 exp(−3‖·‖²)(가중 0.7)와 상자 높이 항(가중 2.0)을 쓰고, 명시적 접촉·마찰 보상 없이 AMP 운반 동작 사전으로 두 손 클램프를 얻음; 공식 코드의 hand_contact 가중은 0.0 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072), [carrybox_config.py](https://github.com/InternRobotics/PhysHSI/blob/main/legged_gym/legged_gym/envs/g1/carrybox_config.py)
- CooHOI 도 "두 손 중점"을 물체 양 끝 중심점에 두는 held 보상 exp(−5‖x_hand − h‖²)(가중 0.4) — [arXiv 2406.14558](https://arxiv.org/abs/2406.14558)
- Xie et al.: 왼손·오른손을 상자 왼쪽·오른쪽 미리 정한 점에 각각 두는 r_box-hand(두 거리 합을 하나의 exp 안에) — [arXiv 2306.09532](https://arxiv.org/abs/2306.09532)
- HDMI: 손별 접촉 보상 = 위치 항 × 힘 항(F_thres 10 N, σ_frc 40), 원하는 접촉 끝단 평균, 가중 5.0(가장 큼); 상자 기준 좌우 ±0.17 m 옆면 목표; 접촉 상실(> 0.2 m 이고 < 1 N 이 25 스텝) 종료 — [arXiv 2509.16757](https://arxiv.org/abs/2509.16757), [hdmi-base.yaml](https://github.com/LeCAR-Lab/HDMI/blob/main/cfg/task/base/hdmi-base.yaml)
- AdaptManip: 대칭 양손 접촉력 장려, 접촉 방향 보상, 접촉 실패 벌점, clamp(Σ_h‖f_h‖·I_box,0,1), 수직 미끄럼 벌점, PPO 에 좌우 대칭 손실 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- ResMimic: 필요한 몸–물체 접촉이 10 프레임 넘게 끊기면 종료 + 가상 물체 제어기로 학습 초기에 물체를 참조 쪽으로 받쳐 줌 — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)
- 과도한 조임 억제: HULK 는 합산 접촉력이 30 N 을 넘으면 e/(e+50 N) 벌점(−0.5), Digit 은 손 힘 크기 벌점(0.05) — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970), [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- GR-1 덱스 손 연구는 손별 접촉 표식 거리 보상을 합하지만 한 손 밀기를 어떻게 막는지는 설명하지 않음 — [arXiv 2502.20396](https://arxiv.org/abs/2502.20396)
- LessMimic Push 평가는 "몸 위주 접촉"을 실패로 셈(손 접촉률) — [arXiv 2602.21723](https://arxiv.org/abs/2602.21723)

### Inferences
- 우리 과거 "한 손 밀기" 국소 최적은 손별 보상을 더하거나 평균하는 꼴에서 자주 생긴다고 본다. 바꿀 순서 권고: ① 접촉/힘 보상을 min(왼손, 오른손)으로, ② 상자 높이·상자 자세 보상에 두 손 접촉 게이트, ③ 손 목표점을 상자 좌우 옆면 중심(우리 상자 폭 37 또는 40 cm 면)으로 두고 두 거리를 한 exp 안에 합산(Xie 식), ④ 접촉 마감 종료(Digit 식). ⑤ 좌우 대칭 손실은 비용이 작아 함께 넣을 만하다.
- 필요한 조임 힘 어림(계산, 인용 아님): 2 kg 상자를 두 손 마찰로만 들려면 손당 법선력 ≥ m·g / (2μ) = 19.6/(2μ) → μ 0.6 에서 약 16 N, μ 1.0 에서 약 10 N. 질량 DR·가속을 감안하면 SplitAdapter 의 20 N 포화 기준이 우리 질량 범위와 맞는다. 팔 kp ≈ 22 N·m/rad 이면 손 끝 힘은 모멘트 팔 길이에 따라 다르므로, 관절 목표를 상자 안쪽으로 얼마나 넣어야 20 N 이 나오는지는 K1 팔 기하로 따로 재야 한다.
- "출력 포화" 문제는 HULK 식 상한 벌점(30 N 초과)이나 Digit 식 손 힘 벌점으로 조임 목표를 유한하게 묶으면 줄어들 수 있다.

### Gaps
- min-힘 보상과 합/평균 보상을 같은 조건에서 직접 비교한 절제 실험은 찾지 못했다(SplitAdapter 는 기준선 PhysHSI 와 보상·어댑터가 함께 다름).
- 어느 논문도 MuJoCo 피라미드 마찰 원뿔 대 타원 원뿔 차이를 다루지 않는다(Hanoi 는 MuJoCo 에서 미끄럼 마찰 0.1–1.0 을 무작위화한다고만 씀).

## 3. 바닥 높이 물체(쪼그림 대 숙임), 들어 올릴 때의 질량, 일어선 뒤 유지 안정성은 어떻게 다루나?

### Takeaway
바닥(0 cm)은 모든 실기 논문에서 가장 어렵고(SplitAdapter 6 kg·0 cm, Hanoi < 0.2 m, PhysHSI 도달 한계), 해결책은 보상보다 **분포 범위**(학습 높이 0–0.6 m, 낮은 높이 전용 데이터 집계, 높이 따라 접근 시간)와 **자세 제약**(몸통 pitch 상한·앞쏠림 벌점, 발 간격)이다. 질량은 대부분 DR + 질량 입력/추정(Digit 입력, SplitAdapter 하중 인코더, AdaptManip LSTM)으로 다루고, 커리큘럼은 HULK(성공 ×1.1/실패 ÷1.1)와 ResMimic(가상 힘 감쇠) 정도다. 유지 안정성은 hold 보상·상자–몸통 상대 속도 벌점·접촉 상실 종료로 다룬다.

### Cited Findings
- 바닥 성능: SplitAdapter 시뮬 6 kg·0 cm 에서 Base(PhysHSI) 5/10 → 10/10, 실기 6 kg·0 cm 1/3 → 2/3, 논문 스스로 "6 kg, 0 cm 가 가장 어려움" — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- Hanoi: 낮은 상자(< 0.2 m) Pickup Base 85.00 % → 데이터 집계 95.03 %; 낮은 집기에서 WBC 실행 오류가 원인 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- PhysHSI: 실기 0–60 cm 안정, 넓거나 무거운 상자는 고무 손·팔 길이 도달 한계로 실패 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 쪼그림/숙임 선택: Hanoi Pickup 은 base pitch 와 height 를 둘 다 출력해 정책이 고르게 하고, base pitch limit 1(|φ|>0.25) −0.1 로 과한 숙임을 벌함; Place 에서는 "내릴 때 앞쏠림을 벌하는 명시적 pitch 제약이 결정적" — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- Digit: 몸통 pitch > 35° 또는 높이 < 40 cm 이면 종료; 실기 8 kg 에서 앞으로 기울어 trim 보정 필요 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- Xie: 참조가 "웅크림→일어섬"이고 학습 0.3–0.7 m 받침으로 0.05 m 까지 일반화 — [arXiv 2306.09532](https://arxiv.org/abs/2306.09532)
- ResMimic: Squat(팔·몸통으로 들기) 80 %, Kneel 90 % 로 무릎 꿇기도 별도 과제 — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)
- SplitAdapter: 발목 간격이 좁으면 벌점, 상자 근처에서 상자가 낮은 채 2 s 넘게 머물면 누적 벌점 — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- 질량 처리: Digit 은 상자 질량·치수를 정책 입력으로(±0.5 kg, ±5 cm 잡음), 학습 1–10 kg, 분포 밖 22.9 kg 까지 성공 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191); SplitAdapter 는 하중 인코더가 질량·적재 여부를 추정(질량 손실 가중 2.0) — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297); HULK 는 질량 상한 0.5–5 kg 을 성공 ×1.1·실패 ÷1.1 로 조절 — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970); PhysHSI 는 밀도 10–100 kg/m³ 로 질량을 크기와 함께 무작위화, 실기 4.5 kg 0/3 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- 유지 안정성: SplitAdapter hold* = exp(−0.3 e_stand) − 0.05‖ω_pelvis,xy‖² − 0.02‖ω_torso,xy‖² — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297); HULK 몸통 기준 물체 미끄럼 −2, 떨어짐 −250, 물체 상대 이동 > 0.15 m 종료 — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970); AdaptManip exp(−‖v_root − v_box‖) 와 수직 미끄럼 벌점 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363); Digit StandBox/WalkBox 는 손 접촉 상실 시 종료, 상자 가속 벌점 0.05 — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191); Hanoi 는 끝에 120 스텝 서기 연장 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- 초기화로 단계 다루기: PhysHSI 혼합 RSI(참조 단계 시작 + 기본 자세 시작), Embrace 세 초기 상황(멀리/안기 직전/이미 안음), Digit 이전 기술 끝 상태 사용 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072), [arXiv 2509.13534](https://arxiv.org/abs/2509.13534), [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)

### Inferences
- K1 은 골반 높이 0.335 m 까지, pitch ±45° 가 가능하므로 Hanoi 처럼 높이·pitch 를 둘 다 상위 정책에 맡기고 pitch 상한 벌점으로 과한 숙임만 막는 편이 우리 구조와 맞다. 바닥 상자 도달 한계는 보상으로 못 고친다는 우리 과거 결론과 PhysHSI 의 "도달 한계" 보고가 일치한다.
- 받침 높이 0–0.3 m 범위를 학습하되 Hanoi 식으로 접근 시간을 높이에 따라 늘리고, 들기 시작 후 받침을 없애는 장치가 "상자를 받침에 기대 끌기" 같은 편법을 막는 데 쓸 만하다.
- 질량 0.5–2 kg 범위면 커리큘럼보다 DR + (선택) 질량 입력으로 충분할 가능성이 크다; HULK 식 ×1.1 커리큘럼은 2 kg 상한 근처에서 미끄러짐이 잦을 때 고려.

### Gaps
- 같은 로봇에서 쪼그림 대 숙임 전략을 정량 비교한 연구는 찾지 못했다.
- 바닥(0 cm) 상자에서 어느 논문도 무릎·발목 관절 한계와 손 도달의 관계를 수치로 보고하지 않았다.

## 4. 파지 성공은 어떻게 정의·평가하나?

### Takeaway
세 부류다: (1) **들기 성공**(상자가 일정 높이 이상, 일정 시간 유지: LessMimic 0.3 m·3 s), (2) **배치 성공**(목표까지 거리 < 0.1–0.2 m, 기울기 조건 추가: PhysHSI·SplitAdapter·CooHOI·TokenHSI·I-BFM), (3) **넘어지지 않고 끝에 상자가 손에 있음**(Digit). 실기는 대부분 3–10회 시행의 성공 횟수다.

### Cited Findings
- LessMimic PickUp: 상자가 지면 0.3 m 위로, 3 s 이상 안정 유지; Carry 는 경로 이탈 최대 0.6 m — [arXiv 2602.21723](https://arxiv.org/abs/2602.21723)
- PhysHSI Carry Box: 목표 배치 오차 < 0.1 m; 실기 집기 8/10·전체 6/10 따로 셈 — [arXiv 2510.11072](https://arxiv.org/abs/2510.11072)
- SplitAdapter 학습 성공: 상자 수평 projected-gravity 노름 < 0.1(기울기)이고 최종 거리 < 0.1 m; Lift-up 과 Full-task 를 따로 보고 — [arXiv 2606.03297](https://arxiv.org/abs/2606.03297)
- Digit: 넘어지지 않고 에피소드 끝에 상자가 손에 있음 + 성공 에피소드의 목표 위치 오차(cm) — [arXiv 2310.03191](https://arxiv.org/abs/2310.03191)
- Hanoi: 성공률 외에 CoM 오차·발 힘 분포·상자 위치/yaw 오차를 함께 보고, 1000 에피소드×10 시드 — [arXiv 2602.13850](https://arxiv.org/abs/2602.13850)
- AdaptManip: 단계별 성공(Stage1 항법, Stage2 파지) + 떨어뜨림 횟수 + 재파지 횟수, 135 시행(질량·크기·마찰 3×3×3 × 5 시드), 학습 시뮬(IsaacLab)과 미학습 시뮬(MuJoCo) 둘 다 — [arXiv 2602.14363](https://arxiv.org/abs/2602.14363)
- HDMI 시뮬 성공 = 어떤 종료 조건도 안 걸리고 완주(4096 env 평균) — [arXiv 2509.16757](https://arxiv.org/abs/2509.16757)
- ResMimic: 물체 오차 E_o 가 임계 미만이고 균형 유지 — [arXiv 2510.05070](https://arxiv.org/abs/2510.05070)
- HULK 실기: 넘어짐·관절 토크 보호 정지·떨어뜨림 없이 완료 — [arXiv 2610.08970](https://arxiv.org/abs/2610.08970)
- I-BFM: 3D 거리 < 0.2 m 를 100 스텝 연속 유지 — [arXiv 2610.06129](https://arxiv.org/abs/2610.06129)
- CooHOI: 최종 거리 < 0.2 m; TokenHSI: 상자 중심이 목표 20 cm 구 안, 조합 시 상자 최저점 < 20 cm 이면 실패 — [arXiv 2406.14558](https://arxiv.org/abs/2406.14558), [arXiv 2503.19901](https://arxiv.org/abs/2503.19901)
- HOTICE: 5 s 안에 목표 0.1 m 이내, 넘어짐·떨어뜨림·충돌 없음 — [arXiv 2609.25363](https://arxiv.org/abs/2609.25363)

### Inferences
- 우리 "집기·서기·유지" 1단계에는 LessMimic 식(높이 + 유지 시간)에 SplitAdapter 식 기울기 조건과 Digit 식 "끝에 두 손 접촉 유지"를 합친 정의가 맞다. 예: 상자 바닥이 시작 높이 + Δh 이상, 수평 기울기 노름 < 0.1, 두 손 접촉을 N 초 유지, 넘어짐 없음.
- AdaptManip 처럼 학습 시뮬과 다른 시뮬(우리 경우 Isaac 학습 → MuJoCo)에서 마찰·질량 격자로 따로 재고, 떨어뜨림·재파지 횟수를 같이 보는 것이 sim2sim 차이를 드러내기 좋다.

### Gaps
- 여러 논문이 성공 임계값(ResMimic σ_o, E_o 임계)을 공개하지 않았다.
- 실기 시행 수가 작아(3–10) 통계적 비교는 어렵다.

## 5. 공개 코드와 자산(상자 URDF/USD, Isaac Lab 태스크)은?

### Takeaway
박스 집기 코드를 바로 읽을 수 있는 것은 **PhysHSI(legged_gym/IsaacGym, G1 carrybox, CC BY-NC-SA 4.0)**, **HDMI(G1 상자·여행가방 설정, 라이선스 파일 없음)**, **OmniContact(Isaac Lab, 라이선스 파일 없음)**, **Humanoid Hanoi(MuJoCo 벤치마크, 라이선스 파일 없음)**, **ResMimic(Apache-2.0)**이다. AdaptManip·SplitAdapter·HULK·HOTICE·Embrace·Digit 박스는 코드가 없다. 상자 자산은 대부분 코드 안에서 절차적으로 만드는 직육면체이다.

### Cited Findings
- PhysHSI: `legged_gym/legged_gym/envs/g1/carrybox.py`, `carrybox_config.py`(상자 크기·밀도·마찰·카메라 시야 마스킹·보상 가중), LICENSE = Attribution-NonCommercial-ShareAlike 4.0 — [InternRobotics/PhysHSI](https://github.com/InternRobotics/PhysHSI)
- HDMI: `cfg/task/G1/hdmi/` 아래 carry_and_place_bread_box, move_suitcase, carry_box_over_shoulder, push_box 등, 공통 `cfg/task/base/hdmi-base.yaml`, IsaacSim 기반; 라이선스 파일 없음 — [LeCAR-Lab/HDMI](https://github.com/LeCAR-Lab/HDMI)
- OmniContact: Isaac Lab 구조(`source/`, `rsl_rl/`, `scripts/`), CF-Gen MuJoCo 코드는 별도 저장소; 라이선스 파일 없음 — [Ingrid789/OmniContact](https://github.com/Ingrid789/OmniContact), [Ingrid789/OmniContact_sim2sim](https://github.com/Ingrid789/OmniContact_sim2sim)
- Humanoid Hanoi: MuJoCo 벤치마크 환경, `box-world-json`, H1/G1/Digit 자산 그림 — [osudrl/Humanoid_Hanoi](https://github.com/osudrl/Humanoid_Hanoi)
- ResMimic 공식 저장소 Apache-2.0(약 28 MB) — [amazon-far/ResMimic](https://github.com/amazon-far/ResMimic)
- LessMimic 저장소는 현재 README·그림만 — [Yutang-Lin/LessMimic](https://github.com/Yutang-Lin/LessMimic)
- AdaptManip 저장소는 논문 PDF·영상·index.html 뿐(코드 아님) — [morganbyrd03/adaptmanip](https://github.com/morganbyrd03/adaptmanip)
- 캐릭터 쪽: CooHOI(NeurIPS 2024, 라이선스 없음, 약 474 MB), TokenHSI(CVPR 2025, 라이선스 없음), InterMimic(MIT) — [Winston-Gu/CooHOI](https://github.com/Winston-Gu/CooHOI), [liangpan99/TokenHSI](https://github.com/liangpan99/TokenHSI), [Sirui-Xu/InterMimic](https://github.com/Sirui-Xu/InterMimic)
- 기타: SkillBlender(NOASSERTION), SoFTA(MIT), FALCON(MIT), DemoHLM(라이선스 없음) — [SkillBlender](https://github.com/Humanoid-SkillBlender/SkillBlender), [SoFTA](https://github.com/LeCAR-Lab/SoFTA), [FALCON](https://github.com/LeCAR-Lab/FALCON), [DemoHLM](https://github.com/BeingBeyond/DemoHLM)

### Inferences
- 라이선스 파일이 없는 저장소(HDMI, OmniContact, Humanoid Hanoi, CooHOI, TokenHSI)는 법적으로 기본 저작권 보호 상태라, 아이디어·수치 참고는 괜찮아도 코드 복사는 피하는 편이 안전하다. PhysHSI 는 비상업(NC) 조건이다. 직접 옮겨 쓸 수 있는 것은 ResMimic(Apache-2.0)·InterMimic·SoFTA·FALCON(MIT) 정도다.
- 우리 Isaac Lab 태스크에 바로 참고할 보상 코드 형태는 PhysHSI `_reward_carryup_task`(양손 평균–상자 중심 + 상자 높이 목표 0.72 m, 거리 게이트)와 HDMI `eef_contact_exp`(위치×힘, 힘 임계 10 N)다.

### Gaps
- Isaac Lab 용 상자 USD 자산을 따로 배포하는 프로젝트는 찾지 못했다(대부분 코드에서 직육면체 생성).
- OmniRetarget(holosoma)·SkillBlender·DemoHLM 저장소 안의 상자 과제 구성은 열어 보지 않았다.
