# LLM 에이전트의 인간 사회적 행동 재현 연구

**주제**: LLM 에이전트가 인간의 사회적 행동 패턴을 재현할 수 있는가?

**연구자**: 종식 정 (@trident86)  
**수집일**: 2026-03-29  
**논문 수**: 20편+  

## 📁 파일 구조

```
research/llm-social-behavior-simulation/
├── 1. 논문 리스트 (20편).md           # 기본 논문 리스트 (피인용수 기준)
├── 2. 종합 분석.md                    # 포괄적 분석 (분야 현황)
├── 3. 확장 리스트.md                  # 30+ 논문 확장, 학습 로드맵
├── 4. 상세분석 (1-4번).md             # 심화: Generative Agents, Survey, Reflexion, CSS
├── 5. 상세분석 (5-8번).md             # 심화: Strategic Deception, ToM, Digital Twins, GroupChat
└── README.md                          # 이 파일
```

## 🎯 핵심 논문 TOP 5

### 1. Generative Agents (1,200 인용)
- **문제**: Believable 에이전트 행동 생성
- **해법**: Memory + Reflection + Planning
- **결과**: Emergent 행동 시연

### 2. AgentSociety (10K+ 에이전트)
- **문제**: 대규모 사회 시뮬레이션
- **결과**: 500만 상호작용, 편극화/정책 효과 검증

### 3. Stanford Digital Twins (1,052명)
- **문제**: 개인 수준 정확도 검증
- **결과**: GSS 85%, 성격 80%, 경제 게임 66%

### 4. Strategic Deception
- **경고**: LLM이 기만할 수 있다 (안전 주의)

### 5. How FaR (Theory of Mind)
- **문제**: 추론 vs 행동의 갭
- **개선**: FaR 프롬팅으로 50% → 71%

## 📊 연구 흐름

```
2023년 (기초)
├─ Generative Agents (기본 아키텍처)
├─ Reflexion (자기 개선)
└─ CSS 활용

2024년 (확장)
├─ Stanford Twins (개인 1,052명)
├─ AgentGroupChat (그룹 토론)
└─ ABM + GenAI 통합

2025년 (정책)
├─ AgentSociety (10K+)
└─ 정책 평가 & 반사실 분석
```

## 🎯 종식의 관심사와의 연결

### 다중 에이전트 사회 시뮬레이션
- ✅ **기초**: Generative Agents 아키텍처
- ✅ **확장**: AgentSociety (10K+ 에이전트)
- ✅ **검증**: Stanford Twins (개인 수준 정확도)

### 디지털 트윈 사회
- ✅ **개인**: 1,052명 85% 정확도
- ✅ **그룹**: 토론의 emergent 동역학
- ✅ **정책**: 반사실 분석 & 평가

## 📈 성과 통계

| 측정 항목 | 달성도 | 출처 |
|---------|--------|------|
| GSS 정확도 | 85% | Stanford |
| 성격 특성 | 80% | Stanford |
| 경제 게임 | 66% | Stanford |
| 사회 실험 복제 | 80% | Stanford |
| 에이전트 규모 | 10K+ | AgentSociety |
| 상호작용 | 5M+ | AgentSociety |

## 🔗 arXiv 링크

### TOP 5
1. [Generative Agents](https://arxiv.org/abs/2304.03442) - 1,200 인용
2. [LLM Multi-Agent Survey](https://arxiv.org/abs/2402.01680) - 420 인용
3. [Reflexion](https://arxiv.org/abs/2303.11366) - 580 인용
4. [AgentSociety](https://arxiv.org/abs/2502.08691) - 85 인용
5. [Stanford Digital Twins](https://arxiv.org/abs/2411.10109) - 145 인용

### 전체 20편 논문
각 문서의 "논문 리스트"에 모든 arXiv 링크 포함

## 💡 주요 발견

### 성공 사례
✅ LLM 에이전트는 **85% 정확도**로 인간 행동 복제 가능  
✅ **10K+ 에이전트** 대규모 사회 시뮬레이션 가능  
✅ 그룹 토론의 **emergent 합의** 모델링 가능  

### 주의사항
⚠️ 에이전트가 **기만**할 수 있음 (안전 검증 필수)  
⚠️ **추론** 능력 ≠ **행동** 능력 (둘 다 필요)  
⚠️ 장기 **일관성** 및 **프라이버시** 문제  

## 🚀 향후 분석 계획

- [ ] 9-12번 논문 상세분석
- [ ] 13-16번 논문 상세분석
- [ ] 17-20번 논문 상세분석
- [ ] 전체 통합 분석 및 비교표
- [ ] 종식을 위한 최종 권고사항

## 📌 사용 가이드

### 빠른 시작 (1시간)
1. "1. 논문 리스트"로 전체 20편 개요 파악
2. "2. 종합 분석"으로 분야 현황 이해

### 심화 학습 (1주)
1. "3. 확장 리스트"의 Phase별 로드맵 따라가기
2. "4. 상세분석 (1-4번)" 읽기
3. "5. 상세분석 (5-8번)" 읽기

### 심층 연구 (2주+)
- 각 논문의 arXiv 링크에서 원본 논문 읽기
- GitHub 리포지토리 확인
- 실제 구현 코드 탐색

## 📝 문서 작성자

**Jerry** (@종식의 AI 어시스턴트)  
작성일: 2026-03-29  
최종 업데이트: 진행 중

---

**상태**: 8/20 논문 상세분석 완료 (40%)  
**다음**: 9-12번 논문 분석 예정
