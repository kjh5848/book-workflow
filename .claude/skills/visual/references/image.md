# 이미지 생성 및 관리 규칙

> **2026-05-09 개정**: gpt-image-2 베이스 프롬프트 도입, 스토리 이미지 디자인 토큰을 별도 분리. 토큰 단일 진실원: `projects/<책>/planning/image-tokens.md` (책별) 또는 `.claude/rules/image-tokens.md` (글로벌, 향후 이관). 베이스 프롬프트는 토큰 파일을 참조 조립한다.

## 0. 시각 자료 유형별 도구 선택

| 유형 | 도구 | 서브폴더 | 생성 시점 |
|------|------|---------|----------|
| 흐름도, 아키텍처 | **Mermaid / D2** | `diagram/` | 집필 중 즉시 |
| 시퀀스/단계 흐름 (ReAct, 파이프라인) | **플로우 카드** | `diagram/` | 유저 요청 시 (메인 세션) |
| **스토리 이미지** (오프닝·인물·비유·감정 순간) | **gpt-image-2** | `gemini/` | 집필 완료 후 일괄 |
| 추상 개념 인포그래픽 (다이어그램으로 안 풀리는 비유) | **gpt-image-2** | `gemini/` | 집필 완료 후 일괄 |
| 실습 결과 스크린샷 (터미널/UI) | **Direct Capture** | `terminal/` | 예제 코드 실행 후 |

**중요한 분리**:

- **다이어그램** — `.claude/rules/brand-tokens.md` 토큰 적용 (인디고 + 무채색 + 흰 배경)
- **스토리 이미지** — `planning/image-tokens.md` 토큰 적용 (흑백 라인아트 + 웜 액센트 1색 + 한글 라벨)

서브폴더 이름은 역사적 이유로 `gemini/` 그대로 유지(이미지 모델만 gpt-image-2로 교체). 플레이스홀더 마커는 `[GPT-IMAGE-2 PROMPT: ...]` 또는 호환을 위해 `[GEMINI PROMPT: ...]` 둘 다 인식한다.

집필 시점에는 실제 이미지를 만들 수 없으므로 **플레이스홀더**를 삽입하고, 실제 이미지는 집필 완료 후 일괄 생성한다.

---

## 0.5. 경로 규칙

모든 이미지는 **챕터별 폴더 + 유형별 서브폴더**에 저장한다.

```
projects/{책이름}/
├── chapters/NN-제목.md        <- 챕터 원고
├── assets/
│   ├── CH01/
│   │   ├── diagram/           <- Mermaid/D2 렌더링
│   │   ├── terminal/          <- 터미널 캡처
│   │   └── gemini/            <- 스토리 이미지 (gpt-image-2)
│   ├── CH02/
│   │   ├── diagram/
│   │   ├── terminal/
│   │   └── gemini/
│   └── ...
```

**두 가지 경로를 플레이스홀더에 모두 명시:**

| 용도 | 경로 기준 | 형식 | 예시 |
|------|----------|------|------|
| `path:` (스크립트용) | 프로젝트 루트 | `assets/CH{N}/{subfolder}/{id}.png` | `assets/CH01/gemini/01_chapter-opening.png` |
| `![alt](src)` (마크다운) | 챕터 파일 위치 | `../assets/CH{N}/{subfolder}/{id}.png` | `../assets/CH01/gemini/01_chapter-opening.png` |

**서브폴더 매핑:**

| 플레이스홀더 | 서브폴더 |
|-------------|---------|
| `[GPT-IMAGE-2 PROMPT]` 또는 `[GEMINI PROMPT]` | `gemini/` |
| `[CAPTURE NEEDED]` (터미널) | `terminal/` |
| Mermaid/D2 렌더링 | `diagram/` |

> **경로 일관성**: 일부 챕터에서 `assets/챕터 N/` 한글 폴더가 사용 중. 신규·재생성 시 `assets/CH{NN}/`로 통일한다 (image-tokens.md §9 참조).

---

## 0.7. D2 다이어그램 빌드 규칙

D2 다이어그램을 PNG로 변환할 때 **반드시 `--layout elk`** 옵션을 사용한다. elk 레이아웃은 직각 꺾인선(orthogonal routing)을 자동 적용하여 깔끔한 다이어그램을 만든다. 기본 dagre 레이아웃은 곡선을 생성하므로 사용하지 않는다.

