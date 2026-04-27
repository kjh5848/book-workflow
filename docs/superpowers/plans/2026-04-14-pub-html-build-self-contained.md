# pub-html-build 자기완결형 재설계 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `pub-html-build` 스킬을 자기완결형으로 재설계한다. superpowers 플러그인이 없는 사용자도 "디자인 탐색 → 컴포넌트 카탈로그에서 재사용 or 신규 설계 → 빌드" 흐름을 독립적으로 완주할 수 있게 만든다.

**Architecture:** 기존 단일 스킬에 `modes/`(재사용·탐색 2모드) + `components-catalog/`(6 카테고리, 챕터에서 추출한 실재 컴포넌트) 두 레이어를 추가한다. `SKILL.md`를 진입점/분기 가이드로 리팩터한다. superpowers가 있으면 `brainstorming`을 선택적으로 연계할 수 있지만, 없어도 내장 질문 세트·강제 변형 축으로 탐색이 완료되도록 한다.

**Tech Stack:** Markdown 문서, 기존 `styles/components.css` 참조(수정은 최소), HTML 예시, `build_pdf_html.py`는 건드리지 않는다.

**작업 루트:** `.claude/skills/pub-html-build/`

---

## 파일 구조 (최종)

```
.claude/skills/pub-html-build/
├── SKILL.md                        # [수정] 진입점 + 분기 가이드
├── build_pdf_html.py               # 손대지 않음
├── scripts/                        # 손대지 않음
├── templates/                      # 손대지 않음
├── styles/                         # 기존 CSS 유지
│   ├── base.css
│   ├── components.css
│   ├── diagrams.css
│   ├── fonts.css
│   ├── print.css
│   └── tokens.css
├── modes/                          # [신규]
│   ├── reuse.md                    # 기본 재사용 (tokens 오버라이드)
│   └── design-explore.md           # 디자인 탐색 (내장 질문+변형)
└── components-catalog/             # [신규]
    ├── README.md                   # 카탈로그 색인 + 추가 절차
    ├── inventory.md                # 챕터에서 추출한 컴포넌트 전체 목록
    ├── boxes/                      # :::goal, ::::prep, :::tip, :::note, :::term-box, :::remember
    │   └── README.md
    ├── fullmap/                    # .arch-fullmap + afm-*
    │   └── README.md
    ├── cards/                      # .cwm-card, .eer-card, .rag-step
    │   └── README.md
    ├── comparisons/                # .annotated-compare, .overlap-text-demo, .cache-diff, .reindex-compare, .dual-image
    │   └── README.md
    ├── pipelines/                  # .rag-pipeline-box, .rc-timeline, .ec-cabinet
    │   └── README.md
    └── captions/                   # .rl-caption, .eer-caption, .afm-tag, .afm-zone-*
        └── README.md
```

**메모리**: `~/.claude/projects/.../memory/project_pub_html_skill.md` 갱신 (외부 파일, outer commit 대상 아님)

---

## Task 1: 컴포넌트 인벤토리 추출

**Files:**
- Create: `.claude/skills/pub-html-build/components-catalog/inventory.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p ".claude/skills/pub-html-build/components-catalog"
```

- [ ] **Step 2: CSS에서 클래스 목록 추출**

```bash
grep -nE "^\s*\.[a-zA-Z][a-zA-Z0-9_-]+" ".claude/skills/pub-html-build/styles/components.css" | head -200 > /tmp/css-classes.txt
grep -nE "^\s*\.[a-zA-Z][a-zA-Z0-9_-]+" ".claude/skills/pub-html-build/styles/print.css" | head -100 >> /tmp/css-classes.txt
```

- [ ] **Step 3: 챕터에서 실제 사용 클래스 추출**

```bash
for f in projects/사내AI비서_v2/chapters/0[1-9]-*.md projects/사내AI비서_v2/chapters/10-*.md; do
  grep -oE 'class="[^"]+"' "$f" | sort -u
done > /tmp/chapter-classes.txt

# :::/:::: directive도 추출
for f in projects/사내AI비서_v2/chapters/0[1-9]-*.md projects/사내AI비서_v2/chapters/10-*.md; do
  grep -oE '^:::+[a-z-]+' "$f"
done | sort -u > /tmp/chapter-directives.txt
```

- [ ] **Step 4: `inventory.md` 작성** — CSS·챕터 양쪽에서 확인된 컴포넌트를 6 카테고리로 분류한 단일 표

아래 구조로 작성한다(실제 클래스명/출현 챕터는 Step 2~3 결과로 채움).

