# 시각(깊이·RGB) 상위 loco-manipulation 정책: 특권 RL teacher → 시각 student 증류 (휴머노이드 + 다리 달린 매니퓰레이터)

조사일 2026-10-23. 대상: 2022년부터 2026년 10월까지, 최신 우선. "프리프린트"는 arXiv 페이지·프로젝트 페이지에서 학회 표기를 찾지 못한 것. 다른 조사자가 맡은 범위(명령 인터페이스 계층 HOMIE·AMO·FALCON, 휴머노이드 박스 집기 전용 방법, 동결 제어기 위 인터페이스·학습 요령)와 겹치는 항목은 짧게만 적었다.

우리 기준(유사도 판단용): K1(23 DoF, 고무 공 손 → 양손 조여 쥐기), 하위 = 골반 명령(vx, vy, wz, 높이 0.335–0.77 m, pitch ±45°, roll) 추종 RL + 상체 11 관절 외부 PD, 상위 = 상체 11 관절 목표 + 골반 명령, 박스 37×40×29 cm·0.5–2 kg·바닥 또는 0–0.3 m 받침, teacher(박스 자세·크기·질량·손–박스 접촉력) → student(D436 깊이 26×64 크롭, 6 프레임 + 고유감각, DAgger), Isaac Lab. 이전 결과 student 약 69 % vs teacher 약 90 %(Isaac), MuJoCo 약 50 %. 격차 원인은 접촉 정보로 추정.

## 질문 1. 관련 방법 목록: 로봇·과제·teacher 관측·student 입력·구조·증류법·격차 대책·sim2real·수치·코드·유사도

### Takeaway
우리 구조(동결 하위 제어기 + 특권 PPO teacher → 시각 DAgger student)와 뼈대가 같은 공개 연구는 VBC(사족+팔, 깊이), VIRAL·DoorMan(G1+HOMIE, RGB), VisualMimic(G1, 깊이, 키포인트 명령), PRISM·ULTRA(G1 박스 집기·운반, 깊이/점구름)다. 이들 중 student가 teacher에 근접하거나 넘은 경우는 거의 모두 **DAgger 뒤(또는 동시에) student RL(PPO/GRPO)** 을 붙였거나(DoorMan, PRISM, ULTRA, SLIM), 물체 위치를 명시 입력으로 넣었다(Lin et al., DemoHLM). 순수 DAgger만 쓴 곳은 teacher 대비 손실이 크다(VBC 긴 상자 0.93 → 0.42, ULTRA 추종 97.6 % → 67.3 %).

### Cited Findings

#### 1-0. 요약표