```bash
# SVG 생성 (elk 필수, 그룹 컨테이너 있으면 theme 0)
d2 --layout elk --theme 0 --pad 40 파일.d2 파일.svg

# PNG 변환 (폭 1600px)
rsvg-convert -o 파일.png -w 1600 파일.svg
```

- `--layout elk`: 직각 꺾인선(orthogonal routing) 자동 적용
- `--theme 0`: 테마 없음. 테마(300 등)를 쓰면 루트 컨테이너에 자동 경계선이 추가되어 그룹 점선과 이중으로 보임
- 스타일은 `.d2` 파일 내 classes로 직접 제어

---

## 1. 플레이스홀더 삽입 (3가지 방식)

### 방식 A — 스토리 이미지: gpt-image-2 프롬프트 플레이스홀더

스토리 이미지(인물·비유·감정 순간)와 추상 개념 시각화를 삽입할 때 사용. **베이스 프롬프트(§3)**와 **인물·사물 앵커(§5)**를 조립한다.

```markdown
<!-- [GPT-IMAGE-2 PROMPT: {NN}_{identifier}]
path: assets/CH{N}/gemini/{NN}_{identifier}.png
mode: thinking | instant
ratio: 4:5 | 16:9
characters: [오픈이 | 팀장 | 동료 | 사서 | none]
objects: [memo-pad, bookshelf, magnifier, ...] (해당 없으면 생략)
in_image_text:
  - position: bottom-center-bold
    text: "입사 3일 차, 첫 번째 미션"
  - position: speech-bubble
    text: "AI 비서 만들어봐"
scene: { 1~3문장의 장면 묘사. 카메라 시점·인물 동작·핵심 사물 위치 }
accent_target: "Wi-Fi PW 포스트잇"  (§2.3 1장 1포인트 규칙)
references:
  - role: style anchor
    path: assets/CH01/gemini/01_chapter-opening.png
  - role: character anchor
    path: assets/CH01/gemini/01_chapter-opening.png
-->
![](../assets/CH{N}/gemini/{NN}_{identifier}.png)
*그림 {N}-{순번}. {캡션}*
```

플레이스홀더의 **세부 필드**는 모두 메인 세션이 §3 베이스 프롬프트와 토큰 파일을 결합해 최종 영문 프롬프트로 풀어낸다. 작성자(writer)는 위 구조화된 키만 채우면 된다.

**예시 (CH01 챕터 오프닝 재생성)**:

```markdown
<!-- [GPT-IMAGE-2 PROMPT: 01_chapter-opening]
path: assets/CH01/gemini/01_chapter-opening.png
mode: thinking
ratio: 4:5
characters: [오픈이]
objects: [laptop, sticky-note]
in_image_text:
  - position: bottom-center-bold
    text: "입사 3일 차, 첫 번째 미션"
  - position: speech-bubble
    text: "AI 비서 만들어봐"
scene: 오픈이가 사무실 책상에 앉아 노트북을 보고 있다. 책상 한쪽에는 Wi-Fi PW가 적힌 포스트잇이 한 장 붙어 있다. 화면 너머에서 팀장의 목소리가 말풍선으로 들려온다.
accent_target: "Wi-Fi PW 포스트잇"
references: []  (CH01 첫 이미지이므로 자체가 앵커가 됨)
-->
![](../assets/CH01/gemini/01_chapter-opening.png)
*그림 1-1. 입사 3일 차, 첫 번째 미션*
```

### 방식 B — 실습 결과: 캡처 필요 플레이스홀더

실습 섹션에서 실제 실행 결과 화면을 캡처해야 할 위치에 삽입한다.
이미지 생성이 아니므로 프롬프트 없이 **무엇을 캡처할지**만 명시한다.

```markdown
<!-- [CAPTURE NEEDED: {NN}_{identifier}
  path: assets/CH{N}/terminal/{NN}_{identifier}.png
  desc: {어떤 명령을 실행하고 어떤 상태를 보여주는지}
] -->
![{캡션}](../assets/CH{N}/terminal/{NN}_{identifier}.png)
*그림 {N}-{순번}: {캡션}*
```