```markdown
# 컴포넌트 인벤토리

## 목적
챕터에서 실제 사용된 HTML 컴포넌트와 마크다운 directive를 전수 카탈로그화한다. 이 표가 `components-catalog/` 각 카테고리 문서의 원본 데이터다.

## 분류 규칙 (6 카테고리)
- **boxes**: `:::`/`::::` directive + 박스형 블록(.goal-box, .prep-section, .term-box, .remember-box 등)
- **fullmap**: 전체 구성도(.arch-fullmap, .afm-*)
- **cards**: 개별 카드 단위(.cwm-card=청크, .eer-card=임베딩, .rag-step 등)
- **comparisons**: 비교형 시각 요소(.annotated-compare, .overlap-text-demo, .reindex-compare, .cache-diff, .dual-image)
- **pipelines**: 흐름/타임라인(.rag-pipeline-box, .rc-timeline, .ec-cabinet, .wrapper-arch)
- **captions**: 인라인/라벨(.rl-caption, .eer-caption, .afm-tag, .afm-zone-*)

## 목록

| 카테고리 | 컴포넌트 | 출현 챕터 | CSS 위치 |
|---------|---------|----------|---------|
| boxes | `:::goal` | CH01~CH10 | components.css `.goal-box` |
| boxes | `::::prep` | CH01~CH10 | components.css `.prep-section` |
| boxes | `:::tip` | CH01,02,04~07 | ... |
| ... | ... | ... | ... |
```

- [ ] **Step 5: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/inventory.md
git commit -m "$(cat <<'EOF'
docs(skill): pub-html-build 컴포넌트 인벤토리 추출

챕터 10개 + components.css/print.css 전수 조사. 6 카테고리로 분류.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: 카탈로그 디렉토리 + 진입 README

**Files:**
- Create: `.claude/skills/pub-html-build/components-catalog/README.md`
- Create: `.claude/skills/pub-html-build/components-catalog/{boxes,fullmap,cards,comparisons,pipelines,captions}/README.md` (6 stub)

- [ ] **Step 1: 6 하위 디렉토리 생성**

```bash
cd ".claude/skills/pub-html-build/components-catalog"
mkdir -p boxes fullmap cards comparisons pipelines captions
```

- [ ] **Step 2: 진입 `README.md` 작성**

파일 내용:

```markdown
# components-catalog

`pub-html-build` 스킬이 제공하는 HTML/CSS 컴포넌트의 카탈로그.
새 챕터를 집필할 때 **여기서 조립**하면 된다. 없는 컴포넌트는 `modes/design-explore.md`로 신규 설계한다.

## 카테고리

| 디렉토리 | 담당 |
|---------|------|
| [boxes](boxes/) | `:::`/`::::` directive + 박스형 블록 |
| [fullmap](fullmap/) | 책 전체 구성도와 그 내부 요소 |
| [cards](cards/) | 개별 카드(청크·임베딩·단계 카드) |
| [comparisons](comparisons/) | 비교형 시각 요소 (A vs B, before/after) |
| [pipelines](pipelines/) | 흐름·타임라인·파이프라인 |
| [captions](captions/) | 인라인 라벨·캡션·태그 |

전체 목록은 [inventory.md](inventory.md) 참조.

## 컴포넌트 추가 절차 (4단계)

1. **카탈로그 검색** — 기존 6 카테고리에서 비슷한 게 있는지 확인 (`inventory.md`)
2. **이름 충돌 확인** — `grep -rE "^\\.이름-후보" styles/` 로 CSS에 동명 클래스가 없는지 검증
3. **CSS 추가** — `styles/components.css`에 클래스 정의 (토큰 변수 사용 필수: `var(--color-*)`, `var(--font-*)`)
4. **카탈로그 등록** — 알맞은 카테고리 `README.md`에 "언제 쓰는가 + HTML 예 + CSS 위치 + 변형 + 피해야 할 것" 5항목으로 기록

## 이름 규칙

- 접두어 2~4자로 컴포넌트 군을 식별 (`cwm-*`: chunk with meta, `eer-*`: embedding example row, `afm-*`: architecture full map, `rl-*`: react-loop caption)
- 상태/변형은 modifier (`--strike`, `--faint`, `--on`) 또는 boolean class (`.afm-faint`, `.afm-on`)
- 새 접두어는 3글자 이상, 기존과 겹치지 않게
```

- [ ] **Step 3: 각 카테고리 stub README.md 6개 생성**

각 파일은 다음 스켈레톤으로 시작(Task 3~8에서 채워짐):

```markdown
# {카테고리명}

> {한 줄 정의}

## 컴포넌트 목록

_Task 3~8에서 채워짐_

## 이 카테고리에 속하는 것 / 속하지 않는 것

- 속함: ...
- 속하지 않음: ... → `../{다른-카테고리}/`
```

- [ ] **Step 4: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/
git commit -m "feat(skill): components-catalog 디렉토리 골격"
```

---

## Task 3: Boxes 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/boxes/README.md`

담당 컴포넌트: `:::goal`, `::::prep`, `:::tip`, `:::note`, `:::term-box`, `:::remember`

- [ ] **Step 1: 각 directive의 실제 사용처·렌더 결과 파악**

```bash
grep -B1 -A6 "^:::goal" projects/사내AI비서_v2/chapters/04-*.md | head -30
grep -B1 -A6 "^:::term-box" projects/사내AI비서_v2/chapters/04-*.md | head -20
grep -B1 -A6 "^:::remember" projects/사내AI비서_v2/chapters/04-*.md | head -20
grep -B1 -A10 "^::::prep" projects/사내AI비서_v2/chapters/04-*.md | head -30
```

