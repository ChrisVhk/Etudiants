#!/usr/bin/env python3
"""
plot_results.py - Graphiques des résultats V2
Hagen-Poiseuille OpenFOAM 2412 — Canal 2D

Usage :
    python3 scripts/plot_results.py
    python3 scripts/plot_results.py case0 case3
"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

# Physique
H      = 1.0
L      = 10.0
NU_DEFAULT = 0.001
RHO    = 1000.0
U_MEAN = 1.0

COLORS = {
    "case0": "#1f77b4",
    "case1": "#2ca02c",
    "case2": "#ff7f0e",
    "case3": "#d62728",
    "case4": "#9467bd",
}
LABELS = {
    "case0": "icoFoam — U inlet fixe",
    "case1": "icoFoam — p inlet fixe",
    "case2": "icoFoam — U+p mixte",
    "case3": "simpleFoam — steady-state",
    "case4": "potentialFoam — écoulement potentiel",
}
SOLVERS = {
    "case0": "icoFoam",
    "case1": "icoFoam",
    "case2": "icoFoam",
    "case3": "simpleFoam",
    "case4": "potentialFoam",
}

NY = 10
X_PROFILE_TARGET = 9.0

CASE_U_MEAN = {
    "case0": 1.0,
    "case1": 0.5,
    "case2": 1.5,
    "case3": 1.5,
    "case4": 1.0,
}

# ──────────────────────────────────────────────────────────────────
def analytical_profile(y, u_mean=U_MEAN):
    return 1.5 * u_mean * (1.0 - (2.0 * y / H) ** 2)

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

def extract_velocity_profile(case_name):
    t_str = get_last_timestep(case_name)
    if t_str is None:
        return None

    u_file = BASE_DIR / case_name / t_str / "U"
    if not u_file.exists():
        return None

    u_vals = read_foam_vector_field(u_file)
    if u_vals is None or len(u_vals) < NY or u_vals.shape[1] < 1:
        return None

    ux = u_vals[:, 0]
    if len(ux) % NY != 0:
        return None

    nx = len(ux) // NY
    dx = L / nx
    x_idx = max(0, min(nx - 1, int(X_PROFILE_TARGET / dx)))
    start = x_idx * NY
    stop = start + NY

    y = np.linspace(-H / 2 + H / (2 * NY), H / 2 - H / (2 * NY), NY)
    return y, ux[start:stop]

def extract_pressure_gradient(case_name):
    t_str = get_last_timestep(case_name)
    if t_str is None:
        return None

    p_file = BASE_DIR / case_name / t_str / "p"
    if not p_file.exists():
        return None

    p_vals = read_foam_scalar_field(p_file)
    if p_vals is None or len(p_vals) < NY or len(p_vals) % NY != 0:
        return None

    nx = len(p_vals) // NY
    dx = L / nx
    x = np.linspace(dx / 2, L - dx / 2, nx)
    p_line = p_vals.reshape(nx, NY).mean(axis=1)
    return x, p_line

def read_residuals(case_name):
    """Parse log OpenFOAM → (times, res_p, res_Ux)."""
    solver   = SOLVERS.get(case_name, "icoFoam")
    log_file = BASE_DIR / case_name / f"log.{solver}"
    if not log_file.exists():
        return None

    times, res_p, res_Ux = [], [], []
    t_cur = 0.0
    re_t  = re.compile(r"^(?:Time|Iteration)\s*=\s*([\d.eE+\-]+)")
    re_r  = re.compile(
        r"Solving for (\w+),\s+Initial residual\s*=\s*([\d.eE+\-]+)"
    )

    with open(log_file) as f:
        for line in f:
            m = re_t.match(line)
            if m:
                t_cur = float(m.group(1))
                continue
            m = re_r.search(line)
            if m:
                field, res = m.group(1), float(m.group(2))
                if field in ("p", "pFinal"):
                    times.append(t_cur)
                    res_p.append(res)
                elif field == "Ux":
                    res_Ux.append(res)

    if not times:
        return None
    n = min(len(times), len(res_p))
    return {
        "times":  np.array(times[:n]),
        "res_p":  np.array(res_p[:n]),
        "res_Ux": np.array(res_Ux[:n]) if len(res_Ux) >= n else None,
    }

# ── Figure 1 : Profils de vitesse ─────────────────────────────────
def plot_velocity_profiles(cases):
    fig, ax = plt.subplots(figsize=(7, 7))

    # Analytique de référence globale (case0)
    y_ana = np.linspace(-H/2, H/2, 300)
    ax.plot(analytical_profile(y_ana, CASE_U_MEAN.get("case0", U_MEAN)), y_ana,
            "k--", lw=2.5, zorder=5,
        label=f"Analytique case0\n$U_{{max}}={1.5*CASE_U_MEAN.get('case0', U_MEAN):.2f}$ m/s")
    ax.axvline(1.5 * CASE_U_MEAN.get("case0", U_MEAN), color="gray", ls=":", alpha=0.4, lw=1)
    ax.axhline(0,            color="gray", ls=":", alpha=0.4, lw=1)

    # Numérique : extrait des champs OpenFOAM
    for case in cases:
        profile = extract_velocity_profile(case)
        if profile is None:
            print(f"  ⚠️  Profil non disponible : {case}")
            continue
        y_cells, u_num = profile
        ax.plot(u_num, y_cells, "o-",
                color=COLORS.get(case, "gray"), lw=1.5, ms=6,
                label=LABELS.get(case, case))

    ax.set_xlabel("$U_x$ (m/s)", fontsize=13)
    ax.set_ylabel("$y$ (m)", fontsize=13)
    ax.set_title("Profils de vitesse — 4 cas\n(Poiseuille plan, canal 2D)",
                 fontsize=12)
    ax.set_xlim(-0.05, 1.75)
    ax.set_ylim(-0.55, 0.55)
    ax.legend(fontsize=9, loc="center left")
    ax.grid(True, alpha=0.3)

    out = OUTPUT_DIR / "velocity_profiles_V2.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ── Figure 2 : Résidus ────────────────────────────────────────────
def plot_residuals(cases):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Résidus de convergence — Hagen-Poiseuille V2",
                 fontsize=13, fontweight="bold")

    for case in cases:
        data = read_residuals(case)
        if data is None:
            print(f"  ⚠️  Résidus non disponibles : {case}")
            continue
        c   = COLORS.get(case, "gray")
        lbl = LABELS.get(case, case)
        axes[0].semilogy(data["times"], data["res_p"],
                         color=c, lw=1.5, label=lbl)
        if data["res_Ux"] is not None:
            axes[1].semilogy(data["times"], data["res_Ux"],
                             color=c, lw=1.5, label=lbl)

    for ax, title, ylabel in zip(
        axes,
        ["Résidus — Pression $p$", "Résidus — Vitesse $U_x$"],
        ["Résidu initial $p$",     "Résidu initial $U_x$"],
    ):
        ax.axhline(1e-5, color="red", ls="--", lw=1.2,
                   alpha=0.6, label="Seuil 1e-5")
        ax.set_xlabel("Temps / Itération", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.set_title(title, fontsize=11)
        ax.legend(fontsize=8)
        ax.grid(True, which="both", alpha=0.3)

    out = OUTPUT_DIR / "residuals_V2.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ── Figure 3 : Gradient de pression ──────────────────────────────
def plot_pressure_gradient(cases):
    fig, ax = plt.subplots(figsize=(8, 5))
    x_ana = np.linspace(0, L, 200)

    for case in cases:
        u_ref = CASE_U_MEAN.get(case, U_MEAN)
        nu = get_case_nu(case)
        # p est cinématique dans OpenFOAM incompressible [m2/s2]
        dpdx_kin = 12.0 * nu * u_ref / H**2
        p_ana = dpdx_kin * (L - x_ana)
        ax.plot(x_ana, p_ana, ls="--", lw=1.2,
                color=COLORS.get(case, "gray"), alpha=0.6,
                label=f"Analytique {case}")

        gradient = extract_pressure_gradient(case)
        if gradient is None:
            print(f"  ⚠️  Gradient de pression non disponible : {case}")
            continue
        x_num, p_num = gradient
        ax.plot(x_num, p_num,
                color=COLORS.get(case, "gray"), lw=1.5, alpha=0.8,
                label=LABELS.get(case, case))

    ax.set_xlabel("Position $x$ (m)", fontsize=12)
    ax.set_ylabel("Pression cinématique $p$ (m$^2$/s$^2$)", fontsize=12)
    ax.set_title("Gradient de pression cinématique le long du canal", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    out = OUTPUT_DIR / "pressure_gradient_V2.png"
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  GRAPHIQUES — Hagen-Poiseuille V2 (OpenFOAM 2412)")
    print(f"{'='*60}")
    print(f"  Sortie : Results/\n")

    cases = sys.argv[1:] if len(sys.argv) > 1 \
            else ["case0", "case1", "case2", "case3"]

    print("  → Figure 1 : Profils de vitesse")
    plot_velocity_profiles(cases)

    print("  → Figure 2 : Résidus de convergence")
    plot_residuals(cases)

    print("  → Figure 3 : Gradient de pression")
    plot_pressure_gradient(cases)

    print("\n✅ Graphiques générés dans Results/\n")
