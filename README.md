# Supports pédagogiques ENSM — Mécanique des Fluides / OpenFOAM

Dépôt public des supports de TP pour les étudiants de l'École Nationale Supérieure Maritime (ENSM).

---

## Structure

```
Etudiants/
├── InstallOff/                  — Guide d'installation OpenFOAM (en préparation)
├── MecaFlux/
│   ├── InstallOpenFoam/         — Parcours d'installation OpenFOAM 2412
│   └── Poiseuille/              — TP CFD : Écoulement de Hagen-Poiseuille
├── Python&Dep/                  — Dépendances Python pour le post-traitement
├── TenueMer/                    — TP Tenue à la mer (en préparation)
├── VScode&WSL/                  — Installation WSL + VS Code (Windows)
└── scripts/
    └── init_tp.sh               — Script d'initialisation d'un nouveau TP
```

---

## TP Poiseuille — `MecaFlux/Poiseuille/`

Simulation de l'écoulement de Hagen-Poiseuille (canal 2D) avec OpenFOAM 2412.

### Prérequis

- OpenFOAM 2412 installé et sourcé (`source /opt/openfoam2412/etc/bashrc`)
- Python 3 avec `numpy` et `matplotlib`

### Démarrage rapide

```bash
git clone https://github.com/ChrisVhk/Etudiants
cd Etudiants/MecaFlux/Poiseuille
bash run_workflow.sh
```

Le script `run_workflow.sh` exécute les 4 étapes automatiquement :
1. **Clean** — supprime les anciens cas
2. **Setup** — crée les 6 cas (`master_setup_V2.sh`)
3. **Simulation** — lance blockMesh + solveur + foamToVTK (`run_all_cases_V2.sh`)
4. **Post-traitement** — génère les figures dans `Results/` (`run_postproc.sh`)

Pour relancer uniquement le post-traitement (sans recalculer) :
```bash
bash run_postproc.sh
```

### Cas simulés

| Cas   | Solveur       | Re   | L (m) | Objectif pédagogique |
|-------|---------------|------|-------|----------------------|
| case0 | icoFoam       | 1000 | 100   | Référence — Poiseuille transient |
| case1 | icoFoam       |  500 |  50   | Effet du nombre de Reynolds (faible) |
| case2 | icoFoam       | 1500 | 150   | Effet du nombre de Reynolds (élevé) |
| case3 | simpleFoam    | 1500 | 150   | Comparaison solveur steady-state |
| case4 | potentialFoam |  —   |  10   | Écoulement potentiel (inviscide) |
| case5 | icoFoam       | 1000 | 200   | Poiseuille **pleinement établi** (4×L_dev) |

### Documents pédagogiques (`Enonce/`)

| Fichier | Contenu |
|---------|---------|
| `00_SYNTHESE_TP.md` | Vue d'ensemble du TP |
| `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` | Guide étudiant pas à pas |
| `02_QCM_PREREQUIS_ETUDIANT.md` | QCM de prérequis |
| `03_QCM_FINAL_ETUDIANT.md` | QCM d'évaluation finale |
| `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` | Base théorique et formules |
| `06_FICHE_ETUDIANT_CONSIGNE.md` | Consignes de TP |
| `08_GUIDE_PARAVIEW_PAS_A_PAS.md` | Guide de visualisation ParaView |

---

## Environnement de développement

### WSL + VS Code — `VScode&WSL/`

Guide pas à pas pour installer Ubuntu 24.04 sous Windows via WSL et configurer VS Code avec l'extension Remote WSL.

Voir [`VScode&WSL/Install_VSCode_WSL.md`](VScode%26WSL/Install_VSCode_WSL.md)

### Dépendances Python — `Python&Dep/`

Installation des bibliothèques Python nécessaires au post-traitement (numpy, matplotlib, scipy, pandas, reportlab).

```bash
bash Python\&Dep/install_python_deps.sh
```

Voir [`Python&Dep/Install_Python_Deps.md`](Python%26Dep/Install_Python_Deps.md)

---

## Initialiser un nouveau TP

```bash
# Squelette vide
./scripts/init_tp.sh MonNouveauTP

# Copie depuis Poiseuille comme template
./scripts/init_tp.sh MonNouveauTP --from Poiseuille
```
