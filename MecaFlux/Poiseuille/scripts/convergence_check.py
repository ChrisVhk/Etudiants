#!/usr/bin/env python3
"""
convergence_check.py - Vérification de la convergence V2
Hagen-Poiseuille OpenFOAM 2412 — Canal 2D

Usage :
    python3 scripts/convergence_check.py
    python3 scripts/convergence_check.py case3
"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

SOLVERS = {
    "case0": "icoFoam",
    "case1": "icoFoam",
    "case2": "icoFoam",
    "case3": "simpleFoam",
    "case4": "potentialFoam",
}
COLORS = {
    "case0": "#1f77b4", "case1": "#2ca02c",
    "case2": "#ff7f0e", "case3": "#d62728",
    "case4": "#9467bd",
}
THRESHOLD = 1e-5

# ──────────────────────────────────────────────────────────────────
def parse_log(case_name):
    solver   = SOLVERS.get(case_name, "icoFoam")
    log_file = BASE_DIR / case_name / f"log.{solver}"

    if not log_file.exists():
        print(f"  ❌ Log absent : {log_file.relative_to(BASE_DIR)}")
        return None

    times, res_p, res_Ux, res_Uy, res_phi = [], [], [], [], []
    exec_time = None
    t_cur     = 0.0

    re_time = re.compile(r"^(?:Time|Iteration)\s*=\s*([\d.eE+\-]+)")
    re_res  = re.compile(
        r"Solving for (\w+),\s+Initial residual\s*=\s*([\d.eE+\-]+)"
        r"(?:,\s+Final residual\s*=\s*([\d.eE+\-]+))?"
    )
    re_exec = re.compile(r"ExecutionTime\s*=\s*([\d.]+)\s*s")

    with open(log_file) as f:
        for line in f:
            m = re_time.match(line)
            if m:
                t_cur = float(m.group(1))
                continue
            m = re_res.search(line)
            if m:
                field = m.group(1)
                res_i = float(m.group(2))
                res_f = float(m.group(3)) if m.group(3) else None
                if field in ("p", "pFinal"):
                    times.append(t_cur); res_p.append(res_i)
                elif field == "Ux":
                    res_Ux.append(res_i)
                elif field == "Uy":
                    res_Uy.append(res_i)
                elif field == "Phi":
                    times.append(float(len(times) + 1))
                    res_phi.append(res_f if res_f is not None else res_i)
                continue
            m = re_exec.search(line)
            if m:
                exec_time = float(m.group(1))

    if not times:
        print(f"  ⚠️  Aucun résidu dans {log_file.name}")
        return None

    target = res_p if len(res_p) else res_phi
    n = min(len(times), len(target))
    return {
        "case":      case_name,
        "solver":    solver,
        "times":     np.array(times[:n]),
        "res_p":     np.array(target[:n]),
        "res_Ux":    np.array(res_Ux[:n]) if len(res_Ux) >= n else None,
        "res_Uy":    np.array(res_Uy[:n]) if len(res_Uy) >= n else None,
        "exec_time": exec_time,
        "target_field": "p" if len(res_p) else "Phi",
    }

def status(data, icons=True):
    if data is None:
        return "? Pas de donnees" if not icons else "❓ Pas de données"
    r = data["res_p"][-1] if len(data["res_p"]) else 1.0
    if data.get("solver") == "potentialFoam":
        if r < 1e-2:
            return "Potentiel resolu" if not icons else f"✅ Potentiel résolu (res={r:.1e})"
        return "Potentiel partiel" if not icons else f"⚠️  Potentiel partiel (res={r:.1e})"
    if r < THRESHOLD:
        return f"Converge (res={r:.1e})" if not icons else f"✅ Convergé   (res={r:.1e})"
    elif r < 1e-3:
        return f"Partiel (res={r:.1e})" if not icons else f"⚠️  Partiel    (res={r:.1e})"
    return f"Divergent (res={r:.1e})" if not icons else f"❌ Divergent  (res={r:.1e})"

def print_report(all_data):
    w = 65
    print(f"\n{'='*w}")
    print("  RAPPORT DE CONVERGENCE — Hagen-Poiseuille V2")
    print(f"{'='*w}")
    print(f"  Seuil : {THRESHOLD:.0e}\n")
    for data in all_data:
        if data is None:
            continue
        print(f"  ── {data['case'].upper()} ({data['solver']}) ──")
        print(f"     {status(data)}")
        print(f"     Champ suivi : {data.get('target_field', 'p')}")
        if data["exec_time"]:
            print(f"     CPU : {data['exec_time']:.1f} s")
        print(f"     Pas  : {len(data['times'])}")
        if data["res_Ux"] is not None and len(data["res_Ux"]):
            print(f"     Résidu Ux final : {data['res_Ux'][-1]:.2e}")
        print()
    print(f"{'='*w}")

def plot_convergence(all_data):
    """2×2 subplots — un par cas."""
    valid = [d for d in all_data if d is not None]
    n     = len(valid)
    cols  = 2
    rows  = (n + 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(13, 5 * rows))
    fig.suptitle(
        "Convergence des résidus — Hagen-Poiseuille V2\n(OpenFOAM 2412)",
        fontsize=13, fontweight="bold"
    )
    axes = np.array(axes).flatten()

    for ax, data in zip(axes, valid):
        c = COLORS.get(data["case"], "gray")
        t = data["times"]

        ax.semilogy(t, data["res_p"],
                    color=c, lw=2, label="Résidu $p$")
        if data["res_Ux"] is not None and len(data["res_Ux"]) == len(t):
            ax.semilogy(t, data["res_Ux"],
                        color=c, lw=1.5, ls="--", alpha=0.7,
                        label="Résidu $U_x$")
        if data["res_Uy"] is not None and len(data["res_Uy"]) == len(t):
            ax.semilogy(t, data["res_Uy"],
                        color=c, lw=1.2, ls=":", alpha=0.5,
                        label="Résidu $U_y$")

        ax.axhline(THRESHOLD, color="red", ls="--", lw=1.5, alpha=0.7,
                   label=f"Seuil {THRESHOLD:.0e}")
        ax.set_title(
            f"{data['case']} — {data['solver']}\n"
            f"{status(data, icons=False).split('(')[0].strip()}",
            fontsize=10
        )
        ax.set_xlabel("Temps / Itération", fontsize=10)
        ax.set_ylabel("Résidu initial", fontsize=10)
        ax.set_ylim(1e-8, 1e0)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", alpha=0.3)
        if data["exec_time"]:
            ax.annotate(f"CPU: {data['exec_time']:.0f} s",
                        xy=(0.98, 0.05), xycoords="axes fraction",
                        ha="right", fontsize=8, color="gray")

    # Masquer axes vides
    for ax in axes[len(valid):]:
        ax.set_visible(False)

    plt.tight_layout()
    out = OUTPUT_DIR / "convergence_V2.png"
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

def plot_summary(all_data):
    """Résidu final par cas — vue synthétique."""
    valid = [d for d in all_data
             if d is not None and len(d["res_p"]) > 0]
    if not valid:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    cases_v  = [d["case"] for d in valid]
    res_fin  = [d["res_p"][-1] for d in valid]
    colors_v = [COLORS.get(c, "gray") for c in cases_v]

    bars = ax.bar(cases_v, res_fin, color=colors_v,
                  alpha=0.85, edgecolor="white", lw=1.5)
    ax.axhline(THRESHOLD, color="red", ls="--", lw=2,
               label=f"Seuil = {THRESHOLD:.0e}")
    ax.set_yscale("log")
    ax.set_ylabel("Résidu final $p$", fontsize=12)
    ax.set_title("Résidu final par cas — Synthèse", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(axis="y", which="both", alpha=0.3)
    for bar, val in zip(bars, res_fin):
        ax.text(bar.get_x() + bar.get_width()/2,
                val * 1.5, f"{val:.1e}",
                ha="center", va="bottom",
                fontsize=9, fontweight="bold")

    plt.tight_layout()
    out = OUTPUT_DIR / "convergence_summary_V2.png"
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  CONVERGENCE — Hagen-Poiseuille V2 (OpenFOAM 2412)")
    print(f"{'='*60}")

    cases = sys.argv[1:] if len(sys.argv) > 1 \
            else list(SOLVERS.keys())

    all_data = [parse_log(c) for c in cases]
    print_report(all_data)

    print("  → Figure 1 : Résidus par cas")
    plot_convergence(all_data)

    print("  → Figure 2 : Synthèse résidus finaux")
    plot_summary(all_data)

    print("\n✅ Vérification terminée.\n")
