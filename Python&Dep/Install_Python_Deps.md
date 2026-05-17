# Dépendances Python pour le post-traitement

> Ce guide couvre toutes les bibliothèques Python utilisées dans les TPs (Poiseuille et futurs TPs).  
> Un script d'installation automatique est fourni : [`install_python_deps.sh`](install_python_deps.sh)

---

## Installation rapide

```bash
bash install_python_deps.sh
```

---

## Vue d'ensemble des dépendances

### 1. NumPy — calcul numérique de base

**Paquet :** `numpy`  
**Usage :** tableaux multidimensionnels, opérations vectorielles, algèbre linéaire.

```python
import numpy as np

x = np.linspace(0, 1, 100)    # 100 points entre 0 et 1
u = 1 - x**2                  # profil parabolique (Poiseuille)
```

Utilisé dans **tous les scripts** de post-traitement Poiseuille (`plot_results.py`, `analyze_results.py`, `compare_cases.py`, `extract_profile.py`, `convergence_check.py`).

---

### 2. Matplotlib — visualisation 2D

**Paquet :** `matplotlib`  
**Usage :** courbes, histogrammes, profils de vitesse, graphes de convergence.

```python
import matplotlib.pyplot as plt

plt.plot(x, u, label='Poiseuille théorique')
plt.xlabel('r/R')
plt.ylabel('U/Umax')
plt.legend()
plt.savefig('profil_vitesse.png', dpi=150)
plt.show()
```

Utilisé dans : `plot_results.py`, `compare_cases.py`, `stabilization_study.py`.

---

### 3. SciPy — calcul scientifique

**Paquet :** `scipy`  
**Usage :** intégration numérique, interpolation, optimisation, traitement du signal.

```python
from scipy.integrate import quad
from scipy.interpolate import interp1d

# Intégrale du profil pour calculer le débit volumique
Q, _ = quad(lambda r: 2 * np.pi * r * u_func(r), 0, R)
```

Utilisé dans : `analyze_results.py` (calcul de débit, erreur L2 par rapport à la solution analytique).

---

### 4. Pandas — manipulation de données tabulaires

**Paquet :** `pandas`  
**Usage :** lecture de fichiers CSV, tableaux de résultats, comparaisons multi-cas.

```python
import pandas as pd

df = pd.read_csv('results/case0/profile.csv')
print(df.head())
print(df.describe())
```

Utilisé dans : `compare_cases.py`, `convergence_check.py`.

---

### 5. ReportLab — génération de PDF

**Paquet :** `reportlab`  
**Usage :** création de PDFs (pack de diffusion enseignant, fiches résultats).

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

c = canvas.Canvas("rapport.pdf", pagesize=A4)
c.drawString(100, 750, "Résultats TP Poiseuille")
c.save()
```

Utilisé dans : `build_pack_diffusion_pdf.py` (génération automatique du pack enseignant).

> ⚠️ **Non disponible via `apt`** — installation via `pip` uniquement (voir script).

---

### 6. Récapitulatif

| Bibliothèque | Version min. | Via apt | Via pip | Utilisé dans Poiseuille |
|---|---|---|---|---|
| `numpy` | 1.24 | ✅ `python3-numpy` | ✅ | Tous les scripts |
| `matplotlib` | 3.5 | ✅ `python3-matplotlib` | ✅ | plot, compare, stabilization |
| `scipy` | 1.10 | ✅ `python3-scipy` | ✅ | analyze, convergence |
| `pandas` | 2.0 | ✅ `python3-pandas` | ✅ | compare, convergence |
| `reportlab` | 3.6 | ❌ | ✅ | build_pack_diffusion_pdf |

---

## Bibliothèques standard Python (pas d'installation)

Ces modules sont inclus dans Python 3 et **ne nécessitent pas d'installation** :

| Module | Usage |
|---|---|
| `pathlib` | Chemins de fichiers (`Path(...)`) |
| `os` | Variables d'environnement, système de fichiers |
| `sys` | Arguments en ligne de commande, `sys.exit()` |
| `re` | Expressions régulières (parsing de logs OpenFOAM) |
| `xml.etree.ElementTree` | Lecture des fichiers `.pvsm` ParaView (XML) |

---

## Note sur ParaView Python (`paraview.simple`)

Le module `paraview` n'est **pas un paquet pip** — il est livré avec l'installation ParaView :

```bash
# Utiliser le Python embarqué dans ParaView :
pvpython mon_script.py

# Ou l'ajouter au PYTHONPATH si ParaView est installé via apt :
export PYTHONPATH=/usr/lib/python3/dist-packages:$PYTHONPATH
```

Les scripts `make_paraview_post_5cases.py` utilisent `pvpython` (voir les scripts d'orchestration du TP).

---

## Vérification de l'installation

```bash
python3 -c "
import numpy as np
import matplotlib
import scipy
import pandas as pd
import reportlab
print('numpy      :', np.__version__)
print('matplotlib :', matplotlib.__version__)
print('scipy      :', scipy.__version__)
print('pandas     :', pd.__version__)
print('reportlab  :', reportlab.Version)
print()
print('Toutes les dépendances sont disponibles.')
"
```