### 방식 C — 플로우 카드: HTML/CSS → Puppeteer PNG

시퀀스/단계 흐름 다이어그램에 사용. Writer는 **어떤 그림이 필요한지 자연어로 서술(desc)**만 한다. 상세: `references/flow-card.md`

```markdown
<!-- [FLOW CARD: {NN}_{identifier}]
path: assets/CH{N}/diagram/{NN}_{identifier}.png
desc: {이 그림이 보여줘야 할 것을 자연어로 서술.
  어떤 흐름인지, 어디가 강조 포인트인지, 앞뒤 맥락.}
-->
![](../assets/CH{N}/diagram/{NN}_{identifier}.png)
*{캡션}*
```

---

## 2. 캡처 가이드라인 (방식 B)

| 항목 | 기준 |
|------|------|
| 캡처 범위 | 전체 터미널 화면 (명령어 입력 줄 포함) |
| 해상도 | Retina/HiDPI 권장, 최소 1280px 너비 |
| 터미널 테마 | 라이트/다크 모두 허용; 인쇄 시 그레이스케일 고려 |
| 에러 화면 | 의도적 에러 예시는 빨간 텍스트 포함하여 그대로 캡처 |
| 민감 정보 | API 키, 비밀번호 등 실제 값은 블러 처리 후 캡처 |

### 스크린샷과 코드 블록 중복 금지

실행 결과를 보여줄 때 **스크린샷과 터미널 출력 코드 블록을 동시에 사용하지 않는다.**

| 상황 | 사용할 형식 |
|------|-----------|
| 스크린샷이 있는 경우 | 스크린샷만 사용. 코드 블록으로 같은 출력 반복 금지 |
| 스크린샷이 없는 경우 (플레이스홀더 단계) | 코드 블록으로 예상 출력 표시 |
| 소스 코드 (python, bash 등) | 실행 명령이므로 스크린샷과 무관하게 유지 |

> **핵심**: 스크린샷이 확보된 시점에서 동일 내용의 출력 코드 블록을 제거한다.

---

## 3. gpt-image-2 베이스 프롬프트 (영문 조립 규격)

스토리 이미지 한 장을 만들 때 **메인 세션이 자동 조립**하는 프롬프트의 표준 구조다. 토큰 파일(`planning/image-tokens.md`)의 §2~§7을 참조해 빈 슬롯을 채운다.

### 3.1 권장 순서 — gpt-image-2 베스트 프랙티스 반영

gpt-image-2는 다음 순서로 프롬프트를 받을 때 가장 안정적이다:

```
[Style/Medium] → [Subject(Character Anchors)] → [Environment/Setting]
→ [Lighting/Mood] → [Composition/Aspect Ratio] → [In-Image Text]
→ [Negative/Constraints] → [References]
```

각 절은 빈 줄로 구분한다.

### 3.2 베이스 프롬프트 템플릿 (영문 골격)

아래는 **메인 세션이 어떤 스토리 이미지를 만들든 출발점**으로 삼는 템플릿이다. `{}` 슬롯은 토큰 파일과 플레이스홀더에서 채운다.

```text
# Style
A minimalist black ink line illustration in the same visual style as the
attached reference images. Flat 2D vector line art, no perspective tricks,
no 3D, no shading, no gradient, no shadow, no texture. Solid pure white
background (#ffffff). Uniform medium-thick line weight (~3px feel),
consistent across every element.

# Subject
{character_anchor_blocks}
{object_token_blocks}

The scene: {scene_one_to_three_sentences}.

# Color
Strict three-color palette only:
- Black ink (#0d0d0d) for all line work and Korean text.
- Pure white (#ffffff) interior fills and background.
- A single warm-orange accent (#e07a3c) applied ONLY to: {accent_target}.
No other color anywhere. No red, no blue, no green, no gray fills.

# Composition
Aspect ratio: {ratio}. Global centering: the visual mass sits in the
middle of the frame with at least 8% safe margin on every edge.
Reading direction: left to right.

# In-Image Text (Korean)
Render the following Korean text inside the image with a clean
sans-serif typeface (Pretendard / Noto Sans KR feel).
Wrap each exact phrase in double quotes:
{in_image_text_lines}
Maximum 12 Korean characters per line. Solid black (#0d0d0d).

# Constraints (must avoid)
No real-world brand logos (Apple, OpenAI, ChatGPT, Notion, Google,
Microsoft, etc). No real Korean celebrities or public figures. No
robot or android depiction of AI — AI is metaphorized as a librarian,
a memo, a magnifying glass, a calculator, etc. No gradient, no drop
shadow, no rounded glow, no blur. No 3D, no isometric view, no
foreshortening. No watercolor or photorealistic texture. No emoji.
No red color — failure or hallucination is shown with the warm-orange
accent (✗ marks, dashed strikethrough, broken outlines).

# References
Image 1: style anchor — uniform line weight and warm-accent rule.
Image 2: 오픈이 character anchor — keep face proportions and outfit.
Image 3 (if 4:5): portrait + bottom Korean title layout anchor.
Image 3 (if 16:9): abstract concept + labels layout anchor.
{additional_chapter_anchor}
Generate the new image consistent with these references. Do not
redesign the characters or change the line weight.
```

