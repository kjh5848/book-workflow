#!/usr/bin/env python3
"""사내AI비서_test — PDF 빌드 스크립트 (Typst)"""

import sys
from pathlib import Path

# 스킬 엔진 경로
SKILL_SCRIPTS = Path(__file__).resolve().parent.parent.parent.parent / ".claude/skills/pub-build/references/scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from typst_builder import build  # noqa: E402

BASE = Path(__file__).resolve().parent.parent  # projects/사내AI비서_test

config = {
    "title": "ConnectHR — 사내 AI 비서 만들기 (테스트)",
    "base": BASE,
    "assets_dir": BASE / "assets",
    "mermaid_out": BASE / "book" / "_mermaid_out",
    "template": BASE / "book" / "templates" / "book.typ",
    "font_path": None,

    "front": [],
    "chapters": [
        BASE / "chapters/01-AI에게-물어봤더니-거짓말을-한다.md",
    ],
    "back": [],

    "output_md": BASE / "book" / "ConnectHR_test_통합본.md",
    "output_typ": BASE / "book" / "ConnectHR_test_통합본.typ",
    "output_pdf": BASE / "book" / "book_ConnectHR_test_typst.pdf",
}

if __name__ == "__main__":
    build(config)
