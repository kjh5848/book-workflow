// ── 프로젝트 설정 ──

#let book-title = "ConnectHR"
#let book-subtitle = "사내 AI 비서 만들기 (테스트)"
#let book-description = [사내 문서를 학습한 AI 비서, RAG 시스템을 처음부터 끝까지 만들어보는 실전 가이드]
#let book-header-title = "ConnectHR — 사내 AI 비서 만들기"

// ── 범용 북 템플릿 (Typst) ──
// 이 파일은 스킬(pub-typst-design) 소유. 프로젝트에서 심볼릭 링크로 참조.
// 프로젝트의 book.typ에서 정의한 변수(book-title 등)를 사용합니다.
//
// 필수 변수 (book.typ에서 정의):
//   #let book-title = "책 제목"
//   #let book-subtitle = "부제"
//   #let book-description = [설명]
//   #let book-header-title = "헤더 표시 제목"

// ── 챕터 추적 (헤더용) ──
#let chapter-title = state("chapter-title", none)

// ── 페이지 설정 ──
// 46배판 (188x257mm) — 국내 IT 서적 표준 판형
#set page(
  width: 188mm,
  height: 257mm,
  margin: (top: 20mm, bottom: 28mm, left: 20mm, right: 20mm),
  numbering: "1",
  number-align: center,
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      set text(8pt, fill: rgb("#999999"))
      grid(
        columns: (1fr, 1fr),
        align(left)[#book-header-title],
        align(right)[#chapter-title.get()],
      )
      v(2pt)
      line(length: 100%, stroke: 0.3pt + rgb("#dddddd"))
    }
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 2 {
      align(center, text(9pt, fill: rgb("#888888"))[#counter(page).display()])
    }
  },
)

// ── 폰트 설정 ──
#set text(
  font: ("KoPubDotum_Pro", "Apple SD Gothic Neo"),
  size: 10pt,
  lang: "ko",
  fill: rgb("#1a1a1a"),
)

#set par(
  leading: 1.0em,
  first-line-indent: 0pt,
  justify: true,
)

// ── 제목 스타일 ──
#show heading.where(level: 1): it => {
  chapter-title.update(it.body)
  pagebreak(weak: true)
  v(60pt)  // 챕터 오프닝: 상단 1/3 여백 (출판 표준)
  block(
    width: 100%,
    below: 16pt,
    sticky: true,
    {
      text(26pt, weight: "bold", fill: rgb("#1a1a1a"))[#it.body]
      v(8pt)
      line(length: 100%, stroke: 3pt + rgb("#2563eb"))
    }
  )
  v(14pt)
}

#show heading.where(level: 2): it => {
  v(24pt)
  block(
    width: 100%,
    below: 8pt,
    sticky: true,
    inset: (left: 12pt),
    stroke: (left: 4pt + rgb("#2563eb")),
    text(16pt, weight: "bold", fill: rgb("#1e40af"))[#it.body]
  )
  v(6pt)
}

#show heading.where(level: 3): it => {
  v(16pt)
  block(
    below: 6pt,
    sticky: true,
    text(13pt, weight: "semibold", fill: rgb("#1e3a5f"))[#it.body]
  )
  v(4pt)
}

#show heading.where(level: 4): it => {
  v(12pt)
  block(
    below: 4pt,
    sticky: true,
    text(11pt, weight: "semibold", fill: rgb("#374151"))[#it.body]
  )
  v(2pt)
}

// ── 코드 블록 (페이지 넘김 허용) ──
#show raw.where(block: true): it => {
  set text(size: 8pt, weight: "bold", font: ("Menlo", "KoPubDotum_Pro"))
  block(
    width: 100%,
    fill: white,
    inset: (x: 16pt, y: 14pt),
    radius: 8pt,
    stroke: 1pt + rgb("#d1d5db"),
    breakable: true,
    text(fill: rgb("#1a1a1a"))[#it]
  )
}

// ── 인라인 코드 ──
#show raw.where(block: false): it => {
  box(
    fill: rgb("#f3f4f6"),
    inset: (x: 4pt, y: 2pt),
    radius: 3pt,
    text(size: 8.5pt, fill: rgb("#1e40af"), font: ("Menlo", "KoPubDotum_Pro"))[#it]
  )
}

// ── 인용 블록 (blockquote) ──
#show quote.where(block: true): it => {
  block(
    width: 100%,
    above: 10pt,
    below: 10pt,
    inset: (left: 14pt, right: 14pt, top: 10pt, bottom: 10pt),
    stroke: (left: 3pt + rgb("#93b4e8")),
    fill: rgb("#f5f8ff"),
    radius: (right: 4pt),
    {
      set par(justify: true, leading: 0.9em)
      text(size: 9pt, fill: rgb("#4b5563"))[#it.body]
    }
  )
}

