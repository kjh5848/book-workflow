# 스토리 이미지 디자인 토큰 단일 진실원

이 파일은 **챕터 본문에 등장하는 "스토리 이미지"** (오프닝, 감정·환각·실패 순간, 비유 시각화)의 디자인 토큰을 정의한다. **다이어그램·플로우 카드·터미널 캡처와는 별개의 시스템**이다.

- **다이어그램 토큰** (Mermaid/D2/HTML): `.claude/rules/brand-tokens.md` 참조 — 본문 흰 배경 + 인디고/웜 액센트 + 무채색
- **스토리 이미지 토큰** (이 파일): 흑백 라인아트 + 웜 액센트 1색 + 한글 라벨/제목 포함

> **단일 진실원**: 토큰 변경은 이 파일에서만. 베이스 프롬프트(`.claude/skills/visual/references/image.md`)는 이 파일을 참조한다.
>
> **딥인터뷰 결정 기록 (2026-05-09 · 사내AI비서_v2)**: 흑백+웜 액센트 1색 / 인물 4:5·개념 16:9 / CH01 5장을 스타일 앵커 / 인물 외형 앵커 문장 토큰화 / 그림 안 한글 제목 포함 / 비유 사물 10개 사전 고정.

---

## 1. 모델·해상도

| 항목 | 값 |
|------|----|
| 기본 모델 | **gpt-image-2** (OpenAI, 2026 출시. 한글 텍스트 정확 렌더링·참조 이미지 16장·8장 일관성) |
| 모드 | Thinking (캐릭터·팔레트 일관성이 필요한 모든 챕터) / Instant (단발 추상 개념도) |
| 해상도 | 2K (`2048x2560` for 4:5, `2560x1440` for 16:9). 인쇄 본문 720px width 표시 기준 |
| 출력 포맷 | PNG (라인아트 깨끗한 경계) |

---

## 2. 화풍 토큰

### 2.1 베이스 미디엄

