# Mémo — Commandes UNIX essentielles
*WSL Ubuntu · ENSM Nantes · Génie maritime*

> **Comment lire ce mémo :** `$` = invite de commande (ne pas taper le `$`). Les textes entre `< >` sont à remplacer par vos valeurs. Les textes entre `[ ]` sont optionnels.

---

## 1. Naviguer dans les dossiers

| Commande | Ce que ça fait | Exemple |
|----------|---------------|---------|
| `pwd` | Affiche le dossier courant (**P**rint **W**orking **D**irectory) | `$ pwd` → `/home/etudiant` |
| `ls` | Liste les fichiers du dossier | `$ ls` |
| `ls -lh` | Liste détaillée avec tailles lisibles | `$ ls -lh` |
| `ls -a` | Inclut les fichiers cachés (`.bashrc`, `.foam`…) | `$ ls -a` |
| `cd <chemin>` | Se déplace dans un dossier | `$ cd MecaFlux/Poiseuille` |
| `cd ..` | Remonte d'un niveau | `$ cd ..` |
| `cd ~` | Revient au dossier personnel | `$ cd ~` |
| `cd -` | Revient au dossier précédent | `$ cd -` |

> **Raccourci indispensable :** appuyer sur `Tab` pour **compléter automatiquement** les noms de fichiers et de dossiers. Si rien ne s'affiche, frapper `Tab` deux fois pour voir les candidats.

---

## 2. Créer, copier, déplacer, supprimer

| Commande | Ce que ça fait | Exemple |
|----------|---------------|---------|
| `mkdir <dossier>` | Crée un dossier | `$ mkdir resultats` |
| `mkdir -p a/b/c` | Crée toute l'arborescence en une fois | `$ mkdir -p docs/images` |
| `cp <source> <dest>` | Copie un fichier | `$ cp rapport.md rapport_v2.md` |
| `cp -r <dossier> <dest>` | Copie un dossier entier (récursif) | `$ cp -r case0 case0_backup` |
| `mv <source> <dest>` | Déplace ou renomme | `$ mv brouillon.md rapport_final.md` |
| `rm <fichier>` | Supprime un fichier (**irréversible**) | `$ rm log_old.txt` |
| `rm -r <dossier>` | Supprime un dossier et son contenu (**irréversible**) | `$ rm -r case_test` |
| `rm -ri <dossier>` | Idem avec confirmation avant chaque suppression | `$ rm -ri ancien_calcul` |

> ⚠️ **Il n'y a pas de corbeille en UNIX.** `rm` supprime définitivement. Toujours vérifier avant.

---

## 3. Lire et écrire des fichiers texte

| Commande | Ce que ça fait | Exemple |
|----------|---------------|---------|
| `cat <fichier>` | Affiche le contenu entier | `$ cat controlDict` |
| `less <fichier>` | Affichage page par page (quitter : `q`) | `$ less log.icoFoam` |
| `head -n 20 <fichier>` | Affiche les 20 premières lignes | `$ head -n 20 log.icoFoam` |
| `tail -n 20 <fichier>` | Affiche les 20 dernières lignes | `$ tail -n 20 log.icoFoam` |
| `tail -f <fichier>` | Suit un fichier en temps réel (quitter : `Ctrl+C`) | `$ tail -f log.icoFoam` |
| `grep <motif> <fichier>` | Cherche un texte dans un fichier | `$ grep "SIMPLE" log.simpleFoam` |
| `grep -r <motif> <dossier>` | Cherche dans tous les fichiers d'un dossier | `$ grep -r "nu" constant/` |
| `wc -l <fichier>` | Compte le nombre de lignes | `$ wc -l log.icoFoam` |

**Enchaîner des commandes avec les pipes `|` :**
```bash
# Afficher uniquement les lignes contenant "Time" dans le log
$ cat log.icoFoam | grep "Time ="

# Compter combien de fois "converged" apparaît
$ grep -c "converged" log.simpleFoam
```

---

## 4. Lancer et gérer des processus

| Commande | Ce que ça fait | Exemple |
|----------|---------------|---------|
| `bash <script>` | Exécute un script shell | `$ bash tp_poiseuille.sh all` |
| `Ctrl + C` | **Interrompt** le programme en cours | (pendant un calcul qui bloque) |
| `Ctrl + Z` | Met en **pause** le programme en cours | |
| `bg` | Reprend le programme mis en pause en **arrière-plan** | `$ bg` |
| `fg` | Ramène un programme de l'arrière-plan **au premier plan** | `$ fg` |
| `<commande> &` | Lance directement en arrière-plan | `$ paraview &` |
| `ps aux` | Liste tous les processus en cours | `$ ps aux` |
| `kill <PID>` | Arrête un processus par son numéro | `$ kill 12345` |
| `htop` | Moniteur interactif (quitter : `q`) | `$ htop` |

