# 부록

---

## A. 이 책에 나온 핵심 용어 정리

책 전체에서 비유로 소개한 개념들의 정식 정의를 한곳에 모았습니다. "아, 그게 그 말이었구나" 싶을 때 이 표를 찾아보세요.

| 비유 | 용어 | 정식 정의 |
|------|------|----------|
| 회사 서랍장 | **데이터베이스 (DB)** | 구조화된 데이터를 체계적으로 저장·관리하는 시스템. 이 책에서는 PostgreSQL 사용 |
| 창구 담당자 | **API (Application Programming Interface)** | 소프트웨어 간 요청·응답을 주고받는 인터페이스. 이 책에서는 FastAPI 사용 |
| 서랍에 넣고 꺼내는 4가지 행동 | **CRUD** | Create(생성), Read(조회), Update(수정), Delete(삭제) |
| 아이비리그 출신 외부 컨설턴트 | **LLM (Large Language Model)** | 대규모 텍스트 데이터로 학습한 언어 모델. GPT-4, Ollama 등 |
| 없는 것을 있다고 대답하는 현상 | **환각 (Hallucination)** | LLM이 학습 데이터에 없는 정보를 그럴듯하게 만들어내는 현상 |
| 컨설턴트의 서류 가방 | **컨텍스트 윈도우 (Context Window)** | LLM이 한 번에 처리할 수 있는 텍스트의 최대 길이. 단위: 토큰 |
| 서류함 | **문서 저장소 (docs/)** | 파싱 대상이 되는 PDF, DOCX, XLSX 등의 사내 문서 폴더 |
| 문서에서 텍스트 꺼내기 | **파싱 (Parsing)** | PDF, DOCX, XLSX 등 형식별로 텍스트를 추출하는 과정 |
| 색인 카드로 자르기 | **청킹 (Chunking)** | 텍스트를 일정 크기의 조각으로 나누는 작업. 크기·겹침(overlap) 조절 가능 |
| 색인 카드에 분류 번호 붙이기 | **임베딩 (Embedding)** | 텍스트를 고차원 숫자 벡터로 변환하는 과정. 의미가 비슷한 텍스트는 가까운 벡터를 가짐 |
| 벡터 도서관 | **벡터 데이터베이스 (Vector DB)** | 벡터(임베딩) 형태의 데이터를 저장하고 유사도 기반 검색을 지원하는 DB. 이 책에서는 ChromaDB 사용 |
| 조립 라인 (서류 찾기→건네기→대본→답변) | **RAG 체인 (RAG Chain)** | Retrieval-Augmented Generation. 검색(Retrieval)으로 관련 문서를 찾아 LLM에 제공해 답변을 생성하는 파이프라인 |
| 비서에게 건네는 대본 | **프롬프트 (Prompt)** | LLM에게 역할과 행동 방식을 지정하는 지시문 |
| 안내데스크 | **라우터 (Router)** | 질문의 종류를 분류해서 적절한 처리 경로로 연결하는 컴포넌트 |
| 비서의 연장통 | **도구 (Tools)** | LangChain에서 LLM이 외부 기능을 호출할 수 있게 해주는 함수. `@tool` 데코레이터로 정의 |
| 스스로 연장통에서 도구를 꺼내는 비서 | **에이전트 (Agent)** | 질문을 받아 어떤 도구를 써서 답할지 스스로 판단하고 실행하는 LLM 기반 시스템 |
| 메모 패드 | **캐시 (Cache)** | 자주 요청되는 결과를 임시 저장해 다음 번 요청 속도를 높이는 기법. TTL로 만료 시간 설정 |
| 업무 일지 | **로그 (Log)** | 시스템 동작 기록. 어떤 도구를 몇 번 호출했는지, 응답 시간, 오류 내역 등을 파일에 기록 |
| 비서 근무 규정서 | **설정 파일 (.env / config)** | 코드를 수정하지 않고 LLM 종류, API 키, 캐시 설정 등을 바꿀 수 있는 외부 설정 |
| 색인 카드 크기 조정 | **청킹 튜닝** | 청크 크기(size)와 겹침(overlap)을 실험해 검색 품질을 최적화하는 작업 |
| 면접관처럼 다시 평가하기 | **ReRanker** | 1차 검색 결과(k개)를 질문과 함께 재평가해 더 관련 높은 순서로 재정렬하는 모델 |
| 키워드+의미 동시 검색 | **하이브리드 검색 (Hybrid Search)** | BM25(키워드 빈도 기반)와 Vector Search(의미 유사도 기반)를 결합한 검색 방식 |
| 질문을 다양하게 바꿔서 재검색 | **Query Rewriting** | HyDE(가상 문서 생성), Multi-Query(다각도 쿼리) 등 원본 질문을 변형해 검색 coverage를 높이는 기법 |
| 비서 성적표 | **평가 프레임워크 (Eval Framework)** | 테스트 질문셋에 대해 Precision@k, Recall@k 등 지표를 측정해 RAG 성능을 수치화하는 도구 |

---

## B. 환경 설정 빠른 참조

### 필수 도구

