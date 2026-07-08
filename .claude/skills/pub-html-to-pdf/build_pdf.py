#!/usr/bin/env python3
"""
build_pdf.py — pub-html-build이 생성한 HTML 프리뷰를 Playwright Chromium으로 A4 PDF로 변환.

정식 전자책 PDF는 `pub-build`(Typst) 파이프라인으로 생성한다. 이 스킬은 프리뷰 한 장을
파일로 공유하고 싶을 때만 사용하는 유틸.

의존성:
  pip install playwright
  python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote


PAGEDJS_CDN = "https://unpkg.com/pagedjs@0.4.3/dist/paged.polyfill.js"


# Chromium 헤더/푸터 템플릿. <span class="title"> 은 페이지 <title>에서 자동 채워짐.
HEADER_TEMPLATE = (
    '<div style="font-size:8pt; color:#999; width:100%; padding:0 18mm; '
    'box-sizing:border-box; display:flex; justify-content:space-between; '
    'font-family:-apple-system, sans-serif; -webkit-print-color-adjust:exact;">'
    '<span>{book_title}</span>'
    '<span class="title"></span>'
    '</div>'
)

FOOTER_TEMPLATE = (
    '<div style="font-size:9pt; color:#666; width:100%; text-align:center; '
    'font-family:-apple-system, sans-serif; -webkit-print-color-adjust:exact;">'
    '<span class="pageNumber"></span>'
    '</div>'
)


def find_html_files(build_dir: Path, which: int | None) -> list[Path]:
    files = sorted(build_dir.glob("[0-9][0-9]-*.html"))
    if which is not None:
        files = [f for f in files if f.name.startswith(f"{which:02d}-")]
    return files


def detect_book_title(project_root: Path, override: str | None) -> str:
    """progress.json에서 책 제목을 읽거나, 디렉토리 이름에서 추출."""
    if override:
        return override
    progress = project_root / "progress.json"
    if progress.is_file():
        try:
            data = json.loads(progress.read_text(encoding="utf-8"))
            title = data.get("title")
            if title:
                return title
        except Exception:
            pass
    name = project_root.name
    return re.sub(r"_v\d+$", "", name)


def build_merged_html(build_dir: Path, files: list[Path]) -> Path:
    """모든 챕터 HTML을 하나로 결합한 임시 HTML 작성. 페이지 번호 연속용."""
    if not files:
        raise ValueError("결합할 HTML 파일이 없습니다.")

    head_re = re.compile(r"<head[^>]*>(.*?)</head>", re.DOTALL | re.IGNORECASE)
    body_re = re.compile(r"<body[^>]*>(.*?)</body>", re.DOTALL | re.IGNORECASE)

    first = files[0].read_text(encoding="utf-8")
    head_m = head_re.search(first)
    head_html = head_m.group(1) if head_m else ""
    # head 안의 <title>은 통합본 제목으로 변경
    head_html = re.sub(
        r"<title>.*?</title>",
        "<title>통합본</title>",
        head_html,
        flags=re.DOTALL | re.IGNORECASE,
    )

    bodies: list[str] = []
    for i, html_file in enumerate(files):
        text = html_file.read_text(encoding="utf-8")
        body_m = body_re.search(text)
        body = body_m.group(1) if body_m else text
        if i > 0:
            # 챕터 사이 강제 페이지 분할
            bodies.append(
                '<div style="page-break-before:always; break-before:page; height:0;"></div>'
            )
        bodies.append(body)

    merged = (
        "<!DOCTYPE html>\n<html lang=\"ko\">\n<head>"
        + head_html
        + "</head>\n<body>"
        + "\n".join(bodies)
        + "\n</body>\n</html>"
    )

    out = build_dir / "_merged.html"
    out.write_text(merged, encoding="utf-8")
    return out


def render_pdf(
    html_path: Path,
    pdf_path: Path,
    pagedjs: bool,
    book_title: str = "",
) -> None:
    """Playwright로 HTML을 PDF로 렌더한다."""
    from playwright.sync_api import sync_playwright

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    url = "file://" + quote(str(html_path.resolve()))

    header_html = HEADER_TEMPLATE.format(book_title=book_title)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=["--allow-file-access-from-files"],
        )
        # HiDPI 뷰포트로 이미지 리샘플링 화질 확보
        context = browser.new_context(
            viewport={"width": 1240, "height": 1754},
            device_scale_factor=2,
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        # print.css가 <link media="print">로 걸려 있어 print 미디어를 활성화해야
        # paged.js와 Chromium이 인쇄용 규칙(코드블록 white-space: pre-wrap 등)을 적용한다.
        page.emulate_media(media="print")
        if pagedjs:
            # PDF 렌더링 시에만 Paged.js 주입 — HTML 파일은 건드리지 않음
            page.add_script_tag(url=PAGEDJS_CDN)
            # Paged.js 완료 신호. 'pagedjs_done' 클래스가 우선이지만 일부 챕터에서
            # done 이벤트가 발화 안 되는 케이스가 있어, 페이지 수가 3초간 안정되면
            # 분할 완료로 간주하는 폴백을 둔다.
            page.wait_for_function(
                """() => {
                    if (document.body.classList.contains('pagedjs_done')) return true;
                    const cur = document.querySelectorAll('.pagedjs_page').length;
                    if (cur === 0) return false;
                    const now = performance.now();
                    const stamp = window.__pageStamp;
                    if (!stamp || stamp.count !== cur) {
                        window.__pageStamp = { count: cur, t: now };
                        return false;
                    }
                    return now - stamp.t > 3000;
                }""",
                timeout=120000,
            )
            # 페이지 분할 후 이미지를 새로 fetch한다.
            # 모든 이미지가 실제 로드(complete && naturalWidth>0)될 때까지 대기.
            page.wait_for_function(
                """() => {
                    const imgs = document.querySelectorAll('.pagedjs_pages img');
                    if (imgs.length === 0) return true;
                    return Array.from(imgs).every(
                        img => img.complete && img.naturalWidth > 0
                    );
                }""",
                timeout=60000,
            )
            page.wait_for_timeout(1500)
            page.pdf(
                path=str(pdf_path),
                prefer_css_page_size=True,
                print_background=True,
                display_header_footer=True,
                header_template=header_html,
                footer_template=FOOTER_TEMPLATE,
            )
        else:
            page.emulate_media(media="print")
            page.pdf(
                path=str(pdf_path),
                format="A4",
                margin={
                    "top": "26mm",      # 헤더 공간 (8pt + 여백)
                    "bottom": "20mm",   # 푸터 공간 (9pt + 여백)
                    "left": "18mm",
                    "right": "18mm",
                },
                print_background=True,
                display_header_footer=True,
                header_template=header_html,
                footer_template=FOOTER_TEMPLATE,
            )
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pub-html-build 산출 HTML을 Playwright로 A4 PDF로 변환"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        required=True,
        help="책 프로젝트 루트 경로 (예: projects/사내AI비서_v2)",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        default=None,
        help="특정 챕터 번호만 변환 (예: --chapter 11)",
    )
    parser.add_argument(
        "--no-pagedjs",
        action="store_true",
        help="Paged.js 주입 없이 Chromium 기본 인쇄로 렌더 (빠름, 조판 품질 낮음)",
    )
    parser.add_argument(
        "--book-title",
        type=str,
        default=None,
        help="헤더에 표시할 책 제목. 생략 시 progress.json 또는 디렉토리 이름에서 추출",
    )
    parser.add_argument(
        "--merged",
        action="store_true",
        help="모든 챕터를 하나의 PDF로 결합 빌드 (페이지 번호가 1부터 끝까지 연속)",
    )
    parser.add_argument(
        "--merged-output",
        type=str,
        default=None,
        help="--merged 모드의 출력 파일명 (기본: <책이름>-챕터통합본.pdf)",
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    build_dir = project_root / ".build"
    if not build_dir.is_dir():
        print(
            f"❌ {build_dir} 를 찾지 못했습니다. 먼저 pub-html-build로 HTML을 빌드하세요.\n"
            f"   python .claude/skills/pub-html-build/build_html.py "
            f"--project-root {args.project_root} --chapter {args.chapter or 'N'}",
            file=sys.stderr,
        )
        return 1

    files = find_html_files(build_dir, args.chapter)
    if not files:
        print(
            f"❌ {build_dir} 안에 변환할 HTML이 없습니다. pub-html-build로 먼저 빌드하세요.",
            file=sys.stderr,
        )
        return 1

    pdf_dir = build_dir / "pdf"
    use_pagedjs = not args.no_pagedjs
    book_title = detect_book_title(project_root, args.book_title)

    if args.merged:
        merged_html = build_merged_html(build_dir, files)
        out_name = args.merged_output or f"{project_root.name.split('_v')[0]}-챕터통합본.pdf"
        pdf_path = pdf_dir / out_name
        print(f"📚 통합본 빌드: {len(files)}개 챕터 → {pdf_path.name}")
        render_pdf(merged_html, pdf_path, use_pagedjs, book_title)
        print(f"  ✅ PDF: {pdf_path.relative_to(project_root)}")
        # 임시 HTML은 보관 — 디버깅용
        return 0

    for html_path in files:
        print(f"📄 {html_path.name}")
        pdf_path = pdf_dir / f"{html_path.stem}.pdf"
        render_pdf(html_path, pdf_path, use_pagedjs, book_title)
        print(f"  ✅ PDF: {pdf_path.relative_to(project_root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
