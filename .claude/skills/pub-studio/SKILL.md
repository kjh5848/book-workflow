# pub-studio — 프리뷰 에디터 + 검증 빌드

model: claude-sonnet-4-6
user_invocable: false

## 하는 일

MD→Typst→PDF/SVG 전체 파이프라인을 브라우저 프리뷰 에디터로 통합한다.
디자인 실시간 프리뷰, 개별 이미지 크기 제어, 레이아웃 검증 루프(build→check→auto-fix→rebuild)를 제공한다.

## 아키텍처

```
preview.py  (얇은 진입점 ~40줄)
  └→ PreviewServer  (HTTP 라우팅)
       ├→ BuildCache       (2단계 캐시: Stage 1 file_hash, Stage 2 design_hash)
       ├→ BuildPipeline    (typst_builder.py 래핑)
       │    ├→ ImageRegistry   (개별 이미지 추적 + 오버라이드)
       │    └→ DesignEngine    (design_assembler.py 래핑)
       ├→ LayoutChecker    (pdf_layout_checker.py 래핑 + 심각도 분류)
       └→ VerificationLoop (build→check→fix 사이클, 최대 3라운드)
```

## 파일 구조

```
.claude/skills/pub-studio/
├── SKILL.md
└── references/scripts/
    ├── __init__.py
    ├── models.py              # 데이터 클래스
    ├── build_cache.py         # 2단계 캐시
    ├── image_registry.py      # 개별 이미지 추적/오버라이드
    ├── build_pipeline.py      # MD→Typst→PDF/SVG
    ├── design_engine.py       # 컴포넌트 조립
    ├── layout_checker.py      # PDF 분석 + 심각도 분류
    ├── verification_loop.py   # build→check→fix 사이클
    └── preview_server.py      # HTTP 서버 + API

preview.py                      # 진입점
preview_editor.html             # UI
```

## 실행

```bash
python3 preview.py                     # 프로젝트 자동 감지
python3 preview.py 사내AI비서_v2        # 프로젝트 지정
python3 preview.py --port 8080         # 포트 지정
python3 preview.py --file book/통합본.typ  # 파일 모드
```

## 2단계 빌드 캐시

| 단계 | 트리거 | 소요 | 캐시 키 |
|------|--------|------|---------|
| Stage 1 | MD 파일 변경 | ~5-10s | file_hash (MD 내용 기반) |
| Stage 2 | 디자인 설정 변경 | ~200ms | design_hash (state 기반) |

디자인만 변경하면 Stage 2만 재실행 → 실시간 프리뷰.

## 검증 루프

```
Round 1: compile_pdf → analyze → auto_fixable 3건 + manual 1건
         → reduce_image_width() × 3 → assemble → write .typ
Round 2: compile_pdf → analyze → 0 auto_fixable + manual 1건
         → 종료, manual 1건 UI에 보고
```

자동수정 가능: `blank_page`, `orphan_content`, `large_image`
수동확인 필요: `low_usage`, `push_pattern`

## API 엔드포인트

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/api/project` | GET | 프로젝트 정보 |
| `/api/files` | GET | 파일 목록 |
| `/api/images` | GET | 감지된 이미지 목록 + 오버라이드 |
| `/api/layout-issues` | GET | 레이아웃 이슈 + 페이지별 사용률 |
| `/api/verification-status` | GET | 검증 진행 상태 |
| `/api/build-svg` | POST | SVG 프리뷰 빌드 |
| `/api/build-verified` | POST | 검증 루프 빌드 (백그라운드) |
| `/api/export-pdf` | POST | PDF 내보내기 |
| `/api/image-override` | POST | 개별 이미지 오버라이드 |

## 의존 스킬

- `pub-build` — typst_builder.py, design_assembler.py
- `pub-layout-check` — pdf_layout_checker.py
- `pub-typst-design` — 템플릿, 컴포넌트, 변수