### 3.3 슬롯 → 토큰 매핑

| 슬롯 | 출처 (토큰 파일 섹션) |
|------|--------------------|
| `{character_anchor_blocks}` | §3.1~§3.4 — 등장 인물 해당 블록만 |
| `{object_token_blocks}` | §4 사전에서 등장 사물 해당 행만 |
| `{scene_one_to_three_sentences}` | 플레이스홀더 `scene` 필드 |
| `{accent_target}` | 플레이스홀더 `accent_target` (§2.3 1장 1포인트) |
| `{ratio}` | 플레이스홀더 `ratio` (인물 4:5 / 개념 16:9) |
| `{in_image_text_lines}` | 플레이스홀더 `in_image_text` 배열을 줄별로 풀어서 |
| `{additional_chapter_anchor}` | 챕터 첫 이미지 이후, 그 챕터 이전 이미지 1장 추가 |

### 3.4 모드 선택

| 상황 | 모드 | 이유 |
|------|------|------|
| 캐릭터·팔레트 일관성이 핵심 (인물 등장) | `thinking` | 8장까지 일관성 보장 |
| 같은 챕터 안에서 여러 장을 한 번에 | `thinking` | 한 호출로 멀티 패널 |
| 단발 추상 개념도 (인물·캐릭터 없음) | `instant` | 빠르고 비용 적음 |

### 3.5 기존 베이스 프롬프트 (legacy)

이전 Gemini용 베이스(흑백 16:9 인포그래픽)는 더 이상 새 이미지에 사용하지 않는다. 다만 CH01의 5장은 이 프롬프트로 만들어진 결과물이며, 새 이미지의 **스타일 앵커**로 그대로 사용한다 (image-tokens.md §10.1).

---

## 4. 실행 흐름 (메인 세션이 일괄 생성)

```
1. 작성자가 챕터에 [GPT-IMAGE-2 PROMPT: ...] 플레이스홀더 삽입
2. 챕터 본문 완성
3. 메인 세션이 "스토리 이미지 일괄 생성" 명령 수신
4. 메인 세션이 다음을 수행:
   a. 모든 플레이스홀더 수집
   b. 챕터 그룹 단위로 묶음 (한 챕터 = 한 thinking 호출)
   c. 각 슬롯을 토큰 파일에서 채워 §3 템플릿으로 조립
   d. CH01 5장을 references로 자동 첨부
   e. gpt-image-2 호출 → PNG 수신 → assets/CH{N}/gemini/ 저장
5. 본문의 플레이스홀더는 그대로 두되, <img> 태그로 교체 (방식 D)
6. 유저가 결과 검수 후 재생성 요청 시 같은 플레이스홀더로 다시 호출
```

> 챕터를 **순차로** 처리한다. CH01 → CH02 순서. 같은 챕터 내에서는 thinking 모드로 한 번에. CH01 5장이 변경되면 모든 후속 챕터 영향을 받으므로 CH01은 토큰 변경 시에만 재생성.

---

## 5. 인물·사물 토큰 사용 가이드 (요약)

전체 정의는 `planning/image-tokens.md` §3 (인물 앵커), §4 (사물 사전) 참조.

### 5.1 캐릭터 앵커 — 등장 시에만 포함