---

## 5. Droits et permissions

```bash
# Rendre un script exécutable
$ chmod +x tp_poiseuille.sh
$ bash tp_poiseuille.sh all     # ou directement : ./tp_poiseuille.sh

# Voir les permissions
$ ls -l tp_poiseuille.sh
# -rwxr-xr-x  →  r=lecture, w=écriture, x=exécution
#  ^^^           (propriétaire / groupe / autres)
```

---

## 6. Variables d'environnement et chemins

```bash
# Afficher la valeur d'une variable
$ echo $HOME          # /home/etudiant
$ echo $PATH          # chemins des exécutables

# OpenFOAM — activer l'environnement (si pas dans .bashrc)
$ source /usr/lib/openfoam/openfoam2412/etc/bashrc

# Vérifier qu'OpenFOAM est actif
$ foamVersion         # doit afficher : OpenFOAM-v2412
$ echo $FOAM_TUTORIALS   # doit pointer vers les tutoriels
```

---

## 7. Astuces WSL / VS Code

| Situation | Solution |
|-----------|----------|
| Ouvrir le dossier courant dans VS Code | `$ code .` |
| Ouvrir l'explorateur Windows sur le dossier courant | `$ explorer.exe .` |
| Copier un fichier de Windows vers WSL | Glisser dans l'explorateur vers `\\wsl$\Ubuntu-24.04\home\<user>` |
| Trouver le chemin Windows d'un fichier WSL | `$ wslpath -w ~/fichier.txt` |
| Connaître sa distribution WSL | `$ cat /etc/os-release` |
| Mettre à jour les paquets | `$ sudo apt update && sudo apt upgrade -y` |
| Installer un outil manquant | `$ sudo apt install -y <nom_outil>` |

---

## 8. Recherche et aide

| Commande | Ce que ça fait |
|----------|---------------|
| `man <commande>` | Manuel complet (quitter : `q`) — ex. `man ls` |
| `<commande> --help` | Aide rapide — ex. `ls --help` |
| `which <commande>` | Chemin de l'exécutable — ex. `which python3` |
| `find <dossier> -name "<motif>"` | Cherche des fichiers — ex. `find . -name "*.foam"` |
| `history` | Affiche les commandes récentes |
| `!!` | Répète la dernière commande |
| `Ctrl + R` | Recherche dans l'historique (taper quelques lettres) |

---

## 9. Commandes spécifiques OpenFOAM

| Commande | Ce que ça fait |
|----------|---------------|
| `blockMesh` | Génère le maillage structuré depuis `blockMeshDict` |
| `icoFoam` | Lance le solveur transitoire visqueux laminaire |
| `simpleFoam` | Lance le solveur stationnaire visqueux |
| `potentialFoam` | Lance le solveur de fluide potentiel |
| `foamToVTK` | Convertit les résultats au format VTK (ParaView) |
| `checkMesh` | Vérifie la qualité du maillage |
| `foamInfo <solveur>` | Infos sur un solveur ou une classe OF |
| `paraFoam` | Lance ParaView sur le cas courant (si installé) |

**Lancer un solveur en enregistrant le log :**
```bash
$ icoFoam > log.icoFoam 2>&1      # tout dans log
$ icoFoam | tee log.icoFoam       # affiche ET enregistre simultanément
```

**Voir les résidus en temps réel :**
```bash
$ tail -f log.icoFoam | grep "Solving for"
```

---

## 10. Raccourcis clavier terminal indispensables

| Raccourci | Action |
|-----------|--------|
| `Tab` | Complétion automatique |
| `↑ / ↓` | Naviguer dans l'historique des commandes |
| `Ctrl + C` | Interrompre la commande en cours |
| `Ctrl + L` | Effacer l'écran (= `clear`) |
| `Ctrl + A` | Aller au début de la ligne |
| `Ctrl + E` | Aller à la fin de la ligne |
| `Ctrl + W` | Effacer le mot précédent |
| `Ctrl + D` | Fermer le terminal (= `exit`) |

---

## 11. Structure de chemin — mémo rapide

```
/                    ← racine du système Linux
├── home/
│   └── etudiant/    ← votre dossier personnel (~)
│       ├── Etudiants/MecaFlux/Poiseuille/   ← vos TPs
│       └── .bashrc  ← fichier de config du terminal
├── usr/
│   └── lib/openfoam/openfoam2412/   ← installation OpenFOAM
└── tmp/             ← fichiers temporaires

# Chemins absolus vs relatifs
/home/etudiant/Etudiants/   ← absolu (commence par /)
Etudiants/MecaFlux/         ← relatif (depuis le dossier courant)
../autre_dossier/           ← relatif, remonte d'un niveau
~/Etudiants/                ← ~ = /home/etudiant
```

---

*ENSM Nantes — Génie maritime — Mai 2026*