- [ ] **Step 2: `boxes/README.md`에 6개 컴포넌트 기록**

각 컴포넌트마다 아래 5항목으로 작성:

```markdown
### :::goal

**언제 쓰는가**: 챕터 첫 머리에 "이번 챕터가 끝나면 무엇을 할 수 있는가"를 3~5개 불릿으로 제시.

**사용 챕터**: CH01~CH10 (전 챕터)

**Markdown 사용 예**:
​```markdown
:::goal
**이번 챕터가 끝나면**

- 사내 문서를 벡터DB로 색인하는 파이프라인을 직접 돌립니다
- 고정 크기 청킹(500자/100자 오버랩)의 동작을 이해합니다
- 검색 결과를 눈으로 확인하고 품질 감을 잡습니다
:::
​```

**렌더 CSS**: `styles/components.css` `.goal-box`, `.gl` (초록 그라데이션 좌측 라인 + 제목 라벨)

**변형**: 없음(단일 스타일). 목표 수는 3~5개 권장(1개는 빈약, 6개 이상이면 과함).

**피해야 할 것**
- 목표를 절대 기술 용어만 나열하지 말 것. "할 수 있다" 관점의 행동 문장으로.
- `:::goal` 안에 코드블록, 이미지, 표를 넣지 말 것. 순수 텍스트 불릿만.
```

같은 패턴으로 `::::prep`, `:::tip`, `:::note`, `:::term-box`, `:::remember` 5개 추가 작성. **각 항목의 실제 HTML 렌더 예시는 현재 챕터에서 Copy**.

- [ ] **Step 3: 카테고리 소개부 완성**

`boxes/README.md` 상단에 "이 카테고리에 속함/속하지 않음" 정리:

```markdown
# Boxes

> `:::`/`::::` directive 기반 박스 블록. 챕터의 구조적 박스(목표·준비·팁·용어·기억·주의)를 담당한다.

## 속함
- 6개 directive: `:::goal`, `::::prep`, `:::tip`, `:::note`, `:::term-box`, `:::remember`

## 속하지 않음
- 책 전체 구성도 박스 → `fullmap/`
- 청크/임베딩 단위 카드 → `cards/`
- 비교형(A vs B) 블록 → `comparisons/`
```

- [ ] **Step 4: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/boxes/README.md
git commit -m "docs(skill): boxes 카테고리 6개 directive 카탈로그화"
```

---

## Task 4: Fullmap 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/fullmap/README.md`

담당 컴포넌트: `.arch-fullmap` (컨테이너) + `.afm-row` / `.afm-box` / `.afm-faint` / `.afm-on` / `.afm-zone` / `.afm-zone-ch` / `.afm-zone-label` / `.afm-tag` / `.afm-label` / `.afm-sub` / `.afm-note` / `.afm-dashed` / `.afm-round` / `.afm-three` / `.afm-ext` / `.arch-fullmap-title`

- [ ] **Step 1: 실제 사용 코드 추출**

CH02·CH05·CH07·CH10에 등장. 가장 완성도 높은 CH02(L195~286) 복사해 예시로 사용.

```bash
sed -n '195,286p' "projects/사내AI비서_v2/chapters/02-일단-사내-시스템부터.md"
```

- [ ] **Step 2: `fullmap/README.md` 작성**

구조:

```markdown
# Fullmap

> 책 전체 구성도. 각 챕터가 시스템의 어디에 해당하는지 보여주는 최상위 시각 요소.

## 용법

각 챕터 끝자락에 "## N.N 전체 구성도에서 챕터 N의 자리" H2로 삽입. 이번 챕터가 만든 박스는 `.afm-on`(진함)으로, 앞뒤 챕터 박스는 `.afm-faint`(흐림)로 표시.

## HTML 스켈레톤

​```html
<div class="arch-fullmap">
  <div class="arch-fullmap-title">전체 구성도. 짙은 박스가 챕터 N 범위</div>

  <div class="afm-row afm-user">
    <div class="afm-box afm-faint afm-round">
      <div class="afm-label">사내 직원·관리자</div>
    </div>
  </div>

  <div class="afm-zone">
    <span class="afm-zone-ch">챕터 N</span>
    <span class="afm-zone-label">{영역명}</span>
    <div class="afm-row">
      <div class="afm-box afm-on">
        <div class="afm-tag">오늘 만든 부분</div>
        <div class="afm-label">{기술 이름}</div>
        <div class="afm-sub">{한 줄 요약}</div>
      </div>
    </div>
  </div>

  <!-- 다른 챕터 zone은 .afm-faint -->

  <div class="afm-note">오늘 띄운 건 … 입니다. 나머지는 챕터 N부터 …</div>
