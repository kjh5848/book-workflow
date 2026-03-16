# Why-Log

실수에서 배운 규칙을 기록한다. 각 항목은 YAML 프론트매터 블록으로 관리하며,
해당 규칙이 반영된 에이전트/파일을 `rule_added_to`로 추적한다.

---

```yaml
- id: "2026-03-15-2"
  date: 2026-03-15
  category: dispatch
  summary: 디스패치 테이블 에이전트 순서 생략 금지
  detail: >
    챕터 작성 시 일러스트레이터를 건너뛰고 writer → editor만 호출하여
    다이어그램/캡처가 누락된 채 챕터가 완료 처리됨.
  rule_added_to:
    - .claude/agents/meta/AGENT.md

- id: "2026-03-15-5"
  date: 2026-03-15
  category: layout
  summary: PDF 페이지 하단 1/3 이상 공백 시 조치 필수
  detail: >
    빌드 후 하단 공백을 방치하여 페이지 밀도가 떨어짐.
    이미지 축소, 위치 조정, 텍스트 재배치로 해소해야 함.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

- id: "2026-03-15-6"
  date: 2026-03-15
  category: design
  summary: D2 생성 시 샘플 디자인 classes 복사 필수
  detail: >
    새 D2 파일을 만들 때 classes를 직접 정의하여 디자인 불일치 발생.
    반드시 references/samples/sample_diagram.d2의 classes를 복사하여 사용.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

- id: "2026-03-15-7"
  date: 2026-03-15
  category: design
  summary: 다이어그램 강조색 금지 — 화이트로 통일
  detail: >
    빨강/초록/노랑 등 의미 색상을 사용하여 디자인 통일성이 깨짐.
    danger/success 등 시맨틱 색상도 화이트 배경으로 통일.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

- id: "2026-03-15-10"
  date: 2026-03-15
  category: layout
  summary: build_chapter() 레이아웃 자동 교정 최대 3회 반복
  detail: >
    layout-check 실패 후 수동 개입 없이 방치됨.
    이미지 축소 + 재빌드를 자동으로 최대 3회 반복하도록 변경.
  rule_added_to:
    - .claude/agents/publisher/AGENT.md

- id: "2026-03-15-22"
  date: 2026-03-15
  category: writing
  summary: '"이번 버전: exNN → exNN" 메타데이터를 챕터에 넣지 마라'
  detail: >
    챕터 본문에 버전 메타데이터가 노출되어 독자 경험을 해침.
    메타데이터는 planning 문서에만 기록.
  rule_added_to:
    - .claude/agents/writer/AGENT.md

- id: "2026-03-15-23"
  date: 2026-03-15
  category: writing
  summary: 실습 순서를 다이어그램으로 만들지 마라
  detail: >
    실습 순서를 Mermaid/D2 다이어그램으로 표현하여 오히려 복잡해짐.
    번호 목록으로 작성하는 것이 더 명확.
  rule_added_to:
    - .claude/agents/writer/AGENT.md

- id: "2026-03-16-1"
  date: 2026-03-16
  category: dispatch
  summary: STEP 완료 전 호출된 에이전트 목록 대조 필수
  detail: >
    STEP 완료 처리 시 디스패치 테이블의 에이전트 전체가 호출되었는지
    검증하지 않아 누락이 발생. 완료 전 반드시 목록 대조.
  rule_added_to:
    - .claude/agents/meta/AGENT.md
```
