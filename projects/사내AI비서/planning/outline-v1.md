# 목차

## 코드 실습 분류 기준

| 분류 | 표시 | 의미 | 독자 액션 |
|------|------|------|----------|
| 실습 | [실습] | 챕터 핵심 코드 | 파일 실행하고 결과 확인 |
| 설명 | [설명] | 중요하지만 핵심 아닌 코드 | 코드 읽고 이해 |
| 참고 | [참고] | 이 챕터 주제가 아닌 코드 | 파일명 + 한 줄만 |

> 이 책은 이해 중심이다. 독자가 코드를 짜는 게 아니라, 실행해서 결과를 확인하며 개념을 이해한다.

---

## Part 1: 재료 준비

### Ch.1: 회사 장부를 열어보자 — v0.1

**핵심 개념**: 정형 데이터, REST API, CRUD
**비유**: 회사 장부 = DB, 웨이터 = API, 주문서 = 스키마
**기술**: FastAPI, PostgreSQL, Pydantic, Jinja2
**버전 성과**: 브라우저에서 직원/매출 대시보드가 보인다
**예상 분량**: ~15p

**코드 실습 분류**:
```
v0.1/
├── app/
│   ├── main.py         [실습] FastAPI 앱 실행
│   ├── database.py     [설명] DB 연결 방식
│   ├── crud.py         [설명] SQL CRUD 함수
│   ├── schemas.py      [참고] Pydantic 모델
│   ├── api.py          [설명] REST API 엔드포인트
│   └── views.py        [참고] Admin UI 라우터
├── docker-compose.yml  [실습] PostgreSQL 실행
└── templates/          [참고] HTML 템플릿
```

**실습 요약**: 실행 2개, 설명 3개, 참고 3개

---

### Ch.2: ChatGPT에게 사내 문서를 보여줬더니 — v0.2

**핵심 개념**: LLM의 한계(환각, 토큰 한도, 보안), RAG가 왜 필요한지
**비유**: ChatGPT = 똑똑하지만 우리 회사를 모르는 외부 컨설턴트, RAG = 회사 자료를 읽게 해주는 것
**기술**: OpenAI API 직접 호출, 컨텍스트 스터핑, RAG 기초
**버전 성과**: 실패(환각) → 컨텍스트 → RAG 3단계를 눈으로 확인
**예상 분량**: ~12p

**코드 실습 분류**:
```
v0.2/
├── step1_fail.py             [실습] LLM에게 사내 질문 → 환각 확인
├── step2_context.py          [실습] 문서를 통째로 넣기 → 토큰 한계
├── step3_rag.py              [실습] RAG로 해결
├── step3_rag_no_chunking.py  [설명] 청킹 없는 RAG (비교)
├── step4_rag.py              [설명] 개선된 RAG
└── requirements.txt          [참고] 의존성
```

**실습 요약**: 실행 3개, 설명 2개, 참고 1개

---

### Ch.3: 서류함을 뒤져보자 — v0.3

**핵심 개념**: 문서 파싱, 청킹, 임베딩, 벡터DB
**비유**: 서류함 = docs/, 색인 카드 = 청크, 분류 번호 = 벡터, 도서관 = ChromaDB
**기술**: pypdf, python-docx, openpyxl, ko-sroberta, ChromaDB
**버전 성과**: CLI에서 "연차 규정" 검색하면 관련 문단이 나온다
**예상 분량**: ~18p

**코드 실습 분류**:
```
v0.3/
├── src/
│   ├── main.py          [실습] 전체 파이프라인 실행
│   ├── extractor.py     [설명] 문서 파싱 공통 모듈
│   ├── extract_pdf.py   [설명] PDF 파싱
│   ├── extract_docx.py  [참고] DOCX 파싱
│   ├── extract_xlsx.py  [참고] XLSX 파싱
│   ├── chunker.py       [설명] 500자 청킹 + 오버랩
│   ├── store.py         [설명] 임베딩 + ChromaDB 저장
│   └── cli_search.py    [실습] CLI 검색 도구
└── data/docs/           [실습] 사내 문서 6종 (입력)
```

**실습 요약**: 실행 3개, 설명 4개, 참고 2개

---

## Part 2: 비서 만들기

