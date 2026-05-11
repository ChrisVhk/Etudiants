# Guide Étudiant Pas à Pas — Premier OpenFOAM
## TP Mécanique des fluides — Canal de Poiseuille 2D

---

## 1. Mission globale

Comparer **3 modèles physiques** et **2 solveurs** sur un canal plan 2D (Poiseuille) :
1. **Écoulement visqueux transitoire** (icoFoam) : case0, case1, case2, case5.
2. **Écoulement visqueux permanent** (simpleFoam) : case3.
3. **Écoulement potentiel** (potentialFoam) : case4.

En fin de TP, vous devez répondre clairement :
- Pourquoi le profil numérique de case0 s'écarte-t-il de la parabole analytique ?
- Pourquoi case5 (L=100m) donne-t-il un profil quasi-parfait ?
- Pourquoi potentialFoam ne peut pas remplacer un solveur visqueux pour les pertes de charge ?
- Quel solveur choisir selon l'objectif (rapidité, précision, fidélité physique) ?

---

## 2. Parcours conseillé (4h)

| Phase | Durée | Activité |
|-------|-------|----------|
| 0h00 – 0h15 | 15 min | QCM prérequis (`02_QCM_PREREQUIS_ETUDIANT.md`) |
| 0h15 – 0h45 | 30 min | Vérification environnement + génération des cas |
| 0h45 – 1h45 | 60 min | Lancement des 6 simulations |
| 1h45 – 2h30 | 45 min | Post-traitement Python + analyse des figures |
| 2h30 – 3h15 | 45 min | Interprétation physique + comparaison case0 vs case5 |
| 3h15 – 4h00 | 45 min | Rédaction de la conclusion + QCM final |

---

## 3. Bloc d'exécution complet (une seule commande)

```bash
# Option 1 : tout en une commande (recommandé)
bash run_workflow.sh

# Option 2 : étape par étape
bash master_setup_V2.sh       # Génère les 6 cas (case0 à case5)
bash run_all_cases_V2.sh      # blockMesh + solveurs + foamToVTK
bash run_postproc.sh          # Tous les scripts Python (figures + stats)
```

> **case5 (L=100m) prend environ 5-10 min de calcul** — lancez-le en premier !

---

## 4. Observation prioritaire — La longueur de développement

### Pourquoi les profils numériques ne sont-ils pas paraboliques ?

$$L_{dev} \approx 0.05 \times Re \times H$$

| Cas   | Re   | $L_{dev}$ | Canal | Développement à la sortie |
|-------|------|-----------|-------|--------------------------|
| case0 | 1000 | **50 m**  | 10 m  | **20 %** seulement       |
| case1 | 500  | **25 m**  | 10 m  | **40 %** seulement       |
| case2 | 1500 | **75 m**  | 10 m  | **13 %** seulement       |
| case5 | 1000 | **50 m**  | 100 m | **100 %** ✅             |

> **Ce n'est pas un bug — c'est de la physique.** Pour atteindre le profil parabolique de Poiseuille, il faut un canal suffisamment long. case5 est la démonstration expérimentale.

---

## 5. Checkpoints de robustesse

### Checkpoint 1 — Exécution
- Les 6 cas se lancent sans erreur fatale.
- Les logs de solveur existent et se terminent par `End`.

### Checkpoint 2 — Convergence numérique
- Résidus < 10⁻⁵ pour les cas icoFoam et potentialFoam.
- simpleFoam : message `SIMPLE solution converged`.
- ⚠️ **Terminé ≠ Convergé** — vérifiez les résidus !

### Checkpoint 3 — Cohérence physique
- case5 : $U_{max} \approx 1.50$ m/s (≈ 1.5 × U_moy) → parabole de Poiseuille.
- case4 : $\Delta P \approx 0$ Pa → aucune viscosité → normal.
- case2 ≈ case3 (même Re=1500, solveurs différents) → résultats cohérents.

### Checkpoint 4 — Analyse physique
- Comparer explicitement case4 vs case0 : au moins **deux indicateurs chiffrés**.
- Comparer case0 vs case5 : quantifier l'effet de la longueur de développement.

---

## 6. Questions obligatoires (à traiter dans votre restitution)

1. **Longueur de développement** : calculez $L_{dev}$ pour case0. Qu'observe-t-on à x=9m ? Comparez avec case5.
2. **Potentiel vs visqueux** : comparez case4 et case0 sur le temps CPU, $U_{max}$, $\Delta P$. Concluez sur les limites de potentialFoam.
3. **Convergence numérique** : que signifie un résidu ? Quand peut-on dire qu'une simulation est **validée** ?
4. **Solveur stationnaire vs transitoire** : comparez case2 (icoFoam, t=20s) et case3 (simpleFoam, 180 iter). Quelles différences ? Quel est l'intérêt de chaque solveur ?
5. **Conclusion ingénieur** : quel solveur recommanderiez-vous pour calculer la perte de charge dans une conduite navale ? Justifiez.

---

## 7. Livrables obligatoires

1. **Tableau comparatif** des 6 cas : solveur, statut convergence, $U_{max}$, $\Delta P$ (numérique vs analytique, % écart).
2. **Figure profils** : superposition case0 / case5 / analytique → illustration de la longueur de développement.
3. **Figure convergence** : résidus d'au moins 2 cas, commentés.
4. **Section potentiel vs visqueux** (10 lignes minimum, argumentée avec chiffres).
5. **Conclusion d'ingénieur** (10-15 lignes) : solveur recommandé selon l'usage, limites, amélioration proposée.
6. **Scène ParaView** `paraview_cases.pvsm` + 3 captures comparatives.

---

## 8. Erreurs fréquentes à éviter

1. Confondre **simulation terminée** (log `End`) et **simulation convergée** (résidus < seuil).
2. Conclure que "le modèle est faux" parce que le profil n'est pas parabolique → c'est la **zone d'entrée**.
3. Affirmer que potentialFoam est inutile → il est utile pour **initialiser** ou **pré-diagnostiquer**.
4. Ne pas quantifier les écarts (rester qualitatif = note limitée).
5. Oublier que $p_{OF}$ est en m²/s² (cinématique) → multiplier par $\rho=1000$ pour obtenir des Pa.

---

## 9. Mini-défis (ludique)

- **Défi 1 (chrono)** : obtenir une première comparaison case0 vs case5 en moins de 15 minutes.
- **Défi 2 (précision)** : calculer à la main $\Delta P$ de case5 et comparer au résultat OpenFOAM.
- **Défi 3 (expert)** : proposer un cas supplémentaire (géométrie ou Re différent) pour étudier la transition laminaire/turbulente.
