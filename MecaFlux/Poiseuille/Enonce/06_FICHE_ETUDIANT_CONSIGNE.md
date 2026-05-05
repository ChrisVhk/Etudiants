# Fiche Etudiant (Concise)
## TP Note Mecanique des fluides (4h) - Genie maritime

## 1. Mission
Mobiliser la théorie de mécanique des fluides et la confronter à des résultats CFD sur un cas de canal 2D (Poiseuille) avec OpenFOAM.

## 2. Ce que vous devez savoir montrer
1. Distinguer fluide potentiel, fluide visqueux laminaire et ecoulement turbulent modele.
2. Interpréter l'effet des conditions aux limites sur la solution numérique.
3. Vérifier la qualité d'une simulation (et pas seulement son exécution).
4. Formuler une conclusion d'ingénieur argumentée.

## 3. Deroule (4h)
1. 0h00-0h40: rappel théorique et cadrage.
2. 0h40-1h40: génération des cas et calculs OpenFOAM.
3. 1h40-2h35: post-traitement et comparaison des cas.
4. 2h35-3h25: interprétation physique (validité, limites).
5. 3h25-4h00: restitution notée.

## 4. Commandes minimales
```bash
bash master_setup_V2.sh
bash run_all_cases_V2.sh
# optionnel
bash Workflow_final.sh all
```

## 5. Questions obligatoires (a traiter dans votre restitution)
1. Quelles hypothèses différentielles distinguent potentiel, visqueux laminaire et turbulent modélisé?
2. Quel cas est le plus robuste numériquement et pourquoi?
3. Quelles limites du setup actuel empêchent de conclure sur le décollement réel?
4. Quelle modification minimale rendrait l'étude plus représentative d'un cas maritime?

## 6. Livrables attendus
1. Memo theorie (1 page max) couvrant: potentiel, visqueux, decollement, turbulence.
2. Dossier numérique: 3 à 5 figures commentées + 1 tableau comparatif des cas.
3. Conclusion technique (10 à 15 lignes) avec recommandation argumentée.

## 7. Bareme (sur 20)
1. Théorie: 5 pts
2. Qualité numérique (workflow, checks, reproductibilité): 6 pts
3. Interprétation physique: 5 pts
4. Analyse critique (limites, incertitudes): 2 pts
5. Clarté de la restitution: 2 pts

## 8. Checkpoints de robustesse
- Checkpoint A: les cas tournent et les logs sont lisibles.
- Checkpoint B: au moins un indicateur numerique est quantifie.
- Checkpoint C: la conclusion mentionne clairement les limites.

## 9. Mini-defis (ludique)
- Defi chrono: produire une figure comparative validee en moins de 15 min.
- Defi precision: expliquer un ecart simulation/theorie avec une cause numerique plausible.

## 10. Rappels importants
- Le cas de base est surtout laminaire; soyez explicites sur ce qui est hors domaine (décollement fort, turbulence développée).
- Une simulation terminée n'est pas automatiquement validée: appuyez-vous sur les logs, profils et cohérence physique.
