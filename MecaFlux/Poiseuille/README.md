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
├── Enonce/               → documents pédagogiques (voir ci-dessous)
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
| 1 — Démarrage | 15 min | `Enonce/02_QCM_PREREQUIS_ETUDIANT.md` |
| 2 — Simulation | 60–90 min | `Enonce/01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` |
| 3 — Visualisation | 45 min | `Enonce/08_GUIDE_PARAVIEW_PAS_A_PAS.md` |
| 4 — Analyse et validation | — | `Enonce/04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` + `Enonce/03_QCM_FINAL_ETUDIANT.md` |

## Documents du dossier `Enonce/`

| Fichier | Rôle | Destinataire |
|---------|------|-------------|
| `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` | Colonne vertébrale opérationnelle du TP | Étudiant |
| `02_QCM_PREREQUIS_ETUDIANT.md` | Diagnostic d'entrée | Étudiant |
| `03_QCM_FINAL_ETUDIANT.md` | Vérification des acquis en sortie | Étudiant |
| `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` | Appui méthodologique et théorique | Étudiant |
| `05_CORRIGE_QCM_PREREQUIS_FINAL.md` | Correction des QCM | Enseignant |
| `06_FICHE_ETUDIANT_CONSIGNE.md` | Consignes, barème, attentes | Étudiant |
| `07_FICHE_ENSEIGNANT_CORRIGE_TYPE.md` | Correction type et grille d'évaluation | Enseignant |
| `08_GUIDE_PARAVIEW_PAS_A_PAS.md` | Visualisation, export, sauvegarde `.pvsm` | Étudiant |

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
