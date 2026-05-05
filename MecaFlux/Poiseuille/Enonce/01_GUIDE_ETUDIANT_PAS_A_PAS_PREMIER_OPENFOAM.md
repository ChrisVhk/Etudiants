# Guide Etudiant Pas a Pas (Premier OpenFOAM)
## TP Mecanique des fluides - Version robuste et ludique

## 1. Mission globale
Comparer 3 modeles physiques et numeriques:
1. Ecoulement visqueux transitoire (icoFoam): case0, case1, case2.
2. Ecoulement visqueux permanent (simpleFoam): case3.
3. Ecoulement potentiel (potentialFoam): case4.

En fin de TP, vous devez repondre clairement:
- Quand le modele potentiel est pertinent.
- Pourquoi il ne remplace pas un modele visqueux pour les pertes de charge.
- Quel solveur choisir selon l'objectif (rapidite, precision, fidelite physique).

## 2. Parcours conseille (4h)
1. 0h00-0h30: verification environnement + creation des cas.
2. 0h30-1h15: lancement des 5 cas.
3. 1h15-2h00: comparaison physique et numerique.
4. 2h00-2h45: convergence (residus + stabilisation temporelle).
5. 2h45-4h00: interpretation et redaction.

## 3. Bloc execution minimal (copier-coller)
```bash
bash master_setup_V2.sh
bash run_all_cases_V2.sh

python3 scripts/analyze_results.py
python3 scripts/compare_cases.py
python3 scripts/plot_results.py
python3 scripts/convergence_check.py
python3 scripts/stabilization_study.py
```

## 4. Checkpoints de robustesse
### Checkpoint 1 - Execution
- Les 5 cas se lancent sans erreur fatale.
- Les logs de solveur existent et sont exploitables.

### Checkpoint 2 - Convergence
- Vous commentez les residus (pas uniquement "ca tourne").
- Vous justifiez la stabilisation avec un critere quantifie.

### Checkpoint 3 - Analyse physique
- Vous comparez explicitement case4 vs case0-3.
- Vous donnez au moins un ecart chiffre (temps de calcul, Delta p, Umax, etc.).

## 5. Ce qu'il faut observer en priorite
### 5.1 Comparaison des solveurs
- case0/1/2 (icoFoam): evolution temporelle et approche du regime etabli.
- case3 (simpleFoam): convergence vers une solution stationnaire.
- case4 (potentialFoam): calcul tres rapide mais sans dissipation visqueuse.

### 5.2 Question obligatoire: potentiel vs visqueux
Comparez case4 avec case0-3 sur:
- temps de calcul,
- chute de pression,
- validite physique pour les pertes de charge.

Conclusion attendue:
- potentialFoam est utile pour initialiser ou faire un pre-diagnostic,
- mais ne remplace pas un solveur Navier-Stokes visqueux.

### 5.3 Question obligatoire: convergence
Deux niveaux a documenter:
1. Convergence iterative (residus): `scripts/convergence_check.py`.
2. Stabilisation temporelle (transitoire): `scripts/stabilization_study.py`.

Critere recommande:
- variation relative <= 1% sur Umax et Delta p_kin en fin de simulation.

## 6. Livrables obligatoires
1. Tableau comparatif des 5 cas (solveur, statut, CPU, interpretation physique).
2. Deux figures de convergence:
   - residuals/convergence,
   - stabilisation temporelle.
3. Section "potentiel vs visqueux" (10 lignes minimum, argumentee).
4. Conclusion d'ingenieur (10 a 15 lignes):
   - solveur recommande selon l'usage,
   - limites du choix,
   - amelioration proposee.
5. Scene ParaView globale `paraview_cases.pvsm` + captures comparatives.

Pour la procedure detaillee ParaView:
- `08_GUIDE_PARAVIEW_PAS_A_PAS.md`

## 7. Mini-defis (ludique)
- Defi 1 (chrono): obtenir une premiere comparaison case3 vs case4 en moins de 15 minutes.
- Defi 2 (qualite): produire une figure comparative sans biais d'echelle couleur.
- Defi 3 (expert): proposer un protocole pour valider la stabilite numerique.

## 8. Questions du compte-rendu
1. Quel cas est le plus robuste numeriquement et pourquoi?
2. Quel cas est le plus pertinent pour estimer une perte de charge visqueuse?
3. Quel est l'interet de potentialFoam dans une chaine CFD?
4. A partir de quel temps les grandeurs deviennent-elles stables?

## 9. Erreurs frequentes a eviter
1. Confondre simulation terminee et simulation convergee.
2. Conclure sur la turbulence alors que le regime est laminaire.
3. Oublier les limites du modele potentiel.
4. Ne pas quantifier les ecarts.