// ── 표 스타일 ──
#set table(
  stroke: (bottom: 0.5pt + rgb("#e5e7eb")),
  inset: (x: 10pt, y: 8pt),
  fill: (_, y) => if y == 0 { rgb("#1e40af") } else if calc.odd(y) { rgb("#f8fafc") } else { white },
)

#show table.cell.where(y: 0): set text(fill: white, weight: "medium")

#show table: it => {
  set text(size: 8.5pt)
  block(breakable: true)[#it]
}

// ── 볼드/이탤릭 ──
#show strong: set text(fill: rgb("#1e3a5f"))
#show emph: set text(fill: rgb("#6b7280"))

// ── 수평선은 후처리에서 #v + block으로 변환됨 ──

// ── figure 스타일 ──
#show figure: it => {
  v(8pt)
  align(center, it.body)
  if it.caption != none {
    v(2pt)
    align(center, text(8pt, fill: rgb("#6b7280"))[#it.caption.body])
  }
  v(4pt)
}

// ── 링크 스타일 ──
#show link: it => {
  text(fill: rgb("#2563eb"))[#it]
}

// ── 자동 크기 조절 이미지 ──
// 남은 페이지 공간을 감지하여 이미지 크기를 자동으로 조절합니다.
// max-width: 이미지 최대 너비 비율 (0.0~1.0)
// 이미지가 남은 공간보다 크면 자동 축소, 너무 작아지면 다음 페이지로 넘김
#let auto-image(path, alt: none, max-width: 0.7) = layout(size => context {
  let target-width = size.width * max-width
  let img = image(path, width: target-width)
  let img-size = measure(img)
  let caption-h = if alt != none { 28pt } else { 0pt }
  let needed = img-size.height + caption-h + 24pt

  let final-width = if needed > size.height and size.height > 120pt {
    // 남은 공간에 맞게 축소 시도
    let available = size.height - caption-h - 24pt
    let ratio = available / img-size.height
    if ratio >= 0.5 {
      target-width * ratio
    } else {
      target-width  // 너무 작아지면 원래 크기 (다음 페이지로)
    }
  } else {
    target-width
  }

  if alt != none {
    figure(image(path, width: final-width), caption: [#alt])
  } else {
    align(center, image(path, width: final-width))
  }
})

// ── 사이드 이미지 (2열 레이아웃) ──
// 작은 이미지를 텍스트 옆에 나란히 배치합니다.
// img-width: 이미지 열 너비 비율 (0.0~1.0), 나머지가 텍스트 열
#let side-image(path, body, img-width: 0.35, gap: 16pt) = {
  v(8pt)
  grid(
    columns: (img-width * 100% - gap / 2, 1fr),
    column-gutter: gap,
    align: (center + horizon, left + top),
    image(path, width: 100%),
    body,
  )
  v(8pt)
}

// ══════════════════════════════════════
// 표지
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(1fr)
  #align(center)[
    // 상단 장식선
    #line(length: 40%, stroke: 2pt + rgb("#2563eb"))
    #v(24pt)
    #text(42pt, weight: "bold", fill: rgb("#1e40af"), tracking: 2pt)[#book-title]
    #v(16pt)
    #line(length: 60%, stroke: 0.5pt + rgb("#93c5fd"))
    #v(16pt)
    #text(15pt, fill: rgb("#374151"), weight: "medium")[#book-subtitle]
    #v(48pt)
    #block(
      width: 70%,
      inset: (x: 20pt, y: 16pt),
      radius: 4pt,
      fill: rgb("#f8fafc"),
      stroke: 0.5pt + rgb("#e2e8f0"),
      text(10.5pt, fill: rgb("#64748b"))[#book-description]
    )
  ]
  #v(1fr)
  #align(center)[
    #text(9pt, fill: rgb("#94a3b8"))[RAG 실전 가이드]
  ]
  #v(20pt)
]

// ══════════════════════════════════════
// 목차 (자동 생성)
// ══════════════════════════════════════
#page(numbering: none, header: none, footer: none)[
  #v(30pt)
  #block(width: 100%, below: 12pt, {
    text(24pt, weight: "bold", fill: rgb("#1a1a1a"))[목차]
    v(6pt)
    line(length: 100%, stroke: 3pt + rgb("#2563eb"))
  })
  #v(12pt)

  #show outline.entry.where(level: 1): set text(weight: "bold", size: 11pt)
  #show outline.entry.where(level: 1): it => {
    v(6pt)
    it
  }
  #show outline.entry.where(level: 3): set text(size: 8.5pt, fill: rgb("#6b7280"))

  #outline(
    title: none,
    indent: 1.5em,
    depth: 2,
  )
]

