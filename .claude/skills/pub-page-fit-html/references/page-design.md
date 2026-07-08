# PDF 페이지 디자인 가이드

기술 서적의 PDF 페이지를 한 장씩 균형 있게 만드는 원칙과 진단 워크플로우. `pub-html-build` + `pub-html-to-pdf` 파이프라인 기준.

> **요약**: 페이지 디자인은 CSS만으로 끝나지 않는다. 광역 `page-break-inside: avoid` 강제는 빈 공간 부작용을 만든다. 자동 도구 → 부작용 없는 최소 CSS → 저자의 콘텐츠 다듬기 3단으로 접근한다.

---

## 1. 페이지 분할 원칙 (CSS Paged Media + 책 조판 표준)

### 그림은 깨지지 않게

```css
.chapter-image, figure, .figure-group, .terminal-log, .rag-pipeline-box {
  page-break-inside: avoid;
  break-inside: avoid;
}
```

`break-inside`는 모던 표기, `page-break-inside`는 레거시 alias. 두 줄 같이 둔다 (헤드리스 Chromium 호환).

### 그림과 캡션은 묶음

```css
.chapter-image, figure {
  break-after: avoid;        /* 그림 다음 페이지로 넘어가도 캡션은 따라감 */
}
.caption {
  break-before: avoid;       /* 캡션이 그림과 분리되어 다음 페이지로 가는 것 방지 */
}
```

### 헤딩 처리

| 헤딩 | 규칙 |
|------|------|
| h1 (챕터 제목) | `break-before: page` — 새 페이지에서 시작 |
| h2, h3 | `break-after: avoid` — 단독으로 페이지 끝에 남지 않게 |
| h2, h3 | `break-inside: avoid` — 두 줄짜리 제목이 가운데서 끊기지 않게 |

### 위젯·오펀

```css
p { orphans: 3; widows: 3; }
```

문단 끝 한두 줄만 다음 페이지로 넘어가는 것 방지.

### 광역 `avoid`는 위험

`figure, [class*="-flow"], [class*="-scene"]` 같은 광역 셀렉터로 모든 컴포넌트에 `avoid`를 걸면 페이지보다 큰 박스가 강제로 다음 페이지로 밀린다. 그 결과 **앞 페이지에 더 큰 빈 공간**이 생긴다. **부작용 없는 명시 클래스만 등록**한다.

---

## 2. 그림 배치 원칙 (기술 출판 표준)

- **본문 가까이** — 처음 참조된 직전이나 직후
- **페이지 상단·하단** — running text 한가운데 끼우면 흐름이 끊긴다
- **캡션 위치**: 그림은 아래 (Figure N. ...), 표는 위 (Table N. ...)
- **밀도**: 한 페이지에 그림 1~2장이 적정. 3장 이상이면 코드블록·문단을 줄이거나 다음 페이지로 분산

---

## 3. 3단 진단 매트릭스

| 단계 | 도구 | 처리 가능한 것 |
|------|------|----------------|
| **1단 자동** | `pub-layout-check` → `pub-page-fit-html` | 빈 공간 자동 감지, 컴포넌트 padding·gap 점진 축소 (density-scale 1.00 → 0.75) |
| **2단 반자동 (CSS)** | `print.css` 보강 | 누락된 컴포넌트에 `break-inside: avoid` 추가, 그림+캡션 묶음 |
| **3단 수동 (저자)** | 챕터 마크다운 편집 | 텍스트 분량 조절, 그림 위치 이동, 코드블록 분할, 헤딩 위치 조정 |

**1단으로 안 되면 2단, 2단으로 안 되면 3단으로 내려간다.** 처음부터 3단으로 가지 말고, 처음부터 2단을 광역으로 적용하지 않는다.

### 1단 실행

```bash
PY=".claude/skills/pub-html-to-pdf/.venv/bin/python"

# 진단
"$PY" .claude/skills/pub-layout-check/references/scripts/pdf_layout_checker.py \
  projects/<책>/.build/pdf/01-*.pdf

# 자동 fit (이슈가 보이면)
"$PY" .claude/skills/pub-page-fit-html/auto_fit.py \
  --project-root projects/<책> --chapter 1
```

### 2단 보강 예시

