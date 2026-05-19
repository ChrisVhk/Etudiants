#!/usr/bin/env python3
"""Build PDF deliverables via pandoc + XeLaTeX.

PACK_DIFFUSION contains ONLY PDFs — no intermediate .md files.

Files generated:
  PACK_DIFFUSION/ETUDIANT_PACK.pdf        — pack complet étudiant (docs 01→07 concaténés)
  PACK_DIFFUSION/07_AIDE_MEMOIRE.pdf      — aide-mémoire A4 standalone (imprimable)
  PACK_DIFFUSION/MEMO_COMMANDES_UNIX.pdf  — mémo commandes UNIX/WSL standalone

Requires: pandoc >= 2.x, texlive-xetex, texlive-fonts-recommended
  sudo apt install pandoc texlive-xetex texlive-fonts-recommended texlive-latex-extra texlive-lang-french
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # WorkSpace/MecaFlux/Poiseuille
WORKSPACE = ROOT.parents[1]                  # WorkSpace/
PACK_DIR = ROOT / "docs" / "PACK_DIFFUSION"

# Options pandoc communes
PANDOC_OPTS = [
    "--pdf-engine=xelatex",
    "-V", "geometry:a4paper,top=2cm,bottom=2cm,left=2.5cm,right=2cm",
    "-V", "lang=fr",
    "-V", "mainfont=DejaVu Sans",
    "-V", "monofont=DejaVu Sans Mono",
    "-V", "fontsize=11pt",
    "-V", "colorlinks=true",
    "-V", "linkcolor=NavyBlue",
    "--highlight-style=tango",
]


def build_pdf(md_paths: list[Path], out_path: Path, title: str | None = None) -> None:
    """Concatène les fichiers markdown et génère un PDF via pandoc."""
    parts: list[str] = []

    # En-tête YAML avec métadonnées
    if title:
        parts.append(
            f"---\ntitle: \"{title}\"\nauthor: \"ENSM Nantes — Génie maritime\"\ndate: \"2025\"\n---\n"
        )

    for i, p in enumerate(md_paths):
        if not p.exists():
            print(f"  –  ignoré (absent) : {p.name}")
            continue
        if i > 0:
            parts.append("\n\n\\newpage\n\n")
        parts.append(p.read_text(encoding="utf-8"))

    if not parts:
        print(f"  –  aucune source valide pour {out_path.name}")
        return

    combined = "\n".join(parts)

    with tempfile.NamedTemporaryFile(
        suffix=".md", mode="w", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(combined)
        tmp_path = Path(tmp.name)

    try:
        result = subprocess.run(
            ["pandoc", str(tmp_path), "-o", str(out_path)] + PANDOC_OPTS,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  ✓  {out_path.relative_to(WORKSPACE)}")
        else:
            print(f"  ✗  {out_path.name}")
            print(result.stderr[:600])
    finally:
        tmp_path.unlink(missing_ok=True)


def main() -> int:
    # Vérification pandoc
    if subprocess.run(["which", "pandoc"], capture_output=True).returncode != 0:
        print("ERREUR : pandoc non trouvé.")
        print("  sudo apt install pandoc texlive-xetex texlive-fonts-recommended")
        return 1

    docs = ROOT / "docs"

    # Docs étudiants dans l'ordre de lecture (GroupeB = version recommandée)
    student_docs = [
        docs / "01_FICHE_CONSIGNE.md",
        docs / "02_QCM_PREREQUIS_GroupeB.md",
        docs / "03_BASE_THEORIQUE.md",
        docs / "04_GUIDE_PAS_A_PAS.md",
        docs / "05_GUIDE_PARAVIEW.md",
        docs / "06_QCM_FINAL_GroupeB.md",
        docs / "07_AIDE_MEMOIRE.md",
    ]

    jobs: list[tuple[list[Path], Path, str | None]] = [
        # Pack complet — tous les docs étudiants en un seul PDF
        (student_docs,
         PACK_DIR / "ETUDIANT_PACK.pdf",
         "TP Hagen-Poiseuille — Pack étudiant complet"),
        # Aide-mémoire standalone (A4 imprimable)
        ([docs / "07_AIDE_MEMOIRE.md"],
         PACK_DIR / "07_AIDE_MEMOIRE.pdf",
         "Aide-mémoire — TP Hagen-Poiseuille"),
        # Mémo UNIX/WSL standalone
        ([WORKSPACE / "VScode&WSL" / "MEMO_COMMANDES_UNIX.md"],
         PACK_DIR / "MEMO_COMMANDES_UNIX.pdf",
         "Mémo commandes UNIX / WSL"),
    ]

    print("Génération des PDFs via pandoc + XeLaTeX…")
    errors = 0
    for md_list, pdf_path, title in jobs:
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            build_pdf(md_list, pdf_path, title)
        except Exception as exc:
            print(f"  ✗  {pdf_path.name} : {exc}")
            errors += 1

    return errors


if __name__ == "__main__":
    raise SystemExit(main())
