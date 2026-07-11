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
    url = html_path.resolve().as_uri()

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
        # pub-page-fit-html이 생성하는 밀도 오버라이드. Paged.js 조판 전에 주입해야
        # 축소된 padding·gap 기준으로 페이지가 분할된다.
        density_css = html_path.parent / "_pdf-density.css"
        if density_css.exists():
            page.add_style_tag(path=str(density_css))
        # 페이지 단위 개별 조정(특정 이미지 크기·강제 분할 등). density와 달리
        # 빌드 루프가 덮어쓰지 않는 영구 파일 — 저자·에이전트가 직접 관리한다.
        tweaks_css = html_path.parent / "_pdf-tweaks.css"
        if tweaks_css.exists():
            page.add_style_tag(path=str(tweaks_css))
        if pagedjs:
            # Paged.js는 "공백 전용 텍스트 노드"(span 사이 공백·줄바꿈)를 조판 중 제거해
            # 코드가 한 덩어리로 뭉개진다. <pre>로 감싸면 보존되지만 코드블록이 통짜가 되어
            # 페이지 분할이 막히므로, 맨 공백 노드를 Paged.js가 지우지 못하는 명시적 형태
            # (공백 run → NBSP span, 줄바꿈 → <br>)로 변환한다. 렌더 결과는 동일하고
            # 코드블록은 줄 단위 페이지 분할이 그대로 가능하다.
            page.evaluate("""() => {
                const NBSP = String.fromCharCode(160);
                document.querySelectorAll('.code-block').forEach(cb => {
                    if (cb.dataset.wsFixed) return;
                    cb.dataset.wsFixed = '1';
                    const walker = document.createTreeWalker(cb, NodeFilter.SHOW_TEXT);
                    const targets = [];
                    let n;
                    while ((n = walker.nextNode())) {
                        if (n.parentElement.closest('.cb-title')) continue;
                        if (n.nodeValue.includes('\\n') || /^\\s+$/.test(n.nodeValue)) targets.push(n);
                    }
                    targets.forEach(t => {
                        const frag = document.createDocumentFragment();
                        t.nodeValue.split(/(\\n)/).forEach(part => {
                            if (part === '\\n') frag.appendChild(document.createElement('br'));
                            else if (part) {
                                const s = document.createElement('span');
                                s.textContent = part.split(' ').join(NBSP);
                                frag.appendChild(s);
                            }
                        });
                        t.replaceWith(frag);
                    });
                });
                // zoom으로 축소되는 요소(.arch11, .fig-scale-*)는 신형 Chromium에서
                // Paged.js가 zoom 미반영 원본 높이로 측정해 "페이지에 안 들어가는 요소"로
                // 오판하고 섹션 제목을 고아 페이지로 남긴다. 실측 높이를 고정한 래퍼로
                // 감싸 조판 측정값과 실제 렌더 크기를 일치시킨다.
                document.querySelectorAll('.arch11, [class*="fig-scale-"]').forEach(el => {
                    const z = parseFloat(getComputedStyle(el).zoom || '1');
                    if (!z || z === 1 || el.parentElement.dataset.zoomFixed) return;
                    if (el.classList.contains('arch11')) el.style.zoom = '0.75';
                    const h = el.getBoundingClientRect().height;
                    const wrap = document.createElement('div');
                    wrap.dataset.zoomFixed = '1';
                    wrap.style.cssText = 'height:' + h + 'px;overflow:visible;break-inside:avoid;page-break-inside:avoid';
                    el.parentNode.insertBefore(wrap, el);
                    wrap.appendChild(el);
                });
                // "전체 구성도" 섹션은 제목+구성도가 페이지 하나를 거의 채운다. Paged.js의
                // break-after:avoid가 이 경계 케이스에서 제목만 고아 페이지로 밀어내므로,
                // 섹션을 통째로 새 페이지에서 시작시켜 제목과 구성도를 항상 붙인다.
                document.querySelectorAll('.ch-slot').forEach(slot => {
                    slot.style.breakInside = 'avoid';
                    slot.style.pageBreakInside = 'avoid';
                    let prev = slot.previousElementSibling;
                    if (prev && /^H[23]$/.test(prev.tagName)) {
                        prev.style.breakBefore = 'page';
                        prev.style.pageBreakBefore = 'always';
                        prev.style.breakAfter = 'avoid';
                    }
                });
            }""")
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
                    // complete는 로드 성공·실패 모두 true. 소스 파일이 없는 이미지
                    // (미제작 에셋)를 영원히 기다리지 않도록 naturalWidth 조건을 걸지 않는다.
                    return Array.from(imgs).every(img => img.complete);
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
    _trim_trailing_blank_pages(pdf_path)


def _trim_trailing_blank_pages(pdf_path: Path) -> None:
    """조판 끝단에 생기는 빈 페이지(본문 텍스트·이미지 없음)를 뒤에서부터 제거한다.
    헤더·푸터만 찍힌 페이지도 빈 페이지로 간주. pymupdf 미설치 시 조용히 건너뛴다."""
    try:
        import fitz
    except ImportError:
        return
    doc = fitz.open(pdf_path)
    removed = 0
    while len(doc) > 1:
        page = doc[len(doc) - 1]
        rect = page.rect
        body = fitz.Rect(0, rect.height * 0.08, rect.width, rect.height * 0.92)
        has_text = bool(page.get_text(clip=body).strip())
        has_image = bool(page.get_images(full=True))
        if has_text or has_image:
            break
        doc.delete_page(len(doc) - 1)
        removed += 1
    if removed:
        tmp = pdf_path.with_suffix(".tmp.pdf")
        doc.save(str(tmp), deflate=True)
        doc.close()
        tmp.replace(pdf_path)
        print(f"  🧹 꼬리 빈 페이지 {removed}장 제거")
    else:
        doc.close()


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
