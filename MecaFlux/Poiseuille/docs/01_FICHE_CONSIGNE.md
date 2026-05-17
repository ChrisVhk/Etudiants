# Fiche étudiant — TP Hagen-Poiseuille (4h)
## Mécanique des fluides numérique — Génie maritime

---

## 1. Question centrale du TP

> **Pourquoi le choix du solveur CFD change-t-il la physique que vous simulez ?**

Vous allez comparer trois solveurs OpenFOAM sur un canal 2D simple, puis justifier lequel est adapté à un cas maritime réel.

---

## 2. Ce que vous devez savoir montrer

| Compétence | Ce que l'on attend concrètement |
|---|---|
| **Théorie** | Énoncer les hypothèses de chaque modèle (potentiel / visqueux / turbulent) |
| **Qualité numérique** | Vérifier la convergence (résidus), identifier un profil non développé |
| **Interprétation** | Expliquer pourquoi simulation ≠ analytique, avec une cause précise |
| **Conclusion ingénieur** | Recommander un solveur pour un cas réel avec justification chiffrée |

---

## 3. Les 6 cas — ce qu'ils représentent

| Cas | Solveur | Re | À retenir |
|---|---|---|---|
| case0 | icoFoam | 1000 | **Référence** — profil en développement |
| case1 | icoFoam | 500 | Re plus faible — développement plus lent |
| case2 | icoFoam | 1500 | Re plus élevé — développement plus rapide |
| case3 | simpleFoam | 1500 | **Même physique** que case2, solveur stationnaire |
| case4 | potentialFoam | ∞ | **Fluide parfait** — pas de frottement, pas de perte de charge |
| case5 | icoFoam | 1000 | **Canal long** — seul cas avec profil parabolique pleinement établi |

> **Clé** : $U_{max} = 1{,}5 \times U_{moy}$ en Poiseuille plan établi. Si votre simulation ne donne pas ça, demandez-vous pourquoi.

---

## 4. Déroulé (4h) — actions pas à pas

### Phase 1 — Démarrage (0h00–0h10)
- [ ] Lire cette fiche en entier (5 min)
- [ ] Lancer le workflow de calcul — il tourne environ **20 min**, passez à la Phase 2 sans attendre :
```bash
cd MecaFlux/Poiseuille
bash tp_poiseuille.sh 0-7   # setup + simulations + post-traitement
```

### Phase 2 — Théorie pendant les calculs (0h10–0h40)
- [ ] Répondre au QCM prérequis (`docs/02_QCM_PREREQUIS.md`) — 10 min
- [ ] Lire la base théorique (`docs/03_BASE_THEORIQUE.md`) — solveurs, hypothèses, limites
- [ ] Identifier les différences icoFoam / simpleFoam / potentialFoam avant d'ouvrir les résultats

### Phase 3 — Visualisation ParaView (0h40–1h40)
- [ ] Vérifier que le workflow est terminé (chercher `✅` dans la sortie du terminal)
- [ ] Ouvrir ParaView : `bash tp_poiseuille.sh 8`
- [ ] Visualiser le champ de vitesse U pour case0 et case5 — noter la différence de profil
- [ ] Visualiser case4 (potentialFoam) — noter l'absence de couche limite
- [ ] Consulter le guide si besoin : `docs/05_GUIDE_PARAVIEW.md`

### Phase 4 — Analyse des résultats (1h40–2h40)
- [ ] Ouvrir le dossier `Results/` — vérifier que les figures sont générées
- [ ] Relire les figures `velocity_profiles_V2.png` et `comparison_V2.png`
- [ ] Compléter le **tableau comparatif** (voir section 6)
- [ ] Identifier l'écart case5 vs analytique — est-il < 5 % ?
- [ ] Répondre aux 4 questions obligatoires (section 5)

### Phase 5 — Rédaction et restitution (2h40–4h00)
- [ ] Rédiger la conclusion technique (10 à 15 lignes, au moins deux indicateurs chiffrés)
- [ ] Vérifier que tous les livrables sont présents (section 6)
- [ ] Relire la conclusion — elle doit relier explicitement solveur ↔ décision ingénierie

---

## 5. Questions obligatoires (à traiter dans la restitution)

1. Quelles hypothèses différentielles distinguent fluide potentiel, visqueux laminaire et turbulent modélisé ?
2. Pourquoi case4 (potentialFoam) ne présente aucune perte de charge ? Que manque-t-il physiquement ?
3. Quel cas est le plus robuste numériquement ? Justifiez avec les résidus.
4. Quelle modification minimale (géométrie, conditions aux limites, solveur) rendrait l'étude plus représentative d'un cas maritime réel ?

---

## 6. Livrables attendus

| # | Livrable | Format |
|---|---|---|
| 1 | Mémo théorie | 1 page max — potentiel, visqueux, décolllement, turbulence |
| 2 | Tableau comparatif des 6 cas | U_max num. / U_max ana. / écart (%) / convergence |
| 3 | 3 à 5 figures commentées | Issues de `Results/`, chaque figure avec 2–3 lignes d'interprétation |
| 4 | Conclusion technique | 10 à 15 lignes, recommandation argumentée avec indicateurs chiffrés |

---

## 7. Barème (sur 20)

| Critère | Points | Ce qui est évalué |
|---|---|---|
| Théorie | 5 | Exactitude des hypothèses, formules clés |
| Qualité numérique | 6 | Workflow correct, convergence vérifiée, résultats reproductibles |
| Interprétation physique | 5 | Lien simulation ↔ théorie, explication des écarts |
| Analyse critique | 2 | Limites identifiées, incertitudes reconnues |
| Clarté de la restitution | 2 | Figures lisibles, rédaction soignée |

---

## 8. Auto-contrôle avant de rendre

- [ ] **Checkpoint A** — Les 6 cas ont tourné et les logs ne contiennent pas d'erreur.
- [ ] **Checkpoint B** — J'ai calculé l'écart $U_{max}$ numérique / analytique pour au moins un cas.
- [ ] **Checkpoint C** — Ma conclusion mentionne clairement les limites du modèle.
- [ ] **Checkpoint D** — J'explique pourquoi case5 est le seul cas « valide » au sens de Poiseuille établi.

---

## 9. Mini-défis (optionnels, bonus)

- **Défi chrono** : produire une figure comparative U validée (case0 vs case5) en moins de 15 min.
- **Défi précision** : expliquer un écart simulation/théorie avec une cause numérique précise (maillage, timestep, longueur de développement).
- **Défi physique** : démontrer en 3 phrases pourquoi case4 ne peut pas modéliser un écoulement réel en conduite.

---

## 10. Rappels importants

- Une simulation qui **tourne** n'est pas automatiquement **valide** : appuyez-vous sur les logs, les profils et la cohérence physique.
- Le setup est laminaire — soyez explicites sur ce qui est hors domaine (turbulence développée, décollement fort).
- En cas de doute sur une commande : `bash tp_poiseuille.sh --help` ou consultez le `README.md`.