</div>
​```

## 요소별 규칙

| 클래스 | 역할 |
|-------|------|
| `.arch-fullmap` | 최상위 컨테이너 |
| `.arch-fullmap-title` | 제목 한 줄 |
| `.afm-zone` | 한 챕터(또는 한 layer)의 묶음 |
| `.afm-zone-ch` | "챕터 N" 뱃지 |
| `.afm-zone-label` | 그 영역의 역할명 |
| `.afm-row` | 가로 줄 |
| `.afm-row.afm-three` | 3칸 그리드 |
| `.afm-row.afm-user` | 사용자 레이어 (최상단) |
| `.afm-row.afm-ext` | 외부 의존(LLM 등) (최하단) |
| `.afm-box` | 박스 단위 |
| `.afm-box.afm-on` | "오늘 만든 부분" 진한 스타일 |
| `.afm-box.afm-faint` | 앞뒤 챕터 박스 흐린 스타일 |
| `.afm-box.afm-dashed` | 외부/미구현 대시 테두리 |
| `.afm-box.afm-round` | 둥근 사용자 박스 |
| `.afm-tag` | "오늘 만든 부분" 등 상단 태그 |
| `.afm-label` | 박스 메인 라벨 |
| `.afm-sub` | 박스 서브 설명 |
| `.afm-note` | 하단 요약 노트 |

## 피해야 할 것

- `.afm-on`을 2개 이상 쓰지 말 것. "오늘 만든 부분"은 한 챕터당 1~2박스만 진하게.
- 한 fullmap에 zone 6개 넘기지 말 것. 가독성 붕괴.
- `.afm-zone-ch`에 "Chapter 6" 같은 영문 섞지 말 것. "챕터 N"으로 통일.
```

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/fullmap/README.md
git commit -m "docs(skill): fullmap 카테고리 — arch-fullmap + afm-* 전수 카탈로그"
```

---

## Task 5: Cards 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/cards/README.md`

담당 컴포넌트:
- `.chunk-with-meta` + `.cwm-title` / `.cwm-card` / `.cwm-body` / `.cwm-meta` / `.cwm-tag` / `.cwm-note` (CH04)
- `.embed-example-row` + `.eer-card` / `.eer-group` / `.eer-group-label` / `.eer-item` / `.eer-text` / `.eer-vec` / `.eer-image` / `.eer-caption` (CH04)
- `.rag-pipeline-box` 내부 카드(`.rag-step`, `.s-num`, `.s-title`, `.s-desc`, `.s-meta`, `.rag-arrow`, `.rag-pipeline-title`) — pipeline 카테고리로 옮길지 판단

- [ ] **Step 1: 결정 — 경계 정리**

`rag-step`은 pipeline 내부 카드라 `pipelines/`에 두는 게 정합. `cards/`에는 `chunk-with-meta`·`embed-example-row` 두 군만 둔다. 경계 규칙을 README 상단에 명시.

- [ ] **Step 2: CH04에서 실제 HTML 추출**

```bash
sed -n '269,283p' "projects/사내AI비서_v2/chapters/04-문서를-지식으로-바꾸다.md"   # chunk-with-meta
sed -n '289,314p' "projects/사내AI비서_v2/chapters/04-문서를-지식으로-바꾸다.md"   # embed-example-row
```

- [ ] **Step 3: `cards/README.md` 작성**

2개 컴포넌트를 각각 "언제/HTML/CSS 위치/변형/피해야 할 것" 5항목으로. 특히:
- `chunk-with-meta`: 청크 1건을 "본문 + 메타데이터 라벨"로 시각화. 라벨은 `.cwm-tag` 4개(출처·페이지·분류·chunk_id) 권장.
- `embed-example-row`: 의미 유사 2~3개 묶음 + 의미 다른 1개를 나란히. 오른쪽에 `.eer-image`(임베딩 공간 그림). `.eer-group-label.good` / `.eer-group-label.bad` 2가지 modifier.

- [ ] **Step 4: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/cards/README.md
git commit -m "docs(skill): cards 카테고리 — chunk-with-meta + embed-example-row"
```

---

## Task 6: Comparisons 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/comparisons/README.md`

담당 컴포넌트:
- `.annotated-compare` + `.ac-heading` / `.ac-block.llm` / `.ac-block.truth` / `.ac-label` / `.ac-name` / `.ac-tech` / `.ac-content` / `.ac-strike` / `.ac-note` (CH01 환각 vs 사내규정)
- `.overlap-text-demo` (CH03 청크 오버랩 시각화)
- `.reindex-compare` (CH03 재인덱싱 비교)
- `.cache-diff` (CH07 캐시 전후)
- `.dual-image` + `figure`/`figcaption` (CH04 쿼리 top/bottom)

- [ ] **Step 1: 각 컴포넌트 실제 HTML 추출**

각각 해당 챕터에서 sed로 발췌.

- [ ] **Step 2: `comparisons/README.md` 작성**