| short_id | 제목 | 학회/연도 | arXiv | 코드 | 라이선스 | 유사도 | 내려받은 경로 |
|---|---|---|---|---|---|---|---|
| vbc | Visual Whole-Body Control for Legged Loco-Manipulation | CoRL 2024 (Oral) | [2403.16967](https://arxiv.org/abs/2403.16967) | [Ericonaldo/visual_wholebody](https://github.com/Ericonaldo/visual_wholebody) | CC BY-NC 4.0 | 5 | reference/vbc/ (paper.pdf, code/; 동봉 isaacgym 사본 843 MB는 삭제) |
| viral | VIRAL: Visual Sim-to-Real at Scale for Humanoid Loco-Manipulation | CVPR 2026 포스터 목록에 있음 | [2511.15200](https://arxiv.org/abs/2511.15200) | [NVlabs/GR00T-VisualSim2Real](https://github.com/NVlabs/GR00T-VisualSim2Real) (main) | Apache-2.0 | 5 | reference/viral/ |
| doorman | Opening the Sim-to-Real Door for Humanoid Pixel-to-Action Policy Transfer (DoorMan) | 프리프린트 | [2512.01061](https://arxiv.org/abs/2512.01061) | 같은 저장소 `doorman` 브랜치 (GRPO 코드 없음) | Apache-2.0 | 5 | reference/doorman/ |
| prism | Counterfactual Video Generation Enables Scalable Humanoid Loco-Manipulation (PRISM) | 프리프린트 (2026-09) | [2609.38172](https://arxiv.org/abs/2609.38172) | [amazon-far/PRISM](https://github.com/amazon-far/PRISM) | Apache-2.0 | 5 | reference/prism/ |
| ultra | ULTRA: Unified Multimodal Control for Autonomous Humanoid Whole-Body Loco-Manipulation | IROS 2026 | [2603.03279](https://arxiv.org/abs/2603.03279) | [Sirui-Xu/ULTRA](https://github.com/Sirui-Xu/ULTRA) | Apache-2.0 (+InterMimic) | 4 | reference/ultra/ |
| visualmimic | VisualMimic: Visual Humanoid Loco-Manipulation via Motion Tracking and Generation | 프리프린트 | [2509.20322](https://arxiv.org/abs/2509.20322) | [visualmimic/VisualMimic](https://github.com/visualmimic/VisualMimic) (sim2sim·체크포인트만) | 표기 없음 | 4 | reference/visualmimic/ (다른 조사자가 이미 받음) |
| viloman | ViLoMan: Visual-Proprioceptive Whole-Body Loco-Manipulation for Humanoids | 프리프린트 (2026-09) | [2609.19340](https://arxiv.org/abs/2609.19340) | 없음 | – | 4 | reference/viloman/ (논문만) |
| dexhumanoid_recipe | Sim-to-Real RL for Vision-Based Dexterous Manipulation on Humanoids (Lin et al.) | CoRL 2025 | [2502.20396](https://arxiv.org/abs/2502.20396) | 공개 링크 없음 | – | 3 | reference/dexhumanoid_recipe/ (논문만) |
| demohlm | DemoHLM: From One Demonstration to Generalizable Humanoid Loco-Manipulation | RSS 2026 | [2510.11258](https://arxiv.org/abs/2510.11258) | [BeingBeyond/DemoHLM](https://github.com/BeingBeyond/DemoHLM) (README·docs만) | 표기 없음 | 3 | reference/demohlm/ (다른 조사자가 이미 받음) |
| nowyouseethat | Now You See That: Learning End-to-End Humanoid Locomotion from Raw Pixels | 프리프린트 | [2602.06382](https://arxiv.org/abs/2602.06382) | [Hellod035/Now_You_See_That](https://github.com/Hellod035/Now_You_See_That) (README만) | 표기 없음 | 3 | reference/nowyouseethat/ (논문만) |
| dextrah_g | DextrAH-G: Pixels-to-Action Dexterous Arm-Hand Grasping with Geometric Fabrics | arXiv (학회 표기 확인 못함) | [2407.02274](https://arxiv.org/abs/2407.02274) | [NVlabs/DEXTRAH](https://github.com/NVlabs/DEXTRAH) (Isaac Lab) | NVIDIA License | 3 | reference/dextrah_g/ |
| dextrah_rgb | DextrAH-RGB: Visuomotor Policies to Grasp Anything with Dexterous Hands | 프리프린트 | [2412.01791](https://arxiv.org/abs/2412.01791) | DEXTRAH 저장소에 stereo 증류 코드 포함 | NVIDIA License | 3 | reference/dextrah_rgb/ (논문만) |
| slim | SLIM: Sim-to-Real Legged Instructive Manipulation via Long-Horizon Visuomotor Learning | 프리프린트 | [2501.09905](https://arxiv.org/abs/2501.09905) | 없음 | – | 3 | reference/slim/ (논문만) |
| student_informed_teacher | Student-Informed Teacher Training (SITT) | ICLR 2025 | [2412.09149](https://arxiv.org/abs/2412.09149) | 없음 (프로젝트 페이지만) | – | 3 | reference/student_informed_teacher/ (논문만) |
| robot_parkour | Robot Parkour Learning | CoRL 2023 (Oral) | [2309.05665](https://arxiv.org/abs/2309.05665) | [ZiwenZhuang/parkour](https://github.com/ZiwenZhuang/parkour) | MIT | 2 | 링크만 |
| extreme_parkour | Extreme Parkour with Legged Robots | ICRA 2024 (저자 저장소 표기) | [2309.14341](https://arxiv.org/abs/2309.14341) | [chengxuxin/extreme-parkour](https://github.com/chengxuxin/extreme-parkour) | CC BY-NC 4.0 | 2 | 링크만 |
| hora | In-Hand Object Rotation via Rapid Motor Adaptation | CoRL 2022 | [2210.04887](https://arxiv.org/abs/2210.04887) | [HaozhiQi/hora](https://github.com/HaozhiQi/hora) | MIT 문안 | 2 | 링크만 |
| visual_dexterity | Visual Dexterity | Science Robotics 2023 | [2211.11744](https://arxiv.org/abs/2211.11744) | [Improbable-AI/dexenv](https://github.com/Improbable-AI/dexenv) | MIT | 2 | 링크만 |
| torque_align | Simple Torque-Observation Alignment for Zero-Shot Sim-to-Real Grasping | 프리프린트 (2026-09) | [2609.29031](https://arxiv.org/abs/2609.29031) | 없음 | – | 3 (접촉 격차 기법만) | 링크만 |
| videomimic | VideoMimic (Visual Imitation Enables Contextual Humanoid Control) | arXiv | [2505.03729](https://arxiv.org/abs/2505.03729) | [hongsukchoi/VideoMimic](https://github.com/hongsukchoi/VideoMimic) | MIT | 2 | 링크만 |
| vml | Visual Manipulation with Legs | 프리프린트 | [2410.11345](https://arxiv.org/abs/2410.11345) | 없음 | – | 2 | 링크만 |
| hdmi | HDMI: Learning Interactive Humanoid Whole-Body Control from Human Videos | 프리프린트 | [2509.16757](https://arxiv.org/abs/2509.16757) | [LeCAR-Lab/HDMI](https://github.com/LeCAR-Lab/HDMI) | 표기 없음 | 1 (시각 없음) | reference/hdmi/ (다른 조사자) |
| helpful_doggybot | Helpful DoggyBot | 프리프린트 | [2410.00231](https://arxiv.org/abs/2410.00231) | 없음 | – | 1 | 링크만 |
| umi_on_legs | UMI on Legs | 프리프린트 표기 | [2407.10353](https://arxiv.org/abs/2407.10353) | [real-stanford/umi-on-legs](https://github.com/real-stanford/umi-on-legs) | MIT | 1 | 링크만 |
| pedipulate | Pedipulate | 프리프린트 표기 | [2402.10837](https://arxiv.org/abs/2402.10837) | 확인 못함 | – | 1 | 링크만 |
| roboduet | RoboDuet | letter 형식(학술지명 확인 못함) | [2403.17367](https://arxiv.org/abs/2403.17367) | 프로젝트 페이지에 공개 언급 | – | 1 | 링크만 |
| hitter | HITTER (휴머노이드 탁구) | 프리프린트 | [2508.21043](https://arxiv.org/abs/2508.21043) | – | – | 1 | 링크만 |
| asmp | Learning to See Physical Properties with Active Sensing Motor Policies | CoRL 2023 | [2311.01405](https://arxiv.org/abs/2311.01405) | – | – | 1 | 링크만 |

코드 크기(GitHub API `size`, KB): visual_wholebody 400,693, GR00T-VisualSim2Real 3,512, PRISM 8,540, ULTRA 84,030, VisualMimic 159,802, DEXTRAH 5,673, extreme-parkour 35,574, parkour 114,443, Now_You_See_That 192,767, HDMI 64,571 — [GitHub API](https://api.github.com/repos/Ericonaldo/visual_wholebody) 등 저장소별 조회. visual_wholebody는 얕은 클론 실제 용량이 1.7 GB(동봉 `third_party/isaacgym` 843 MB, `high-level/data` 428 MB)여서 isaacgym 사본만 지웠다(로컬 확인). 이번에 받은 합계 약 1.4 GB.

#### 1-1. VBC — Visual Whole-Body Control (유사도 5)
- 로봇·과제: Unitree B1 + Z1 팔(19 DoF), D435 두 대(머리·그리퍼 근처), 상위 정책은 Jetson Orin, 물체 집기를 바닥·0.3 m 상자·책상 높이에서 평가 — [arXiv html](https://arxiv.org/html/2403.16967v5)
- 하위: 말단 위치·자세(6) + 전진·yaw 속도 명령을 받아 다리 12 관절 출력, 팔은 IK — [arXiv html](https://arxiv.org/html/2403.16967v5)
- teacher 관측: PointNet++ 물체 형상 잠재 1024 + 팔 기준 물체 자세 6 + 고유감각 53 + 기저 속도 3 + 이전 행동; 행동 9(그리퍼 자세 증분 6, 기저 속도 2, 그리퍼 개폐 1) — [arXiv html](https://arxiv.org/html/2403.16967v5)
- student: 물체 분할 마스크 + 분할된 깊이, 4 시점 쌓기, 2층 CNN(커널 5, 3) → 64 잠재 + MLP; DAgger, MSE — [arXiv html](https://arxiv.org/html/2403.16967v5). 코드상 깊이 인코더는 `DepthOnlyFCBackbone54x96`(54×96), 카메라별 마스크+깊이 3 프레임 쌓기, 선택형 보조 출력 `pred_success`(현재 들렸는지 `lifted_now`를 MSE로 예측), 처음 20 % 스텝은 teacher 행동으로 진행(`teacher_pretrain`) — 로컬 코드 `reference/vbc/code/high-level/learning/dagger.py`, `dagger_trainer.py`, `train_multistate_asym.py`
- 깊이 sim2real: 최소 0.2 m 자르기 후 정규화, RandomErasing·GaussianBlur·GaussianNoise·RandomRotation, 카메라 위치·회전 소폭 무작위, 실측 기반 카메라 지연 무작위, 실기 구멍 메우기, 1 스텝 행동 지연, 상위 주기 무작위(하위 6–8 회당 1 회, 약 6.25–8.33 Hz) — [arXiv html](https://arxiv.org/html/2403.16967v5)
- 수치(시뮬 성공률 teacher → student): 공 0.89 → 0.67, 긴 상자 0.93 → 0.42, 정육면체 상자 약 0.82 → 0.74, 병 0.76 → 0.55, 컵 0.89 → 0.74, 그릇 0.78 → 0.52, 드릴 0.84 → 0.47; 계층 없는 기준선 0.0. 실기는 그림으로만 제시 — [arXiv html](https://arxiv.org/html/2403.16967v5)
- 학습 규모: Isaac Gym, teacher 10,240 env 약 36 h(RTX 4090), student 240 env 약 48 h — [arXiv html](https://arxiv.org/html/2403.16967v5)
- 빌릴 것: 받침 높이 0/0.3 m 구성이 우리와 같음, "들렸는가" 보조 헤드와 상위 주기 무작위화·1 스텝 지연.

#### 1-2. VIRAL (유사도 5)
- 로봇: G1 29 DoF + 3손가락 손, D435i; teacher는 사전학습 HOMIE WBC 위에서 **증분(delta) 명령**(기저 x/y/yaw 속도, 팔 관절, 손가락)을 누적해 WBC 명령으로 사용, 절대 행동은 높은 성공률에 못 미침 — [arXiv html](https://arxiv.org/html/2511.15200v1)
- teacher 관측: 전체 고유감각(기저 속도, 중력, 이전 행동, 관절, **손가락 끝 힘**) + 단계·목표·물체·테이블 변환; 원격조종 시뮬 시연 200 개로 단계 리셋, 없으면 성공 10 % 미만, 있으면 약 95 %; 16 GPU PPO — [arXiv html](https://arxiv.org/html/2511.15200v1)
- student: RGB 108×192 한 장 + 실로봇 고유감각(스텝당 113, 손가락 제외), 논문 본문은 DINOv3 128 차원 인코더라 적음; 단일 스텝 MLP < 이력 모델(피드포워드 이력, LSTM), 긴 창이 더 낫다 — [arXiv html](https://arxiv.org/html/2511.15200v1). 공개 코드 설정은 `resnet18` ImageNet 사전학습·학습 가능, `camera_resolutions: [108, 192]`, `ratio_teacher_rollout: 0.5`, 1024 env — 로컬 `reference/viral/code/gr00t/rl/config/exp/loco_manip/wsdpt_student_for_teacher_v8q8.002_resnet_rgb_delay.yaml`
- 증류: 온라인 DAgger + BC 혼합, α = 0.5(env 절반은 teacher 행동으로 진행), 순수 BC(α = 1)는 Isaac→MuJoCo·실기에서 취약 — [arXiv html](https://arxiv.org/html/2511.15200v1)
- 연산 규모: teacher 1–2 GPU는 목표에 크게 못 미치고 8–16 GPU면 90 % 넘김; student 1–64 GPU, 많을수록 수렴 빠르고 분산 작음 — [arXiv html](https://arxiv.org/html/2511.15200v1)
- 시각 DR: 돔 조명 800–2000, HDR 5종, 재질, 밝기·대비·색조·채도·노이즈·블러, 카메라 외부 파라미터 x·z 약 ±2 cm, y ±5 cm, pitch ±0.1 rad, 카메라 지연; 모든 DR 끄면 35.1 % 하락 — [arXiv html](https://arxiv.org/html/2511.15200v1)
- 실기: 연속 54/59(약 91.5 %), 주기 20.2 s; 숙련 원격조종 100 %·21.4 s — [arXiv html](https://arxiv.org/html/2511.15200v1)
- 코드에 손 힘 추정기: 추론 도우미에 `left/right_hand_force_estimator`가 `long_history_for_estimator`(긴 고유감각 이력)를 받아 힘을 추정해 actor 입력에 붙이는 ONNX 내보내기 래퍼(`PPOForceEstimatorWrapper`)가 있다 — 로컬 `reference/viral/code/gr00t/rl/utils/inference_helpers.py`(논문 본문에서 이 부품 설명은 찾지 못함)
- 빌릴 것: teacher 증분 행동, 단계 스냅샷 리셋, teacher 롤아웃 비율 0.5, 이력형 student, 그리고 이력 기반 손 힘 추정기.

#### 1-3. DoorMan (유사도 5, 격차 문제에 가장 직접적)
- 로봇: G1 + 3손가락 손 2개, HOMIE 기반, 50 Hz — [arXiv html](https://arxiv.org/html/2512.01061)
- teacher 관측: 루트→문 변환, 양손→손잡이 변환, **손 18 개 몸체의 순 접촉 렌치**, 루트 선속도; 6 단계 보상; 단계 진입 스냅샷 100 개 롤링 버퍼 리셋(10 개면 4000 반복 넘게, 없으면 잡기 단계에서 실패) — [arXiv html](https://arxiv.org/html/2512.01061)
- student: RGB + 고유감각(관절 각·속도, 루트 각속도), ResNet 계열 인코더 미세조정 → 2층 LSTM(512) → MLP(512, 256, 128); DAgger — [arXiv html](https://arxiv.org/html/2512.01061)
- 격차: DAgger student는 50–70 %에서 정체, teacher는 80–90 %; 원인을 "복구 불가능한 관측 격차"(손잡이가 시야 밖)로 설명; **GRPO 미세조정**(이진 성공 + 관절 속도·가속도·행동 변화 벌점, 그룹 정규화 이점, 가치 함수 없음, PPO식 클리핑) 후 하위 과제 80.8–85.8 % — [arXiv html](https://arxiv.org/html/2512.01061)
- 실기 83 %(숙련 원격조종 80 %, 비숙련 60 %); 시각 DR 없으면 시뮬 5–20 %, 단색 무작위 65.8–70 %, 텍스처+돔 조명 80.8–85.8 % — [arXiv html](https://arxiv.org/html/2512.01061)
- 코드: `doorman` 브랜치에 "grpo" 문자열 0 건(로컬 grep), 즉 GRPO 미세조정은 공개 코드에 없음 — 로컬 `reference/doorman/code`
- 빌릴 것: 접촉 렌치를 보는 teacher → 시각 student 격차를 student RL로 메운 실증. 우리 69 % → 90 % 문제와 구조가 같다.

#### 1-4. PRISM (유사도 5, 2026-09 최신, G1 고무 손 박스 집기·운반)
- 로봇·과제: G1 29 DoF 50 Hz, 양손으로 상자·통·공 등 집어 3 m 이상 운반 — [arXiv html](https://arxiv.org/html/2609.38172v1). 코드 메시 목록에 `combined_left_wrist_rubberhand.STL`이 있어 고무 손 G1 사용 — 로컬 `reference/prism/code/scripts/_student.py`
- teacher: 모션 명령 58, 참조 루트·몸체 자세, 관절, **물체 자세·목표 자세·물체 크기·물체 선속도**; actor 175 차원, critic 310 차원; MLP [512, 256, 128]; 8×L40S, 40K 반복; 접촉 보상(말단–목표 거리와 접촉력 지수 커널) — [arXiv html](https://arxiv.org/html/2609.38172v1)
- student: 고유감각 + 조이스틱(상대 x, y, yaw) + 내려놓기 버튼 + 32 차원 깊이 잠재, 깊이 106×60 → 58×87, 작은 CNN, **이력 없음**, critic은 특권 상태 — [arXiv html](https://arxiv.org/html/2609.38172v1)
- 증류: **L = λ·L_PPO + (1−λ)·L_DAgger**, λ를 500 반복마다 0.1씩 0.1 → 0.9로 올린 뒤 마지막 20K 반복 0.9 유지; 28K 반복; 초기 표준편차 0.01; 상자 전용 23K 체크포인트로 actor만 웜스타트 — [arXiv html](https://arxiv.org/html/2609.38172v1)
- 코드상 student 보상에 `offline-contact-guidance`(teacher 롤아웃에서 뽑은 접촉 일정 "contact sidecar"로 손목·팔꿈치·몸통 접촉 유도) 사용 — 로컬 `reference/prism/code/scripts/_student.py`, `rollout.sh`
- 수치: 시뮬 ablation 기준선 22.5 % → 전체 96.25 %(ID)/72.92 %(OOD); 실기 상자 15/15, ID 합계 약 55/60, OOD 약 32/40(합계는 조회 모델 계산); 목 각도 약 10° 어긋나면 분포 밖 깊이 — [arXiv html](https://arxiv.org/html/2609.38172v1)
- 빌릴 것: λ 경사 PPO+DAgger 동시 학습, teacher 접촉 일정을 student 보상으로, 깊이 노이즈 수치(질문 3).

#### 1-5. ULTRA (유사도 4)
- G1, 실기 양손 상자 들기·운반, 여행가방 운반 — [arXiv html](https://arxiv.org/html/2603.03279)
- teacher: 참조 대비 잔차, 상호작용 그래프 SDF, 참조 물체 자세·속도 13, 총 4052 차원; PPO 4096 env — [arXiv html](https://arxiv.org/html/2603.03279)
- student: 고유감각, 목표(물체·루트 변환), 선택형 MoCap 물체 상태, **머리 기준 점구름 64 점**(PointNet → 256 토큰), 고유감각 이력 10 스텝; 2층 transformer(4 헤드) + 64 차원 잠재, 사전분포(마스크된 student 입력) vs 특권 사후분포, 마스크된 모달리티 복원 보조 디코더 — [arXiv html](https://arxiv.org/html/2603.03279)
- 증류: 500 epoch까지 teacher 롤아웃, 1500 epoch까지 선형으로 student 롤아웃 전환; 손실 = 행동 MSE + KL(0.001 → 0.1 코사인) + 잠재 평활 + 마스크 복원 + 지역 목표 예측 + 사전분포 전용 행동 손실; 모달리티 마스크 확률 커리큘럼 — [arXiv html](https://arxiv.org/html/2603.03279)
- **RL 미세조정**: 배포형(사전분포 전용) student에 PPO, env 약 1/4은 증류 갱신 유지, 정책경사 항을 100 epoch에 걸쳐 서서히 켬, 목표 보상은 가시성 마스크로 게이트 — [arXiv html](https://arxiv.org/html/2603.03279)
- 수치: teacher 추종 97.57 % vs student 67.30 %(ID), 증류만 85.03 %, MuJoCo OOD 점구름 5/20 → 9/20, OOD 위치 4/20 → 12/20(미세조정 전후); 실기 자기중심 시각 수직 5/10, 수평 6/10, MoCap 8/10·9/10 — [arXiv html](https://arxiv.org/html/2603.03279)
- 코드: Isaac Gym Preview 4, `scripts/train_finetune.sh`, `ultra/learning/ultra_agent_distill_vae_rl.py` — [GitHub](https://github.com/Sirui-Xu/ULTRA), 로컬 `reference/ultra/code`
- 빌릴 것: 증류 env 일부를 남긴 채 PPO 항을 서서히 켜는 미세조정 일정.

#### 1-6. VisualMimic (유사도 4, 계층이 가장 비슷)
- G1 + D435i; 하위 = 과제 무관 키포인트 추종기(루트 위치 오차 + 머리·양손·양발 오차 6 항), 상위 = 깊이 + 고유감각 → 키포인트 명령; 실기 상자 들기(0.5 kg를 1 m까지), 상자 밀기 약 3.8 kg 등 — [arXiv html](https://arxiv.org/html/2509.20322v2)
- 상위 teacher: 물체 상태 + 고유감각, PPO 3층 MLP; student: 깊이만(RGB 격차 때문에), 시뮬 80×45, CNN + MLP, DAgger; 카메라 방향 ±5° — [arXiv html](https://arxiv.org/html/2509.20322v2)
- 격차 대책: 하위 student 학습 때 키포인트 명령 각 차원에 λ ∼ U(0.5, 1.5) 곱(50 % 상대 잡음) → 상위가 내는 거친 명령에 견딤; 상위 출력을 하위 입력 정규화기의 μ ± 1.64σ로 자름(약 90 % 질량) — [arXiv html](https://arxiv.org/html/2509.20322v2)
- 깊이 증강: 20 % 확률 왼쪽 아래 흰 마스크, 최대 6 개 사각 마스크(각 10 %), 흰/검정/회색, 30×30 픽셀까지, 화면 25 %까지; 실기 공간·시간 필터 — [arXiv html](https://arxiv.org/html/2509.20322v2)
- 수치(시뮬, teacher / student 시각 / student 시각 없음): Lift Box 상자 떨어뜨림률 34 / 30 / 15 %, Push Box 거리 152 / 37 / 2 m, Kick Ball 189 / 135 / 1 m; 실기는 정성 — [arXiv html](https://arxiv.org/html/2509.20322v2)
- 코드: "논문 채택 후 공개", 현재 sim2sim·체크포인트만 — [README](https://github.com/visualmimic/VisualMimic)
- 빌릴 것: 하위 제어기를 명령 잡음에 강하게 만들고 상위 출력을 하위 학습 분포 안으로 자르기(다른 조사자 (c) 주제와 겹침).

#### 1-7. ViLoMan (유사도 4, student 설계가 우리와 가장 가까움)
- G1 문 닫기; teacher = 동결 GMT + 잔차 PPO(상호작용 맥락: 단계, 문 상태, 접촉 목표, 경첩 참조) — [arXiv html](https://arxiv.org/html/2609.19340v1)
- student: 고유감각 808(각속도, 중력, 관절 위치·속도를 이력 오프셋 [0, 1, 2, 3, 4, 8, 12, 16, 20]에서, 이전 행동 8 개) + **깊이 4 프레임 36×64**(최대 2.5 m 정규화, 가우시안 블러 무작위), 잔차 CNN → 32 차원, MLP 512–256–128, 29 관절 직접 출력 — [arXiv html](https://arxiv.org/html/2609.19340v1)
- 증류: 온라인 DAgger, 정규화 행동 MSE, 미니배치 2/3 현재 롤아웃 + 1/3 리플레이(워커당 300,000) — [arXiv html](https://arxiv.org/html/2609.19340v1)
- 수치: teacher 84.91 % vs student 77.55 %; 실기 32/40; BC만 31.89 %, 시각 없음 33.96 %, env 1/4이면 67.17 %, 1/2이면 69.81 %; mjlab 학습 + MuJoCo sim2sim — [arXiv html](https://arxiv.org/html/2609.19340v1)
- 빌릴 것: 성긴 오프셋 고유감각 이력(최근 0.4 s를 9 점으로), 리플레이 1/3 섞기, env 수 축소가 성능을 깎는다는 수치.

#### 1-8. Lin et al. 2025 (dexhumanoid_recipe, 유사도 3)
- Fourier GR1 + 다지 손, 상자 들기(한 손엔 큰 상자, 크기·색·질량·자세 무작위) — [arXiv html](https://arxiv.org/html/2502.20396v2), [PMLR](https://proceedings.mlr.press/v305/lin25c.html)
- teacher(specialist): 비대칭 actor-critic, **actor는 물체 위치 + 관절만**, critic이 관절 속도·손끝 위치·물체 방향·속도·DR 척도 — [arXiv html](https://arxiv.org/html/2502.20396v2)
- student(generalist): 고유감각 + 물체 위치 → MLP, 깊이 → ResNet-18(GroupNorm), diffusion policy; specialist 성공 롤아웃을 시연으로 BC(DAgger 아님); 물체 위치는 SAM2 마스크 중심 + 깊이(5 Hz) — [arXiv html](https://arxiv.org/html/2502.20396v2)
- 수치: 상자 들기 최고 80 %; 실기 들기에서 깊이+위치 10/10 vs **깊이만 0/10** — [arXiv html](https://arxiv.org/html/2502.20396v2)
- 빌릴 것: 성긴 물체 위치를 명시 입력으로(밀집 깊이와 병행), teacher actor에서 접촉·속도 같은 추정 어려운 값을 빼고 critic에만.

#### 1-9. DemoHLM (유사도 3, 다른 조사자 범위와 겹침)
- G1 + 머리 2 자유도 목 + D435; 하위 WBC는 AMO 채택, 입력이 vx, vy, yaw rate, 몸통 높이·roll·pitch·yaw, 상체 관절 목표 — 우리 인터페이스와 거의 같다 — [arXiv html](https://arxiv.org/html/2510.11258v1)
- 상위: 관절·몸통 roll/pitch + FoundationPose 6D 물체 자세, 10 Hz, 합성 데이터 BC(ACT 등), teacher-student 아님; 고무 손 과제 LiftBox 시뮬 98.83 %, 실기 5/5 — [arXiv html](https://arxiv.org/html/2510.11258v1); 학회 RSS 2026 — [RSS 목록](https://roboticsproceedings.org/rss22/p204.html)
- 빌릴 것: 같은 명령 인터페이스에서 상위 정책이 성공한 예, 물체 자세를 명시 추정해 넣는 대안 경로.

#### 1-10. Now You See That (유사도 3, 깊이 노이즈·증류 손실)
- 맞춤 휴머노이드 + Orbbec Gemini 336L, G1 예비 시험; teacher = 높이 스캔 21×33 + GRU; student = 깊이 24×32(30×40에서 크롭), CNN 3층 + GRU — [arXiv html](https://arxiv.org/html/2602.06382)
- 증류: DAgger식, L = 행동 MSE + 0.1·깨끗/증강 특징 일치(denoise) + 0.1·특징 KL→N(0, I) — [arXiv html](https://arxiv.org/html/2602.06382)
- 실기 88/90 — [arXiv html](https://arxiv.org/html/2602.06382). 노이즈 수치는 질문 3.

#### 1-11. DextrAH-G / DextrAH-RGB (유사도 3, 보조 헤드·KL DAgger)
- DextrAH-G: teacher actor는 잡음 섞인 물체 자세 + 로봇 상태, critic만 관절 힘·손끝 접촉력·참 물체 자세; student는 깊이 160×120(0.5–1.5 m) + 로봇 상태, 출력 = 행동 + 물체 위치 3, 손실 = 행동 L2 + 0.1·위치 L2, 온라인 DAgger; 시뮬 student 약 99 %(배치 평균)로 teacher와 같음, 실기 빈 담기 87 % — [arXiv html](https://arxiv.org/html/2407.02274v3)
- DextrAH-RGB: 스테레오 RGB 320×240, ResNet-18 미세조정 + 2층 transformer, LSTM 512, 물체 위치 보조 헤드; 온라인 DAgger에서 **KL 손실이 L2(평균·분산)보다 4 시드 모두 좋음**; teacher 대비 정규화 성능 0.89(스테레오), 0.83(단안), 0.71(ResNet 동결) — [arXiv html](https://arxiv.org/html/2412.01791)
- 빌릴 것: 보이지 않는 상태를 보조 헤드로 예측(우리는 손 접촉력·박스 질량), KL 증류.

#### 1-12. SLIM (유사도 3, 사족+팔, RL형 증류)
- Go1 + WidowX 팔, 손목 D435 RGB(160×90으로 축소), 언어 지시 7 하위 과제; 하위 = 2D 속도 명령 보행 PPO — [arXiv html](https://arxiv.org/html/2501.09905v1)
- 증류: DAgger 아님, SAC 변형(엔트로피 보상 제거, teacher와의 KL 항, 확률 β로 student 롤아웃), 시각 병목에서 분할·깊이 예측 보조 — [arXiv html](https://arxiv.org/html/2501.09905v1)
- 실기 전체 과제: SLIM 78.3 % vs 증류만 50.0 %, 시각 증강 없음 56.6 % — [arXiv html](https://arxiv.org/html/2501.09905v1)

#### 1-13. 파쿠르 계열(증류 기법만, 유사도 2)
- Robot Parkour Learning: 깊이 48×64(D435 240×424에서 왼 60, 오른 46 픽셀 자름), 10 Hz 깊이·50 Hz 정책, 장애물별 전문 teacher가 라벨하는 DAgger, CNN → GRU 256 → MLP; 성공률 teacher → student: 오르기 95 → 86, 도약 82 → 80, 기울기 100 → 73 — [arXiv html](https://arxiv.org/html/2309.05665); CoRL 2023 Oral — [arXiv](https://arxiv.org/abs/2309.05665v2)
- Extreme Parkour: 2 단계(scandot RL → 깊이 DAgger), 58×87, 깊이 약 10 Hz, 방향(yaw)은 student 예측이 oracle과 0.6 이내일 때만 쓰는 teacher–student 혼합(MTS), actor는 1 단계 정책으로 초기화, 3090 한 장 20 h 미만 — [arXiv html](https://arxiv.org/html/2309.14341)

#### 1-14. 그 밖(유사도 1–2, 짧게)
- HORA: teacher가 물체 위치·크기·질량·마찰·무게중심을 8 차원 extrinsics로 압축, student 적응 모듈은 **최근 30 스텝 관절 위치 + 행동**을 1D conv로 받아 extrinsics를 L2 회귀(student 정책으로 모은 데이터) — [arXiv PDF](https://arxiv.org/pdf/2210.04887); CoRL 2022 — [arXiv](https://arxiv.org/abs/2210.04887)
- Visual Dexterity: 깊이 카메라 1 대, 시뮬 RL, 실기 오리 모양 미학습 물체 56 % 떨어뜨림 — [arXiv](https://arxiv.org/abs/2211.11744)
- VideoMimic: 추종 teacher → 높이맵(11×11, 0.1 m)·루트 방향만 보는 student로 DAgger → 같은 관측으로 PPO 미세조정("성능을 크게 올림", 수치 없음) — [arXiv html](https://arxiv.org/html/2505.03729)
- Visual Manipulation with Legs: Go1, 점구름(물체 400 + 배경 400)으로 TD3 직접 학습, 증류 없음 — [arXiv html](https://arxiv.org/html/2410.11345v3)
- HDMI: 실기 물체 자세를 MoCap으로 받음, 시각·teacher-student 없음 — [arXiv html](https://arxiv.org/html/2509.16757v3)
- Helpful DoggyBot: 하위는 깊이로 시뮬 학습, 상위는 VLM — [arXiv](https://arxiv.org/abs/2410.00231). UMI on Legs: 실세계 UMI 시연 정책 + 말단 궤적 추종 WBC, 시각 증류 없음 — [arXiv](https://arxiv.org/abs/2407.10353). Pedipulate: 한 발 위치 목표 추종 RL — [arXiv](https://arxiv.org/abs/2402.10837). RoboDuet: 보행·조작 두 정책 협조 — [arXiv](https://arxiv.org/abs/2403.17367). HITTER: 시각 teacher-student 언급 없음 — [arXiv](https://arxiv.org/abs/2508.21043). ASMP: 시뮬 추정기가 실세계 이미지에 마찰 라벨을 다는 자기지도 — [arXiv](https://arxiv.org/abs/2311.01405)
- 검색 결과로만 본 2026 깊이-student 휴머노이드(본문 미확인): VIGOR(넘어짐, 깊이 + 짧은 고유감각, DAgger식, G1) [arXiv](https://arxiv.org/html/2602.16511), REACT(사람–휴머노이드 상호작용, 깊이 student on-policy DAgger) [arXiv](https://arxiv.org/html/2610.28523)

### Inferences
- 유사도 5 넷(VBC, VIRAL, DoorMan, PRISM) 중 "teacher가 접촉력·물체 상태를 보고, student는 시각만"인 DoorMan이 우리 상황과 가장 닮았고, 거기서 DAgger만으로는 50–70 % 정체 → student RL로 teacher 수준 회복이라는 같은 모양이 나왔다. 우리 69 % vs 90 %도 같은 계열의 "관측 격차" 정체일 가능성이 높다.
- VBC의 긴 상자(0.93 → 0.42)처럼 **큰 물체일수록 격차가 커지는** 경향은 큰 박스(37×40×29 cm)를 다루는 우리에게 불리한 신호다. 큰 물체는 가까이 가면 시야를 채우고 가장자리가 잘린다.
- 휴머노이드 박스 집기에서 깊이 student가 실기 성공을 낸 최근 예(PRISM 15/15, ULTRA 50–60 %)는 둘 다 **증류 뒤 또는 증류와 함께 PPO**를 돌렸다.

### Gaps
- VIRAL 논문 본문(조회 모델 요약)은 DINOv3 인코더라 하고, 공개 코드 설정은 ResNet-18이다. 어느 판이 실기 결과에 쓰였는지 확인 못함.
- VIRAL 코드의 손 힘 추정기(`hand_force_estimator`)가 teacher·student 중 어디에 쓰였는지, 학습 방법은 논문에서 찾지 못함.
- DoorMan의 RGB 해상도, GRPO 그룹 크기·클리핑 값은 논문에 없음.
- PRISM 학회(alphaXiv에 NeurIPS 2026 목록 표기)는 확인 못함. teacher의 평가셋 성공률은 따로 보고 안 됨.
- VBC 실기 높이별 성공률은 그림에만 있어 숫자를 못 뽑음.
- DextrAH-G의 학회(CoRL 2024로 알려져 있으나) 확인 못함. Extreme Parkour의 ICRA 2024는 저자 저장소 표기만 확인.
- 휴머노이드 + 동결 골반 명령 하위 제어기 + 깊이 student + 양손 조여 쥐기로 바닥 박스 집기를 하면서 teacher–student 격차의 원인(접촉 vs 위치)을 분석한 논문은 찾지 못함.

## 질문 2. 접촉력·질량처럼 시각으로 못 보는 특권 정보 때문에 생기는 격차를 줄이는 구체 기법

### Takeaway
보고된 기법은 네 갈래다. (a) DAgger 뒤 또는 함께 **student RL**(GRPO, λ 경사 PPO+DAgger, 증류 env 일부 유지한 PPO), (b) **teacher를 student가 흉내 낼 수 있게** 만들기(teacher actor에서 추정 불가 값을 빼고 critic에만, 또는 student와의 KL을 teacher 보상에 벌점), (c) student에 **접촉 대리 신호**와 긴 이력 + 보조 예측 헤드(손 힘·물체 상태·"들렸는가"), (d) 롤아웃 혼합·리플레이·단계 리셋 같은 데이터 분포 요령. 수치 효과가 가장 큰 건 (a)와 (b)다.

### Cited Findings
- **(a) student RL 미세조정**
  - DoorMan: DAgger student 50–70 % 정체(teacher 80–90 %) → GRPO(이진 성공 + 평활 벌점, 그룹 정규화, 가치 함수 없음) 후 80.8–85.8 %; student가 teacher가 보이지 않은 보상 행동(손잡이를 시야 중앙에 두기)을 배움 — [arXiv html](https://arxiv.org/html/2512.01061)
  - PRISM: λ·L_PPO + (1−λ)·L_DAgger, λ 0.1 → 0.9(500 반복마다 +0.1) — [arXiv html](https://arxiv.org/html/2609.38172v1)
  - ULTRA: 증류 후 PPO, env 약 1/4은 증류 유지, 정책경사 100 epoch에 걸쳐 켬; MuJoCo OOD 위치 4/20 → 12/20 — [arXiv html](https://arxiv.org/html/2603.03279)
  - SLIM: KL-to-teacher를 넣은 SAC가 증류만보다 실기 78.3 % vs 50.0 % — [arXiv html](https://arxiv.org/html/2501.09905v1)
  - VideoMimic: DAgger 뒤 같은 관측으로 PPO 미세조정, 이유는 "참조 조건으로 배운 행동이 참조 없는 정책엔 최적이 아닐 수 있음" — [arXiv html](https://arxiv.org/html/2505.03729)
  - Bootstrapping RL with Imitation(시각 드론): 특권 teacher → IL student → 적응형 RL 미세조정 3 단계, CoRL 2024 — [arXiv](https://arxiv.org/abs/2403.12203)
  - D-PPO(휴머노이드 지각 보행): student가 POMDP에서 RL을 계속해 상한을 올린다고 주장, 수치 없음 — [arXiv](https://arxiv.org/abs/2503.08299); CTS: teacher·student를 PPO로 동시 학습, 2 단계 대비 속도 추종 오차 최대 20 % 감소 — [arXiv](https://arxiv.org/abs/2405.10830)
- **(b) teacher를 흉내 낼 수 있게**
  - SITT: teacher 보상에 proxy student와의 KL 벌점(λ1 = 0.05) + PPO 손실에 KL(λ2 = 0.01) + 특징 정렬; Franka 서랍 열기(시야 가림) BC 0.16, DAgger 0.34, SITT 0.88 — [arXiv html](https://arxiv.org/html/2412.09149v2). 본문 수치(0.77 vs 0.47 vs 0.27)와 표가 다름.
  - Lin et al.: teacher actor는 물체 위치 + 관절만, 속도·방향·DR 척도는 critic 전용 — [arXiv html](https://arxiv.org/html/2502.20396v2)
  - DextrAH-G: teacher actor는 잡음 섞인 물체 자세, 접촉력·관절 힘은 critic 전용 → student가 시뮬에서 teacher와 같은 약 99 % — [arXiv html](https://arxiv.org/html/2407.02274v3)
  - Teacher-Student Representational Alignment: 공유 임베딩이 student에 없는 정보를 숨기도록 대조 학습, RL 미세조정 없이 격차 감소 주장(ICRA 2026 RL4IL 워크숍 구두) — [arXiv](https://arxiv.org/abs/2605.28372)
  - Realizable Students: student가 필요할 때만 teacher에 묻고 복구 상태에서 리셋 — [arXiv](https://arxiv.org/abs/2505.09546)
  - ADVISOR: 특권 teacher를 흉내 내면 student가 특권 정보를 주변화한 정책을 배워 거의 무작위가 될 수 있음을 분석 — [arXiv PDF](https://arxiv.org/pdf/2007.12173) (검색 요약 기준)
  - TGRL: teacher 감독 가중치를 "보상만으로 학습한 가상 에이전트"와 비교해 자동 조절, ICML 2023 — [arXiv](https://arxiv.org/abs/2307.03186)
- **(c) 접촉 대리 신호·이력·보조 헤드**
  - HORA: 30 스텝 관절 위치 + 행동 이력 → 8 차원 extrinsics(질량·크기·마찰·무게중심 압축) L2 회귀 — [arXiv PDF](https://arxiv.org/pdf/2210.04887)
  - VIRAL 코드: 긴 고유감각 이력으로 좌우 손 힘을 추정해 actor 입력에 붙이는 모듈 — 로컬 `reference/viral/code/gr00t/rl/utils/inference_helpers.py`
  - Torque-Observation Alignment: 원시 토크 대신 **Δτ(t) = τ(t) − τ(t−1)** 을 관측으로 써서 sim–real 상수 오프셋 제거, 토크 상수 다이나모 교정, 측정 기반 가우시안 잡음; 관절 위치 + Δτ만으로 고유감각 쥐기 student, 9 물체 100 % — [arXiv](https://arxiv.org/abs/2609.29031)
  - DextrAH-G: 물체 위치 보조 헤드 β = 0.1 — [arXiv html](https://arxiv.org/html/2407.02274v3); VBC: "현재 들렸는가" 보조 출력(`pred_success`) — 로컬 `reference/vbc/code/high-level/learning/dagger.py`
  - ULTRA: 특권 사후분포 vs student 사전분포 KL(0.001 → 0.1) + 마스크 모달리티 복원 — [arXiv html](https://arxiv.org/html/2603.03279)
  - PRISM: teacher 롤아웃 접촉 일정(손목·팔꿈치·몸통)을 student 보상으로 — 로컬 `reference/prism/code/scripts/_student.py`
  - DexGrasp-Zero: teacher는 손가락별 접촉·충격량, student는 최근 5 스텝 LSTM으로 접촉을 운동 잔차에서 암묵 복원 — [arXiv PDF](https://arxiv.org/pdf/2603.16806) (검색 요약 기준)
  - 반례: 관절형 도구 손안 조작에선 표준 DAgger의 부분 정보 student가 "물체를 일찍 떨어뜨려 탐색을 못 해" 안정 oracle 롤아웃 BC로 바꿈(정량 비교 없음) — [arXiv html](https://arxiv.org/html/2509.23075)
- **(d) 분포 요령**
  - VIRAL: teacher 롤아웃 비율 0.5, 순수 BC는 취약 — [arXiv html](https://arxiv.org/html/2511.15200v1); ViLoMan: 리플레이 1/3, BC만 31.89 % vs DAgger 77.55 % — [arXiv html](https://arxiv.org/html/2609.19340v1); ULTRA: teacher → student 롤아웃 선형 전환(500 → 1500 epoch) — [arXiv html](https://arxiv.org/html/2603.03279); Extreme Parkour: 예측과 oracle이 가까울 때만 student 값을 쓰는 혼합 — [arXiv html](https://arxiv.org/html/2309.14341)
  - DextrAH-RGB: KL 증류가 L2보다 좋음 — [arXiv html](https://arxiv.org/html/2412.01791)
  - 이력: VIRAL은 이력 모델이 단일 스텝보다 좋고 긴 창이 더 좋다 — [arXiv html](https://arxiv.org/html/2511.15200v1); PRISM은 이력 없이도 실기 15/15 — [arXiv html](https://arxiv.org/html/2609.38172v1)

### Inferences
- 우리 teacher가 손–박스 접촉력을 **actor** 관측으로 쓰고 있다면, DoorMan과 같은 "흉내 불가" 구조다. 가장 싼 첫 실험은 DextrAH-G·Lin et al.처럼 접촉력·질량을 critic 전용으로 옮겨 teacher를 다시 학습하고, 그 teacher의 성공률이 얼마나 떨어지는지 보는 것이다. 많이 안 떨어지면 student 격차의 상당 부분이 사라질 수 있다.
- K1 고무 공 손은 손가락이 없어 접촉이 팔 관절 토크·PD 추종 오차로 거의 다 드러난다(조여 쥐기). 그래서 HORA식 이력 회귀나 VIRAL 코드의 손 힘 추정기처럼 "고유감각 이력 → 손별 접촉력" 보조 헤드가 다지 손 연구보다 우리에게 더 잘 맞을 것으로 본다. Δτ 관측(torque_align)은 DYNAMIXEL-Q 전류로 같은 신호를 실기에서 얻을 수 있는지 확인이 먼저다.
- RL 미세조정 형태는 PRISM의 λ 경사 혼합이 가장 단순하다(기존 DAgger 학습기에 PPO 항만 더함). GRPO는 가치 함수가 없어 비대칭 critic이 필요 없지만, 공개 구현이 없다(DoorMan 코드에 없음).
- 우리 6 프레임 26×64 + 고유감각 구조는 ViLoMan(4 프레임 36×64 + 성긴 이력 9 점)·VBC(3–4 프레임 54×96)와 같은 급이라, 해상도·프레임 수를 늘리는 쪽보다 위의 (a)–(c)가 효과가 클 것으로 본다.

### Gaps
- "teacher actor에서 접촉력 제거" 전후의 student 격차를 같은 과제에서 정량 비교한 휴머노이드 논문은 찾지 못함.
- 손 접촉력 보조 헤드가 student 성공률을 얼마나 올리는지 정량 ablation은 찾지 못함(VIRAL 코드 존재만 확인).
- GRPO vs PPO 미세조정을 같은 시각 student에서 비교한 결과는 찾지 못함.
- GPO(Guided Policy Optimization, [arXiv](https://arxiv.org/html/2505.15418v2))는 검색 요약만 봤고 로봇 실험 여부는 확인 못함.

## 질문 3. 깊이 sim2real: 노이즈·구멍 모델, 지연, 카메라 외부 파라미터 무작위화, 크롭 — 보고된 숫자

### Takeaway
보고 수치는 대체로 다음 범위다. 깊이 잡음 표준편차 약 0.03 m(또는 깊이 제곱 비례 계수 ±0.03), 구멍 확률 0.2 또는 스테레오 일관성 기반 구멍, 깊이 오프셋 0.03 m, 카메라 위치 ±1–5 cm·각도 ±5° 또는 ±0.1 rad, 지연 2–4 프레임(또는 0.08 s 고정, 0.2–0.26 s 무작위), 해상도 24×32에서 58×87 사이, 가장자리 몇 픽셀 크롭. 실기 쪽은 RealSense 공간·시간 필터와 구멍 메우기를 쓰는 곳이 많다.

### Cited Findings

| 연구 | 해상도·크롭 | 잡음·구멍 | 지연 | 카메라 무작위 | 출처 |
|---|---|---|---|---|---|
| PRISM | 106×60 → 위 2·좌우 4 px 크롭 → 58×87, 0.3–3.0 m, 30 Hz | 구멍 확률 0.2, 가산 잡음 0.03 m, 깊이 오프셋 0.03 m, 가장자리 잡음, 드롭아웃 | 3–4 프레임(버퍼 6) | 카메라 자세 무작위, 공칭 pitch 37°(코드 마운트 쿼터니언) | [arXiv html](https://arxiv.org/html/2609.38172v1), 로컬 `prism/code/scripts/_student.py` |
| Now You See That | 30×40 → 24×32, 0.3–2.0 m, 위아래 3·좌우 4 px | 스테레오 일관성 τ ∈ [0.05, 0.20] 불일치 → 0, 깊이 제곱 비례 가우시안 계수 U(−0.03, 0.03), Perlin 5 옥타브 U(−0.02, 0.02), 무작위 3×3 conv U(−0.05, 0.05), 척도 U(0.9, 1.1), 픽셀 0/최대 실패 각 0.001 | 2–4 프레임 | 내부 파라미터 척도 U(0.9, 1.1), 위치 ±0.05 m, 각도 ±0.10 rad | [arXiv html](https://arxiv.org/html/2602.06382) |
| Robot Parkour | 240×424 → 좌 60·우 46 px → 48×64, 깊이 10 Hz | 자르기, 픽셀 가우시안, 무작위 인공물(크기 미기재); 실기 구멍 메우기 + 공간·시간 필터 | 0.2–0.26 s 무작위(고유감각 0.0375–0.0475 s) | x 0.27 ± 0.01 m, y 0.0075 ± 0.0025, z 0.033 ± 0.0005, pitch U[0, 5]°, FOV U[85, 88]° | [arXiv html](https://arxiv.org/html/2309.05665) |
| Extreme Parkour | 죽은 픽셀 왼쪽 크롭 → 58×87, 약 10 Hz | (미기재) | 깊이 0.08 s로 고정(빠르면 기다림), 고유감각 0.016 s | (미기재) | [arXiv html](https://arxiv.org/html/2309.14341) |
| VBC | 54×96(코드), 분할 깊이 + 마스크 | 최소 0.2 m 자르기(코드: 하한 무작위 0.18–0.25 m), RandomErasing·Blur·Noise·Rotation | 실측 기반 카메라 지연 무작위, 1 스텝 행동 지연, 상위 6.25–8.33 Hz | 위치·회전 소폭 | [arXiv html](https://arxiv.org/html/2403.16967v5), 로컬 `vbc/code/high-level/envs/b1z1_base.py` |
| VisualMimic | 80×45 | 사각 마스크(흰/검/회색, 30×30까지, 6 개까지, 화면 25 %까지), 고정 왼쪽 아래 마스크 20 %; 실기 공간·시간 필터 | 미보고 | 방향 ±5° | [arXiv html](https://arxiv.org/html/2509.20322v2) |
| ViLoMan | 36×64, 4 프레임, 2.5 m 정규화 | 가우시안 블러 무작위 | 미보고 | G1 머리 카메라 시점 맞춤만 | [arXiv html](https://arxiv.org/html/2609.19340v1) |
| ULTRA(점구름) | 64 점, 전방 ROI·지면 제거·주 클러스터 | 가우시안 0.02 m, 점 드롭 15 %, 이상점 5 %, 가림 10 % | 미보고 | 회전 0.05 rad, 위치 0.02 m | [arXiv html](https://arxiv.org/html/2603.03279) |
| DextrAH-G | 160×120, 0.5–1.5 m | 픽셀 드롭·균일 무작위 각 0.003125, 막대 인공물 p 0.00025(길이 18, 폭 3 px까지), 상관 잡음 σ_s 0.5·σ_d 1/6, 법선 기반 잡음 σ_θ 0.01 | – | – | [arXiv html](https://arxiv.org/html/2407.02274v3), 로컬 `dextrah_g/code/dextrah_lab/tasks/dextrah_kuka_allegro/dextrah_kuka_allegro_env_cfg.py` |
| Lin et al. | 미기재 | 물체 위치 잡음 0.02, 관절 관측 N(0, 0.4), 행동 N(0, 0.1) | 프레임·행동 지연 확률 각 0.1 | 카메라 위치 잡음 0.005(단위 cm 표기), 회전 5°, FOV 5° | [arXiv html](https://arxiv.org/html/2502.20396v2) |
| VIRAL(RGB) | 108×192 | 영상 품질 무작위 | 카메라 지연(코드 `rgb_image_delay_step` 2–3) | x·z 약 ±2 cm, y ±5 cm, pitch ±0.1 rad | [arXiv html](https://arxiv.org/html/2511.15200v1), 로컬 `viral/code` 설정 |

- Now You See That은 실기 깊이 2 시간(약 200,000 장)으로 CycleGAN을 학습해 평가에만 썼고, sim→real FID 67.2 → 23.4 — [arXiv html](https://arxiv.org/html/2602.06382)
- PRISM 실기는 머리 D435i 스테레오(30 Hz)를 외부 PC의 Fast-FoundationStereo로 깊이화, 목을 손으로 약 10° 올렸고 목 각도가 어긋나면 분포 밖 깊이가 된다고 보고 — [arXiv html](https://arxiv.org/html/2609.38172v1)
- VIRAL: 시각 DR을 모두 끄면 35.1 % 하락, 하나만 빼도 손해 — [arXiv html](https://arxiv.org/html/2511.15200v1)

### Inferences
- PRISM의 "목 각도 약 10° 어긋남 → 분포 밖"은 우리 K1 목이 손으로 두 위치(정면 0°/아래 47°)만 고정되는 조건과 직결된다. 카메라 pitch 무작위 폭을 실측 오차(우리 기록의 장착 오차) 이상으로 잡아야 한다.
- 지연은 파쿠르 계열(0.08–0.26 s)보다 휴머노이드 최신 연구(2–4 프레임)가 짧다. 우리 실측 D436 프레임 나이(메모: 14–45 ms)와 50 Hz 정책이면 1–3 스텝 무작위가 같은 급이다.
- 26×64 크롭은 위 표의 하단(24×32)과 상단(58×87) 사이라 해상도 자체가 이상한 값은 아니다.
- 잡음 모형은 표현(픽셀 깊이 vs 점구름 vs 높이 칸)에 따라 다시 재야 한다는 우리 기존 교훈과 같이, 위 수치는 출발점일 뿐 실기 bag으로 재확인이 필요하다.

### Gaps
- PRISM "지연 3–4 프레임"의 단위(30 Hz 카메라 프레임인지 50 Hz 정책 스텝인지) 확인 못함.
- Robot Parkour·VBC의 잡음 크기·인공물 비율은 논문에 수치가 없음(코드에는 있을 수 있음, 이번엔 확인 안 함).
- D436(D435 계열 스테레오) 전용 구멍·가장자리 잡음 실측 모형을 공개한 연구는 찾지 못함.

## 질문 4. 공개 코드(Isaac Lab / Isaac Gym / legged_gym / mjlab), student 학습 코드 포함 여부

### Takeaway
student 학습 코드까지 공개된 것은 VIRAL(Isaac Lab, Apache-2.0), PRISM(holosoma 기반, Apache-2.0, `train_student.sh`), ULTRA(Isaac Gym, Apache-2.0, 미세조정 스크립트 포함), VBC(Isaac Gym, CC BY-NC 4.0), DEXTRAH(Isaac Lab, NVIDIA License), 파쿠르 두 개(legged_gym)다. 우리처럼 Isaac Lab에서 바로 참고할 만한 건 VIRAL과 DEXTRAH, 박스·고무 손·깊이 student 조합은 PRISM, 증류 후 RL 미세조정 일정은 ULTRA·PRISM 코드다.

### Cited Findings
- VIRAL/DoorMan: Isaac Lab(Isaac Sim 5.1) + TRL 기반, teacher PPO·student DAgger·평가·ONNX 내보내기 포함; `doorman` 브랜치 별도 — [README](https://github.com/NVlabs/GR00T-VisualSim2Real), Apache-2.0 — [GitHub API](https://api.github.com/repos/NVlabs/GR00T-VisualSim2Real). DoorMan GRPO 코드는 브랜치에 없음(로컬 grep 0 건).
- PRISM: `main` = teacher 학습·롤아웃·student 증류, `sim2real` = Fast-FoundationStereo 실기 배포; teacher 학습 데이터는 "검토 중"이라 teacher bank는 직접 준비해야 함 — [README](https://github.com/amazon-far/PRISM); Apache-2.0 — [GitHub API](https://api.github.com/repos/amazon-far/PRISM)
- ULTRA: Isaac Gym Preview 4 + MuJoCo sim2sim, `train_teacher.sh`, `train_student.sh`, `train_finetune.sh`, OMOMO 기반 데이터 링크 — [README](https://github.com/Sirui-Xu/ULTRA); Apache-2.0 — [GitHub API](https://api.github.com/repos/Sirui-Xu/ULTRA)
- VBC: `low-level`(legged_gym) + `high-level`(Isaac Gym, skrl 기반 DAgger) — 로컬 `reference/vbc/code`; CC BY-NC 4.0 — [LICENCE](https://github.com/Ericonaldo/visual_wholebody)
- DEXTRAH: Isaac Lab v2.2.1, 특권 FGP teacher → 카메라 입력으로 바꾸는 온라인 증류, 깊이 증강 모듈 `depth_augs.py`, 스테레오 transformer 증류 — [README](https://github.com/NVlabs/DEXTRAH), 로컬 `reference/dextrah_g/code/dextrah_lab/distillation/`
- VisualMimic: sim2sim·체크포인트만, 하위·상위 학습 코드 미공개 — [README](https://github.com/visualmimic/VisualMimic)
- Robot Parkour: MIT — [GitHub API](https://api.github.com/repos/ZiwenZhuang/parkour); Extreme Parkour: legged_gym + rsl_rl, CC BY-NC 4.0 — [GitHub](https://github.com/chengxuxin/extreme-parkour)
- ViLoMan은 mjlab으로 학습했다고 하나 코드 링크 없음 — [arXiv html](https://arxiv.org/html/2609.19340v1)
- 코드 없음 또는 README만: DemoHLM, Now You See That, Lin et al., SLIM, SITT, DoorMan GRPO — [DemoHLM](https://github.com/BeingBeyond/DemoHLM), [Now_You_See_That](https://github.com/Hellod035/Now_You_See_That), [recipe 페이지](https://toruowo.github.io/recipe/)

### Inferences
- 우리 Isaac Lab + Newton 환경에 이식할 때 가장 손이 덜 가는 건 알고리즘 부품 단위 차용이다: PRISM의 λ 경사 PPO+DAgger 손실과 접촉 유도 보상, VIRAL의 teacher 롤아웃 비율·손 힘 추정기, DEXTRAH의 깊이 증강 함수. 환경 전체 이식은 시뮬레이터(Isaac Gym, holosoma)가 달라 이득이 적다.
- 라이선스상 VBC·Extreme Parkour(CC BY-NC)와 DEXTRAH(NVIDIA License)는 상업 사용 제약이 있으니 아이디어 참고에 그치고, 코드 복사는 Apache-2.0(VIRAL, PRISM, ULTRA)·MIT(Robot Parkour) 쪽에서 하는 것이 안전하다.

### Gaps
- NVIDIA License(DEXTRAH) 조항의 상업 사용 범위는 본문을 끝까지 읽지 않았음.
- PRISM이 내부적으로 Isaac Sim/Isaac Lab 중 무엇을 쓰는지(holosoma 백엔드) 코드에서 확인하지 않았음.
- RoboDuet 저장소(GuoPingPan/RoboDuet, 별 1 개)가 공식인지 확인 못함. UMI on Legs·Pedipulate·RoboDuet·VideoMimic의 학회 표기는 arXiv 페이지에서 찾지 못함.
- 내려받은 코드는 읽기만 했고 실행·설치·import는 하지 않음.