| 도구 | 용도 | 설치 |
|------|------|------|
| Python 3.11+ | 실행 환경 | [python.org](https://www.python.org) |
| Docker Desktop | PostgreSQL, ChromaDB 컨테이너 실행 | [docker.com](https://www.docker.com) |
| Git | 버전 코드 내려받기 | [git-scm.com](https://git-scm.com) |

### Docker 기본 명령어

```bash
# 서비스 시작 (백그라운드)
docker compose up -d

# 서비스 중지
docker compose down

# 로그 확인
docker compose logs -f

# 컨테이너 상태 확인
docker compose ps
```

### .env 파일 기본 구조

각 챕터 폴더의 `.env.example`을 복사해서 `.env`로 만든 다음 값을 채워넣으면 됩니다.

```bash
cp .env.example .env
```

```
# LLM 설정
LLM_PROVIDER=ollama          # ollama | openai
LLM_MODEL=llama3.2           # 사용할 모델 이름
OPENAI_API_KEY=sk-...        # OpenAI 사용 시

# DB 설정
DATABASE_URL=postgresql://user:password@localhost:5432/company_db

# 벡터DB 설정
CHROMA_HOST=localhost
CHROMA_PORT=8000
EMBEDDING_MODEL=snunlp/KR-SBERT-V40K-klueNLI-augSTS  # 한국어 임베딩 모델
```

### Ollama 사용 시 (로컬 LLM)

```bash
# Ollama 설치 후 모델 내려받기
ollama pull llama3.2

# 실행 중인지 확인
ollama list
```

---

## C. 더 깊이 가고 싶을 때

### 공식 문서

| 자료 | 내용 | 주소 |
|------|------|------|
| LangChain 공식 문서 | LCEL, 체인, 에이전트, 도구 상세 | langchain.com/docs |
| LangSmith | LLM 앱 트레이싱·디버깅·평가 플랫폼 | smith.langchain.com |
| ChromaDB 문서 | 벡터DB 설정, 컬렉션 관리 | docs.trychroma.com |
| RAGAS | RAG 평가 프레임워크 (Faithfulness, Relevancy 등) | docs.ragas.io |
| FastAPI 문서 | API 설계, Pydantic, 의존성 주입 | fastapi.tiangolo.com |

### 다음 단계 학습 경로

이 책을 다 읽었다면 다음 순서로 나아가는 것을 추천합니다.

**1단계: 직접 써보기**
실제 사내 문서를 `data/docs/`에 넣어서 돌려보세요. 파싱 오류, 검색 품질 문제, 응답 지연 — 실제 데이터에서 만나는 문제가 가장 좋은 선생님입니다.

**2단계: 평가 세우기**
`test_questions.json`을 우리 회사 실제 질문 30~50개로 교체하세요. RAGAS를 연결해서 Faithfulness(답변이 문서에 근거했나), Answer Relevancy(답변이 질문과 맞나)를 수치로 보기 시작하면 개선 방향이 명확해집니다.

**3단계: LangSmith 연결**
`.env`에 `LANGCHAIN_API_KEY`를 설정하면 모든 체인 실행이 LangSmith에 기록됩니다. 어떤 문서가 검색됐는지, LLM이 어떤 답을 만들었는지 — 시각화된 트레이스를 보면서 디버깅하세요.

**4단계: 프로덕션 방향**
이 책은 프로덕션 배포를 다루지 않습니다. 프로덕션으로 가려면 인증/인가 레이어, 레이트 리밋, 고가용성 설정이 필요합니다. "FastAPI 프로덕션 배포", "LangChain 운영 환경 구성" 키워드로 찾아보세요.

### 읽을 만한 자료

- **"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"** (Lewis et al., 2020) — RAG를 처음 제안한 논문. 왜 이 방식이 효과적인지 이해하는 데 도움이 됩니다.
- **LangChain Expression Language (LCEL) 공식 가이드** — Ch.4에서 쓴 파이프라인 패턴을 더 깊이 이해하고 싶을 때.
- **"Advanced RAG Techniques"** (LlamaIndex 블로그) — Ch.7에서 다룬 ReRanker, Hybrid Search를 더 심화하고 싶을 때.

---

## D. 챕터별 핵심 실습 명령어 요약

| 챕터 | 실행 명령 | 결과 |
|------|----------|------|
| Ch.1 | `docker compose up -d` → `uvicorn app.main:app` | 브라우저에서 대시보드 확인 |
| Ch.2 | `python step1_fail.py` → `step2_context.py` → `step3_rag.py` | 실패→컨텍스트→RAG 비교 |
| Ch.3 | `python src/main.py` → `python src/cli_search.py` | 문서 인제스천 → CLI 검색 |
| Ch.4 | `uvicorn app.main:app` | 채팅 UI에서 질의응답 |
| Ch.5 | `python data/schema.sql` → `uvicorn app.main:app` | DB+문서 통합 에이전트 |
| Ch.6 | `python src/main.py --demo` | 데모 모드 + 로그 파일 확인 |
| Ch.7 | `python tuning/chunk_experiment.py` 등 | Before/After 성능 비교표 |
