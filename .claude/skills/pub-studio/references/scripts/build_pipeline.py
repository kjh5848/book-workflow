"""빌드 파이프라인 — typst_builder.py 래핑

MD→Typst→PDF/SVG 전체 파이프라인을 OOP 인터페이스로 제공.
캐시는 소유하지 않음 — 호출자(PreviewServer)가 BuildCache로 관리.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

from models import BuildResult, DesignState, ImageInfo
from design_engine import DesignEngine
from image_registry import ImageRegistry

# typst_builder.py 위치
_SCRIPTS_DIR = (
    Path(__file__).resolve().parents[3]
    / "pub-build"
    / "references"
    / "scripts"
)


def _get_typst_builder():
    if str(_SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(_SCRIPTS_DIR))
    import typst_builder
    return typst_builder


class BuildPipeline:
    """MD→Typst→PDF/SVG 빌드 엔진.

    typst_builder.py 함수에 위임하되, ImageRegistry를 통합하여
    개별 이미지 오버라이드를 Stage 2에서 적용한다.
    """

    def __init__(self, config: dict):
        self._config = config
        self._image_registry = ImageRegistry()
        self._design_engine = DesignEngine()

    @property
    def image_registry(self) -> ImageRegistry:
        return self._image_registry

    @property
    def config(self) -> dict:
        return self._config

    def update_config(self, config: dict):
        self._config = config

    # ── Stage 1: MD → raw .typ ──

    def build_raw_typ(
        self,
        front: list[Path],
        chapters: list[Path],
        back: list[Path],
    ) -> str:
        """Stage 1: MD 파일 통합 → Pandoc 변환 → 후처리 → raw .typ 문자열.

        완료 후 image_registry.scan_raw_typ() 자동 호출.
        """
        tb = _get_typst_builder()
        raw_typ = tb.build_raw_typ(
            front=front,
            chapters=chapters,
            back=back,
            mermaid_out=self._config.get("mermaid_out"),
            assets_dir=self._config.get("assets_dir"),
            md_output=self._config.get("output_md"),
            image_border_preset=self._config.get("image_border_preset", "plain"),
            use_image_variables=self._config.get("use_image_variables", True),
        )
        # Stage 1 완료 → 이미지 스캔
        self._image_registry.scan_raw_typ(raw_typ)
        return raw_typ

    # ── Stage 2: raw .typ + design → final .typ ──

    def assemble_final_typ(
        self,
        raw_typ: str,
        design_state: DesignState,
        skip_cover: bool = False,
        skip_toc: bool = False,
    ) -> str:
        """Stage 2: 이미지 오버라이드 적용 → 디자인 조립 → template merge.

        1. image_registry.apply_overrides()로 개별 이미지 width/style 교체
        2. design_engine으로 컴포넌트 조립
        3. typst_builder.merge_template_and_content()로 최종 .typ 생성
        """
        tb = _get_typst_builder()

        # 1. 이미지 오버라이드 적용
        content = self._image_registry.apply_overrides(raw_typ)

        # 2. design_arg 구성
        design_arg = self._design_engine.build_design_arg(design_state)

        # 3. merge
        final_typ = tb.merge_template_and_content(
            template_path=Path(self._config["template"]),
            content=content,
            design=design_arg,
            design_state=design_state.to_server_dict(),
            skip_cover=skip_cover,
            skip_toc=skip_toc,
        )
        return final_typ

    # ── 컴파일 ──

    def compile_svg(self, typ_path: Path, svg_dir: Path) -> int:
        """컴파일 .typ → 페이지별 SVG. 페이지 수 반환."""
        tb = _get_typst_builder()
        font_path = self._config.get("font_path")
        fp = Path(font_path) if font_path else None
        return tb.typst_compile_svg(typ_path, svg_dir, font_path=fp)

    def compile_pdf(self, typ_path: Path, pdf_path: Path) -> bool:
        """컴파일 .typ → PDF. 성공 여부 반환."""
        tb = _get_typst_builder()
        font_path = self._config.get("font_path")
        fp = Path(font_path) if font_path else None
        return tb.typst_compile(typ_path, pdf_path, font_path=fp)

    # ── 유틸 ──

    @staticmethod
    def resolve_file_lists(
        project_path: Path, files_dict: dict
    ) -> tuple[list[Path], list[Path], list[Path]]:
        """파일 상대경로 dict → Path 리스트 (front, chapters, back)."""
        front = [
            project_path / f
            for f in files_dict.get("front", [])
            if (project_path / f).exists()
        ]
        chapters = [
            project_path / f
            for f in files_dict.get("chapters", [])
            if (project_path / f).exists()
        ]
        back = [
            project_path / f
            for f in files_dict.get("back", [])
            if (project_path / f).exists()
        ]
        return front, chapters, back

    @staticmethod
    def check_dependencies() -> bool:
        """typst, pandoc 설치 확인."""
        tb = _get_typst_builder()
        return tb.check_dependencies()