### Ch.4: 비서가 말을 하기 시작했다 — v0.4 (전환점!)

**핵심 개념**: RAG 체인, 프롬프트 엔지니어링, LCEL, 멀티턴 대화
**비유**: 비서 = LLM + RAG, 족보 = 벡터DB, 대화 기억 = WindowMemory
**기술**: LangChain LCEL, Ollama/OpenAI, FastAPI 채팅 UI
**버전 성과**: 채팅 UI에서 질문하면 근거 + 답변이 나온다
**예상 분량**: ~20p

**코드 실습 분류**:
```
v0.4/
├── src/
│   ├── rag_chain.py         [설명] LCEL 파이프라인 + 프롬프트
│   ├── response_parser.py   [설명] 답변 + 출처 파싱
│   └── conversation.py      [설명] 멀티턴 히스토리
├── app/
│   ├── main.py              [실습] 채팅 서버 실행
│   └── chat_api.py          [설명] /api/chat 엔드포인트
├── templates/chat.html      [참고] 채팅 UI
└── static/js/chat.js        [참고] Fetch 로직
```

**실습 요약**: 실행 1개, 설명 4개, 참고 2개

---

### Ch.5: 비서에게 연장통을 쥐여주자 — v0.5

**핵심 개념**: 질문 라우팅, MCP 도구, ReAct 에이전트
**비유**: 안내데스크 = Router, 연장통 = Tools, 스스로 판단하는 비서 = Agent
**기술**: QueryRouter(3단계), @tool 데코레이터, AgentExecutor
**버전 성과**: "연차 며칠?"도 "보안 규정?"도 한 곳에서 답한다
**예상 분량**: ~18p

**코드 실습 분류**:
```
v0.5/
├── src/
│   ├── router.py        [설명] 3단계 QueryRouter
│   ├── mcp_tools.py     [설명] 4개 도구 정의
│   └── agent.py         [설명] ReAct 에이전트
├── app/
│   ├── main.py          [실습] 에이전트 채팅 서버
│   └── chat_api.py      [참고] 엔드포인트
├── data/schema.sql      [실습] DB 초기화 + 샘플 데이터
└── tests/               [참고] 시나리오 테스트
```

**실습 요약**: 실행 2개, 설명 3개, 참고 2개

---

## Part 3: 비서 키우기

### Ch.6: 비서에게 매뉴얼을 주자 — v0.6

**핵심 개념**: LangChain 표준 구성, 캐시, 모니터링, 운영 설정
**비유**: 비서 매뉴얼 = AgentConfig, 업무 일지 = Langfuse, 메모 = 캐시
**기술**: AgentExecutor, TTL 캐시, JSON 로깅, Langfuse(선택)
**버전 성과**: 데모 모드 실행, 로그 파일 확인, 캐시로 빠른 응답 확인
**예상 분량**: ~15p

**코드 실습 분류**:
```
v0.6/
├── src/
│   ├── main.py          [실습] CLI 실행 (대화형 + 데모)
│   ├── agent_config.py  [설명] LLM + Router + Agent 조립
│   ├── cache.py         [설명] TTL 응답 캐시
│   ├── monitoring.py    [설명] 로깅 + 토큰 추적
│   ├── router.py        [참고] QueryRouter (v0.5와 동일)
│   └── tools/           [참고] 4개 도구 (v0.5와 동일)
└── .env.example         [실습] 환경 변수 설정
```

**실습 요약**: 실행 2개, 설명 3개, 참고 2개

---

### Ch.7: 비서의 실력을 올리자 — v0.7

**핵심 개념**: RAG 튜닝 (청킹, Retriever, ReRanker, Hybrid Search, Query Rewrite, 문서 캡처, 평가)
**비유**: 색인 카드 크기 실험 = 청킹 튜닝, 키워드+의미 동시 검색 = Hybrid, 성적표 = 평가
**기술**: Semantic 청킹, BM25, Cross-Encoder, HyDE, PyMuPDF, OCR, RAGAS
**버전 성과**: Before/After 성능 비교표. 같은 질문에 더 정확한 답변.
**예상 분량**: ~20p

