# TP Hagen-Poiseuille — OpenFOAM 2412

TP de mécanique des fluides numérique autour du profil de Poiseuille plan.
Six cas OpenFOAM permettent de comparer solveurs, effets du nombre de Reynolds et développement spatial du profil.

---

## Démarrage rapide

```bash
# Tout en une commande (setup → simulations → post-traitement → ParaView)
bash tp_poiseuille.sh all

# Étape par étape
bash tp_poiseuille.sh 0      # Installer les dépendances Python (venv)
bash tp_poiseuille.sh 1      # Créer les 6 cas OpenFOAM
bash tp_poiseuille.sh 2      # Lancer les simulations
bash tp_poiseuille.sh 3-7    # Post-traitement Python
bash tp_poiseuille.sh 8      # Ouvrir ParaView

# Utilitaires
bash 04_clean.sh             # Nettoyage complet (avec confirmation)
bash 04_clean.sh --yes       # Nettoyage sans confirmation
bash 04_clean.sh --dry-run   # Aperçu de ce qui serait supprimé
```

---

## Structure du dossier

```
Poiseuille/
├── tp_poiseuille.sh      → orchestrateur complet (étapes 0 à 8)
├── 01_setup.sh           → création des 6 cas OpenFOAM
├── 02_run.sh             → blockMesh + solveur + foamToVTK
├── 03_postprocess.sh     → post-traitement Python seul (étapes 3–7)
├── 04_clean.sh           → nettoyage complet
├── scripts/              → scripts Python d'analyse et de tracé
├── docs/                 → documents pédagogiques (voir ci-dessous)
├── case0/ … case5/       → générés par 01_setup.sh  (ignorés par git)
└── Results/              → générés par post-traitement (ignorés par git)
```

## Scripts

| Script | Rôle | Usage direct |
|--------|------|-------------|
| `tp_poiseuille.sh` | Orchestrateur complet | `bash tp_poiseuille.sh [0‑8 \| all \| 3-7 \| 1,2,5]` |
| `01_setup.sh` | Crée case0–case5 | `bash 01_setup.sh` |
| `02_run.sh` | Simulations + conversion VTK | `bash 02_run.sh` |
| `03_postprocess.sh` | Analyse et graphiques Python | `bash 03_postprocess.sh` |
| `04_clean.sh` | Supprime cas, résultats, venv | `bash 04_clean.sh [--yes] [--dry-run]` |

---

## Les 6 cas simulés

| Cas   | Solveur       | U_moy  | L canal | Re   | Objectif pédagogique principal               |
|-------|---------------|--------|---------|------|----------------------------------------------|
| case0 | icoFoam       | 1.0 m/s| 100 m   | 1000 | Référence — comparaison analytique           |
| case1 | icoFoam       | 0.5 m/s| 50 m    | 500  | Effet Re faible — développement plus lent    |
| case2 | icoFoam       | 1.5 m/s| 150 m   | 1500 | Effet Re élevé — développement plus rapide   |
| case3 | simpleFoam    | 1.5 m/s| 150 m   | 1500 | Même physique que case2, solveur stationnaire|
| case4 | potentialFoam | 1.0 m/s| 10 m    | ∞    | Fluide inviscide — aucune perte de charge    |
| case5 | icoFoam       | 1.0 m/s| 200 m   | 1000 | Poiseuille ÉTABLI — profil parabolique exact |

> **Clé de lecture** : case0–case4 = canal court (L ≤ 2×L_dev). case5 = canal long (L = 4×L_dev) → seul cas où le profil analytique est pleinement atteint.

---

## Parcours pédagogique (4 niveaux)

| Niveau | Durée | Document |
|--------|-------|----------|
| 1 — Lancement | 10 min | `docs/01_FICHE_CONSIGNE.md` |
| 2 — Théorie (pendant les calculs) | 30 min | `docs/02_QCM_PREREQUIS.md` + `docs/03_BASE_THEORIQUE.md` |
| 3 — Visualisation | 60 min | `docs/05_GUIDE_PARAVIEW.md` |
| 4 — Analyse et interprétation | 80 min | `docs/04_GUIDE_PAS_A_PAS.md` |
| 5 — Restitution | 40 min | `docs/06_QCM_FINAL.md` |

## Documents du dossier `docs/`

| # | Fichier | Rôle | Destinataire |
|---|---------|------|-------------|
| 01 | `01_FICHE_CONSIGNE.md` | **Lire en premier** — consignes, barème, déroulé 4h | 👤 Étudiant |
| 02 | `02_QCM_PREREQUIS.md` | Diagnostic d'entrée — à faire pendant les calculs | 👤 Étudiant |
| 03 | `03_BASE_THEORIQUE.md` | Appui théorique solveurs — à lire pendant les calculs | 👤 Étudiant |
| 04 | `04_GUIDE_PAS_A_PAS.md` | Référence opérationnelle étape par étape | 👤 Étudiant |
| 05 | `05_GUIDE_PARAVIEW.md` | Visualisation, export, sauvegarde `.pvsm` | 👤 Étudiant |
| 06 | `06_QCM_FINAL.md` | Vérification des acquis en sortie | 👤 Étudiant |
| 07 | `07_AIDE_MEMOIRE.md` | Aide-mémoire A4 imprimable (équations, solveurs, commandes) | 👤 Étudiant |
| 08 | `08_CORRIGE_QCM.md` | Correction des QCM | 📋 Enseignant |
| 09 | `09_FICHE_ENSEIGNANT.md` | Correction type et grille d'évaluation | 📋 Enseignant |

---

## Checkpoint enseignant (validation rapide)

- **Checkpoint A** : Les 6 cas tournent sans erreur bloquante.
- **Checkpoint B** : case5 montre un profil parabolique proche de l'analytique (écart < 5%).
- **Checkpoint C** : La section « potentiel vs visqueux » est argumentée avec au moins deux indicateurs chiffrés.
- **Checkpoint D** : La conclusion relie clairement le choix du solveur à une contrainte ingénierie (précision, coût, physique).

## Mini-défis de séance (optionnels)

- **Défi chrono** : visualisation propre U+p comparant case0 et case5 en moins de 20 minutes.
- **Défi qualité** : quantifier l'écart entre case0 (non développé) et case5 (établi) et l'expliquer en 3 phrases.
- **Défi physique** : expliquer pourquoi case4 (potentialFoam) n'a aucune chute de pression.

<- TenueMer : en test sync -->