// ══════════════════════════════════════
// 본문 시작 — 이 아래에 Pandoc 변환 내용이 들어갑니다
// ══════════════════════════════════════

= Ch.1: AI에게 물어봤더니 거짓말을 한다 --- v0.1

#quote(block: true)[
이번 버전: 시작 → v0.1 한 줄 요약: LLM은 모르는 것도 자신있게 대답한다 핵심 개념: LLM, 환각(Hallucination), 로컬 LLM
]

== 이야기 파트

=== 미션이 떨어졌다

커넥트에 입사한 지 3일 차. 아직 사내 Wi-Fi 비밀번호를 포스트잇에 적어 모니터에 붙여놓던 시절입니다.

오전 10시, 팀장이 자리로 다가옵니다.

#strong[팀장]: "AI로 사내 문서 검색 시스템 만들어봐. 직원들이 규정이나 정책 찾는 게 너무 번거롭다고 해서."

#emph[사내 문서 검색? AI? ChatGPT 같은 거 만들라는 건가?]

#strong[나]: "어떤 문서요?"

#strong[팀장]: "인사규정, 보안규정, 복지규정… 직원들이 매번 인사팀에 전화하거든. '연차 몇 개야?', '야근 식대 되나?' 이런 거. AI가 대신 답해주면 좋겠어."

얼핏 쉬워 보였습니다. ChatGPT도 뭐든 잘 대답하잖아요. LLM에게 직접 물어보면 되는 거 아닐까요?

=== 세상의 모든 책을 읽은 박사

LLM이 뭔지부터 잠깐 짚고 가겠습니다.

LLM은 #strong[세상의 모든 책을 읽은 박사]라고 생각하면 됩니다. 인터넷에 있는 수십억 개의 문장을 학습해서, 질문하면 그럴듯한 답변을 만들어냅니다.

여기서 중요한 건 #strong["그럴듯한"] 이라는 단어입니다.

이 박사님은 세상의 일반적인 지식은 엄청나게 잘 알고 있어요. "파이썬에서 리스트 정렬하는 법"이나 "HTTP 상태 코드 404가 뭐야" 같은 건 완벽하게 답합니다.

그런데 한 가지 문제가 있습니다. #strong[우리 회사 내부 문서는 읽은 적이 없어요.]

커넥트의 인사규정, 보안정책, 복지제도 --- 이런 건 인터넷에 공개된 적이 없으니까요. 이 박사님의 수십억 권 서재에 우리 회사 취업규칙은 없습니다.

그런데 이 박사님에게는 치명적인 습관이 하나 있어요.

#strong[모르면 모른다고 하지 않습니다.]

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_test/assets/CH01/01_llm-hallucination.png", alt: [그림 1-1: LLM은 학습하지 않은 사내 문서에 대해 환각을 일으킵니다], max-width: 0.6)

=== 자신있게 틀린 답변

#emph[일단 해보자.] 그렇게 생각하고 LLM에게 바로 물어봤습니다.

"우리 회사 커넥트의 신입사원 연차 발생 규정이 어떻게 돼?"

잠시 후 답변이 돌아왔습니다. 아주 자신있는 어조로요.

근데 내용이 이상합니다. 근로기준법에 나오는 일반적인 연차 규정을 마치 커넥트의 규정인 것처럼 답하고 있었어요. "입사 1년 미만 시 매월 1일의 연차가 발생하며…"라고요.

커넥트의 실제 규정은 전혀 다릅니다. 신입사원은 3년간 연차가 없고, 대신 매월 리프레시 데이를 제공하거든요. LLM은 이 독특한 규정을 알 리가 없습니다.

#emph[거짓말을 하고 있잖아. 그것도 아주 자신있게.]

이걸 #strong[환각(Hallucination)] 이라고 부릅니다. AI가 모르는 것을 마치 아는 것처럼, 그럴듯하게 지어내는 현상이에요. 시험에서 답을 모르는데 뭐라도 쓰는 학생처럼요. 다만 이 학생은 빈 칸으로 두는 법을 모릅니다. 항상 뭔가를 써내요.

사내 AI 비서에서 이건 치명적입니다. 직원이 "연차 며칠이야?"라고 물었는데 엉터리 답이 나오면요? 그걸 믿고 휴가 계획을 세우면요?

#emph[이대로는 안 되겠다. 다른 방법을 찾아야 해.]

=== 이것만은 기억하자

- LLM은 세상의 모든 책을 읽은 박사지만, #strong[우리 회사 문서는 읽은 적이 없습니다.] 모르는 것도 자신있게 지어내는 습관이 있어요. 이걸 환각이라고 부릅니다.
- 다음 챕터에서는 "그러면 우리가 정보를 직접 알려주면 어떨까?"라는 아이디어를 시도해봅니다.