**코드 실습 분류**:
```
v0.7/
├── tuning/
│   ├── chunk_experiment.py      [실습] 청킹 비교 실험
│   ├── retriever_experiment.py  [실습] k값/threshold 실험
│   ├── reranker.py              [실습] ReRanker 실행
│   ├── hybrid_search.py         [실습] BM25+Vector 앙상블
│   ├── query_rewrite.py         [설명] HyDE, Multi-Query
│   ├── document_parser.py       [설명] 라이브러리 vs vLLM 비교
│   ├── document_capture.py      [설명] PDF→PNG→메타데이터
│   └── evidence_pipeline.py     [참고] 근거 추적
├── src/eval_framework.py        [실습] 평가 프레임워크
└── data/test_questions.json     [참고] 테스트 질문 30개
```

**실습 요약**: 실행 5개, 설명 3개, 참고 2개

---

## 갭 분석 결과

| 누락 주제 | 우선순위 | 반영 여부 | 비고 |
|----------|---------|----------|------|
| LLM의 한계 (환각, 토큰) | [필수] | 반영 | Ch.2에서 실패 체험으로 |
| 임베딩이란 무엇인가 | [필수] | 반영 | Ch.3 이야기 파트에서 비유로 |
| LLM 기본 원리 | [필수] | 반영 | Ch.2 이야기 파트에서 비유로 |
| 프롬프트 엔지니어링 기초 | [필수] | 반영 | Ch.4 기술 파트에서 |
| 벡터 유사도 검색 원리 | [권장] | 반영 | Ch.3 이야기 파트에서 비유로 |
| Docker 기본 사용법 | [권장] | 생략 | 선행 지식으로 가정, 부록에 한 줄 안내 |
| 토큰/비용 관리 | [권장] | 생략 | 이해 중심이므로 범위 초과 |
| CI/CD 파이프라인 | [선택] | 생략 | 프로덕션 배포는 의도 밖 |
| 보안 (API 키 관리) | [선택] | 생략 | .env 파일 설명 수준으로 충분 |

---

## 여정 맵

```
Ch.1(쉬움) → Ch.2(실패!) → Ch.3(보통) → Ch.4(전환점!) → Ch.5(보통) → Ch.6(쉬어가기) → Ch.7(도전)
 DB기초      LLM한계      벡터DB       RAG체인        에이전트      표준화        튜닝
 "장부열기"  "실패체험"    "서류함"     "비서가 말해!"  "연장통"      "매뉴얼"      "실력UP"
```

---

## 기술 매핑

| 챕터 | 버전 | 핵심 기술 | 완성 코드(CH)와 다른 점 |
|------|------|----------|----------------------|
| Ch.1 | v0.1 | FastAPI, PostgreSQL | CH04 그대로 사용 |
| Ch.2 | v0.2 | OpenAI API, 컨텍스트 스터핑 | CH03 그대로 사용 |
| Ch.3 | v0.3 | pypdf, ChromaDB, ko-sroberta | CH06 그대로 사용 |
| Ch.4 | v0.4 | LangChain LCEL, Ollama | CH07 그대로 사용 |
| Ch.5 | v0.5 | QueryRouter, ReAct Agent | CH08 그대로 사용 |
| Ch.6 | v0.6 | AgentExecutor, 캐시, Langfuse | CH09 그대로 사용 |
| Ch.7 | v0.7 | 청킹/ReRanker/Hybrid/평가 | CH10에서 핵심 실험만 선별 |

---

## 분량 추정

| 항목 | 예상 분량 |
|------|----------|
| 프롤로그 + 로드맵 | ~8p |
| Ch.1 회사 장부를 열어보자 | ~15p |
| Ch.2 ChatGPT에게 사내 문서를 보여줬더니 | ~12p |
| Ch.3 서류함을 뒤져보자 | ~18p |
| Ch.4 비서가 말을 하기 시작했다 | ~20p |
| Ch.5 비서에게 연장통을 쥐여주자 | ~18p |
| Ch.6 비서에게 매뉴얼을 주자 | ~15p |
| Ch.7 비서의 실력을 올리자 | ~20p |
| 서문 + 에필로그 + 부록 | ~6p |
| **합계** | **~132p** |

> 100p 권장 대비 32p 초과. 저자가 나중에 조절 예정.
