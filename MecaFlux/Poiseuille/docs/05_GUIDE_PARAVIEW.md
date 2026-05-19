# Guide ParaView Pas a Pas
## Visualiser, exporter des images, sauvegarder une scene globale

## 1. Mission
Vous devez:
1. Charger les 6 simulations (case0 a case5).
2. Produire des visualisations comparables (U et p).
3. Exporter des images propres pour le rapport.
4. Enregistrer un etat global `paraview_cases.pvsm` reutilisable.

> **Cle pedagogique** : case5 (L=200 m, 4×L_dev) est le seul cas ou le profil parabolique analytique apparait pleinement. Sa visualisation est obligatoire dans votre rapport.

## 2. Preparation robuste
Placez-vous dans votre dossier Poiseuille (le chemin depend de votre installation) :

```bash
# Exemple — adaptez au chemin reel sur votre machine
cd ~/Etudiants/MecaFlux/Poiseuille
ls case0 case1 case2 case3 case4 case5
```

Creation des fichiers `.foam` (recommandee):

```bash
bash scripts/create_foam_files.sh
```

## 3. Charger tous les cas
1. Ouvrir ParaView.
2. `File > Open`.
3. Ouvrir successivement:
   - `case0/case0.foam`
   - `case1/case1.foam`
   - `case2/case2.foam`
   - `case3/case3.foam`
   - `case4/case4.foam`
   - `case5/case5.foam`
4. Cliquer `Apply` pour chaque source.
5. Dans `Animation View`, se placer au dernier pas de temps.

Astuce robustesse:
- Renommer les sources dans le `Pipeline Browser` (ex: `icoFoam_case0`).

## 4. Regles de comparaison (obligatoires)
### 4.1 Vitesse
1. Selectionner un cas.
2. `Coloring` -> `U (Magnitude)`.
3. Fixer la meme echelle min/max pour tous les cas.

### 4.2 Pression
1. Dupliquer la vue ou changer le champ actif.
2. `Coloring` -> `p`.
3. Refixer une echelle commune min/max.

## 5. Vues comparatives recommandees
### 5.1 Slice
1. `Filters > Slice`.
2. Plan de coupe au milieu du canal (ex: normal `0 0 1`).
3. Reproduire le meme filtre sur les autres cas.

### 5.2 Streamlines
1. `Filters > Stream Tracer`.
2. `Seed Type`: `Point Source` ou `Line Source`.
3. Ajuster le nombre de graines pour un rendu lisible.

### 5.3 Lisibilite des figures
1. Representation `Surface`.
2. Activer `Show Color Legend`.
3. Garder la meme camera pour comparer proprement.

## 6. Export d'images
1. Positionner la vue.
2. `File > Save Screenshot`.
3. Parametres recommandes:
   - Resolution: `1920x1080` (ou `2560x1440`).
   - Fond: blanc pour rapport PDF standard.
   - Nom explicite: `U_case3_slice_t180.png`.

Convention de nommage:
- `U_caseX_viewY_tZZZ.png`
- `p_caseX_viewY_tZZZ.png`

Repertoire conseille:

```bash
mkdir -p Results/paraview_images
```

## 7. Sauvegarder la scene globale
1. `File > Save State`.
2. Nom recommande: `paraview_cases.pvsm`.
3. Sauvegarder dans le dossier `Poiseuille`.

## 8. Recharger rapidement
1. `File > Load State`.
2. Selectionner `paraview_cases.pvsm`.
3. Si demande de remappage, pointer vers `case0..case5`.

## 9. Checkpoints de validation
1. Une vue vitesse comparable entre au moins 3 cas.
2. Une vue pression comparable entre au moins 3 cas.
3. Au moins 2 captures correctement nommees.
4. Un `paraview_cases.pvsm` qui se recharge sans erreur.
5. Echelles de couleur homogenes.

## 10. Mini-defis (ludique)
- Defi 1: sortir une figure U comparative en moins de 10 minutes.
- Defi 2: reproduire la meme camera sur 6 cas sans decalage visuel.
- Defi 3: proposer la figure la plus utile pour expliquer la perte de charge.

## 11. Erreurs frequentes a eviter
1. Comparer des cas avec des echelles couleurs differentes.
2. Oublier `Apply` apres ouverture d'une source.
3. Capturer des temps differents sans le signaler.
4. Fermer ParaView sans sauvegarder l'etat `.pvsm`.
