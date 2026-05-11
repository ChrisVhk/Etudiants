#!/usr/bin/env python3
"""
stabilization_study.py - Etude de convergence vers regime etabli
Hagen-Poiseuille OpenFOAM 2412

Usage:
    python3 scripts/stabilization_study.py
    python3 scripts/stabilization_study.py case0 case2
"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

CASES = ["case0", "case1", "case2", "case5"]
COLORS = {"case0": "#1f77b4", "case1": "#2ca02c", "case2": "#ff7f0e", "case5": "#8c564b"}
NY = 10
EPS_STAB = 0.01  # 1%


def read_foam_scalar_field(filepath):
    vals = []
    try:
        lines = filepath.read_text().splitlines()
    except Exception:
        return None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("internalField") and "nonuniform" in line:
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
                vals.append(float(lines[i].strip()))
                i += 1
            break
        i += 1

    return np.array(vals) if vals else None


def read_foam_vector_field(filepath):
    vals = []
    try:
        lines = filepath.read_text().splitlines()
    except Exception:
        return None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("internalField") and "nonuniform" in line:
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
                vals.append(np.fromstring(lines[i].strip().strip("()"), sep=" "))
                i += 1
            break
        i += 1

    return np.array(vals) if vals else None


def timestep_dirs(case_path):
    out = []
    for d in case_path.iterdir():
        if d.is_dir():
            try:
                out.append((float(d.name), d.name))
            except ValueError:
                pass
    return [name for _, name in sorted(out)]


def compute_series(case_name):
    case_path = BASE_DIR / case_name
    times = []
    u_max = []
    dpk = []

    for t_str in timestep_dirs(case_path):
        u_file = case_path / t_str / "U"
        p_file = case_path / t_str / "p"
        if not u_file.exists() or not p_file.exists():
            continue

        u_vals = read_foam_vector_field(u_file)
        p_vals = read_foam_scalar_field(p_file)
        if u_vals is None or p_vals is None or len(p_vals) < 2 * NY:
            continue

        try:
            t = float(t_str)
        except ValueError:
            continue

        times.append(t)
        u_max.append(float(np.max(u_vals[:, 0])))
        p_in = p_vals[:NY].mean()
        p_out = p_vals[-NY:].mean()
        dpk.append(float(p_in - p_out))

    if len(times) < 3:
        return None

    return {
        "times": np.array(times),
        "u_max": np.array(u_max),
        "dpk": np.array(dpk),
    }


def first_stable_time(times, values, eps=EPS_STAB):
    if len(values) < 3:
        return None
    final = values[-1]
    if abs(final) < 1e-14:
        return None

    rel = np.abs((values - final) / final)
    for i in range(len(rel)):
        if np.all(rel[i:] <= eps):
            return float(times[i])
    return None


def main(cases):
    print("\n" + "=" * 68)
    print("  ETUDE DE CONVERGENCE VERS REGIME ETABLI (TRANSITOIRE)")
    print("=" * 68)
    print(f"  Critere stabilisation: ecart relatif <= {EPS_STAB * 100:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    summary = []

    for c in cases:
        data = compute_series(c)
        if data is None:
            print(f"  ⚠ {c}: donnees insuffisantes")
            continue

        t = data["times"]
        umax = data["u_max"]
        dpk = data["dpk"]

        t_u = first_stable_time(t, umax)
        t_p = first_stable_time(t, dpk)
        summary.append((c, umax[-1], dpk[-1], t_u, t_p))

        col = COLORS.get(c, "gray")
        u_mean_val = umax[-1]
        dpk_mean_val = dpk[-1]

        axes[0].plot(t, umax, "o-", color=col, lw=1.8, ms=4,
                     label=f"{c}  (final={u_mean_val:.3f} m/s)")
        axes[1].plot(t, dpk, "o-", color=col, lw=1.8, ms=4,
                     label=f"{c}  (final={dpk_mean_val:.4f} m²/s²)")

        # Ligne horizontale de valeur finale
        axes[0].axhline(u_mean_val, color=col, ls=":", lw=1.0, alpha=0.5)
        axes[1].axhline(dpk_mean_val, color=col, ls=":", lw=1.0, alpha=0.5)

        if t_u is not None:
            axes[0].axvline(t_u, color=col, ls="--", lw=1.5, alpha=0.7)
            axes[0].text(t_u + 0.2, u_mean_val * 0.95,
                         f"t_stab={t_u:.0f}s", fontsize=7.5,
                         color=col, va="top")
        if t_p is not None:
            axes[1].axvline(t_p, color=col, ls="--", lw=1.5, alpha=0.7)
            axes[1].text(t_p + 0.2, dpk_mean_val * 0.95,
                         f"t_stab={t_p:.0f}s", fontsize=7.5,
                         color=col, va="top")

    axes[0].set_title(
        "Stabilisation de $U_{max}(t)$\n"
        "Tirets verticaux = instant de stabilisation (écart relatif ≤ 1%)",
        fontsize=10
    )
    axes[0].set_xlabel("Temps simulé (s)", fontsize=11)
    axes[0].set_ylabel("$U_{max}$ (m/s)", fontsize=11)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=9)
    axes[0].text(0.02, 0.97,
                 "Critère de stabilisation :\n"
                 "  |valeur(t) - valeur_finale| / valeur_finale < 1%\n"
                 "Tirets horizontaux = valeur finale",
                 transform=axes[0].transAxes, fontsize=7.5,
                 va="top", ha="left",
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff9c4", alpha=0.9))

    axes[1].set_title(
        "Stabilisation de $\\Delta p_{kin}(t)$\n"
        "Tirets verticaux = instant de stabilisation (écart relatif ≤ 1%)",
        fontsize=10
    )
    axes[1].set_xlabel("Temps simulé (s)", fontsize=11)
    axes[1].set_ylabel("$\\Delta p_{kin}$ (m²/s²)  [pression cinématique]", fontsize=11)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(fontsize=9)

    out = OUTPUT_DIR / "stabilization_V2.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"\n  ✅ {out.relative_to(BASE_DIR)}")

    print("\n  Resume stabilisation:")
    print("  Case     Umax_final   Delta_p_kin_final   t_stab_Umax   t_stab_Delta_p")
    print("  -----------------------------------------------------------------------")
    for c, uf, pf, tu, tp in summary:
        tu_s = f"{tu:.1f}" if tu is not None else "N/A"
        tp_s = f"{tp:.1f}" if tp is not None else "N/A"
        print(f"  {c:<7} {uf:>10.4f} {pf:>19.4f} {tu_s:>13} {tp_s:>16}")

    print("\n✅ Etude de convergence transitoire terminee.\n")


if __name__ == "__main__":
    selected = sys.argv[1:] if len(sys.argv) > 1 else CASES
    main(selected)
