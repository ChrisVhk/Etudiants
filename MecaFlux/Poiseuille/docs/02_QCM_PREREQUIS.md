# QCM Prerequis Etudiant
## TP OpenFOAM - Niveau d'entree

## 1. Mission
Valider les prerequis avant le lancement des simulations.

## 2. Regles du jeu
- Duree conseillee: 10 a 12 min.
- Une seule reponse par question.
- Sans support externe pour une auto-evaluation honnete.

## 3. QCM

### Q1. En ecoulement incompressible, la conservation de la masse s'ecrit:
A. $\nabla \cdot \vec{U} = 0$
B. $\frac{\partial p}{\partial t}=0$
C. $\nabla \times \vec{U}=0$
D. $\rho = 0$

### Q2. Un nombre de Reynolds faible indique en general:
A. Un régime plus turbulent
B. Un régime plus laminaire
C. Un fluide incompressible
D. Une viscosité nulle

### Q3. Bernoulli est rigoureusement valable si:
A. Ecoulement visqueux avec fortes pertes
B. Ecoulement incompressible, inviscide, sans dissipation sur une ligne de courant
C. Ecoulement turbulent pleinement developpe
D. Ecoulement transitoire compressible

### Q4. La viscosité dynamique $\mu$ caractérise principalement:
A. La compressibilité
B. La diffusion de quantité de mouvement
C. La gravité
D. La vitesse du son

### Q5. Dans un canal plan pleinement développé laminaire, le profil de vitesse est:
A. Linéaire
B. Exponentiel
C. Parabolique
D. Constant

### Q6. Dans OpenFOAM incompressible (icoFoam/simpleFoam), la variable $p$ est:
A. Toujours en Pa
B. Une pression cinématique (Pa/$\rho$)
C. Une vitesse
D. Un potentiel de vitesse

### Q7. Une condition aux limites type "noSlip" sur une paroi impose:
A. Pression nulle
B. Vitesse normale nulle seulement
C. Vitesse fluide nulle à la paroi
D. Gradient de pression nul

### Q8. Une simulation "terminee" est "valide" si:
A. Le log affiche End, cela suffit toujours
B. Les residus, la coherence physique et les bilans sont satisfaisants
C. Le calcul est rapide
D. Il existe un fichier VTK

### Q9. L'objectif principal de potentialFoam est:
A. Résoudre Navier-Stokes visqueux complet
B. Fournir une solution potentielle rapide (souvent utile pour initialiser/diagnostiquer)
C. Modéliser directement la turbulence
D. Calculer automatiquement la couche limite visqueuse

### Q10. Entre un solveur transitoire et stationnaire:
A. Le transitoire ne peut jamais converger
B. Le stationnaire est inutile en pratique
C. Le choix depend de la physique recherchee et du cout numerique admissible
D. Les deux donnent toujours exactement le même coût

---

## 4. Grille de reponses
Q1: ___  Q2: ___  Q3: ___  Q4: ___  Q5: ___
Q6: ___  Q7: ___  Q8: ___  Q9: ___  Q10: ___

## 5. Checkpoint de validation
- 8/10 et plus: prerequis solides.
- 6-7/10: demarrage possible avec vigilance sur la theorie.
- 5/10 et moins: revoir la base theorique avant execution longue.

## 6. Mini-defi (ludique)
- Defi flash: justifier scientifiquement 2 reponses en moins de 2 minutes.
