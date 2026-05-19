# QCM Final — Groupe B
## TP Hagen-Poiseuille OpenFOAM — Validation des acquis

> **Version Groupe B** : ajout de 2 questions chiffrées et d'une question sur les résidus. Les concepts de pression cinématique et de potentialFoam, transférés depuis le QCM prérequis, sont ici testés en sortie de TP.

---

## 1. Mission
Vérifier que vous savez **relier solveur, convergence numérique et validité physique**, et que vous savez **lire les résultats du TP avec un œil d'ingénieur**.

## 2. Règles du jeu
- Durée conseillée : 15 minutes.
- Une seule réponse par question.
- Répondre d'abord, vérifier ensuite avec la correction enseignante.

---

## 3. QCM

### Q1. Dans ce TP, le rôle le plus pertinent de **potentialFoam** est :
A. Estimer fidèlement les pertes de charge visqueuses
B. Fournir un champ potentiel rapide et une référence inviscide (initialisation, diagnostic)
C. Remplacer systématiquement icoFoam et simpleFoam
D. Modéliser les effets turbulents de paroi

### Q2. Dans OpenFOAM incompressible (icoFoam/simpleFoam), la variable `p` est :
A. Toujours en Pa
B. Une **pression cinématique** $p/\rho$ exprimée en m²/s² — la conversion en Pa nécessite de multiplier par $\rho$
C. Une vitesse
D. Un potentiel de vitesse

### Q3. **Calcul.** Pour un canal de hauteur $H = 1$ m, un fluide de $\nu = 10^{-3}$ m²/s et une vitesse moyenne $U_{moy} = 1$ m/s, le nombre de Reynolds vaut :
A. 100
B. 1000
C. 10 000
D. Dépend de la longueur du canal

### Q4. **Calcul.** Avec $Re = 1000$ et $H = 1$ m, la longueur de développement attendue est :
A. ≈ 5 m
B. ≈ 50 m
C. ≈ 500 m
D. ≈ 0,05 m

### Q5. Le solveur le plus adapté pour atteindre **rapidement** une solution permanente est généralement :
A. icoFoam
B. simpleFoam
C. potentialFoam
D. blockMesh

### Q6. Un indicateur de convergence **itérative** (solveur stationnaire) est :
A. Le nombre de captures d'écran
B. L'évolution des résidus de $U$ et $p$
C. La couleur de la figure
D. Le nom du dossier de cas

### Q7. Un indicateur de convergence vers un **régime établi** (solveur transitoire) est :
A. Stabilisation de $U_{max}(t)$ et de $\Delta p(t)$
B. Taille du fichier Python
C. Nombre de lignes dans le README
D. Date de création du dossier

### Q8. **Lecture de résultats.** Vous obtenez sur case5 : $U_{max,num} = 1{,}48$ m/s. La référence analytique étant $U_{max,ana} = 1{,}5$ m/s, l'écart relatif est :
A. ≈ 0,02 %
B. ≈ 1,3 %
C. ≈ 13 %
D. ≈ 50 %

### Q9. L'écart au profil analytique de Poiseuille peut venir de :
A. Uniquement d'erreurs Python
B. De la discrétisation, des conditions aux limites et de la zone d'entrée non développée
C. Uniquement de la carte graphique
D. Uniquement de ParaView

### Q10. La différence principale entre modèle **potentiel** et modèle **visqueux** est :
A. Le potentiel inclut explicitement les contraintes visqueuses pariétales
B. Le visqueux inclut diffusion de quantité de mouvement et pertes associées ; le potentiel ne modélise ni couche limite ni perte de charge visqueuse
C. Ils sont identiques, seul le nom change
D. Le visqueux ne conserve pas la masse

### Q11. Une bonne conclusion d'ingénieur doit :
A. Donner uniquement des impressions qualitatives
B. Citer au moins un indicateur chiffré et reconnaître les limites du modèle
C. Éviter de comparer les solveurs
D. Ignorer les hypothèses du modèle

### Q12. Le **meilleur** solveur au sens absolu est :
A. Toujours le plus rapide
B. Toujours le plus lent
C. Celui qui est adapté à la question physique posée
D. Toujours potentialFoam

---

## 4. Grille de réponses
Q1: ___  Q2: ___  Q3: ___  Q4: ___  Q5: ___  Q6: ___
Q7: ___  Q8: ___  Q9: ___  Q10: ___  Q11: ___ Q12: ___

## 5. Checkpoint de validation
- **10/12 et plus** : objectifs du TP bien maîtrisés.
- **7–9/12** : acquis solides, vigilance sur l'interprétation chiffrée.
- **6/12 et moins** : revoir base théorique + figures de Results/ avant la soutenance.

## 6. Mini-défi argumentaire
- Choisir 1 question parmi Q3, Q4, Q8 et justifier le **calcul** en 3 lignes maximum.
- Choisir 1 question parmi Q1, Q5, Q10 et justifier la **physique** en 3 lignes maximum.

---

*Différences vs Groupe A : 12 questions au lieu de 10. Ajout de Q3 (Re), Q4 (L_dev), Q8 (écart U_max) — calcul direct. Q1 et Q2 du Groupe A déplacées ici depuis le QCM prérequis (potentialFoam, pression cinématique). Une grille de barème reste sur 20 — voir `08_FICHE_ENSEIGNANT.md` pour la conversion 12 → 20.*
