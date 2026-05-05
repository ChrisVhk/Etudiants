#!/usr/bin/env python3
"""Build simple PDF booklets from Enonce/PACK_DIFFUSION markdown files.

This script intentionally keeps dependencies minimal (reportlab only)
and avoids any system-level package installation.
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PACK_DIR = ROOT / "Enonce" / "PACK_DIFFUSION"


def to_text_lines(md_content: str) -> list[str]:
    """Convert markdown to plain printable lines for a lightweight PDF export."""
    cleaned = (
        md_content.replace("\t", "    ")
        .replace("**", "")
        .replace("__", "")
        .replace("`", "")
    )
    return cleaned.splitlines()


def md_to_pdf(lines: list[str], out_path: Path) -> None:
    """Render plain text lines into A4 pages with margins and wrapping."""
    c = canvas.Canvas(str(out_path), pagesize=A4)
    page_w, page_h = A4

    margin_left = 18 * mm
    margin_right = 18 * mm
    margin_top = 18 * mm
    margin_bottom = 18 * mm

    usable_w = page_w - margin_left - margin_right
    y = page_h - margin_top
    line_height = 13

    c.setFont("Helvetica", 11)

    def write_wrapped(text: str) -> None:
        nonlocal y

        if not text:
            y -= line_height
            return

        words = text.split(" ")
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if c.stringWidth(candidate, "Helvetica", 11) <= usable_w:
                current = candidate
            else:
                if y <= margin_bottom:
                    c.showPage()
                    c.setFont("Helvetica", 11)
                    y = page_h - margin_top
                c.drawString(margin_left, y, current)
                y -= line_height
                current = word

        if current:
            if y <= margin_bottom:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = page_h - margin_top
            c.drawString(margin_left, y, current)
            y -= line_height

    for raw in lines:
        if raw.startswith("#"):
            if y <= margin_bottom + line_height * 2:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = page_h - margin_top
            title = raw.lstrip("#").strip()
            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_left, y, title)
            y -= line_height + 2
            c.setFont("Helvetica", 11)
            continue

        write_wrapped(raw)

    c.save()


def main() -> int:
    pairs = [
        (PACK_DIR / "ETUDIANT_PACK.md", PACK_DIR / "ETUDIANT_PACK.pdf"),
        (PACK_DIR / "ENSEIGNANT_PACK.md", PACK_DIR / "ENSEIGNANT_PACK.pdf"),
    ]

    for md_path, pdf_path in pairs:
        if not md_path.exists():
            raise FileNotFoundError(f"Missing input file: {md_path}")
        lines = to_text_lines(md_path.read_text(encoding="utf-8"))
        md_to_pdf(lines, pdf_path)
        print(pdf_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
