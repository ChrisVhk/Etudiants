#!/usr/bin/env python3
"""
analyze_results.py - Analyse statistique des résultats V2
Hagen-Poiseuille OpenFOAM 2412 — Canal 2D

Usage (depuis n'importe où) :
    python3 scripts/analyze_results.py
    python3 scripts/analyze_results.py case0
    python3 scripts/analyze_results.py case0 case1 case2 case3
"""

import sys
import re
import numpy as np
from pathlib import Path

# ── Chemin relatif : scripts/ → parent = Poiseuille/ ──────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

CASES = ["case0", "case1", "case2", "case3", "case4"]

# Physique — canal 2D (Poiseuille plan)
H      = 1.0      # hauteur canal (m)
L      = 10.0     # longueur canal (m)
NU_DEFAULT = 0.001  # viscosité cinématique (m²/s), fallback
RHO    = 1000.0   # densité (kg/m³)
CASE_U_MEAN = {
    "case0": 1.0,
    "case1": 0.5,
    "case2": 1.5,
    "case3": 1.5,
    "case4": 1.0,
}

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

def u_max_ana(u_mean):
    return 1.5 * u_mean

def delta_p_kin_ana(nu, u_mean):
    # OpenFOAM incompressible solvers store kinematic pressure p/rho [m2/s2]
    return 12.0 * nu * u_mean * L / H**2

SOLVERS = {
    "case0": "icoFoam",
    "case1": "icoFoam",
    "case2": "icoFoam",
    "case3": "simpleFoam",
    "case4": "potentialFoam",
}

# ──────────────────────────────────────────────────────────────────
def sep(title=""):
    w = 60
    if title:
        print(f"\n{'='*w}\n  {title}\n{'='*w}")
    else:
        print("  " + "─"*56)

def get_last_timestep(case_dir):
    """Retourne le chemin du dernier dossier timestep."""
    timesteps = []
    for d in case_dir.iterdir():
        if d.is_dir():
            try:
                timesteps.append(float(d.name))
            except ValueError:
                pass
    if not timesteps:
        return None, None
    t = max(timesteps)
    t_str = str(int(t)) if t == int(t) else str(t)
    return t, t_str

def read_foam_scalar_field(filepath):
    """Lit un champ scalaire OpenFOAM, retourne numpy array."""
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
                elif "nonuniform" in line:
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
    except Exception as e:
        print(f"    ⚠️  Lecture {filepath.name} : {e}")
    return np.array(values) if values else None

def analyze_case(case_name):
    sep(f"CAS : {case_name.upper()}")
    case_path = BASE_DIR / case_name

    if not case_path.exists():
        print(f"  ❌ Dossier introuvable : {case_path}")
        return None

    t_last, t_str = get_last_timestep(case_path)
    if t_last is None:
        print(f"  ❌ Aucun timestep dans {case_name}/")
        return None

    print(f"  ⏱️  Dernier timestep : t = {t_str} s")
    results = {"case": case_name, "t_last": t_last}
    u_ref = CASE_U_MEAN.get(case_name, 1.0)
    nu = get_case_nu(case_name)
    dp_ana_kin = delta_p_kin_ana(nu, u_ref)

    # ── Pression ──────────────────────────────────────────────────
    p_file = case_path / t_str / "p"
    if p_file.exists():
        p_vals = read_foam_scalar_field(p_file)
        if p_vals is not None and len(p_vals) > 1:
            # Maillage 100×10×1 → 1000 cellules
            # Inlet : cellules x~0 (premières 10 lignes Y × 1 Z)
            p_inlet  = p_vals[:10].mean()
            p_outlet = p_vals[-10:].mean()
            delta_p_kin  = p_inlet - p_outlet
            delta_p_pa = RHO * delta_p_kin
            print(f"\n  📊 Pression :")
            print(f"     p_inlet  = {p_inlet:10.4f} m²/s²")
            print(f"     p_outlet = {p_outlet:10.4f} m²/s²")
            print(f"     Δp_kin   = {delta_p_kin:10.4f} m²/s²"
                f"  (analytique ≈ {dp_ana_kin:.4f})")
            print(f"     ΔP       = {delta_p_pa:10.2f} Pa"
                f"  (ρ={RHO:.0f} kg/m³)")
            results["delta_p_kin"] = delta_p_kin
            results["delta_p_pa"] = delta_p_pa
    else:
        print(f"  ⚠️  Fichier p absent : {p_file}")

    # ── Log solveur ───────────────────────────────────────────────
    solver   = SOLVERS.get(case_name, "icoFoam")
    log_file = case_path / f"log.{solver}"
    if log_file.exists():
        print(f"\n  📋 Extrait log.{solver} :")
        with open(log_file) as f:
            lines = f.readlines()
        for line in lines[-40:]:
            if any(kw in line for kw in
                   ["ExecutionTime", "End", "converged", "SIMPLE"]):
                print(f"     {line.rstrip()}")
    else:
        print(f"  ⚠️  Log absent : {log_file.name}")

    # ── VTK ───────────────────────────────────────────────────────
    vtk_dir = case_path / "VTK"
    if vtk_dir.exists():
        n_vtm = len(list(vtk_dir.glob("*.vtm")))
        print(f"\n  📁 VTK : {n_vtm} fichiers .vtm")
        results["vtk_count"] = n_vtm
    else:
        print(f"\n  ⚠️  VTK absent → exécuter foamToVTK")

    return results

def print_summary(all_results):
    sep("RÉSUMÉ COMPARATIF")
    print(f"  {'Cas':<10} {'t_last':>8}  {'Δp_kin':>10}  {'ΔP (Pa)':>10}  {'VTK':>6}")
    sep()
    for r in all_results:
        if r is None:
            continue
        dpk = f"{r['delta_p_kin']:>10.4f}" if "delta_p_kin" in r else f"{'N/A':>10}"
        dp  = f"{r['delta_p_pa']:>10.2f}" if "delta_p_pa" in r else f"{'N/A':>10}"
        vtk = f"{r.get('vtk_count', 0):>6}"
        print(f"  {r['case']:<10} {r['t_last']:>8.1f}  {dpk}  {dp}  {vtk}")
    sep()
    print("  Référence : p OpenFOAM = pression cinématique (m²/s²)")
    for c in CASES:
        nu = get_case_nu(c)
        u = CASE_U_MEAN.get(c, 1.0)
        re = u * H / nu
        print(f"    {c}: nu={nu:.4g} | Umean={u:.2f} | Umax_ana={u_max_ana(u):.2f} | Re={re:.0f}")

# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  ANALYSE — Hagen-Poiseuille V2 (OpenFOAM 2412)")
    print(f"{'='*60}")
    print(f"  Répertoire : {BASE_DIR}")

    cases_to_run = sys.argv[1:] if len(sys.argv) > 1 else CASES
    results = [analyze_case(c) for c in cases_to_run]
    print_summary([r for r in results if r])
    print("\n✅ Analyse terminée.\n")