5 컴포넌트를 5항목 포맷으로. 특히 "언제 쓰는가" 차별화:
- `annotated-compare`: **A가 틀렸고 B가 맞을 때**. 취소선(`.ac-strike`)으로 오류 구간 강조.
- `overlap-text-demo`: **순차 텍스트에서 겹침 구간을 하이라이트**.
- `reindex-compare`: **전체 재인덱싱 vs 증분** 같은 전략 비교.
- `cache-diff`: **같은 요청의 before/after 시간선** (캐시 전 vs 후).
- `dual-image`: **단순 2분할 이미지**. 다른 의미 비교 아님.

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/comparisons/README.md
git commit -m "docs(skill): comparisons 카테고리 5 컴포넌트 카탈로그"
```

---

## Task 7: Pipelines 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/pipelines/README.md`

담당 컴포넌트:
- `.rag-pipeline-box` + `.rag-pipeline-title` / `.rag-pipeline` / `.rag-step` / `.s-num` / `.s-title` / `.s-desc` / `.s-meta` / `.rag-arrow` (CH01)
- `.rc-timeline` (CH07 비용/시간 타임라인)
- `.ec-cabinet` (CH07 임베딩 캐시 캐비닛)
- `.wrapper-arch` (CH07 래퍼 아키텍처)

- [ ] **Step 1: 실제 HTML 추출**

```bash
sed -n '288,313p' "projects/사내AI비서_v2/chapters/01-환각과-RAG의-첫-만남.md"  # rag-pipeline
grep -n 'rc-timeline\|ec-cabinet\|wrapper-arch' "projects/사내AI비서_v2/chapters/07-실제로-써보니.md"
```

- [ ] **Step 2: `pipelines/README.md` 작성**

4 컴포넌트 × 5항목. 공통 규칙:
- 단계 수는 3~5개 권장 (1개는 불필요, 6 이상은 표로 대체)
- 각 단계에 `비유 한 줄`(`.s-meta`) + `기술 한 줄`(`.s-desc`)

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/pipelines/README.md
git commit -m "docs(skill): pipelines 카테고리 4 컴포넌트 카탈로그"
```

---

## Task 8: Captions 카테고리 작성

**Files:**
- Modify: `.claude/skills/pub-html-build/components-catalog/captions/README.md`

담당 컴포넌트:
- `.rl-caption` (CH06 ReAct 루프 캡션)
- `.eer-caption` (CH04 임베딩 예시 캡션 — cards와 공용이지만 **독립 요소**로 등록)
- `.afm-tag` / `.afm-zone-ch` / `.afm-zone-label` (fullmap 내부용이지만 라벨 원형은 이 카테고리에 기록)
- 그림 캡션 원칙 `*그림 N-N. 설명*` (Markdown만 쓰는 규칙)

- [ ] **Step 1: `captions/README.md` 작성**

포함 항목:
1. **HTML 캡션(div/span 기반)** — rl-caption 등
2. **Markdown 이탤릭 캡션** — `*그림 N-N. 설명*` (이 프로젝트는 Typst 미경유 전자책이라 수동 번호 유지)
3. **인라인 태그/뱃지** — `.afm-tag`, `.cwm-tag`

**피해야 할 것** 섹션에 "캡션에 반말(`-다/-이다`) 금지", "그림 번호 접두어 콜론 `그림 N-N:` 금지(마침표 `그림 N-N.` OK)" 명시.

- [ ] **Step 2: 커밋**

```bash
git add .claude/skills/pub-html-build/components-catalog/captions/README.md
git commit -m "docs(skill): captions 카테고리 카탈로그"
```

---

## Task 9: `modes/reuse.md` 작성

**Files:**
- Create: `.claude/skills/pub-html-build/modes/reuse.md`

- [ ] **Step 1: 디렉토리 생성**

```bash
mkdir -p ".claude/skills/pub-html-build/modes"
```

- [ ] **Step 2: `reuse.md` 작성**

파일 내용:

```markdown
# Mode: Reuse (기본 재사용)

## 언제 쓰는가

새 책이 기존 디자인(타이포·박스·카드·다이어그램)을 그대로 재사용하고, **브랜드 색상/로고만** 바꾸는 경우. 이 스킬의 기본 모드.

## 절차

1. **새 책 초기화**
   ​```bash
   bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
   ​```
   - `chapters/`, `assets/`, `book/{front,back,build,output}` 생성
   - `book/tokens.css` 오버라이드 템플릿 자동 심기

2. **브랜드 토큰 오버라이드**
   - `projects/<새-책이름>/book/tokens.css` 수정
   - 가능 변수: `--color-accent-*`, `--color-text-*`, `--color-border-*`, `--font-*`
   - **기본 토큰 파일 건드리지 않음** (`.claude/skills/pub-html-build/styles/tokens.css`)

3. **컴포넌트 조립**
   - [`components-catalog/`](../components-catalog/)에서 필요한 블록을 복사해 챕터 원고에 붙여넣기
   - 카테고리 색인: boxes / fullmap / cards / comparisons / pipelines / captions

4. **빌드**
   ​```bash
   python .claude/skills/pub-html-build/build_pdf_html.py \
     --project-root projects/<새-책이름> \
     --chapter 1
   ​```

## 검증

