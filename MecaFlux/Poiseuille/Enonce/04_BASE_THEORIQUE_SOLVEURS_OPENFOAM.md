# Base Theorique - Solveurs OpenFOAM et cours classique de mecanique des fluides

## 0. Mission
Faire le lien entre les equations du cours et le choix du solveur pour une decision d'ingenierie argumentee.

## 1. Du cours vers la simulation
En cours classique, on presente generalement:
1. Continuité (conservation de la masse)
2. Quantité de mouvement (Navier-Stokes)
3. Cas particuliers simplifiés (Bernoulli, potentiel)

Dans OpenFOAM, les solveurs sont des implementations numeriques de ces cadres physiques sous hypotheses differentes.

## 2. Equations de reference (niveau TP)
### 2.1 Continuite incompressible
$\nabla \cdot \vec{U} = 0$

### 2.2 Navier-Stokes incompressible (forme simplifiee)
$$
\frac{\partial \vec{U}}{\partial t} + (\vec{U}\cdot\nabla)\vec{U}
= -\nabla p + \nu \nabla^2 \vec{U}
$$
avec $p$ pression cinematique dans les solveurs incompressibles OpenFOAM.

### 2.3 Bernoulli (cadre inviscide, stationnaire, sans dissipation)
Le long d'une ligne de courant:
$$
\frac{U^2}{2} + \frac{p}{\rho} + gz = \text{constante}
$$

### 2.4 Potentiel de vitesse (cas irrotationnel)
Si $\vec{U} = \nabla \Phi$ et incompressible:
$$
\nabla^2 \Phi = 0
$$

## 3. Lecture pedagogique des solveurs du TP
### 3.1 potentialFoam (case4)
- Cadre: ecoulement potentiel (inviscide / irrotationnel).
- Usage TP: champ rapide, initialisation, comparaison limite inviscide.
- Limite: ne represente pas correctement les pertes de charge visqueuses.

### 3.2 icoFoam (case0, case1, case2)
- Cadre: Navier-Stokes incompressible transitoire (PISO).
- Usage TP: observer l'evolution temporelle vers le regime etabli.
- Force: utile pour analyser stabilisation temporelle ($U_{max}(t)$, $\Delta p(t)$).

### 3.3 simpleFoam (case3)
- Cadre: Navier-Stokes incompressible stationnaire (SIMPLE).
- Usage TP: obtenir plus vite une solution permanente.
- Force: cout souvent plus faible qu'un transitoire long.

## 4. Tableau de correspondance cours -> solveur
| Cadre du cours | Hypotheses principales | Solveur TP associe | Message pedagogique |
|---|---|---|---|
| Potentiel / Bernoulli | Inviscide, dissipation negligee | potentialFoam | Rapide, utile en reference, limite pour pertes visqueuses |
| Navier-Stokes transitoire | Viscosite + evolution temporelle | icoFoam | Montre la mise en regime |
| Navier-Stokes stationnaire | Viscosite + etat permanent | simpleFoam | Efficace pour resultat permanent |

## 5. Ce que les etudiants doivent retenir
1. Un solveur n'est pas meilleur en absolu: il est plus ou moins adapte a une question physique.
2. Bernoulli/potentiel donne une intuition, mais ne remplace pas un modele visqueux pour les pertes.
3. Une simulation exploitable doit etre convergee numeriquement et coherente physiquement.
4. L'analyse doit expliciter hypotheses, domaine de validite et limites.

## 6. Checkpoints de robustesse
- Checkpoint A: hypothese physique du solveur correctement identifiee.
- Checkpoint B: indicateur numerique de convergence explicite.
- Checkpoint C: conclusion rattachee a une limite du modele.

## 7. Mini-defi (ludique)
- Defi modele: en 3 phrases, expliquer pourquoi potentialFoam peut etre utile puis insuffisant.