| 토큰 | 값 |
|------|----|
| `--style` | minimalist black ink line illustration |
| `--medium` | flat 2D vector line art (no perspective, no 3D) |
| `--line-weight` | uniform medium-thick line, ~3px feel, consistent across all elements |
| `--line-style` | clean continuous strokes; no sketch, no double-line, no calligraphic taper |
| `--background` | solid pure white (#ffffff). No paper texture. No gradient |
| `--shading` | **none**. No gray fills, no hatching, no shadow, no gradient. Flat white interior |

### 2.2 컬러 시스템 — "흑백 + 웜 액센트 1색"

| 역할 | 토큰 | HEX | 사용처 |
|------|------|-----|--------|
| 본문 라인·텍스트 | `--ink-primary` | `#0d0d0d` | 인물·소품·말풍선·라벨 외곽선·한글 제목 |
| 보조 그레이 (지나친 디테일 분리용, 최소 사용) | `--ink-secondary` | `#5b5b5b` | 그림자 대신의 약한 보조선. 옷주름 등 극소수 |
| 웜 액센트 1색 | `--accent-warm` | `#e07a3c` | 아래 §2.3 적용 규칙 |
| 흰 배경 | `--bg` | `#ffffff` | 모든 이미지 단일 배경 |

> 위 4색 외 어떤 색도 등장하지 않는다. 가능한 한 검정·흰·웜 3색 안에서 끝낸다.

### 2.3 웜 액센트 적용 규칙 — "감정·주의의 순간" 시그니처

웜 액센트는 책 전체에서 **하나의 시그니처**로 작동한다. 다이어그램의 `--color-accent-warm`(`::remember`/`::tip`/`.term`)과 결을 맞춰, 종이책에서 "여기는 멈추고 보세요"라는 신호가 통일된다.

**적용 대상** (이 두 가지만):

1. **이야기의 넘김점 소품** — 1장당 1~2개. 예: 커피의 김, 치는 포스트잇, 주인공 머리 위의 "!", 메모장의 하이라이트, 발견의 순간에 들리는 책의 모서리
2. **파괴·실패·환각 표시** — 빨간색 대신 웜 주황으로. ✗ 표시, 점선 차단선, 깨진 외곽선, 환각 말풍선의 가장자리. **빨강은 사용하지 않는다** (인쇄 일관성 + 책 전체의 이성적 톤 유지)

**금지 적용처**:

- 인물의 옷·피부·머리카락 (의상·앵커 아이템 §3 참조)
- 큰 면적 (배경·바닥·벽 등)
- 텍스트 본문
- 모든 라인의 굵기·색을 일률 채색

> 원칙: **웜 액센트는 "한 장에 한 개의 시그널"**. 두 군데 이상 들어가면 시선이 분산된다.

### 2.4 종횡비

| 시나리오 | 종횡비 | 슬롯 |
|---------|------|------|
| **인물·소품 장면** (오픈이가 등장하거나 책상·물건 중심) | **4:5 (세로)** | `--ratio-figure: 4:5` |
| **개념 시각화** (외부인 vs 회사 / 컨텍스트 오버플로 / 사서의 두 방 / 코사인 등 추상 흐름) | **16:9 (가로)** | `--ratio-concept: 16:9` |
| 챕터 오프닝 | 4:5 (인물이 있으므로) | — |
| 책 전체 로드맵 (CH01 journey-roadmap) | 16:9 | — |

> 한 장 안에 인물과 추상 개념이 **둘 다** 핵심이면 4:5를 우선한다 (B5 세로 페이지 친화적).

---

## 3. 캐릭터 앵커 (등장인물 외형 토큰)

오픈이·팀장·동료 세 인물은 책 전체에서 외형을 고정한다. CH01 5장이 **스타일 앵커 세트**이며, 모든 새 이미지는 이 5장을 참조 이미지로 첨부해 일관성을 잠근다.

### 3.1 오픈이 — 신입사원, 주인공

```
A young Korean office worker character drawn in minimalist black line art.
Round face, simple bowl-cut short hair (no fringe overlap), small round eyes
drawn as two solid dots, no nose, simple curved mouth line for expression.
Plain crew-neck T-shirt, no logo. Slim trousers. Sneakers.
Body proportions: head about 1/4 of total height (slightly chibi).
Stance is relaxed, slightly slouched (a junior on day-3 of a new job).
This is the protagonist '오픈이' — do not redesign this appearance.
The only color allowed on this character is a single warm-orange
accent (#e07a3c) on a small item: a sneaker stripe OR a wristwatch face,
chosen consistently per chapter set.
```

### 3.2 팀장 — 시니어, 결정자

```
A Korean middle-manager character drawn in minimalist black line art.
Slightly taller than 오픈이. Side-parted short hair, square jaw,
glasses (rectangular frames), thin solid-line eyes, neutral mouth.
Plain shirt with rolled sleeves OR a thin sweater. Slim trousers.
Always carries one of: a coffee mug (with a small steam curl), a notepad,
or a paper folder. Stance: upright, hand sometimes gesturing toward 오픈이.
This is '팀장' — do not redesign this appearance.
No color on this character.
```

### 3.3 동료 — 옆자리, 가벼운 조언자

```
A Korean junior coworker character drawn in minimalist black line art.
Same height as 오픈이 or slightly shorter. Tied-back hair OR a small ponytail
(consistent across appearances), small round glasses, a single solid-dot
eye expression, small relaxed smile. Hooded jacket OR cardigan over a t-shirt.
Always shown swiveled in an office chair, leaning on the chair back.
This is '동료' — do not redesign this appearance.
No color on this character.
```

### 3.4 사서 (CH05~CH07 비유 캐릭터)

```
A friendly Korean librarian character drawn in minimalist black line art.
Mid-thirties, glasses, hair tied back, plain knit cardigan, A-line skirt
or wide trousers. Always holds or stands near a book / a memo card / a
key — never empty-handed. Calm posture, slight forward lean to listen.
This is the '사서' metaphor character — do not redesign this appearance.
No color on this character. The only warm accent allowed is the book
spine OR the memo card edge being warm-orange when that object is the
focus of the scene.
```

> 새 이미지 생성 시 위 4개의 앵커 문장 중 **등장 인물 해당 블록만** 프롬프트에 포함한다. 등장하지 않는 인물의 앵커는 절대 포함하지 않는다 (모델이 강제로 그려넣음).

---

## 4. 비유 사물 사전 (10개 반복 토큰)

같은 비유가 챕터마다 다르게 그려지면 독자가 혼란하다. 아래 10개는 **외형 고정**.

| 사물 | 영문 토큰 | 외형 고정 문장 |
|------|----------|---------------|
| 사서 | `librarian` | §3.4 참조 |
| 메모장 | `memo-pad` | "A small rectangular memo pad with a top spiral binding, single hand-written line drawn as 3 short horizontal strokes" |
| 서가 | `bookshelf` | "A simple 3-tier wooden bookshelf, books shown as plain rectangles with thin vertical line spines, no titles, no decoration" |
| 확대경 | `magnifier` | "A round magnifying glass with a thick handle, perfectly circular lens, single highlight stroke inside" |
| 상자 (컨테이너) | `box` | "An open cardboard box, three flaps visible, tape mark on the side as a single horizontal stroke" |
| 파일철 | `file-binder` | "A 3-ring binder standing upright, label tab on the side, no text on the cover" |
| 도서 카드 (출처) | `library-card` | "A small index card with a single horizontal line at top and 2 short text-lines below, drawn as plain stroke fills" |
| 노트북 컴퓨터 | `laptop` | "A simple opened laptop seen from a 3/4 angle. Plain rectangular screen with no UI inside (only a single small window outline if needed). Closed-flat keyboard. No brand mark" |
| 포스트잇 | `sticky-note` | "A square sticky note with one corner curling up. The Wi-Fi password sticky in CH01 is the canonical reference" |
| 키 (열쇠) | `key` | "A simple old-fashioned key shape, round bow + flat blade, two small notches" |

> 각 사물이 **그 챕터의 핵심 비유**라면 §2.3 규칙에 따라 웜 액센트가 그 사물에 들어갈 수 있다 (예: CH05 메모장의 하이라이트, CH06 사서의 키 손잡이).

---

## 5. 공간감·구도

### 5.1 두 가지 모드

| 모드 | 트리거 | 배경 처리 | 종횡비 |
|------|------|---------|-------|
| **구체 실내** | 오픈이·팀장·동료 등 인물이 등장 | 책상·노트북·의자·창틀 등 정직하게 그림. 한국 사무실 디테일 (포스트잇·텀블러·모니터 받침대) 허용 | 4:5 |
| **추상 개념** | 인물 없이 비유·관계·흐름만 | 배경 비워 흰 캔버스. 요소만 중앙 또는 좌→우 흐름으로 배치 | 16:9 |

> 한 장 안에 두 모드가 섞이지 않는다 (사무실 안에 갑자기 컨텍스트 윈도우 그림이 떠오르는 식 금지).

### 5.2 구도 기본값

- **글로벌 센터링**: 전체 요소의 무게 중심이 프레임 중앙
- **안전 여백**: 요소 외곽이 캔버스 가장자리에서 8% 이상 떨어짐
- **시선 흐름**: 좌→우 (한국어 가로쓰기 일치)
- **앵커 점**: 인물의 얼굴 또는 핵심 사물이 프레임 황금비 교차점

---

## 6. 그림 안 한글 텍스트

gpt-image-2는 한글을 정확히 렌더링한다. CH01의 "입사 3일 차, 첫 번째 미션" 같은 제목을 그림 안에 직접 넣는 현 방식을 유지한다.

### 6.1 허용 위치

| 위치 | 허용 | 예시 |
|------|------|------|
| 그림 하단 중앙의 굵은 한글 제목 | OK | "입사 3일 차, 첫 번째 미션" |
| 인물 머리 위 말풍선 (대사) | OK | "AI 비서 만들어봐" |
| 사물 라벨 (외부인·회사 내부 등) | OK | "외부인", "회사 내부" |
| 작은 부속 라벨 (Wi-Fi PW, 파일명) | OK | "Wi-Fi PW", "regs.pdf" |

### 6.2 한글 텍스트 토큰

```
Korean caption text rendered cleanly in a sans-serif typeface
(Pretendard / Noto Sans KR feel). Bold weight for the bottom-center
chapter line, regular weight for in-scene labels. All Korean text in
solid black (#0d0d0d). Maximum 12 Korean characters per line, single
line preferred. Wrap exact text in double quotes inside the prompt.
```

### 6.3 캡션 중복 방지 규칙

| 그림 안 텍스트 종류 | 그림 밖 마크다운 캡션 | 결과 |
|-------------------|------------------|------|
| 본문 분위기를 이끄는 짧은 제목 ("입사 3일 차") | 다른 문장 (`*그림 1-1. 첫 번째 미션*` 같은 부연) | OK — 의미 보강이라 중복 아님 |
| 그림 안 제목과 동일 문장 | 동일 문장 마크다운 캡션 | **금지** — 한쪽 삭제 |
| 라벨만 있고 제목 없음 | 마크다운 캡션 필수 | OK |

---

## 7. 금지 요소 (재생성 안정화)

아래 항목은 **베이스 프롬프트의 negative 절**에 항상 포함된다.

1. 현실 기업·제품 로고 (Apple, Notion, OpenAI, ChatGPT, Google, Microsoft 등). 대안: '커넥트' 자체 워드마크 또는 일반 명사("HR 시스템", "사내 챗봇")
2. 실존 한국 연예인·정치인·공인. 모든 인물은 §3 앵커에 정의된 가상 캐릭터만
3. AI = 로봇 묘사 (CH01의 PC 속 로봇 말풍선조차 수정 대상). AI는 **사서·메모장·계산기·확대경** 등 일상 은유로
4. 그라데이션·모등(rounded shadow)·드롭섀도우·블러
5. 3D·등각투영·원근 단축법 (모든 그림은 평면 정면 또는 약한 3/4 시점)
6. 다채색 팔레트 (검정·흰·웜 3색 외 모든 색)
7. 사실적 사진·이미지·텍스처 (수채·유화·필름그레인 일체)
8. 폭력·공포·자해 묘사. 환각·실패도 §2.3에 따라 웜 주황 ✗·점선으로만 표시
9. 상표 등록 가능한 캐릭터(예: 둘리·뽀로로·디즈니 캐릭터·일본 IP)
10. 영문 외 외국어 라벨 (한국어 외에 한자·일본어·영어 본문 금지. 단 path 표시·코드 변수명은 영어 OK)

---

## 8. 챕터별 처리 인벤토리 (사내AI비서_v2 · 2026-05-09 기준)

### 8.1 기존 이미지 (업그레이드 대상)

| CH | 파일 | 분류 | 토큰 적용 후 변경점 |
|----|------|------|-----------------|
| 01 | `01_chapter-opening.png` | 인물·실내 4:5 | 오픈이 앵커 적용. PC 속 로봇 말풍선 → 노트북 화면의 일반 채팅 UI로 교체. 포스트잇 "Wi-Fi PW"는 웜 액센트 |
| 01 | `01_hallucination-outsider.png` | 개념 16:9 | 외부인·회사 건물·사내 규정 대비 유지. ✗ 표시를 빨강에서 웜 주황으로 |
| 01 | `01_context-overflow.png` | 개념 16:9 | 프롬프트 윈도우 오버플로우 표시를 웜 주황 점선으로 |
| 01 | `01_journey-roadmap.png` | 책 전체 16:9 | 4파트 흐름. 현재 챕터 위치 표시는 웜 액센트 점 1개 |
| 01 | `01_openbook-exam.png` | 비유 16:9 | 책상·열린 책·연필. 비유 사전 §4의 사물 적용 |
| 02 | `02_chapter-opening.png` | 인물·실내 4:5 | 팀장·오픈이 등장 가능성 검토. 자료실·DB 시각화 |
| 03 | `03_chapter-opening.png` | 개념 16:9 | "공유 드라이브 문서 더미" — `box` `file-binder` 사물 토큰 적용 |
| 04 | `04_chapter-opening.png` | 비유 16:9 | "주방" 비유 — 손질·다지기·양념·냉장고. 사물 4개 정렬 |
| 04 | `04_vectordb-pipeline.png` | 비유 흐름 16:9 | 위와 같은 4단계. 가로 흐름 화살표 |
| 05 | `05_chapter-opening.png` | 비유 4:5 | `librarian` 앵커 첫 등장. 메모 카드를 웜 액센트로 |
| 05 | `05_sliding-window.png` | 개념 16:9 | 메모장 5장 + 6번째 들어와 1번째 빠짐 |
| 06 | `06_chapter-opening-2.png` | 비유 4:5 | 사서가 `key` 들고 있음. 두 방의 문 |
| 06 | `06_librarian-two-rooms.png` | 비유 16:9 | 사서·서가·DB 자료실 |
| 07 | `07_chapter-opening.png` | 비유 4:5 | 사서가 메모장+다이얼+체크리스트 들고 있음 |
| 10 | `10_eval-concept.png` | 개념 16:9 | 질문·정답 쌍 반복 평가. 사물보다는 화살표 흐름 |

### 8.2 신규 필요 (CH08·09·11)

| CH | 슬롯 | 권장 파일명 | 분류 | 핵심 메시지 |
|----|------|----------|------|-----------|
| 08 | 챕터 오프닝 | `08_chapter-opening.png` | 비유 4:5 | "엉뚱한 책을 가져온 사서" — 오픈이가 잘못된 책을 받고 갸우뚱하는 표정 |
| 08 | 청킹 진화 | `08_chunking-evolution.png` | 개념 16:9 | 가위→문단 인식→의미 파악 3단계 |
| 09 | 챕터 오프닝 | `09_chapter-opening.png` | 비유 4:5 | "사서의 언어 능력" — 사서가 헤드폰을 끼고 질문을 다른 형태로 통역 |
| 11 | 챕터 오프닝 | `11_chapter-opening.png` | 인물·실내 4:5 | "완성된 커넥트HR" — 오픈이가 노트북 앞에서 미소 (성취의 순간, 머그잔 김에 웜 액센트) |
| 11 | 회고·로드맵 | `11_journey-end.png` | 책 전체 16:9 | CH01 journey-roadmap의 모든 단계가 채워진 모습 (마지막 점에 웜 액센트) |

---

## 9. 경로 규칙 (확정)

```
projects/<책>/assets/CH{NN}/gemini/{NN}_{slug}.png
```

**중요**: 일부 챕터에서 `assets/챕터 N/` 한글 폴더를 쓰고 있다. 이는 **deprecated** — 새 생성·재생성 시 모두 `CH{NN}` 영문 폴더로 옮긴다. 마크다운 본문 경로도 함께 수정. (deprecated 폴더 정리는 별도 작업)

---

## 10. 참조 이미지 전략 (일관성 잠금)

### 10.1 스타일 앵커 세트

CH01의 5장을 **고정 스타일 앵커**로 운용한다 (현재 5장 모두 흑백 라인아트로 일관됨):

```
projects/사내AI비서_v2/assets/CH01/gemini/
├── 01_chapter-opening.png        ← 인물·실내 + 한글 제목 패턴 앵커
├── 01_hallucination-outsider.png ← 추상·라벨 패턴 앵커
├── 01_context-overflow.png       ← 흐름·웜 주황 ✗ 패턴 앵커
├── 01_journey-roadmap.png        ← 단계·로드맵 패턴 앵커
└── 01_openbook-exam.png          ← 비유 사물 패턴 앵커
```

### 10.2 호출 시 라벨링

gpt-image-2에 참조 이미지를 넘길 때 **역할별 라벨**을 명시한다:

```
Image 1: style anchor — uniform line weight and warm-accent rule.
Image 2: 오픈이 character anchor — keep the exact face proportions.
Image 3: layout anchor for 4:5 portrait + bottom Korean title.
Image 4: layout anchor for 16:9 abstract concept with labels.
Generate the new image in this style. Do not redesign the characters
or change the line weight.
```

### 10.3 챕터별 추가 앵커

각 챕터의 첫 이미지가 확정되면, 그 챕터의 후속 이미지는 **앞 이미지를 1장 추가 참조**한다 (CH04 vectordb-pipeline은 04_chapter-opening의 주방 비유와 사물·인물 위치를 잠금).

---

## 11. 변경 이력

| 일자 | 변경 | 사유 |
|------|------|------|
| 2026-05-09 | 초기 작성 | 사내AI비서_v2 딥인터뷰 결과 반영. 모델 gpt-image-2 전환 + 흑백·웜 액센트 + 캐릭터 앵커 도입 |

---

## 12. 관련 파일

- 베이스 프롬프트 적용처: `.claude/skills/visual/references/image.md`
- 다이어그램 토큰 (이 파일과 별개): `.claude/rules/brand-tokens.md`
- 인벤토리 본 파일 §8 + 산출물 위치: `projects/사내AI비서_v2/assets/CH{NN}/gemini/`