```css
/* print.css에 추가 — 그림+캡션 묶음 (부작용 없음) */
.chapter-image, figure {
  break-after: avoid;
}
.caption {
  break-before: avoid;
}
```

---

## 4. 케이스북 — 5가지 패턴별 처방

### 패턴 1. 고아 페이지 (Orphan)

**증상**: ≤4줄만 페이지 상단에 남고 90%+ 빈 공간

**진단 출력**:
```
p19 |#.......................................|   5%  <<<고아>>>
[!] 페이지 19: 2줄만 있고 하단 94% 빈 공간
```

**처방** (3단 수동):
- 앞 절에서 한두 문장 압축 → 그 줄들이 앞 페이지에 흡수
- 또는 그 두 줄을 다음 절 도입부와 합치기

```markdown
<!-- BEFORE: 한 절이 2줄만 페이지 끝으로 떨어짐 -->
앞 절 내용...
{여기가 페이지 끝}

마지막 두 줄 텍스트.
{여기서 페이지 분할 — 다음 페이지에 이 두 줄만}

## 다음 절

<!-- AFTER: 마지막 두 줄을 앞 절 결론으로 흡수 -->
앞 절 내용 ... 마지막 두 줄 텍스트.

## 다음 절
```

### 패턴 2. 밀림 빈공간 (Push)

**증상**: 큰 그림 또는 코드블록이 다음 페이지로 밀리며 앞 페이지가 35% 미만

**진단 출력**:
```
p14 |#############...........................|  35%  <<빈 공간>>
[~] 페이지 14: 콘텐츠가 38%만 차지
    -> 큰 이미지나 코드 블록이 다음 페이지로 밀렸을 수 있음
```

**처방** (2단 CSS 또는 3단 수동):
- 그림 max-height 12cm → 10cm (해당 챕터만 책별 오버라이드 `.build/tokens.css`)
- 또는 본문에서 한 줄 줄여 그림이 같은 페이지에 들어가게
- 또는 그림 위치를 한 절 뒤로 옮겨 다른 콘텐츠와 짝짓기

### 패턴 3. 그림 직후 빈공간

**증상**: 그림 + 다음 콘텐츠가 한 페이지에 못 들어가서 그림 직후 50% 정도 비고 다음 페이지가 풍부

**처방** (3단 수동):
- 그림을 다음 절 첫머리로 이동 — 다음 절의 도입 그림 역할로 재배치
- 또는 그림 자체를 두 장으로 분할해 가로 배치

### 패턴 4. 그림 잘림 (Cross-page split)

**증상**: page-break가 그림 한가운데를 가른다

**처방**:
- 1단 확인: 해당 컴포넌트 클래스에 `break-inside: avoid`가 적용됐는가
- 2단 추가: 누락된 클래스 명시 등록
- 3단: 그림이 페이지보다 크면 max-height 줄이기 (이미지 자체 또는 컨테이너)

### 패턴 5. 캡션만 다음 페이지로

**증상**: 그림은 페이지 하단에 들어가고 캡션만 다음 페이지로 넘어감

**처방** (2단 CSS):
```css
.chapter-image, figure { break-after: avoid; }
.caption { break-before: avoid; }
```

이 규칙이 그림+캡션을 한 단위로 묶는다.

---

## 5. 워크플로우 예시

`사내AI비서_v2` 프로젝트의 실제 케이스 9건이 BEFORE/AFTER로 시각화된 프리뷰:

`projects/사내AI비서_v2/.build/preview/page-design-cases.html`

각 케이스의 진단 라벨, 처방 단계(1·2·3단), 적용 후 페이지 사용률 변화를 카드로 비교한다.

---

## 출처

- [Designing For Print With CSS — Smashing Magazine](https://www.smashingmagazine.com/2015/01/designing-for-print-with-css/)
- [page-break — CSS-Tricks](https://css-tricks.com/almanac/properties/p/page-break/)
- [How To Print A Book With CSS](https://www.alibaba.com/product-insights/how-to-print-a-book-with-css-reliable-accessible-production-ready.html)
- [LaTeX Floats, Figures and Captions — Wikibooks](https://en.wikibooks.org/wiki/LaTeX/Floats,_Figures_and_Captions)
- [Ten simple rules for typographically appealing scientific texts — PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7774853/)
- [page-break-inside CSS property — MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/page-break-inside)
