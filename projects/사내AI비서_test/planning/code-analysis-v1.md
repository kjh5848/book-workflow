# 코드 분석

## 완성 코드 정보
- 경로: `code/CH01_LLM의_한계와_RAG의_필요성/`
- 언어/프레임워크: Python 3.12 / LangChain + Ollama + ChromaDB

## 전체 구조

```
CH01_LLM의_한계와_RAG의_필요성/
├── step1_fail.py              # LLM 단독 질의 → 환각 체험
├── step2_context.py           # Context Injection → 임시 해결
├── step3_rag_no_chunking.py   # RAG 청킹 미적용 → 비효율 체감
├── step3_rag.py               # RAG + 청킹 → 성공
├── step4_rag.py               # RAG + 추론 → 심화
└── requirements.txt
```

> **순서 변경**: 원본 코드에서는 `step3_rag.py` → `step3_rag_no_chunking.py` 순서였으나,
> 책에서는 **청킹 미적용(실패) → 청킹 적용(성공)** 순서로 재배치하여 스토리텔링 강화.

## 핵심 기능 (의도 안)

| # | 기능 | 관련 코드 | 주요 기술 | 코드 분류 |
|---|------|----------|----------|----------|
| 1 | LLM 환각 체험 | `step1_fail.py` | ChatOllama, DeepSeek R1 | **실습** |
| 2 | Context Injection | `step2_context.py` | f-string 프롬프트 구성 | **실습** |
| 3 | RAG 청킹 미적용 | `step3_rag_no_chunking.py` | Chroma, 통째 Document | **실습** (실패 체험) |
| 4 | RAG 청킹 적용 | `step3_rag.py` | RetrievalQA, 개별 Document | **실습** (성공) |
| 5 | RAG + 추론 | `step4_rag.py` | 동일 스택 + 복잡 질문 | **실습** |

### 스토리 흐름 (실패 → 성공 패턴)

```
step1: LLM에게 물어봄 → 환각 (완전 실패)
  ↓ "그럼 정보를 직접 넣어주면?"
step2: 프롬프트에 문서 삽입 → 정확해짐 (임시 해결, 스케일 X)
  ↓ "문서가 1000개면?"
step3a: RAG인데 청킹 안 함 → 비효율 (부분 실패)
  ↓ "잘게 쪼개면?"
step3b: RAG + 청킹 → 관련 문서만 검색 (성공!)
  ↓ "계산이 필요한 질문은?"
step4: RAG + 추론 → 규정 기반 계산 (심화 성공)
```

## 의도 밖 기능 (제외)

| 기능 | 관련 코드 | 제외 이유 |
|------|----------|----------|
| LangChain 내부 체인 구조 | RetrievalQA 내부 동작 | seed.md 의도 밖 |
| 프롬프트 엔지니어링 심화 | PromptTemplate 고급 기법 | seed.md 의도 밖 |
| 모델 비교 | DeepSeek 외 모델 | seed.md 의도 밖 |

## 기술 스택 정리 (의도 안)

| 기술 | 역할 | 책에서 설명 수준 |
|------|------|----------------|
| Ollama | 로컬 LLM 서버 | 비유: "내 컴퓨터 안의 AI 엔진" |
| DeepSeek R1:8b | 추론 가능 LLM | 모델 선택 이유 간단히 |
| ChatOllama | LangChain↔Ollama 연결 | 사용법만, 내부 X |
| ChromaDB | 인메모리 벡터 DB | 비유: "AI 전용 도서관 색인" |
| nomic-embed-text | 임베딩 모델 | 비유: "문장을 좌표로 변환" |
| RetrievalQA | RAG 체인 | 파이프라인 흐름만 |
| Document | LangChain 문서 객체 | 데이터 포맷 정도 |

## 기술 의존성 메모

| 선행 개념 | 필요한 곳 | 해결 방법 |
|----------|----------|----------|
| 임베딩이란 | OllamaEmbeddings | 비유 ("단어를 좌표로") → 기술파트에서 정의 |
| 벡터 DB란 | Chroma.from_documents | 비유 ("AI 전용 도서관 색인") → 기술파트에서 정의 |
| 환각(Hallucination) | step1 출발점 | step1 실행 결과로 체험 → 기술파트에서 정의 |
| Retriever 패턴 | as_retriever() | 비유 ("검색 도우미") → 간단 설명 |
