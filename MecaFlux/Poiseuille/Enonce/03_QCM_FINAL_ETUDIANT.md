# QCM Final Etudiant
## TP OpenFOAM - Validation des acquis

## 1. Mission
Verifier que vous savez relier solveur, convergence numerique et validite physique.

## 2. Regles du jeu
- Duree conseillee: 12 a 15 min.
- Une seule reponse par question.
- Repondre d'abord, corriger ensuite.

## 3. QCM

### Q1. Dans ce TP, le role le plus pertinent de potentialFoam est:
A. Estimer fidèlement les pertes de charge visqueuses
B. Fournir un champ potentiel rapide et une référence inviscide
C. Remplacer systématiquement icoFoam et simpleFoam
D. Modéliser les effets turbulents de paroi

### Q2. Le solveur le plus adapte pour atteindre vite une solution permanente est generalement:
A. icoFoam
B. simpleFoam
C. potentialFoam
D. blockMesh

### Q3. Un indicateur de convergence iterative est:
A. Le nombre de captures d’écran
B. L’évolution des résidus
C. La couleur de la figure
D. Le nom du dossier de cas

### Q4. Un indicateur de convergence vers regime etabli (transitoire) est:
A. Stabilisation de $U_{max}(t)$ et de $\Delta p(t)$
B. Taille du fichier Python
C. Nombre de lignes dans README
D. Date de création du dossier

### Q5. Si un cas est très rapide mais physiquement incomplet pour la dissipation, il faut:
A. Le rejeter systématiquement
B. Le présenter comme vérité unique
C. Le positionner dans son domaine de validité et compléter avec solveur visqueux
D. Ignorer la physique

### Q6. L’écart au profil analytique de Poiseuille peut venir:
A. Uniquement d’erreurs Python
B. De la discrétisation, des conditions aux limites et de la zone d’entrée
C. Uniquement de la carte graphique
D. Uniquement de ParaView

### Q7. Une bonne conclusion d'ingenieur doit:
A. Donner uniquement des impressions qualitatives
B. Citer au moins un indicateur chiffré et ses limites
C. Éviter de comparer les solveurs
D. Ignorer les hypothèses du modèle

### Q8. La différence principale entre modèle potentiel et modèle visqueux est:
A. Le potentiel inclut explicitement les contraintes visqueuses pariétales
B. Le visqueux inclut diffusion de quantité de mouvement et pertes associées
C. Ils sont identiques, seul le nom change
D. Le visqueux ne conserve pas la masse

### Q9. Dans un TP pédagogique, comparer plusieurs solveurs sert surtout à:
A. Multiplier les fichiers sans but
B. Relier hypothèses de modèle, coût de calcul et validité physique
C. Éviter les équations
D. Supprimer l’analyse critique

### Q10. Le meilleur "solveur" au sens absolu est:
A. Toujours le plus rapide
B. Toujours le plus lent
C. Celui qui est adapté à la question physique posée
D. Toujours potentialFoam

---

## 4. Grille de reponses
Q1: ___  Q2: ___  Q3: ___  Q4: ___  Q5: ___
Q6: ___  Q7: ___  Q8: ___  Q9: ___  Q10: ___

## 5. Checkpoint de validation
- 8/10 et plus: objectifs du TP bien maitrises.
- 6-7/10: acquis partiels, renforcer la partie interpretation.
- 5/10 et moins: revoir guide + base theorique avant soutenance.

## 6. Mini-defi (ludique)
- Defi argumentaire: choisir 1 question et defendre la reponse en 4 lignes techniques maximum.
