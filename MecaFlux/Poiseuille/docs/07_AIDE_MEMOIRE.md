# Aide-mémoire — TP Hagen-Poiseuille · OpenFOAM
*À imprimer recto-verso · format A4 · ENSM Nantes — i4 GM*

---

## ① Équations fondamentales

**Continuité (incompressible)**
$$\nabla \cdot \vec{U} = 0 \quad \Leftrightarrow \quad \frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0$$

**Navier-Stokes (incompressible, Newtonien)**
$$\rho\left(\frac{\partial \vec{U}}{\partial t} + (\vec{U}\cdot\nabla)\vec{U}\right) = -\nabla p + \mu\,\Delta\vec{U}$$

**Forme adimensionnelle — nombre de Reynolds**
$$Re = \frac{U_{moy}\,H}{\nu} \qquad \nu = \frac{\mu}{\rho}$$

*Dans le TP :* $\nu = 10^{-3}$ m²/s, $\rho = 1000$ kg/m³, $H = 1$ m

---

## ② Solution analytique de Poiseuille plan (régime établi)

**Profil de vitesse** ($y \in [-H/2,\, +H/2]$)
$$U(y) = \frac{3}{2}\,U_{moy}\left(1 - \left(\frac{2y}{H}\right)^2\right)$$

| Grandeur | Formule | Valeur (case0, U_moy=1 m/s) |
|----------|---------|-----------------------------|
| $U_{max}$ | $\tfrac{3}{2}\,U_{moy}$ | **1,50 m/s** |
| $U_{moy}$ | $\tfrac{2}{3}\,U_{max}$ | 1,00 m/s |
| $\Delta p_{ana}$ | $\dfrac{12\,\mu\,U_{moy}\,L}{H^2}$ | 1 200 Pa (L=100 m) |
| $p_{OF}$ | $\Delta p / \rho$ | **1,2 m²/s²** ← unité OpenFOAM |

**Longueur de développement hydrodynamique**
$$L_{dev} \approx 0{,}05 \times Re \times H$$

| Cas | Re | $L_{dev}$ | L canal | Profil à la sortie |
|-----|----|-----------|---------|---------------------|
| case0 | 1000 | 50 m | 100 m | partiellement établi (2×$L_{dev}$) |
| case1 | 500  | 25 m | 50 m  | partiellement établi |
| case2 | 1500 | 75 m | 150 m | partiellement établi |
| case3 | 1500 | 75 m | 150 m | idem case2 (simpleFoam) |
| case4 | ∞   | 0   | 10 m  | **uniforme** — fluide parfait |
| case5 | 1000 | 50 m | 200 m | **pleinement établi** (4×$L_{dev}$) ✅ |

---

## ③ Les trois solveurs — hypothèses et limites

| Solveur | Physique modélisée | Hypothèses | Ce qu'il ne capture pas |
|---------|-------------------|------------|-------------------------|
| **icoFoam** | Visqueux laminaire transitoire | $Re < 2300$, incompressible, $\rho$ = cste | Turbulence, compressibilité |
| **simpleFoam** | Visqueux laminaire **stationnaire** | Régime permanent, même physique que icoFoam | Transitoire, instabilités |
| **potentialFoam** | Fluide parfait (inviscide, irrotationnel) | $\mu = 0$, $\nabla \times \vec{U} = 0$ | Frottement, couche limite, $\Delta p$ |

> **Règle clé :** case4 (potentialFoam) → $U_{max} = U_{moy}$ (profil plat) et $\Delta p \approx 0$. Physiquement : sans viscosité, pas de pertes de charge.

---

## ④ Pression cinématique OpenFOAM ⚠️

OpenFOAM résout la pression **cinématique** $p_{OF} = p / \rho$ — unité **m²/s²**, pas Pa.

$$p_{[Pa]} = p_{OF} \times \rho \qquad (ex.\; 1{,}2\;\text{m}^2/\text{s}^2 \times 1000\;\text{kg/m}^3 = 1200\;\text{Pa})$$

---

## ⑤ Validation — critères à vérifier

