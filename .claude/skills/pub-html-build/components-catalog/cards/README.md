# Cards

> 개별 카드 단위 시각화. 청크 한 건, 임베딩 예시 한 건 같은 "단일 개체"를 보여준다.

## 속함

- `.card-meta` + `.cwm-*` 계열 (청크 1건 = 본문 + 메타데이터 라벨, CH04)
- `.example-row` + `.eer-*` 계열 (의미 비슷/다른 2~3개 묶음, CH04)

## 속하지 않음

- 파이프라인 단계 카드(`.step-card`, `.s-*`) → [`../pipelines/`](../pipelines/)
- 책 전체 구성도 박스 → [`../fullmap/`](../fullmap/)

## 컴포넌트 목록

### .card-meta

**언제 쓰는가**: 벡터 DB에 들어간 **청크 한 건**이 어떻게 생겼는지 시각적으로 보여줄 때. 본문과 메타데이터(출처·페이지·분류·chunk_id) 라벨을 카드 한 장에 묶어 독자가 "청크 = 텍스트 + 메타데이터" 모델을 직관적으로 이해하게 함.

**사용 챕터**: CH04

**HTML 사용 예**:
```html
<div class="card-meta">
  <div class="cm-title">청크 한 조각 = 본문 + 메타데이터 라벨</div>
  <div class="cm-card">
    <div class="cm-body">
      제5조(연차유급휴가) 신입사원은 입사 후 3년 동안은 연차가 없다. 대신 매월 1회 '리프레시 데이'를 유급으로 제공한다. 3년 근속 시점에 30일의 연차가 일시에 발생한다. …
    </div>
    <div class="cm-meta">
      <span class="cm-tag"><b>출처</b> HR_취업규칙_v1.0.pdf</span>
      <span class="cm-tag"><b>페이지</b> 3</span>
      <span class="cm-tag"><b>분류</b> HR</span>
      <span class="cm-tag"><b>chunk_id</b> hr_취업규칙_v1_0_text_p003_c0002</span>
    </div>
  </div>
  <div class="cm-note">이 라벨들이 ChromaDB에 <code>metadata</code> 필드로 같이 저장됩니다. 검색할 때 "HR 폴더의 3페이지 근처 문서만"처럼 필터링도 가능하고, 답변에 출처를 붙일 때도 이 값을 그대로 씁니다.</div>
</div>
```

**렌더 CSS**: `styles/diagrams.css:1772-1838` (`.card-meta`, `.cm-title`, `.cm-card`, `.cm-body`, `.cm-meta`, `.cm-tag`, `.cm-note`)

**변형**: `.cm-tag`는 4개 권장 (출처·페이지·분류·chunk_id). 3개 이하면 빈약, 6개 이상이면 밀도 과잉. `.cm-note` 내부에서 짧은 코드는 `<code>` 인라인으로 감싼다.

**피해야 할 것**
- 본문에 인라인 스타일 추가 금지 (모든 시각 규정은 CSS로)
- `.cm-card`를 한 문서 내에 3개 이상 배치 금지 — 독자 피로. 2개까지만
- `.cm-tag` 한 개에 긴 설명 문장 금지 (tag는 짧은 라벨 전용)

### .example-row

**언제 쓰는가**: "의미가 비슷한 것끼리는 임베딩 벡터도 비슷하다"를 시각화. 의미 유사 2~3개 묶음(`.er-group.similar` + `.er-group-label.good`) 옆에 의미 다른 1개(`.er-group.different` + `.er-group-label.bad`)를 대비시키고, 오른쪽에 임베딩 공간 이미지(`.er-image`)로 좌표 감각을 보강함. 임베딩 개념을 처음 소개하는 지점에서 1회 사용.

**사용 챕터**: CH04

**HTML 사용 예**:
```html
<div class="example-row">
  <div class="er-card">
    <div class="er-group similar">
      <div class="er-group-label good">의미가 비슷하면 숫자도 비슷</div>
      <div class="er-item">
        <div class="er-text">"연차 사용 규정"</div>
        <div class="er-vec">[ 0.92, 0.87, ... ]</div>
      </div>
      <div class="er-item">
        <div class="er-text">"휴가 관련 정책"</div>
        <div class="er-vec">[ 0.91, 0.85, ... ]</div>
      </div>
    </div>
    <div class="er-group different">
      <div class="er-group-label bad">의미가 다르면 숫자도 다름</div>
      <div class="er-item">
        <div class="er-text">"매출 현황 보고서"</div>
        <div class="er-vec">[-0.15, 0.08, ... ]</div>
      </div>
    </div>
  </div>
  <div class="er-image">
    <img src="../assets/CH04/image/04_embedding-concept.png" alt="">
  </div>
</div>
<div class="er-caption">그림 4-5. 왼쪽(문장 임베딩 벡터 예시. 앞 몇 자리만 봐도 비슷/다름이 드러남), 오른쪽(임베딩 공간에 찍힌 좌표. 의미가 가까운 문서가 한 곳에 모임)</div>
```

**렌더 CSS**: `styles/diagrams.css:1841-1924` (`.example-row`, `.er-card`, `.er-group`, `.er-group.similar`/`.different`, `.er-group-label.good`/`.bad`, `.er-item`, `.er-text`, `.er-vec`, `.er-image`, `.er-caption`)

**변형**: `.er-group`은 `.similar` / `.different` modifier로 배경·보더 색이 갈린다. `.er-group-label`은 `.good` / `.bad` modifier와 짝을 이룬다. `.er-image`는 선택 요소. 오른쪽 이미지가 없어도 벡터 대비만으로 의미는 전달되지만, 임베딩 공간 이미지가 있을 때 좌표 감각까지 생긴다.

**피해야 할 것**
- 의미 다른 그룹(`.different`)을 2개 이상 배치 금지 — "비슷 vs 다름" 대비가 약해짐
- `.er-vec` 숫자를 길게 나열 금지. 앞 2자리 + `...` 권장 (`[ 0.92, 0.87, ... ]`)
- 캡션(`.er-caption`)에 반말 종결(-다, -이다) 금지. 존댓말(해요체/합니다체)로 통일
- `.er-group-label.good`에 `.different` 그룹을 붙이는 등 modifier 짝 어긋나게 쓰지 말 것 (색 대비가 무너짐)
