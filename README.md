# Supports pédagogiques ENSM

Dépôt public des supports de TP pour les étudiants de l'École Nationale Supérieure Maritime (ENSM).

---

## Structure

```
Etudiants/
├── InstallOff/          — Installation pandapower & OpenFAST (NREL)
├── MecaFlux/            — Mécanique des fluides numérique (OpenFOAM)
├── Python&Dep/          — Dépendances Python pour le post-traitement
├── TenueMer/            — Tenue à la mer : Capytaine & Nemoh V3
├── VScode&WSL/          — Environnement WSL + VS Code (Windows)
└── scripts/             — Scripts utilitaires
```

---

## Modules disponibles

| Module | Description | Documentation |
|--------|-------------|---------------|
| **MecaFlux** | CFD avec OpenFOAM 2412 — TP Poiseuille | [MecaFlux/README.md](MecaFlux/README.md) |
| **TenueMer** | Tenue à la mer — Capytaine & Nemoh V3 | *(en préparation)* |
| **InstallOff** | Éolien offshore — pandapower & OpenFAST | *(en préparation)* |

---

## Mise en place de l'environnement

### 1. WSL + VS Code (Windows)

→ [`VScode&WSL/Install_VSCode_WSL.md`](VScode%26WSL/Install_VSCode_WSL.md)

### 2. Dépendances Python

```bash
bash Python\&Dep/install_python_deps.sh
```

→ [`Python&Dep/Install_Python_Deps.md`](Python%26Dep/Install_Python_Deps.md)

### 3. OpenFOAM 2412

```bash
bash MecaFlux/InstallOpenFoam/install_openfoam2412.sh
```

→ [`MecaFlux/InstallOpenFoam/Install_OpenFoam2412.md`](MecaFlux/InstallOpenFoam/Install_OpenFoam2412.md)

---

## Démarrage rapide — TP Poiseuille

```bash
git clone https://github.com/ChrisVhk/Etudiants
cd Etudiants/MecaFlux/Poiseuille
bash tp_poiseuille.sh all
```
