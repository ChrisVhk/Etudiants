# Base Théorique — Solveurs OpenFOAM et mécanique des fluides

## 0. Mission
Faire le lien entre les équations du cours et le choix du solveur pour une décision d'ingénierie argumentée.

---

## 1. Du cours vers la simulation

En cours classique, on présente généralement :
1. Continuité (conservation de la masse)
2. Quantité de mouvement (Navier-Stokes)
3. Cas particuliers simplifiés (Bernoulli, potentiel)

Dans OpenFOAM, les solveurs sont des implémentations numériques de ces cadres physiques sous hypothèses différentes.

---

## 2. Équations de référence (niveau TP)

### 2.1 Continuité incompressible
$$\nabla \cdot \vec{U} = 0$$

### 2.2 Navier-Stokes incompressible
$$\frac{\partial \vec{U}}{\partial t} + (\vec{U} \cdot \nabla)\vec{U} = -\nabla p + \nu \nabla^2 \vec{U}$$
avec $p$ = **pression cinématique** dans les solveurs incompressibles OpenFOAM ($p_{OF} = P_{SI} / \rho$, en m²/s²).

### 2.3 Bernoulli (cadre inviscide, stationnaire, sans dissipation)
Le long d'une ligne de courant :
$$\frac{U^2}{2} + \frac{p}{\rho} + gz = \text{constante}$$
> ⚠️ **Bernoulli est valable uniquement sans viscosité.** Il ne prédit aucune perte de charge.

### 2.4 Potentiel de vitesse (cas irrotationnel)
Si $\vec{U} = \nabla \Phi$ et incompressible :
$$\nabla^2 \Phi = 0$$

### 2.5 Solution analytique de Poiseuille plan (écoulement établi)

Pour un canal plan de hauteur $H$, avec $U_{moy}$ la vitesse débitante :
$$U(y) = \frac{3}{2} U_{moy} \left[1 - \left(\frac{2y}{H}\right)^2\right], \quad y \in [-H/2, H/2]$$

Profil parabolique, vitesse maximale en $y=0$ :
$$U_{max} = \frac{3}{2} U_{moy}$$

Gradient de pression (pression cinématique, OpenFOAM) :
$$\frac{dp}{dx} = -\frac{12\,\nu\,U_{moy}}{H^2}$$

Chute de pression totale sur un canal de longueur $L$ :
$$\Delta p_{kin} = \frac{12\,\nu\,U_{moy}}{H^2} \times L \quad [\text{m}^2/\text{s}^2]$$
$$\Delta P = \rho \times \Delta p_{kin} \quad [\text{Pa}]$$

---

## 3. Longueur de développement hydrodynamique — point clé du TP

La solution de Poiseuille n'est **valide que si l'écoulement est pleinement établi**. En pratique, il faut que le fluide ait parcouru une distance suffisante depuis l'entrée pour que les profils de vitesse aient convergé vers la parabole.

$$L_{dev} \approx 0.05 \times Re \times H \quad \text{(laminaire)}$$

**Application numérique du TP :**

| Cas   | $U_{moy}$ | Re   | $L_{dev}$ | $L_{canal}$ | % développé à la sortie |
|-------|-----------|------|-----------|-------------|--------------------------|
| case0 | 1.0 m/s   | 1000 | 50 m      | 10 m        | 20 %                     |
| case1 | 0.5 m/s   | 500  | 25 m      | 10 m        | 40 %                     |
| case2 | 1.5 m/s   | 1500 | 75 m      | 10 m        | 13 %                     |
| case5 | 1.0 m/s   | 1000 | 50 m      | 100 m       | 100 % ✅                 |

> **Conclusion** : Les cas 0 à 2 simulent un écoulement **en cours de développement**. Les profils numériques sont plus "plats" que la parabole analytique. Seul **case5** (L=100 m) atteint le régime de Poiseuille établi.

---

## 4. Lecture pédagogique des solveurs du TP

### 4.1 potentialFoam (case4)
- **Cadre** : écoulement potentiel (inviscide / irrotationnel).
- **Équation résolue** : $\nabla^2 \Phi = 0$.
- **Résultat** : profil de vitesse plat, $\Delta P \approx 0$ (aucune dissipation).
- **Usage TP** : champ rapide, initialisation, comparaison limite inviscide.
- **Limite** : ne représente pas les pertes de charge, ni la couche limite visqueuse.

### 4.2 icoFoam (case0, case1, case2, case5)
- **Cadre** : Navier-Stokes incompressible **transitoire** (algorithme PISO).
- **Usage TP** : observer l'évolution temporelle vers le régime établi.
- **Force** : permet d'analyser la stabilisation temporelle ($U_{max}(t)$, $\Delta p(t)$).

### 4.3 simpleFoam (case3)
- **Cadre** : Navier-Stokes incompressible **stationnaire** (algorithme SIMPLE).
- **Usage TP** : obtenir une solution permanente sans intégrer le transitoire.
- **Force** : coût souvent bien plus faible qu'un transitoire long.

---

## 5. Tableau de correspondance cours → solveur

| Cadre du cours         | Hypothèses principales             | Solveur TP associé | Message pédagogique |
|------------------------|------------------------------------|--------------------|---------------------|
| Potentiel / Bernoulli  | Inviscide, sans dissipation        | potentialFoam      | Rapide, mais ΔP=0 — inutilisable pour pertes de charge |
| N-S transitoire        | Visqueux + évolution temporelle    | icoFoam            | Montre la mise en régime, nécessite $t > t_{stab}$ |
| N-S stationnaire       | Visqueux + état permanent          | simpleFoam         | Efficace pour résultat permanent |

---

## 6. Ce que les étudiants doivent retenir

1. Un solveur n'est pas **meilleur en absolu** : il est plus ou moins adapté à une question physique.
2. Bernoulli/potentiel donne une intuition mais **ne remplace pas un modèle visqueux pour les pertes**.
3. Une simulation exploitable doit être **convergée numériquement** ET **cohérente physiquement**.
4. Un canal trop court ne permet pas d'atteindre le régime de Poiseuille — **c'est de la physique, pas un bug**.
5. L'analyse doit expliciter hypothèses, domaine de validité et limites.

---

## 7. Vérification quantitative attendue

Pour case0 (référence, écoulement non développé, L=10m) :
- $U_{max}$ numérique ≈ **1.28 m/s** (au lieu de 1.50 m/s analytique, écart ≈ 15%)
- $\Delta P$ numérique ≈ **311 Pa** (au lieu de 120 Pa analytique, écart ≈ 159%)
  - L'écart sur ΔP est grand car la zone d'entrée crée une surpression d'accélération.

Pour case5 (établi, L=100m) :
- $U_{max}$ numérique → **1.50 m/s** (proche de l'analytique, écart < 5%)
- $\Delta P$ numérique → **1200 Pa** (analytique = 1200 Pa, écart < 2%)

---

## 8. Mini-défi (ludique)
- **Défi modèle** : en 3 phrases, expliquer pourquoi potentialFoam peut être utile puis insuffisant.
- **Défi longueur** : calculer à la main $L_{dev}$ pour Re=2000. À partir de quelle longueur de canal le profil est-il établi à 95% ?