| 키 | 토큰 파일 §3 위치 |
|----|----------------|
| `오픈이` (주인공·신입) | §3.1 |
| `팀장` (시니어) | §3.2 |
| `동료` (옆자리) | §3.3 |
| `사서` (CH05~CH07 비유) | §3.4 |

> **금지**: 등장하지 않는 인물의 앵커 블록은 절대 프롬프트에 포함하지 않는다 (모델이 강제로 그려넣음).

### 5.2 사물 사전 — 챕터별 등장만 포함

10개 사물 토큰: `librarian`, `memo-pad`, `bookshelf`, `magnifier`, `box`, `file-binder`, `library-card`, `laptop`, `sticky-note`, `key`. 각 외형 고정 문장은 `image-tokens.md` §4 표 참조.

---

## 6. 이미지 삽입 및 캡션 규칙 (이미지 준비 후)

플레이스홀더를 실제 이미지로 교체할 때 `<img>` 태그 + `width` 속성을 사용한다. HTML 주석 블록(플레이스홀더 메타데이터)은 **유지** — 재생성 시 다시 사용한다 (이전 Gemini 방식과 차이).

### 이미지 사이즈 규칙

모든 이미지는 `<img>` HTML 태그로 삽입하고, **`width="720"`** 을 기본값으로 사용한다.

| 유형 | width | 용도 |
|------|-------|------|
| 전체 화면 캡처 | `720` | 기본값 |
| 터미널 출력 | `720` | 기본값 |
| 스토리 이미지 (4:5) | `560` | 인물·세로 비율 (B5 페이지에서 너무 크지 않게) |
| 스토리 이미지 (16:9) | `720` | 개념·가로 비율 기본 |

> `![alt](src)` 대신 반드시 `<img src="..." width="720" alt="...">` 를 사용한다. 캡션은 `<img>` 태그 다음 빈 줄 뒤에 작성한다.

**Before (플레이스홀더):**

```markdown
<!-- [GPT-IMAGE-2 PROMPT: 01_chapter-opening]
path: assets/CH01/gemini/01_chapter-opening.png
mode: thinking
ratio: 4:5
characters: [오픈이]
...
-->
![](../assets/CH01/gemini/01_chapter-opening.png)
*그림 1-1. 입사 3일 차, 첫 번째 미션*
```

**After (이미지 생성 완료):**

```markdown
<!-- [GPT-IMAGE-2 PROMPT: 01_chapter-opening]
path: assets/CH01/gemini/01_chapter-opening.png
mode: thinking
ratio: 4:5
characters: [오픈이]
...
-->
<img src="../assets/CH01/gemini/01_chapter-opening.png" width="560" alt="입사 3일 차">

*그림 1-1. 입사 3일 차, 첫 번째 미션*
```

- **파일명 형식**: 소문자 영문, 밑줄, 하이픈 (예: `01_chapter-opening.png`)
- **캡션 중복 방지**: `image-tokens.md` §6.3 참조. 그림 안 한글 제목과 마크다운 캡션이 같은 문장이면 한쪽 삭제.
- **HTML 주석은 유지**: 재생성 시 동일 프롬프트로 일관성 보장

---

## 7. 변경 이력

| 일자 | 변경 |
|------|------|
| 2026-05-09 | gpt-image-2 베이스 프롬프트 도입. Gemini 베이스 프롬프트 deprecate(CH01 5장은 스타일 앵커로 유지). 인물·사물 토큰화. 플레이스홀더 구조화 키 도입(`mode`, `ratio`, `characters`, `objects`, `in_image_text`, `accent_target`, `references`) |
| (이전) | Gemini Image 베이스 프롬프트 + 4가지 플레이스홀더 방식 (A/B/C/D) |

---

## 8. 관련 파일

| 위치 | 내용 |
|------|------|
| `projects/<책>/planning/image-tokens.md` | 스토리 이미지 디자인 토큰 단일 진실원 (책별) |
| `.claude/rules/brand-tokens.md` | 다이어그램·HTML 컴포넌트 토큰 (이 파일과 별개 시스템) |
| `references/flow-card.md` | 플로우 카드 생성 규격 (방식 C) |
| `references/mermaid.md` | Mermaid 다이어그램 규칙 |