- [ ] `book/output/<책이름>_ch01.pdf` 생성됨
- [ ] tokens.css에 정의한 브랜드 색상이 결과물에 반영됨
- [ ] 카탈로그에서 복사한 컴포넌트가 렌더링됨(누락 클래스 없음)

## 이 모드로 충분하지 않을 때

- 카탈로그에 없는 **새 컴포넌트**가 필요하다 → [`design-explore.md`](design-explore.md)로 전환
- 전체 톤(레이아웃/타이포)을 바꾸고 싶다 → [`design-explore.md`](design-explore.md)
```

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/modes/reuse.md
git commit -m "feat(skill): modes/reuse.md — 기본 재사용 모드 절차"
```

---

## Task 10: `modes/design-explore.md` 작성

**Files:**
- Create: `.claude/skills/pub-html-build/modes/design-explore.md`

- [ ] **Step 1: 파일 작성**

파일 내용(핵심은 **내장 질문 세트 + 강제 변형 축**이라 superpowers 없이도 동작):

```markdown
# Mode: Design Explore (디자인 탐색)

## 언제 쓰는가

- 카탈로그에 없는 **새 컴포넌트**가 필요
- 책 전체 톤(레이아웃/타이포)을 바꾸고 싶음
- 브랜드 색상 외의 디자인 방향 변경

## 의도 수집 (내장 질문 7개)

책 집필을 시작하는 저자에게 차례로 묻는다. **모든 질문에 답을 받지 않고 다음 단계로 진행 금지.**

1. **타깃 독자** — 이 책을 누가 읽는가? (경력 N년 / 직무 / 관심사)
2. **톤** — 한 줄로 표현하면? (예: "조용하고 단단한" / "실험적이고 대담한" / "친근하고 부드러운")
3. **유사 책** — 디자인적으로 참고할 책/사이트 2~3개 (있으면 URL, 없으면 "없음")
4. **금기 요소** — 절대 들어가면 안 되는 것 (예: "이모지 금지", "네온 컬러 금지", "과도한 그라데이션 금지")
5. **주인공 컴포넌트** — 이 책에서 가장 자주 등장할 시각 요소 1~2개 (예: "실습 코드 박스", "대화문", "다이어그램")
6. **분량 감** — 한 챕터 평균 몇 페이지? 이미지/다이어그램 비중은? (저·중·고)
7. **파이프라인** — PDF 인쇄본도 만들 예정인가? (Y면 Typst 경유 가능, N이면 전자책만)

답변을 [`projects/<책>/planning/design-brief.md`](../../../../projects/) 같은 경로에 저장.

## 카탈로그 우선 검토

답변을 기반으로 [`../components-catalog/`](../components-catalog/) 전체를 훑어 **재사용 가능한 컴포넌트 리스트**를 먼저 뽑는다. 80% 이상이 재사용 가능하면 이 모드를 종료하고 [`reuse.md`](reuse.md)로 전환한다.

재사용 불가 컴포넌트만 아래 "신규 설계" 단계로.

## 신규 설계 — 강제 변형 4축

각 신규 컴포넌트에 대해 다음 4축을 **반드시** 하나씩 변형으로 뽑는다. 자유 발상은 금지(품질 편차 방지).

| 축 | 방향 | 예시 |
|----|------|------|
| A. **고급(Editorial)** | 여백 크게, 세리프 제목, 단색 액센트 | `Wired`, `The New Yorker` 디지털 기사 |
| B. **캐주얼(Playful)** | 둥근 코너, 파스텔, 손글씨 느낌 일러 | `Duolingo`, `Figma` 블로그 |
| C. **미니멀(Technical)** | 격자 정렬, 모노스페이스 강조, 대비 |`Stripe Docs`, `Linear` |
| D. **대담(Bold)** | 큰 블록 컬러, 굵은 산세리프, 강한 그림자 | `Vercel`, `Posthog` 랜딩 |

각 변형을 **HTML+CSS 미리보기 페이지**로 만들어 브라우저로 열어 유저가 고른다. (`pub-studio` 스킬의 표지 위자드 패턴 차용)

### 실행 예

​```bash
# 예: ".chapter-note" 라는 신규 박스를 만들 때
python .claude/skills/pub-html-build/scripts/component_variants.py \
  --component chapter-note \
  --axes A,B,C,D \
  --out projects/<책>/design-preview/chapter-note.html
open projects/<책>/design-preview/chapter-note.html
​```

(`component_variants.py`는 Task 11에서 명세만 잡고, 실제 구현은 별도 PR로.)

## 선택 후 반영

1. `styles/components.css`에 클래스 정의 추가
2. [`../components-catalog/<카테고리>/README.md`](../components-catalog/)에 "언제 쓰는가 / HTML 예 / CSS 위치 / 변형 / 피해야 할 것" 5항목으로 등록
3. 첫 사용 챕터의 마크다운에 실제 HTML 삽입

## superpowers 연계 (선택)

`superpowers:brainstorming`이 설치돼 있으면 "의도 수집" 단계를 이 스킬로 대체해 더 깊이 있는 대화를 나눌 수 있다. 없어도 위 7개 질문으로 충분하다.

​```
if superpowers 설치됨:
    superpowers:brainstorming 호출 → 결과를 design-brief.md에 저장