| Critère | Seuil attendu | Où regarder |
|---------|--------------|-------------|
| Résidus $U_x$, $U_y$ | $< 10^{-6}$ | `log.icoFoam` ou terminal |
| Résidu $p$ | $< 10^{-5}$ | idem |
| $U_{max}$ case5 | $1{,}48$ – $1{,}50$ m/s (écart $<2\%$) | `Results/` figures |
| $\Delta p$ case5 | $\approx 2400$ Pa (écart $<1\%$) | `Results/` figures |
| $U_{max}$ case4 | $= U_{moy} = 1{,}0$ m/s (profil plat) | ParaView |

> **Convergence ≠ validation.** Un calcul peut converger sur une mauvaise physique (case0 est convergé mais profil non établi).

---

## ⑥ Commandes TP en un coup d'œil

```bash
# Tout en une commande
bash tp_poiseuille.sh all

# Étape par étape
bash tp_poiseuille.sh 1        # setup — génère les 6 cas
bash tp_poiseuille.sh 2        # run  — blockMesh + solveurs + foamToVTK
bash tp_poiseuille.sh 3-7      # post — figures Python
bash tp_poiseuille.sh 8        # ParaView

# Nettoyer (garder configs, supprimer résultats)
bash tp_poiseuille.sh clean --dry-run   # aperçu avant suppression
bash tp_poiseuille.sh clean --yes       # supprime
```

---

## ⑦ Structure d'un cas OpenFOAM

```
case0/
├── 0/                  ← conditions initiales et aux limites
│   ├── U               ← champ de vitesse (m/s)
│   └── p               ← pression cinématique (m²/s²)
├── constant/
│   ├── transportProperties   ← ν (nu)
│   └── polyMesh/       ← maillage (généré par blockMesh)
└── system/
    ├── blockMeshDict   ← définition du maillage
    ├── controlDict     ← durée, Δt, fréquence d'écriture
    ├── fvSchemes       ← schémas de discrétisation
    └── fvSolution      ← solveurs linéaires + tolérances
```

**Paramètres clés de `controlDict` :**
| Clé | Rôle | Valeur typique |
|-----|------|----------------|
| `endTime` | Fin de la simulation | 200 s |
| `deltaT` | Pas de temps | 0,1 s |
| `writeInterval` | Fréquence d'écriture | 20 s |
| `maxCo` | Nombre de Courant max | 0,5 |

---

## ⑧ ParaView — actions essentielles

| Action | Chemin menu | Raccourci |
|--------|------------|-----------|
| Ouvrir un cas `.foam` | File → Open | `Ctrl+O` |
| Appliquer un filtre | clic `Apply` dans Properties | — |
| Changer le champ affiché | Barre `Coloring` | — |
| Aller au dernier pas de temps | bouton `⏭` | `Fin` |
| Ajouter un plan de coupe | Filters → Slice | — |
| Tracer un profil (ligne) | Filters → Plot Over Line | — |
| Exporter une image | File → Save Screenshot | `Ctrl+Shift+S` |

> **Astuce :** fixer la même échelle de couleurs pour tous les cas avant de comparer (clic droit sur la barre de couleur → *Edit Color Map* → décocher *Automatic Rescale*).

---

## ⑨ Tableau comparatif à compléter (restitution)

| Cas | Solveur | Re | $U_{max}$ (num.) | $U_{max}$ (ana.) | Écart % | $\Delta p$ (num.) | $\Delta p$ (ana.) | Profil établi ? |
|-----|---------|----|-------------------|-------------------|---------|-------------------|-------------------|-----------------|
| case0 | icoFoam | 1000 | | 1,50 m/s | | | 1200 Pa | ✗ |
| case1 | icoFoam | 500  | | 0,75 m/s | | | 600 Pa  | ✗ |
| case2 | icoFoam | 1500 | | 2,25 m/s | | | 1800 Pa | ✗ |
| case3 | simpleFoam | 1500 | | 2,25 m/s | | | 1800 Pa | ✗ |
| case4 | potentialFoam | ∞ | | N/A | — | | ≈ 0 Pa | — |
| case5 | icoFoam | 1000 | | 1,50 m/s | | | 2400 Pa | **✅** |

---

*Références : Çengel & Cimbala, Fluid Mechanics 3rd ed. — Magdeleine N., Simulations Numériques i4, ENSM 2023*
