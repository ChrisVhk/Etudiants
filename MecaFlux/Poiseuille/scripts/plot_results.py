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
    "case5": "#8c564b",
}
LABELS = {
    "case0": "icoFoam — Re=1000 (référence)",
    "case1": "icoFoam — Re=500 (effet Re faible)",
    "case2": "icoFoam — Re=1500 (effet Re élevé)",
    "case3": "simpleFoam — Re=1500 (steady-state)",
    "case4": "potentialFoam — inviscide",
    "case5": "icoFoam — L=200m (Poiseuille établi)",
}
SOLVERS = {
    "case0": "icoFoam",
    "case1": "icoFoam",
    "case2": "icoFoam",
    "case3": "simpleFoam",
    "case4": "potentialFoam",
    "case5": "icoFoam",
}

NY = 10
X_PROFILE_TARGET = 9.0

CASE_U_MEAN = {
    "case0": 1.0,
    "case1": 0.5,
    "case2": 1.5,
    "case3": 1.5,
    "case4": 1.0,
    "case5": 1.0,
}

CASE_L = {
    "case0": 100.0,
    "case1":  50.0,
    "case2": 150.0,
    "case3": 150.0,
    "case4":  10.0,
    "case5": 200.0,
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
    # Use actual canal length for this case
    case_l = CASE_L.get(case_name, L)
    dx = case_l / nx
    # Profile at 90% of canal length
    x_target = 0.9 * case_l
    x_idx = max(0, min(nx - 1, int(x_target / dx)))
    start = x_idx * NY
    stop = start + NY

    y = np.linspace(-H / 2 + H / (2 * NY), H / 2 - H / (2 * NY), NY)
    return y, ux[start:stop]

def extract_profile_at_x(case_name, x_fraction):
    """Profil de vitesse à x = x_fraction * L (0 < x_fraction <= 1)."""
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
    nx     = len(ux) // NY
    case_l = CASE_L.get(case_name, L)
    dx     = case_l / nx
    x_target = min(x_fraction * case_l, case_l - dx / 2)
    x_idx    = max(0, min(nx - 1, int(x_target / dx)))
    x_actual = (x_idx + 0.5) * dx
    y = np.linspace(-H / 2 + H / (2 * NY), H / 2 - H / (2 * NY), NY)
    return y, ux[x_idx * NY:(x_idx + 1) * NY], x_actual

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

    case_l = CASE_L.get(case_name, L)
    nx = len(p_vals) // NY
    dx = case_l / nx
    x = np.linspace(dx / 2, case_l - dx / 2, nx)
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
    fig, axes = plt.subplots(1, 2, figsize=(15, 6),
                             gridspec_kw={"width_ratios": [1.6, 1]})
    fig.suptitle(
        "Profils de vitesse transversaux — Poiseuille plan 2D\n"
        "OpenFOAM à x = 9 m  vs  solution analytique établie",
        fontsize=12, fontweight="bold"
    )

    # ── Panneau gauche : profils ──────────────────────────────────
    ax = axes[0]
    y_ana = np.linspace(-H / 2, H / 2, 300)

    for case in cases:
        u_mean = CASE_U_MEAN.get(case, U_MEAN)
        nu = get_case_nu(case)
        re = u_mean * H / nu

        # Parabole analytique propre à ce cas (tirets)
        u_ana_prof = analytical_profile(y_ana, u_mean)
        ax.plot(u_ana_prof, y_ana, ls="--", lw=1.5,
                color=COLORS.get(case, "gray"), alpha=0.45)

        # Profil numérique OpenFOAM (trait plein)
        result = extract_velocity_profile(case)
        if result is None:
            print(f"  ⚠️  Profil non disponible : {case}")
            continue
        y_cells, u_num = result
        u_max_num = float(np.max(u_num))
        u_max_ana = 1.5 * u_mean
        err_pct = abs(u_max_num - u_max_ana) / u_max_ana * 100

        lbl = (f"{LABELS.get(case, case)}\n"
               f"  $U_{{max}}$={u_max_num:.2f} m/s  "
               f"(écart={err_pct:.0f}%)")
        ax.plot(u_num, y_cells, "o-",
                color=COLORS.get(case, "gray"), lw=2, ms=6,
                label=lbl)

    # Parois du canal
    ax.axhline( H / 2, color="black", lw=2.5, zorder=10)
    ax.axhline(-H / 2, color="black", lw=2.5, zorder=10)
    ax.axhline(0, color="gray", ls=":", lw=0.8, alpha=0.4)
    ax.text(0.01,  H / 2 + 0.02, "Paroi (no-slip)", fontsize=7.5, color="black")
    ax.text(0.01, -H / 2 - 0.05, "Paroi (no-slip)", fontsize=7.5, color="black")

    ax.set_xlabel("$U_x$ (m/s)", fontsize=12)
    ax.set_ylabel("$y$ (m)  [position transversale]", fontsize=12)
    ax.set_title(
        "Trait plein + ● = simulation numérique\n"
        "Tirets = profil parabolique établi (Poiseuille, analytique)\n"
        "Écart = effet de zone d'entrée (écoulement non encore développé)",
        fontsize=9
    )
    ax.set_ylim(-H / 2 - 0.08, H / 2 + 0.08)
    ax.legend(fontsize=8, loc="center left", framealpha=0.92)
    ax.grid(True, alpha=0.3)

    # Boîte pédagogique
    ax.text(0.03, 0.04,
            "Les tirets représentent la solution EXACTE de Poiseuille\n"
            "pour un écoulement PLEINEMENT ÉTABLI.\n"
            "Si le profil numérique s'en écarte, c'est que\n"
            "l'écoulement n'est pas encore développé à x=9m.",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#fffde7", alpha=0.95))

    # ── Panneau droit : taux de développement ────────────────────
    ax2 = axes[1]
    vis_cases = [c for c in cases if c != "case4"]
    y_pos = np.arange(len(vis_cases))

    for i, case in enumerate(vis_cases):
        u_mean = CASE_U_MEAN.get(case, U_MEAN)
        nu_c = get_case_nu(case)
        re = u_mean * H / nu_c
        l_dev = 0.05 * re * H
        pct = min(10.0 / l_dev * 100, 100.0)

        ax2.barh(y_pos[i], pct, height=0.5,
                 color=COLORS.get(case, "gray"), alpha=0.82)
        ax2.text(pct + 1.5, y_pos[i],
                 f"{pct:.0f}%  (L_dev ≈ {l_dev:.0f} m)",
                 va="center", fontsize=9)

    ax2.axvline(100, color="green", ls="--", lw=2.5,
                label="100 % = écoulement établi")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(
        [f"{c}\n(Re = {CASE_U_MEAN.get(c, 1.0) * H / get_case_nu(c):.0f})"
         for c in vis_cases],
        fontsize=9
    )
    ax2.set_xlim(0, 140)
    ax2.set_xlabel("% de développement hydrodynamique à x = 10 m", fontsize=10)
    ax2.set_title(
        "Longueur de développement\n"
        "$L_{dev} = 0.05 \\times Re \\times H$",
        fontsize=10
    )
    ax2.legend(fontsize=9, loc="lower right")
    ax2.grid(axis="x", alpha=0.3)

    ax2.text(0.03, 0.03,
             "Un canal de 10 m est trop court pour que\n"
             "l'écoulement atteigne le profil parabolique\n"
             "théorique. → case5 (L=100 m) résout cela.",
             transform=ax2.transAxes, fontsize=7.5, va="bottom",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e9", alpha=0.9))

    plt.tight_layout()
    out = OUTPUT_DIR / "velocity_profiles_V2.png"
    plt.savefig(out, dpi=150)
    print(f"  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ── Figure 2 : Développement spatial du profil ───────────────────
def plot_development_profiles(cases):
    """Coupes transversales à 25 %, 50 %, 75 % et 95 % de L pour chaque cas."""
    FRACTIONS = [0.25, 0.50, 0.75, 0.95]
    FRAC_LABELS = ["25 %", "50 %", "75 %", "95 %"]

    valid_cases = [c for c in cases if c != "case4"]
    n = len(valid_cases)
    if n == 0:
        return

    fig, axes = plt.subplots(1, n, figsize=(3.2 * n, 5), sharey=True)
    if n == 1:
        axes = [axes]
    fig.suptitle(
        "Développement spatial du profil de vitesse — coupes à 25 %, 50 %, 75 %, 95 % du canal\n"
        "Tirets noirs = parabole analytique Poiseuille établi",
        fontsize=11, fontweight="bold"
    )

    cmap = plt.cm.plasma
    frac_colors = [cmap(0.15), cmap(0.40), cmap(0.65), cmap(0.90)]

    for ax, case in zip(axes, valid_cases):
        u_mean = CASE_U_MEAN.get(case, U_MEAN)
        case_l = CASE_L.get(case, L)
        nu     = get_case_nu(case)
        Re     = u_mean * H / nu
        L_dev  = 0.05 * Re * H

        y_ana  = np.linspace(-H / 2, H / 2, 200)
        u_ana  = analytical_profile(y_ana, u_mean)
        ax.plot(u_ana, y_ana, "k--", lw=1.8, label="Analytique", zorder=5)

        for frac, flabel, fcol in zip(FRACTIONS, FRAC_LABELS, frac_colors):
            result = extract_profile_at_x(case, frac)
            if result is None:
                continue
            y_num, u_num, x_actual = result
            umax_num = float(np.max(u_num))
            umax_ana = 1.5 * u_mean
            err = abs(umax_num - umax_ana) / umax_ana * 100
            ax.plot(u_num, y_num, "-o", ms=4, lw=1.6, color=fcol,
                    label=f"x={flabel}  ({x_actual:.0f} m)  Δ={err:.0f}%")

        ax.set_title(
            f"{case}\nRe={Re:.0f}  L={case_l:.0f} m\n"
            f"$L_{{dev}}$={L_dev:.0f} m  (L/{L_dev:.0f}={case_l/L_dev:.1f}×)",
            fontsize=8.5
        )
        ax.set_xlabel("$U_x$ (m/s)", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7, loc="upper left")

        # Zone développée annotée
        x_dev_frac = min(L_dev / case_l, 1.0)
        ax.axhline(0, color="gray", lw=0.5, ls=":")

    axes[0].set_ylabel("Position $y$ (m)", fontsize=10)

    plt.tight_layout()
    out = OUTPUT_DIR / "development_profiles_V2.png"
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  ✅ {out.relative_to(BASE_DIR)}")


# ── Figure 3 : Résidus ────────────────────────────────────────────
def plot_residuals(cases):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Résidus de convergence — Hagen-Poiseuille V2",
                 fontsize=13, fontweight="bold")

    # Boîte pédagogique globale (axe de gauche)
    expl = (
        "Qu'est-ce qu'un résidu ?\n"
        "C'est l'écart entre deux itérations consécutives.\n"
        "Convergé ≠ Terminé !\n"
        "• Résidu < 10⁻⁵ → convergence numérique\n"
        "• Résidu > 10⁻³ → solution peu fiable"
    )

    for case in cases:
        data = read_residuals(case)
        if data is None:
            print(f"  ⚠️  Résidus non disponibles : {case}")
            continue
        c   = COLORS.get(case, "gray")
        lbl = LABELS.get(case, case)
        axes[0].semilogy(data["times"], data["res_p"],
                         color=c, lw=1.8, label=lbl)
        if data["res_Ux"] is not None:
            axes[1].semilogy(data["times"], data["res_Ux"],
                             color=c, lw=1.8, label=lbl)

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
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(
        "Évolution axiale de la pression cinématique — Canal 2D\n"
        "Pression cinématique p [m²/s²] = p_SI [Pa] / ρ  (ρ = 1000 kg/m³)",
        fontsize=11, fontweight="bold"
    )

    ax = axes[0]
    for case in cases:
        case_l = CASE_L.get(case, L)
        x_ana = np.linspace(0, case_l, 300)
        u_ref = CASE_U_MEAN.get(case, U_MEAN)
        nu = get_case_nu(case)
        dpdx_kin = 12.0 * nu * u_ref / H**2
        p_ana = dpdx_kin * (case_l - x_ana)
        ax.plot(x_ana, p_ana, ls="--", lw=1.5,
                color=COLORS.get(case, "gray"), alpha=0.55,
                label=f"Analytique {case}  (dp/dx={dpdx_kin*RHO:.1f} Pa/m)")

        gradient = extract_pressure_gradient(case)
        if gradient is None:
            print(f"  ⚠️  Gradient de pression non disponible : {case}")
            continue
        x_num, p_num = gradient
        ax.plot(x_num, p_num,
                color=COLORS.get(case, "gray"), lw=2, alpha=0.9,
                label=LABELS.get(case, case))

    ax.set_xlabel("Position axiale $x$ (m)", fontsize=12)
    ax.set_ylabel("Pression cinématique $p$ (m²/s²)", fontsize=12)
    ax.set_title(
        "Profil de pression cinématique le long du canal\n"
        "Tirets = linéaire analytique · Trait plein = simulation",
        fontsize=9
    )
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.03,
            "Dans OpenFOAM incompressible, p = P/ρ\n"
            "Pour convertir en Pa : multiplier par ρ = 1000 kg/m³\n"
            "Gradient analytique (Poiseuille) : dp/dx = 12νU/H²",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#fce4ec", alpha=0.9))

    # Panneau droit : chute de pression totale ΔP en Pa
    ax2 = axes[1]
    vis_cases = [c for c in cases if c != "case4"]
    x2 = np.arange(len(vis_cases))
    dp_num  = []
    dp_ana  = []
    colors2 = []
    for case in vis_cases:
        u_ref = CASE_U_MEAN.get(case, U_MEAN)
        nu = get_case_nu(case)
        case_l = CASE_L.get(case, L)
        dp_ana.append(12.0 * nu * u_ref / H**2 * case_l * RHO)
        grad = extract_pressure_gradient(case)
        if grad is not None:
            p_num = grad[1]
            dp_num.append((p_num[0] - p_num[-1]) * RHO)
        else:
            dp_num.append(0.0)
        colors2.append(COLORS.get(case, "gray"))

    width = 0.35
    bars1 = ax2.bar(x2 - width/2, dp_ana, width, label="Analytique (établi)",
                    color=colors2, alpha=0.45, edgecolor="gray", hatch="//")
    bars2 = ax2.bar(x2 + width/2, dp_num, width, label="OpenFOAM",
                    color=colors2, alpha=0.88)
    for i, (va, vn) in enumerate(zip(dp_ana, dp_num)):
        err = abs(vn - va) / va * 100 if va > 0 else 0
        ax2.text(x2[i] + width/2, vn + 2, f"{vn:.0f} Pa\n(+{err:.0f}%)",
                 ha="center", va="bottom", fontsize=8)
        ax2.text(x2[i] - width/2, va + 2, f"{va:.0f} Pa",
                 ha="center", va="bottom", fontsize=8, color="gray")

    ax2.set_xticks(x2)
    ax2.set_xticklabels(
        [f"{c}\nRe={CASE_U_MEAN.get(c,1.0)*H/get_case_nu(c):.0f}" for c in vis_cases],
        fontsize=9
    )
    ax2.set_ylabel("Chute de pression ΔP (Pa)", fontsize=11)
    ax2.set_title(
        "ΔP numérique vs analytique (en Pa)\n"
        "Écart = écoulement non développé (zone d'entrée)",
        fontsize=9
    )
    ax2.legend(fontsize=9)
    ax2.grid(axis="y", alpha=0.3)

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
            else ["case0", "case1", "case2", "case3", "case5"]

    print("  → Figure 1 : Profils de vitesse (sortie de canal)")
    plot_velocity_profiles(cases)

    print("  → Figure 2 : Développement spatial (coupes 25/50/75/95 %)")
    plot_development_profiles(cases)

    print("  → Figure 3 : Résidus de convergence")
    plot_residuals(cases)

    print("  → Figure 4 : Gradient de pression")
    plot_pressure_gradient(cases)

    print("\n✅ Graphiques générés dans Results/\n")
