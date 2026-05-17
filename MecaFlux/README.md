# MecaFlux — Mécanique des fluides numérique

Module de mécanique des fluides numérique (CFD) avec OpenFOAM 2412.

---

## Contenu

```
MecaFlux/
├── InstallOpenFoam/     — Guide d'installation OpenFOAM 2412
└── Poiseuille/          — TP CFD : Écoulement de Hagen-Poiseuille
```

---

## Installation OpenFOAM 2412

→ Voir [`InstallOpenFoam/Install_OpenFoam2412.md`](InstallOpenFoam/Install_OpenFoam2412.md)

Prérequis : Ubuntu 22.04 / 24.04 (natif ou WSL2).

```bash
bash InstallOpenFoam/install_openfoam2412.sh
```

---

## TP Poiseuille

Simulation de l'écoulement de Hagen-Poiseuille (canal 2D, laminaire) avec OpenFOAM 2412.
Six cas permettent de comparer solveurs, effets du nombre de Reynolds et développement spatial du profil.

→ Voir [`Poiseuille/README.md`](Poiseuille/README.md) pour la documentation complète du TP.

### Démarrage rapide

```bash
cd Poiseuille
bash tp_poiseuille.sh 0      # Dépendances Python (venv)
bash tp_poiseuille.sh 1      # Créer les 6 cas OpenFOAM
bash tp_poiseuille.sh 2      # Lancer les simulations
bash tp_poiseuille.sh 3-7    # Post-traitement Python
bash tp_poiseuille.sh 8      # Ouvrir ParaView

# ou tout en une commande :
bash tp_poiseuille.sh all
```

### Les 6 cas simulés

| Cas   | Solveur       | U_moy   | L (m) | Re   | Objectif pédagogique                              |
|-------|---------------|---------|-------|------|---------------------------------------------------|
| case0 | icoFoam       | 1.0 m/s | 100   | 1000 | Référence — comparaison analytique                |
| case1 | icoFoam       | 0.5 m/s | 50    | 500  | Effet Re faible — développement plus lent         |
| case2 | icoFoam       | 1.5 m/s | 150   | 1500 | Effet Re élevé — développement plus rapide        |
| case3 | simpleFoam    | 1.5 m/s | 150   | 1500 | Même physique que case2, solveur stationnaire     |
| case4 | potentialFoam | 1.0 m/s | 10    | ∞    | Fluide inviscide — aucune perte de charge         |
| case5 | icoFoam       | 1.0 m/s | 200   | 1000 | Poiseuille **pleinement établi** (4×L_dev)        |

> **Clé de lecture** : case0–case4 = canal court (L ≤ 2×L_dev). case5 = canal long (L = 4×L_dev) → seul cas où le profil parabolique analytique est pleinement atteint.

### Documents pédagogiques (`Poiseuille/docs/`)

| Fichier | Contenu | Destinataire |
|---------|---------|-------------|
| `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` | Guide étudiant opérationnel pas à pas | 👤 Étudiant |
| `02_QCM_PREREQUIS_ETUDIANT.md` | QCM de prérequis (pendant les calculs) | 👤 Étudiant |
| `03_QCM_FINAL_ETUDIANT.md` | QCM d'évaluation finale | 👤 Étudiant |
| `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` | Base théorique — solveurs et formules | 👤 Étudiant |
| `06_FICHE_ETUDIANT_CONSIGNE.md` | Consignes, barème, déroulé 4h | 👤 Étudiant |
| `08_GUIDE_PARAVIEW_PAS_A_PAS.md` | Visualisation, export, fichiers `.pvsm` | 👤 Étudiant |

### Parcours pédagogique

| Étape | Durée | Action |
|-------|-------|--------|
| 1 | 10 min | Lire `06_FICHE_ETUDIANT_CONSIGNE.md`, lancer `bash tp_poiseuille.sh all` |
| 2 | 30 min | `02_QCM_PREREQUIS_ETUDIANT.md` + `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` (pendant les calculs) |
| 3 | 60 min | Visualisation ParaView — `08_GUIDE_PARAVIEW_PAS_A_PAS.md` |
| 4 | 80 min | Analyse et interprétation — `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` |
| 5 | 40 min | `03_QCM_FINAL_ETUDIANT.md` — restitution |
