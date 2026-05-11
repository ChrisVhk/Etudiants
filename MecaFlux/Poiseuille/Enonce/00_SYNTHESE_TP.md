# Synthèse TP — Parcours pédagogique Poiseuille

Ce dossier contient les documents nécessaires pour un TP de mécanique des fluides numérique progressif et évaluable.

## Mode de jeu (4 niveaux)
1. **Niveau 1 — Démarrage** (15 min) : `02_QCM_PREREQUIS_ETUDIANT.md`
2. **Niveau 2 — Simulation** (60 à 90 min) : `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md`
3. **Niveau 3 — Visualisation** (45 min) : `08_GUIDE_PARAVIEW_PAS_A_PAS.md`
4. **Niveau 4 — Analyse et validation** : `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` puis `03_QCM_FINAL_ETUDIANT.md`

## Les 6 cas simulés

| Cas   | Solveur       | U_moy  | L canal | Re   | Objectif pédagogique principal              |
|-------|---------------|--------|---------|------|----------------------------------------------|
| case0 | icoFoam       | 1.0 m/s| 10 m    | 1000 | Référence — comparaison analytique          |
| case1 | icoFoam       | 0.5 m/s| 10 m    | 500  | Effet Re faible — développement plus lent   |
| case2 | icoFoam       | 1.5 m/s| 10 m    | 1500 | Effet Re élevé — développement plus rapide  |
| case3 | simpleFoam    | 1.5 m/s| 10 m    | 1500 | Même physique que case2, solveur stationnaire|
| case4 | potentialFoam | 1.0 m/s| 10 m    | ∞    | Fluide inviscide — aucune perte de charge   |
| case5 | icoFoam       | 1.0 m/s| 100 m   | 1000 | Poiseuille ÉTABLI — profil parabolique exact|

> **Clé de lecture** : case0 à case4 = canal court (L < L_dev). case5 = canal long (L > 2×L_dev) → seul cas où le profil analytique est atteint.

## Checkpoint enseignant (validation rapide)
- **Checkpoint A** : Les 6 cas tournent sans erreur bloquante.
- **Checkpoint B** : case5 montre un profil parabolique proche de l'analytique (écart < 5%).
- **Checkpoint C** : La section « potentiel vs visqueux » est argumentée avec au moins deux indicateurs chiffrés.
- **Checkpoint D** : La conclusion relie clairement le choix du solveur à une contrainte ingénierie (précision, coût, physique).

## Documents et rôles
- `01_GUIDE_ETUDIANT_PAS_A_PAS_PREMIER_OPENFOAM.md` : colonne vertébrale opérationnelle du TP.
- `02_QCM_PREREQUIS_ETUDIANT.md` : diagnostic d'entrée (niveau de départ).
- `03_QCM_FINAL_ETUDIANT.md` : vérification des acquis en sortie.
- `04_BASE_THEORIQUE_SOLVEURS_OPENFOAM.md` : appui méthodologique et théorique.
- `05_CORRIGE_QCM_PREREQUIS_FINAL.md` : correction enseignant des QCM.
- `06_FICHE_ETUDIANT_CONSIGNE.md` : consignes, barème, attentes.
- `07_FICHE_ENSEIGNANT_CORRIGE_TYPE.md` : correction type et grille d'évaluation.
- `08_GUIDE_PARAVIEW_PAS_A_PAS.md` : visualisation, export d'images, sauvegarde `paraview_cases.pvsm`.

## Mini-défi de séance (optionnel)
- **Défi chrono** : produire une visualisation propre U+p comparant case0 et case5 en moins de 20 minutes.
- **Défi qualité** : quantifier l'écart entre case0 (non développé) et case5 (établi) et l'expliquer en 3 phrases.
- **Défi physique** : expliquer pourquoi case4 (potentialFoam) n'a aucune chute de pression.

## Périmètre du dossier
Les fichiers redondants ont été retirés pour limiter la charge cognitive et garder un parcours clair en séance.
