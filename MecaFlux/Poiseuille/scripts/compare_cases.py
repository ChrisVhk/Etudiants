#!/usr/bin/env python3
"""
compare_cases.py - Comparaison quantitative des 4 cas V2
Hagen-Poiseuille OpenFOAM 2412 — Canal 2D

Usage :
    python3 scripts/compare_cases.py
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import re

BASE_DIR   = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

# Physique
H      = 1.0
L      = 10.0
NU_DEFAULT = 0.001
RHO    = 1000.0

CASE_U_MEAN = {
    "case0": 1.0,
    "case1": 0.5,
    "case2": 1.5,
    "case3": 1.5,
    "case4": 1.0,
}

CASES = {
    "case0": {"label": "icoFoam\nU inlet fixe",    "color": "#1f77b4", "solver": "icoFoam"},
    "case1": {"label": "icoFoam\np inlet fixe",    "color": "#2ca02c", "solver": "icoFoam"},
    "case2": {"label": "icoFoam\nU+p mixte",       "color": "#ff7f0e", "solver": "icoFoam"},
    "case3": {"label": "simpleFoam\nsteady-state", "color": "#d62728", "solver": "simpleFoam"},
    "case4": {"label": "potentialFoam\npotentiel", "color": "#9467bd", "solver": "potentialFoam"},
}

NY = 10

def get_case_nu(case_name):
    tp = BASE_DIR / case_name / "constant" / "transportProperties"
    if not tp.exists():
        return NU_DEFAULT
    try:
        content = tp.read_text()
        m = re.search(r"\bnu\b\s+nu\s+\[[^\]]+\]\s+([\d.eE+\-]+);", content)
        if m:
            return float(m.group(1))
    except Exception:
        pass
    return NU_DEFAULT

def u_max_ana(case_name):
    if case_name == "case4":
        return None
    return 1.5 * CASE_U_MEAN.get(case_name, 1.0)

def delta_p_ana_kin(case_name):
    if case_name == "case4":
        return None
    nu = get_case_nu(case_name)
    u = CASE_U_MEAN.get(case_name, 1.0)
    return 12.0 * nu * u * L / H**2

# ──────────────────────────────────────────────────────────────────
def get_vtk_count(case_name):
    vtk_dir = BASE_DIR / case_name / "VTK"
    return len(list(vtk_dir.glob("*.vtm"))) if vtk_dir.exists() else 0

def get_cpu_time(case_name):
    solver   = CASES[case_name]["solver"]
    log_file = BASE_DIR / case_name / f"log.{solver}"
    if not log_file.exists():
        return None
    with open(log_file) as f:
        for line in reversed(f.readlines()):
            if "ExecutionTime" in line:
                try:
                    return float(line.split("=")[1].split("s")[0].strip())
                except:
                    pass
    return None

def get_last_timestep(case_name):
    case_dir = BASE_DIR / case_name
    timesteps = []
    for d in case_dir.iterdir():
        if d.is_dir():
            try:
                timesteps.append(float(d.name))
            except ValueError:
                pass
    if not timesteps:
        return None
    t = max(timesteps)
    return str(int(t)) if t == int(t) else str(t)

def read_foam_scalar_field(filepath):
    values = []
    try:
        with open(filepath) as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("internalField"):
                if "uniform" in line and "nonuniform" not in line:
                    m = re.search(r"uniform\s+([\d.eE+\-]+)", line)
                    if m:
                        values = [float(m.group(1))]
                    break
                if "nonuniform" in line:
                    i += 1
                    while i < len(lines) and not lines[i].strip().isdigit():
                        i += 1
                    if i >= len(lines):
                        break
                    n = int(lines[i].strip())
                    i += 1
                    while i < len(lines) and lines[i].strip() != "(":
                        i += 1
                    i += 1
                    for _ in range(n):
                        if i >= len(lines):
                            break
                        values.append(float(lines[i].strip()))
                        i += 1
                    break
            i += 1
    except Exception:
        return None
    return np.array(values) if values else None

def read_foam_vector_field(filepath):
    values = []
    try:
        with open(filepath) as f:
            lines = f.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("internalField"):
                if "uniform" in line and "nonuniform" not in line:
                    raw = line.replace(";", "").split("uniform", 1)[1].strip()
                    raw = raw.strip("()")
                    values = [np.fromstring(raw, sep=" ")]
                    break
                if "nonuniform" in line:
                    i += 1
                    while i < len(lines) and not lines[i].strip().isdigit():
                        i += 1
                    if i >= len(lines):
                        break
                    n = int(lines[i].strip())
                    i += 1
                    while i < len(lines) and lines[i].strip() != "(":
                        i += 1
                    i += 1
                    for _ in range(n):
                        if i >= len(lines):
                            break
                        raw = lines[i].strip().strip("()")
                        values.append(np.fromstring(raw, sep=" "))
                        i += 1
                    break
            i += 1
    except Exception:
        return None
    return np.array(values) if values else None

def get_u_max(case_name):
    t_str = get_last_timestep(case_name)
    if t_str is None:
        return None
    u_file = BASE_DIR / case_name / t_str / "U"
    if not u_file.exists():
        return None
    u_vals = read_foam_vector_field(u_file)
    if u_vals is None or u_vals.shape[1] < 1:
        return None
    return float(np.max(u_vals[:, 0]))

def get_delta_p(case_name):
    t_str = get_last_timestep(case_name)
    if t_str is None:
        return None
    p_file = BASE_DIR / case_name / t_str / "p"
    if not p_file.exists():
        return None
    p_vals = read_foam_scalar_field(p_file)
    if p_vals is None or len(p_vals) < 2 * NY:
        return None
    p_in = p_vals[:NY].mean()
    p_out = p_vals[-NY:].mean()
    return float(p_in - p_out)

def check_convergence(case_name):
    solver   = CASES[case_name]["solver"]
    log_file = BASE_DIR / case_name / f"log.{solver}"
    if not log_file.exists():
        return "❓ Log absent"
    content = log_file.read_text()
    if "FOAM FATAL" in content or "FOAM exiting" in content:
        return "❌ Erreur"
    if "SIMPLE solution converged" in content:
        return "✅ Convergé (SIMPLE)"
    if content.rstrip().endswith("End"):
        return "✅ Terminé"
    return "⚠️  Incomplet"

def print_table():
    w = 72
    print(f"\n{'='*w}")
    print("  COMPARAISON DES 5 CAS — Hagen-Poiseuille V2")
    print(f"{'='*w}")
    print(f"  {'Cas':<10} {'Solveur':<14} {'Statut':<22} "
          f"{'VTK':>5} {'CPU (s)':>9}")
    print("  " + "─"*68)
    for case, props in CASES.items():
        statut  = check_convergence(case)
        vtk     = get_vtk_count(case)
        cpu     = get_cpu_time(case)
        cpu_str = f"{cpu:.1f}" if cpu else "N/A"
        print(f"  {case:<10} {props['solver']:<14} {statut:<22} "
              f"{vtk:>5} {cpu_str:>9}")
    print("  " + "─"*68)
    print("\n  📐 Référence analytique (Poiseuille plan, p cinématique OpenFOAM) :")
    for case in CASES:
        nu = get_case_nu(case)
        u = CASE_U_MEAN.get(case, 1.0)
        re = u * H / nu
        dp_kin = delta_p_ana_kin(case)
        umax = u_max_ana(case)
        if dp_kin is None or umax is None:
            print(f"     {case}: Re≈{re:.0f} | potentiel (référence visqueuse non applicable)")
        else:
            print(f"     {case}: Re={re:.0f} | Umax_ana={umax:.3f} m/s | "
                  f"Δp_kin={dp_kin:.4f} m²/s² | ΔP={RHO*dp_kin:.1f} Pa")
    print(f"{'='*w}\n")

def plot_bar_comparison():
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle(
        "Comparaison des 4 cas — Hagen-Poiseuille V2\n"
        "(OpenFOAM 2412, Canal 2D)",
        fontsize=13, fontweight="bold"
    )

    case_names = list(CASES.keys())
    colors     = [CASES[c]["color"] for c in case_names]
    labels     = [CASES[c]["label"] for c in case_names]
    x          = np.arange(len(case_names))

    # ── U_max ──────────────────────────────────────────────────
    ax = axes[0]
    u_vals = [get_u_max(c) for c in case_names]
    u_ana_vals = [u_max_ana(c) for c in case_names]
    u_plot = [0.0 if v is None else v for v in u_vals]
    valid_u_ana = [i for i, v in enumerate(u_ana_vals) if v is not None]
    if valid_u_ana:
        ax.plot([x[i] for i in valid_u_ana], [u_ana_vals[i] for i in valid_u_ana],
                "k--", lw=2, marker="x", ms=8, label="Analytique (cas visqueux)")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("$U_{max}$ (m/s)"); ax.set_title("Vitesse maximale")
    ax.set_ylim(0, 2.0); ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
    bars = ax.bar(x, u_plot, color=colors, alpha=0.85,
                  edgecolor="white", lw=1.5)
    for bar, val in zip(bars, u_vals):
        if val is None:
            ax.text(bar.get_x() + bar.get_width()/2,
                    0.02, "N/A", ha="center", va="bottom", fontsize=9)
        else:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.02,
                    f"{val:.2f}", ha="center", va="bottom", fontsize=9)

    # ── ΔP ─────────────────────────────────────────────────────
    ax = axes[1]
    dp_vals = [get_delta_p(c) for c in case_names]
    dp_ana_vals = [delta_p_ana_kin(c) for c in case_names]
    dp_plot = [0.0 if v is None else v for v in dp_vals]
    bars = ax.bar(x, dp_plot, color=colors, alpha=0.85,
                  edgecolor="white", lw=1.5)
    valid_dp_ana = [i for i, v in enumerate(dp_ana_vals) if v is not None]
    if valid_dp_ana:
        ax.plot([x[i] for i in valid_dp_ana], [dp_ana_vals[i] for i in valid_dp_ana],
                "k--", lw=2, marker="x", ms=8, label="Analytique (cas visqueux)")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("$\\Delta p_{kin}$ (m$^2$/s$^2$)")
    ax.set_title("Chute de pression cinématique")
    ax.set_ylim(bottom=0)
    ax.legend(fontsize=8); ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, dp_vals):
        if val is None:
            ax.text(bar.get_x() + bar.get_width()/2,
                    1, "N/A", ha="center", va="bottom", fontsize=9)
        else:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 1,
                    f"{val:.0f}", ha="center", va="bottom", fontsize=9)

    # ── VTK count ──────────────────────────────────────────────
    ax = axes[2]
    vtk_vals = [get_vtk_count(c) for c in case_names]
    bars = ax.bar(x, vtk_vals, color=colors, alpha=0.85,
                  edgecolor="white", lw=1.5)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Fichiers .vtm"); ax.set_title("Fichiers VTK générés")
    ax.grid(axis="y", alpha=0.3)
    for bar, val in zip(bars, vtk_vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 0.2,
                str(val), ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    plt.tight_layout()
    out = OUTPUT_DIR / "comparison_V2.png"
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  COMPARAISON — Hagen-Poiseuille V2 (OpenFOAM 2412)")
    print(f"{'='*60}")
    print_table()
    print("  → Génération du graphique comparatif...")
    plot_bar_comparison()
    print("\n✅ Comparaison terminée.\n")
