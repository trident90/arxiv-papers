# 종식 정의 arXiv Curator 설정

## 기본 정보

- **사용자**: 종식 정 (trident86)
- **시작 날짜**: 2026-04-22
- **주요 프로젝트**: arXiv 논문 자동 큐레이션

## arXiv Curator 시스템

### 목적
- arXiv 평일(월-금) 발표 논문 중 **실무 적용 가능 TOP 5** 자동 선정
- 요약을 Claude로 **한글 번역**
- 자동으로 GitHub에 커밋 및 푸시

### 스케줄
**화요일~토야일 아침 6시 UTC 자동 실행**

| 실행 요일 | 수집 대상 |
|---------|---------|
| 화요일 06:00 | 월요일 논문 TOP 5 |
| 수요일 06:00 | 화요일 논문 TOP 5 |
| 목요일 06:00 | 수요일 논문 TOP 5 |
| 금요일 06:00 | 목요일 논문 TOP 5 |
| 토요일 06:00 | 금요일 논문 TOP 5 |

### 선정 기준 (점수 기반)

**실무 적용 관련 (+3점 각각)**
- efficient, fast, optimization, scalable, production
- real-world, practical, robust, reliable, secure
- benchmark, sota, method, framework, system, application

**주목받는 분야 (+1점 각각)**
- llm, multimodal, vision, language, transformer
- diffusion, reasoning, agent, retrieval, knowledge
- 3d, video, image, text, speech

**콜라보레이션**
- 3명 이상 저자 (+1점)

### 리포트 형식

```markdown
# 📰 arXiv 엄선 리포트 - YYYY-MM-DD

📊 **선정 기준**: 실무 적용 가능성 + 주목도
🔗 **소스**: arXiv 공식 API | **업데이트**: UTC 시간
🎯 **선정 논문**: TOP 5 (점수 기반)

---

## 🏆 주목할 논문 TOP 5

### N. 논문 제목

[분야 이모지] **분야**: 한글명 (영문코드)
- **저자**: 저자1, 저자2
- **arXiv ID**: XXXX.XXXXX
- **점수**: XX점
- **요약 (한글)**: Claude 번역 요약 (300자)
- **링크**: https://arxiv.org/abs/XXXX.XXXXX
```

### 파일 위치

| 파일 | 위치 |
|------|------|
| 스크립트 | `/home/node/.openclaw/workspace/arxiv_curator.py` |
| 리포트 | `/home/node/.openclaw/workspace/2026-04/YYYY-MM-DD.md` |
| 설정 | `/home/node/.openclaw/workspace/ARXIV_CRON_CONFIG.md` |

### GitHub 저장소

- **URL**: https://github.com/trident90/arxiv-papers
- **Branch**: main (master는 삭제됨)
- **토큰**: [환경 변수에 저장됨 - GITHUB_TOKEN]
- **아이디**: trident90

### API 설정

**Claude 번역**
- 모델: anthropic/claude-3.5-haiku (OpenRouter)
- 환경 변수: `OPENROUTER_API_KEY`
- 번역 길이: 300자 이내 한글 요약

**arXiv API**
- Rate limit: 초당 3개 요청
- 요청 간 딜레이: 0.6초

### 수집 분야 (5개)

1. 🤖 **cs.AI** - 인공지능
2. 🧠 **cs.LG** - 머신러닝
3. 👁️ **cs.CV** - 컴퓨터비전
4. 🌐 **cs.NI** - 네트워킹
5. ⛓️ **cs.CR** - 보안/암호

### Cron 표현식

```
0 6 * * 2-6 cd /home/node/.openclaw/workspace && python3 arxiv_curator.py >> /tmp/arxiv_curator.log 2>&1
```

## 테스트 완료

✅ **2026-04-21 테스트 실행 완료**
- 313편 수집 (cs.AI 100, cs.LG 93, cs.CV 92, cs.NI 5, cs.CR 23)
- TOP 5 선정 및 Claude 한글 번역 완료
- GitHub main branch에 푸시 완료

### TOP 5 선정 예시 (2026-04-21)

1. [33점] Multi-modal Reasoning with LLMs
2. [33점] Tstars-Tryon 1.0: Virtual Try-On
3. [31점] FedProxy: Federated Fine-Tuning
4. [29점] How Far Are Video Models
5. [28점] VCE: Hallucination Mitigation

## 다음 실행 일정

✅ **내일 4월 23일 아침 6시 UTC**
- 4월 22일 논문 TOP 5 자동 수집
- Claude 한글 번역 자동 적용
- GitHub main branch 자동 푸시

## 주의사항

- arXiv Rate limit 주의 (초당 3개, 요청 간 0.6초 대기)
- GitHub 토큰은 보안 유지
- 리포트 형식은 일관되게 유지
- Claude 번역 실패 시 원문 사용

---

**상태**: ✅ 완벽 준비 완료, 내일부터 자동 실행
**마지막 업데이트**: 2026-04-22 13:34 UTC
