# QCM de positionnement — Groupe B
## TP Hagen-Poiseuille OpenFOAM — Diagnostic d'entrée

> **Version Groupe B** : centrée sur les pré-requis **physiques** de mécanique des fluides. Les questions sur la pression cinématique OpenFOAM et potentialFoam ont été déplacées vers le QCM final, où elles testent des **acquis du TP** et non des pré-requis.

---

## 1. Mission
Valider que vous disposez du bagage physique nécessaire avant le TP. **Ce n'est pas une note** — c'est un point d'auto-diagnostic.

## 2. Règles du jeu
- Durée conseillée : 10 minutes.
- Une seule réponse par question.
- Sans support externe pour une auto-évaluation honnête.

## 3. Rappels utiles avant de commencer

- Équation de continuité incompressible : $\nabla \cdot \vec{U} = 0$
- Équation de Navier-Stokes (incompressible, sans gravité) :
$$\rho\frac{D\vec{U}}{Dt} = -\nabla p + \mu\,\Delta\vec{U}$$
- Nombre de Reynolds : $Re = \dfrac{\rho U L}{\mu} = \dfrac{U L}{\nu}$
- Condition de **non-glissement** (noSlip) à une paroi : $\vec{U}_{paroi} = \vec{0}$

---

## 4. QCM

### Q1. En écoulement incompressible, la conservation de la masse s'écrit :
A. $\nabla \cdot \vec{U} = 0$
B. $\frac{\partial p}{\partial t}=0$
C. $\nabla \times \vec{U}=0$
D. $\rho = 0$

### Q2. Un nombre de Reynolds *faible* indique en général :
A. Un régime plus turbulent
B. Un régime plus laminaire
C. Un fluide incompressible
D. Une viscosité nulle

### Q3. Le théorème de Bernoulli est **rigoureusement** valable si :
A. Écoulement visqueux avec fortes pertes
B. Écoulement incompressible, inviscide, sans dissipation, le long d'une ligne de courant
C. Écoulement turbulent pleinement développé
D. Écoulement transitoire compressible

### Q4. La viscosité dynamique $\mu$ caractérise principalement :
A. La compressibilité
B. La diffusion de quantité de mouvement
C. La gravité
D. La vitesse du son

### Q5. Dans un canal plan 2D **pleinement développé** en régime laminaire, le profil de vitesse est :
A. Linéaire
B. Exponentiel
C. Parabolique
D. Constant

### Q6. La **longueur de développement** d'un écoulement laminaire dans un canal de hauteur $H$ s'estime par :
A. $L_{dev} \approx 0{,}05 \cdot Re \cdot H$
B. $L_{dev} \approx Re / H$
C. $L_{dev} \approx H^2$
D. $L_{dev}$ est indépendante du Reynolds

### Q7. Une condition aux limites **noSlip** sur une paroi impose :
A. Pression nulle
B. Vitesse normale nulle seulement
C. Vitesse fluide nulle à la paroi
D. Gradient de pression nul

### Q8. Une simulation « **terminée** » est « **valide** » si :
A. Le log affiche `End`, cela suffit toujours
B. Les résidus, la cohérence physique et les bilans sont satisfaisants
C. Le calcul est rapide
D. Il existe un fichier VTK

### Q9. Le profil parabolique de Poiseuille relie $U_{max}$ et $U_{moy}$ par :
A. $U_{max} = U_{moy}$
B. $U_{max} = 1{,}5 \cdot U_{moy}$
C. $U_{max} = 2 \cdot U_{moy}$
D. $U_{max} = U_{moy}^2$

### Q10. Entre un solveur **transitoire** et un solveur **stationnaire** :
A. Le transitoire ne peut jamais converger
B. Le stationnaire est inutile en pratique
C. Le choix dépend de la physique recherchée et du coût numérique admissible
D. Les deux donnent toujours exactement le même coût

---

## 5. Grille de réponses
Q1: ___  Q2: ___  Q3: ___  Q4: ___  Q5: ___
Q6: ___  Q7: ___  Q8: ___  Q9: ___  Q10: ___

## 6. Checkpoint de validation
- **8/10 et plus** : pré-requis solides, vous pouvez démarrer.
- **6–7/10** : démarrage possible, mais relisez le §1 de `03_BASE_THEORIQUE.md` pendant les calculs.
- **5/10 ou moins** : revoir cours de mécanique des fluides du semestre précédent avant le TP. En particulier : continuité, Re, noSlip, profil de Poiseuille.

## 7. Mini-défi
- Défi flash : justifier deux réponses en moins de 2 minutes, à l'écrit.

---

*Différences vs Groupe A : remplacement de Q6 (pression cinématique) et Q9 (potentialFoam) — qui testaient des acquis du TP — par Q6 (formule L_dev) et Q9 (relation U_max/U_moy), qui sont des pré-requis pertinents.*