== 기술 파트

=== 용어 정리

#figure(
  align(center)[#table(
    columns: (1fr, 1fr, 1fr),
    align: (auto,auto,auto,),
    table.header([이야기 속 비유], [진짜 용어], [정식 정의],),
    table.hline(),
    [세상의 모든 책을 읽은 박사], [LLM (Large Language Model)], [대규모 텍스트 데이터로 학습된 언어 모델. 입력된 텍스트를 바탕으로 다음에 올 가능성이 높은 텍스트를 생성합니다.],
    [모르면서 자신있게 지어내는 것], [환각 (Hallucination)], [LLM이 학습 데이터에 없는 내용을 사실인 것처럼 생성하는 현상. 특히 특정 조직의 내부 정보처럼 학습 데이터에 포함되지 않은 질문에서 자주 발생합니다.],
    [내 컴퓨터 안의 AI 엔진], [Ollama], [로컬 환경에서 LLM을 실행할 수 있게 해주는 도구. 클라우드 API 없이 내 컴퓨터에서 직접 AI를 돌릴 수 있습니다.],
  )]
  , kind: table
  )

=== 이번 챕터 파일 구조

```
v0.1/
└── main.py    [실습] LLM 연결 + 질문 → 환각 답변 체험
```

=== 환경 설정

실습을 시작하기 전에 Ollama와 모델을 준비합니다.

#strong[\1. Ollama 설치]

Ollama 공식 사이트에서 설치 파일을 다운로드합니다.

```bash
# macOS (Homebrew)
brew install ollama
```

#strong[\2. 모델 다운로드]

이 책에서는 DeepSeek R1:8b 모델을 사용합니다. 추론 능력이 뛰어나면서도 로컬에서 돌릴 수 있는 크기입니다.

```bash
ollama pull deepseek-r1:8b
```

#strong[\3. Ollama 서버 실행]

```bash
ollama serve
```

#quote(block: true)[
#strong[팁: 모델 크기와 RAM] deepseek-r1:8b는 약 5GB의 RAM을 사용합니다. 컴퓨터 RAM이 부족하면 `deepseek-r1:1.5b`로 대체할 수 있습니다.
]

#strong[\4. Python 환경 준비]

```bash
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
pip install langchain langchain-ollama
```

=== 실습: main.py

아래 코드를 `main.py`에 작성합니다.

```python
from langchain_ollama import ChatOllama

# 로컬 LLM 연결
llm = ChatOllama(model="deepseek-r1:8b", temperature=0)

# 질문: 모델이 학습했을 리 없는 가상의 회사 규정
question = "우리 회사(커넥트)의 신입사원 연차 발생 규정이 어떻게 돼?"

print(f"질문: {question}\n")
response = llm.invoke(question)
print(f"답변:\n{response.content}")
```

이 코드가 하는 일은 단순합니다.

+ `ChatOllama`로 로컬에서 돌아가는 DeepSeek R1 모델에 연결합니다.
+ 커넥트의 연차 규정을 질문합니다.
+ LLM의 답변을 출력합니다.

`temperature=0`은 답변의 랜덤성을 없앤 설정입니다. 같은 질문에 항상 같은 답이 나오게 합니다.

실행해봅니다.

```bash
python main.py
```

결과를 보면 LLM이 근로기준법의 일반적인 연차 규정을 커넥트의 규정인 것처럼 답합니다. 커넥트만의 독특한 규정(3년간 연차 없음, 리프레시 데이 제공)은 전혀 언급하지 않습니다.

이것이 환각입니다. LLM은 "커넥트"라는 회사를 모르지만, 질문에 답하려고 자신이 알고 있는 가장 그럴듯한 정보를 끌어와 대답합니다.

#auto-image("/Users/nomadlab/Desktop/김주혁/workspace/coding-study/집필에이전트 v2/projects/사내AI비서_test/assets/CH01/01_hallucination-result.png", alt: [그림 1-2: LLM이 자신있게 내놓은 엉터리 답변], max-width: 0.6)

=== 더 알아보기

- #strong[왜 로컬 LLM인가요?] --- 사내 문서를 다루기 때문에 외부 API로 보내면 보안 문제가 생길 수 있습니다. Ollama를 사용하면 모든 데이터가 내 컴퓨터에서만 처리됩니다.
- #strong[DeepSeek R1은 어떤 모델인가요?] --- 중국 DeepSeek사에서 만든 오픈소스 LLM으로, 특히 추론(Reasoning) 능력이 뛰어납니다. 8b 버전은 80억 개의 파라미터를 가진 모델로, 일반 노트북에서도 실행 가능합니다.

#v(4pt)
#block(width: 100%, height: 0.5pt, fill: rgb("#e5e7eb"))
#v(4pt)
