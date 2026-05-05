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
sudo sh -c "wget -O - https://dl.openfoam.com/add-debian-repo.sh | bash"
sudo apt-get update
sudo apt-get install openfoam2412-default
echo "source /usr/lib/openfoam/openfoam2412/etc/bashrc" >> ~/.bashrc
source ~/.bashrc
foamInstallationTest
```

## 4. Installation detaillee

### A. Ajouter le depot OpenFOAM

Ajouter le depot officiel OpenCFD/ESI, puis rafraichir la liste des paquets.

### B. Installer le paquet principal

Installer `openfoam2412-default`, qui fournit l'environnement, les solveurs usuels et les utilitaires de base.

### C. Charger l'environnement automatiquement

Ajouter le `source` du fichier `bashrc` OpenFOAM dans `~/.bashrc`, puis recharger le shell.

### D. Verifier l'installation

Lancer :

```bash
foamInstallationTest
```

Verifier aussi :

```bash
which icoFoam
which simpleFoam
echo $WM_PROJECT_VERSION
```

### E. Installer ParaView si necessaire

Selon l'installation retenue, installer le paquet ParaView associe a OpenFOAM, puis verifier qu'un lancement simple fonctionne.

## 5. Checkpoints de validation

- Checkpoint 1 : `foamInstallationTest` se termine sans erreur bloquante.
- Checkpoint 2 : `icoFoam` et `simpleFoam` sont trouvables depuis le terminal.
- Checkpoint 3 : l'environnement OpenFOAM est charge automatiquement dans un nouveau shell.

## 6. Cas test pitzDaily

Utiliser un cas tutorial standard pour valider la chaine complete :

```bash
cd $FOAM_TUTORIALS/incompressible/simpleFoam/pitzDaily
blockMesh
simpleFoam
```

Objectif : verifier que le maillage se construit, que le solveur s'execute, et qu'un post-traitement de base est possible.

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