else:
    내장 7개 질문 순회
​```

## 검증

- [ ] `design-brief.md`에 7개 질문 모두 답변 기록됨
- [ ] 카탈로그 재사용 리스트 작성됨 (재사용 %)
- [ ] 신규 컴포넌트별 4축 변형 모두 프리뷰됨
- [ ] 선택된 변형이 `styles/components.css` + 카탈로그 양쪽에 기록됨
```

- [ ] **Step 2: 커밋**

```bash
git add .claude/skills/pub-html-build/modes/design-explore.md
git commit -m "feat(skill): modes/design-explore.md — 내장 질문 7개 + 강제 변형 4축"
```

---

## Task 11: `scripts/component_variants.py` 명세 (실구현은 후속 PR)

**Files:**
- Create: `.claude/skills/pub-html-build/scripts/component_variants.SPEC.md`

- [ ] **Step 1: 스펙 문서만 작성**

```markdown
# component_variants.py 스펙

## 역할

디자인 탐색 모드(`modes/design-explore.md`)에서 신규 컴포넌트의 4축 변형을 HTML 프리뷰 페이지로 생성.

## 인자

| 플래그 | 의미 |
|-------|------|
| `--component NAME` | 컴포넌트 클래스명(예: `chapter-note`) |
| `--axes A,B,C,D` | 생성할 변형 축(쉼표 구분). 기본 전체 |
| `--out PATH` | 결과 HTML 경로 |
| `--sample-text TEXT` | 컴포넌트 내부에 넣을 샘플 텍스트(기본: "샘플 본문") |

## 산출물

단일 HTML 파일. 상단에 `<style>`로 4개 변형 CSS 포함, 하단에 4열 그리드로 렌더.

유저가 브라우저에서 확인 후 `--select A|B|C|D`로 재실행하면 선택된 CSS를 `styles/components.css`에 append.

## 구현 (향후 PR)

- Python, Jinja2 템플릿 1개
- 외부 의존 없음
- 실행 시간 1초 이내 목표
```

- [ ] **Step 2: 커밋**

```bash
git add .claude/skills/pub-html-build/scripts/component_variants.SPEC.md
git commit -m "docs(skill): component_variants.py 스펙 — 4축 변형 프리뷰 툴"
```

---

## Task 12: `SKILL.md` 재작성

**Files:**
- Modify: `.claude/skills/pub-html-build/SKILL.md`

- [ ] **Step 1: 현재 SKILL.md 확인**

```bash
cat ".claude/skills/pub-html-build/SKILL.md"
```

- [ ] **Step 2: 재작성 (진입점 + 분기 가이드)**

파일 내용:

```markdown
---
name: pub-html-build
description: Use when building a book project from Markdown chapters to HTML/PDF. Owns templates, design tokens, custom markdown blocks, and the Playwright-based PDF pipeline. Invoke with --project-root to point at the book source.
---

# pub-html-build

마크다운 챕터 → HTML → PDF(전자책) 파이프라인. 이 프로젝트의 **HTML 출판 경로 전담**.

## 이 스킬을 언제 쓰는가 (2가지 모드)

| 시나리오 | 모드 |
|---------|------|
| 디자인 그대로 재사용 (브랜드 컬러만 바꾸기) | [`modes/reuse.md`](modes/reuse.md) |
| 새 컴포넌트/새 톤 탐색 | [`modes/design-explore.md`](modes/design-explore.md) |

## 컴포넌트 카탈로그

이 스킬이 제공하는 HTML/CSS 컴포넌트는 [`components-catalog/`](components-catalog/)에 카테고리별로 정리돼 있다. 새 챕터 집필 시 **여기서 조립**하는 게 우선이다. 없으면 design-explore 모드.

| 카테고리 | 담당 |
|---------|------|
| [boxes](components-catalog/boxes/) | `:::`/`::::` directive 박스 |
| [fullmap](components-catalog/fullmap/) | 책 전체 구성도 |
| [cards](components-catalog/cards/) | 청크·임베딩 카드 |
| [comparisons](components-catalog/comparisons/) | A vs B 비교 |
| [pipelines](components-catalog/pipelines/) | 흐름·타임라인 |
| [captions](components-catalog/captions/) | 라벨·캡션 |

## 빌드 실행 (기본)

​```bash
python .claude/skills/pub-html-build/build_pdf_html.py \
  --project-root projects/<책> \
  --chapter N
