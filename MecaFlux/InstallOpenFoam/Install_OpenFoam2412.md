# Installation OpenFOAM v2412

## 1. Mission

Installer OpenFOAM v2412 sur Ubuntu, verifier que l'environnement fonctionne, puis executer un premier cas test avant d'attaquer les TP de MecaFlux.

## 2. Prerequis

- Ubuntu avec acces administrateur
- Connexion Internet pour les paquets
- Terminal bash
- Espace disque suffisant pour OpenFOAM, ParaView et les utilitaires associes

## 3. Parcours rapide

Executer les etapes suivantes dans un terminal :

```bash
wget -q -O - https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt update
sudo apt upgrade
sudo apt install openfoam2412-default
sudo apt install paraview   # paraviewopenfoam2412-default n'existe plus (supprimé post-2024)
echo "source /usr/lib/openfoam/openfoam2412/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
foamVersion
foamInstallationTest
```

## 4. Installation detaillee

### A. Ajouter le depot OpenFOAM

La methode recommande est :

```bash
wget -q -O - https://dl.openfoam.com/add-debian-repo.sh | sudo bash
```

Alternative manuelle :

```bash
curl https://dl.openfoam.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "http://dl.openfoam.com/ubuntu $(lsb_release -cs) main"
```

Puis rafraichir les paquets :

```bash
sudo apt update
sudo apt upgrade
```

### B. Identifier les paquets utiles

Pour explorer les versions disponibles :

```bash
apt search openfoam | grep -E "openfoam[0-9]+"
apt search openfoam2 | sort
apt show openfoam2412-dev
apt show openfoam2412-default
```

### C. Installer OpenFOAM et ParaView

```bash
sudo apt install openfoam2412-default
sudo apt install paraview   # paraviewopenfoam2412-default n'existe plus (supprimé post-2024)
```

### D. Charger l'environnement automatiquement

```bash
echo "source /usr/lib/openfoam/openfoam2412/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
```

Verifier ensuite :

```bash
foamVersion
which simpleFoam
which blockMesh
```

### E. Verifier l'installation

Lancer :

```bash
foamInstallationTest
```

Points a verifier dans la sortie :

- `OpenFOAM: openfoam2412`
- `Base configuration ok.`
- `Critical systems ok.`

La ligne `ThirdParty: [missing]` n'est pas forcement bloquante dans cette installation Ubuntu.

## 5. Checkpoints de validation

- Checkpoint 1 : `foamInstallationTest` se termine sans erreur bloquante.
- Checkpoint 2 : `simpleFoam` et `blockMesh` sont trouvables depuis le terminal.
- Checkpoint 3 : l'environnement OpenFOAM est charge automatiquement dans un nouveau shell.

## 6. Cas test pitzDaily

Utiliser un cas tutorial standard pour valider la chaine complete :

```bash
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily ~/pitzDaily
cd ~/pitzDaily
blockMesh
simpleFoam
```

Signes attendus :

- `blockMesh` construit le maillage sans erreur critique.
- `simpleFoam` avance jusqu'a convergence.
- une sortie de type `SIMPLE solution converged` apparait en fin de calcul.

## 7. Mini-defis

- Retrouver ou se situe `pitzDaily` via les variables d'environnement OpenFOAM.
- Expliquer la difference entre un solveur transitoire et stationnaire avec `icoFoam` et `simpleFoam`.
- Ouvrir le cas dans ParaView et identifier l'entree, la sortie et les parois.

## 8. Depannage

- Si `foamInstallationTest` est introuvable, verifier le `source` de `bashrc`.
- Si une commande OpenFOAM n'est pas reconnue, ouvrir un nouveau terminal puis retester.
- Si ParaView ne se lance pas, verifier le paquet installe et les dependances graphiques.
- Si `sudo` ou `apt` echouent, verifier la connexion reseau et les droits de la machine.

## 9. Notes

Ce guide sert de point d'entree commun pour les supports de MecaFlux. Il pourra etre enrichi avec des captures, des variantes selon la distribution Linux, et une procedure de verification enseignant.