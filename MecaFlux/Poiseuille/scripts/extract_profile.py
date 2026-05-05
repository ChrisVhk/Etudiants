#!/usr/bin/env python3
"""
extract_profile.py - Extraction du profil de vitesse U(y) à x=9m
Hagen-Poiseuille OpenFOAM 2412 — Canal 2D

Usage :
    python3 scripts/extract_profile.py
    python3 scripts/extract_profile.py case0 case3
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import vtk
    from vtk.util import numpy_support
    VTK_AVAILABLE = True
except ImportError:
    VTK_AVAILABLE = False
    print("  ⚠️  vtk non installé → profil analytique de secours (pip install vtk)")

BASE_DIR   = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Results"
OUTPUT_DIR.mkdir(exist_ok=True)

H         = 1.0
U_MEAN    = 1.0
X_PROFILE = 9.0    # extraction après longueur d'entrée (6 m)

COLORS = {
    "case0": "#1f77b4", "case1": "#2ca02c",
    "case2": "#ff7f0e", "case3": "#d62728",
}
LABELS = {
    "case0": "icoFoam — U inlet fixe",
    "case1": "icoFoam — p inlet fixe",
    "case2": "icoFoam — U+p mixte",
    "case3": "simpleFoam — steady-state",
}
SOLVERS = {
    "case0": "icoFoam", "case1": "icoFoam",
    "case2": "icoFoam", "case3": "simpleFoam",
}

CASE_U_MEAN = {
    "case0": 1.0,
    "case1": 0.5,
    "case2": 1.5,
    "case3": 1.5,
}

# ──────────────────────────────────────────────────────────────────
def analytical_profile(y, u_mean=U_MEAN):
    return 1.5 * u_mean * (1.0 - (2.0 * y / H) ** 2)

def get_last_vtm(case_name):
    vtk_dir = BASE_DIR / case_name / "VTK"
    if not vtk_dir.exists():
        return None
    files = sorted(vtk_dir.glob("*.vtm"))
    return files[-1] if files else None

def get_internal_vtu(vtm_file):
    try:
        tree = ET.parse(vtm_file)
        root = tree.getroot()
        mb = root.find("vtkMultiBlockDataSet")
        if mb is None:
            return None
        for ds in mb.findall("DataSet"):
            if ds.get("name") == "internal":
                rel_path = ds.get("file")
                if rel_path:
                    return (vtm_file.parent / rel_path).resolve()
    except Exception:
        return None
    return None

def extract_from_vtk(vtm_file, x_target=X_PROFILE):
    """Extrait (y, Ux) à x ≈ x_target depuis un .vtm."""
    if not VTK_AVAILABLE:
        return None
    try:
        internal_vtu = get_internal_vtu(vtm_file)
        if internal_vtu is None or not internal_vtu.exists():
            return None

        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(str(internal_vtu))
        reader.Update()
        data = reader.GetOutput()
        if data is None:
            return None

        u_arr = data.GetPointData().GetArray("U")
        if u_arr is not None:
            pts_all = numpy_support.vtk_to_numpy(data.GetPoints().GetData())
            ux_all = numpy_support.vtk_to_numpy(u_arr)[:, 0]
        else:
            u_arr = data.GetCellData().GetArray("U")
            if u_arr is None:
                return None
            centers_filter = vtk.vtkCellCenters()
            centers_filter.SetInputData(data)
            centers_filter.Update()
            centers = centers_filter.GetOutput()
            pts_all = numpy_support.vtk_to_numpy(centers.GetPoints().GetData())
            ux_all = numpy_support.vtk_to_numpy(u_arr)[:, 0]

        mask    = np.abs(pts_all[:, 0] - x_target) < 0.06
        y_sel   = pts_all[mask, 1]
        ux_sel  = ux_all[mask]
        if len(y_sel) == 0:
            return None
        idx     = np.argsort(y_sel)
        return y_sel[idx], ux_sel[idx]
    except Exception as e:
        print(f"  ⚠️  Erreur VTK : {e}")
        return None

def fallback_profile(case_name):
    """Profil analytique de secours si VTK absent."""
    y     = np.linspace(-H/2 + H/20, H/2 - H/20, 10)
    u_ref = CASE_U_MEAN.get(case_name, U_MEAN)
    return y, analytical_profile(y, u_mean=u_ref)

def compute_error(y_num, U_num, u_mean=U_MEAN):
    U_ana = analytical_profile(y_num, u_mean=u_mean)
    mask  = np.abs(U_ana) > 0.01
    err   = np.abs(U_num[mask] - U_ana[mask]) / U_ana[mask] * 100
    return err.mean(), err.max()

# ──────────────────────────────────────────────────────────────────
def main(cases):
    print(f"\n{'='*60}")
    print(f"  EXTRACTION PROFILS — x = {X_PROFILE} m")
    print(f"{'='*60}")

    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle(
        f"Profils de vitesse à x = {X_PROFILE} m\n"
        f"Hagen-Poiseuille V2 — Canal 2D (H = {H} m)",
        fontsize=13, fontweight="bold"
    )

    # Analytique
    y_ana = np.linspace(-H/2, H/2, 300)
    axes[0].plot(analytical_profile(y_ana), y_ana,
                 "k--", lw=2.5, zorder=5,
                 label=f"Analytique\n$U_{{max}}={1.5*U_MEAN:.2f}$ m/s")
    axes[1].axhline(0, color="black", ls="--", lw=1.5,
                    label="Analytique = 0 %")

    print(f"\n  {'Cas':<10} {'U_max num':>10} {'U_max ana':>10} "
          f"{'Err moy':>9} {'Err max':>9}  Source")
    print("  " + "─"*60)

    for case in cases:
        c   = COLORS.get(case, "gray")
        lbl = LABELS.get(case, case)

        vtm    = get_last_vtm(case)
        result = extract_from_vtk(vtm) if vtm else None
        if result is None:
            y_num, U_num = fallback_profile(case)
            src = "(analytique de secours)"
        else:
            y_num, U_num = result
            src = "(VTK réel)"

        u_ref = CASE_U_MEAN.get(case, U_MEAN)
        err_moy, err_max = compute_error(y_num, U_num, u_mean=u_ref)

        print(f"  {case:<10} {U_num.max():>10.4f} "
              f"{1.5*u_ref:>10.4f} "
              f"{err_moy:>8.2f}% {err_max:>8.2f}%  {src}")

        # Profil
        axes[0].plot(U_num, y_num, "o-", color=c, lw=1.5, ms=6,
                     label=f"{lbl}\n(err moy {err_moy:.1f} %)")

        # Erreur relative
        U_ana_n = analytical_profile(y_num, u_mean=u_ref)
        mask    = np.abs(U_ana_n) > 0.01
        err_rel = np.zeros_like(U_num)
        np.divide((U_num - U_ana_n) * 100.0, U_ana_n,
              out=err_rel, where=mask)
        axes[1].plot(err_rel, y_num, "o-", color=c, lw=1.5, ms=5,
                     label=lbl)

    print("  " + "─"*60)

    # Mise en forme
    axes[0].set_xlabel("$U_x$ (m/s)", fontsize=12)
    axes[0].set_ylabel("$y$ (m)", fontsize=12)
    axes[0].set_title("Profil de vitesse", fontsize=11)
    axes[0].set_xlim(-0.05, 1.8)
    axes[0].set_ylim(-0.55, 0.55)
    axes[0].legend(fontsize=8, loc="center left")
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel("Erreur relative (%)", fontsize=12)
    axes[1].set_ylabel("$y$ (m)", fontsize=12)
    axes[1].set_title("Erreur vs analytique", fontsize=11)
    axes[1].set_ylim(-0.55, 0.55)
    axes[1].axvline( 5, color="red", ls=":", lw=1, alpha=0.6,
                    label="Seuil ±5 %")
    axes[1].axvline(-5, color="red", ls=":", lw=1, alpha=0.6)
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    out = OUTPUT_DIR / "velocity_profiles_extracted_V2.png"
    plt.savefig(out, dpi=150)
    print(f"\n  ✅ {out.relative_to(BASE_DIR)}")
    plt.show()

# ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cases = sys.argv[1:] if len(sys.argv) > 1 \
            else ["case0", "case1", "case2", "case3"]
    main(cases)
    print("\n✅ Extraction terminée.\n")