​```

옵션:
- `--project-root PATH` (필수): 책 프로젝트 루트
- `--chapter N` (선택): 특정 챕터만 빌드
- `--html-only`: HTML 중간 산출물만 생성 (PDF 생략)
- `--no-pagedjs`: Chromium 기본 인쇄 (빠른 빌드)

## 새 책 초기화

​```bash
bash .claude/skills/pub-html-build/scripts/init_book.sh projects/<새-책이름>
​```

## 파일 구조

- `templates/chapter-template.html` — Jinja2 챕터 템플릿
- `styles/tokens.css` — 디자인 토큰 (브랜드 오버라이드 가능)
- `styles/{fonts,base,components,diagrams,print}.css` — 공용 스타일
- `build_pdf_html.py` — 파이프라인 진입점 (markdown-it + Pygments + Playwright)
- `modes/` — 재사용/탐색 2모드
- `components-catalog/` — 컴포넌트 카탈로그 (6 카테고리)

## superpowers 연계 (선택)

설치돼 있으면 `modes/design-explore.md`의 "의도 수집" 단계에서 `superpowers:brainstorming`을 호출할 수 있다. 없어도 내장 7개 질문으로 충분히 탐색 가능.
```

- [ ] **Step 3: 커밋**

```bash
git add .claude/skills/pub-html-build/SKILL.md
git commit -m "refactor(skill): SKILL.md 진입점 재작성 — 2모드 분기 + 카탈로그 색인"
```

---

## Task 13: 메모리 업데이트

**Files:**
- Modify: `~/.claude/projects/-Users-nomadlab-Desktop-----workspace-coding-study--------v2/memory/project_pub_html_skill.md`
- Modify: `~/.claude/projects/-Users-nomadlab-Desktop-----workspace-coding-study--------v2/memory/MEMORY.md`

- [ ] **Step 1: `project_pub_html_skill.md` 갱신**

이전 기록에 `modes/`와 `components-catalog/` 추가. 핵심은:
- "superpowers 유무와 무관하게 자기완결" 원칙
- "카탈로그에서 먼저 조립, 없으면 design-explore"

- [ ] **Step 2: `MEMORY.md` 인덱스 줄 갱신**

기존 줄:
```
- [project_pub_html_skill.md](project_pub_html_skill.md) — HTML→PDF 파이프라인 스킬 추출 완료. templates·styles·build_pdf_html.py를 .claude/skills/pub-html-build/로 이동 (2026-04-14)
```

→

```
- [project_pub_html_skill.md](project_pub_html_skill.md) — HTML→PDF 자기완결형 스킬. modes/(reuse·design-explore) + components-catalog/(6 카테고리) 보유. superpowers 선택 연계 (2026-04-14)
```

- [ ] **Step 3: 커밋 없음** (메모리는 outer repo 밖)

---

## Task 14: 검증 (Verification-before-completion)

- [ ] **Step 1: 전수 링크 체크**

```bash
# 카탈로그 내부 상호 참조가 깨지지 않았는지
find ".claude/skills/pub-html-build" -name "*.md" \
  -exec grep -Hn '\]\(\.' {} \; \
  | head -50
```

각 상대 경로가 실제 파일을 가리키는지 육안 확인.

- [ ] **Step 2: 기존 빌드가 깨지지 않았는지**

```bash
python ".claude/skills/pub-html-build/build_pdf_html.py" \
  --project-root "projects/사내AI비서_v2" \
  --chapter 1 \
  --html-only
```

기대: 성공. `projects/사내AI비서_v2/book/build/01-*.html` 갱신. 이 리팩터는 styles/ 파일을 건드리지 않으므로 동일 결과여야 한다.

- [ ] **Step 3: 카탈로그 HTML 예시의 CSS 매칭 스팟 체크**

랜덤 3개 컴포넌트 선정 후 각 HTML 예시의 클래스가 `styles/components.css`에 실제 정의돼 있는지 확인:

```bash
for cls in goal-box arch-fullmap cwm-card; do
  grep -n "\.$cls" ".claude/skills/pub-html-build/styles/components.css" | head -1
done
```

모두 매칭되어야 함.

- [ ] **Step 4: 최종 리포트 작성 + 푸시**

리포트 내용:
- 생성된 파일 개수
- 추가된 카탈로그 컴포넌트 개수(카테고리별)
- 검증 결과 (빌드 성공 여부)

```bash
git log --oneline -15
git push origin book_v6
```

---

## Self-Review 체크리스트

**Spec coverage:**
- [x] modes/ 2개 생성 (reuse + design-explore) → Task 9, 10
- [x] components-catalog/ 6 카테고리 → Task 2~8
- [x] SKILL.md 재작성 → Task 12
- [x] 메모리 갱신 → Task 13
- [x] superpowers 선택 연계 → Task 10 (design-explore.md 내부)
- [x] 기존 빌드 비회귀 검증 → Task 14

**Placeholder scan:** "TBD"/"추후" 없음. 각 Task는 실행 명령·파일 내용 구체적으로 포함.

**Type consistency:** 카테고리 이름(boxes/fullmap/cards/comparisons/pipelines/captions)이 Task 2·3·4·5·6·7·8·9·10·12 전체에서 동일.

---

## 실행 권고

Task 1 → 2 → (3~8 병렬 가능) → 9, 10 순차 → 11 → 12, 13 순차 → 14.

**Task 3~8은 서브에이전트 6개 병렬 디스패치가 효율적.** 각 카테고리가 독립적이라 충돌 없음.
