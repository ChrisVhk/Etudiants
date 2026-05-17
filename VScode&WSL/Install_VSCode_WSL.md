# Installer WSL Ubuntu 24.04 et VS Code sous Windows

> **Public :** étudiants sous Windows qui souhaitent travailler avec des outils Linux (OpenFOAM, Python, etc.) sans quitter leur machine.  
> **Durée estimée :** 20 à 40 minutes selon la vitesse du réseau.

---

## Prérequis

| Élément | Exigence minimale |
|---|---|
| Système | Windows 10 version 2004 (build 19041) ou Windows 11 |
| RAM | 8 Go recommandés |
| Espace disque | 10 Go libres minimum |
| Droits | Compte **administrateur** local |

Pour vérifier votre build Windows : touche `Win + R` → tapez `winver` → Entrée.

---

## Étape 1 — Installer WSL 2 avec Ubuntu 24.04

### 1.1 Ouvrir PowerShell en administrateur

Clic droit sur le bouton **Démarrer** → **Terminal Windows (administrateur)**  
ou chercher « PowerShell » dans le menu Démarrer → **Exécuter en tant qu'administrateur**.

![Ouvrir PowerShell en administrateur](Images/01_powershell_admin.png)

> 💡 Une fenêtre bleue ou noire avec le titre « Administrateur » doit s'afficher.

---

### 1.2 Lancer l'installation en une commande

Dans PowerShell, tapez :

```powershell
wsl --install -d Ubuntu-24.04
```

Cette commande :
- Active le composant WSL et la plateforme de virtualisation
- Télécharge et installe le noyau Linux WSL 2
- Installe **Ubuntu 24.04 LTS** comme distribution par défaut

![PowerShell exécutant wsl --install](https://learn.microsoft.com/fr-fr/windows/wsl/media/wsl-install.png)

> ⚠️ **Un redémarrage est nécessaire** à la fin du téléchargement. Sauvegardez votre travail avant.

---

### 1.3 Redémarrer Windows

Après le redémarrage, Ubuntu s'ouvre automatiquement dans une fenêtre de terminal et finalise l'installation (décompression ~2 minutes).

---

## Étape 2 — Configurer Ubuntu (utilisateur et mot de passe)

Au premier lancement, Ubuntu vous demande de créer un compte Linux :

```
Enter new UNIX username: prenom        ← votre prénom en minuscules, sans espace
New password:                          ← le curseur ne bouge pas, c'est normal
Retype new password:
passwd: password updated successfully
```

![Ubuntu demande un nom d'utilisateur](https://learn.microsoft.com/fr-fr/windows/wsl/media/ubuntuinstall.png)

> ⚠️ Ce compte Linux est **indépendant** de votre compte Windows. Notez ce mot de passe, il sera demandé pour toute commande `sudo`.

---

## Étape 3 — Mettre à jour Ubuntu

Dans le terminal Ubuntu, exécutez :

```bash
sudo apt update && sudo apt upgrade -y
```

Saisissez votre mot de passe Linux quand demandé. Cette étape installe toutes les mises à jour de sécurité.

![Terminal Ubuntu après apt update](Images/03_apt_update.png)

---

## Étape 4 — Installer VS Code sur Windows

### 4.1 Télécharger l'installateur

Rendez-vous sur **[https://code.visualstudio.com](https://code.visualstudio.com)** et cliquez sur **Download for Windows**.

![Page de téléchargement VS Code](Images/04_vscode_download.png)

---

### 4.2 Lancer l'installation

Exécutez le fichier `.exe` téléchargé. Pendant l'installation, cochez les cases suivantes :

- ✅ Ajouter l'action « Ouvrir avec Code » au menu contextuel des fichiers
- ✅ Ajouter l'action « Ouvrir avec Code » au menu contextuel des dossiers
- ✅ Ajouter à PATH

![Options d'installation VS Code](Images/04_vscode_install_options.png)

---

## Étape 5 — Installer l'extension WSL dans VS Code

### 5.1 Ouvrir VS Code

Lancez VS Code depuis le menu Démarrer ou en tapant `code` dans PowerShell.

---

### 5.2 Installer l'extension WSL

Dans VS Code :
1. Cliquez sur l'icône **Extensions** dans la barre latérale gauche (ou `Ctrl+Shift+X`)
2. Cherchez **WSL**
3. Installez l'extension **WSL** publiée par *Microsoft* (identifiant : `ms-vscode-remote.remote-wsl`)

![Extension WSL dans VS Code](https://learn.microsoft.com/fr-fr/windows/wsl/media/vscode-remote-wsl-extensions.png)

> 💡 Vous pouvez aussi installer le pack complet **Remote Development** (`ms-vscode-remote.vscode-remote-extensionpack`) qui inclut SSH et Dev Containers en plus de WSL.

---

### 5.3 Extensions installées

Certaines extensions s'installent **côté Windows** (une seule fois), d'autres doivent aussi être installées **côté WSL** (VS Code le signale avec un bouton **"Install in WSL"** dans le panneau Extensions).

---

#### 🔵 Connexion distante — côté Windows uniquement

| Extension | Identifiant | Rôle |
|---|---|---|
| **Remote Development** (pack) | `ms-vscode-remote.vscode-remote-extensionpack` | Installe WSL + SSH + Remote Explorer en un clic |
| **WSL** | `ms-vscode-remote.remote-wsl` | Pont Windows ↔ Linux — inclus dans le pack ci-dessus |
| **Remote SSH** | `ms-vscode-remote.remote-ssh` | Connexion à des machines distantes via SSH |
| **Remote Explorer** | `ms-vscode.remote-explorer` | Panneau listant les connexions WSL/SSH actives |

---

#### 🐍 Python & data — à installer dans WSL

| Extension | Identifiant | Rôle |
|---|---|---|
| **Python** | `ms-python.python` | IntelliSense, débogage, sélection d'environnement |
| **Pylance** | `ms-python.vscode-pylance` | Analyse statique avancée (auto-installé avec Python) |
| **Debugpy** | `ms-python.debugpy` | Débogueur Python (auto-installé avec Python) |
| **Python Envs** | `ms-python.vscode-python-envs` | Gestion des environnements virtuels (venv, conda) |
| **Jupyter** | `ms-toolsai.jupyter` | Notebooks `.ipynb` directement dans VS Code |
| **Ruff** | `charliermarsh.ruff` | Linter + formateur Python ultrarapide (remplace flake8/black) |

---

#### 📊 Git

| Extension | Identifiant | Rôle |
|---|---|---|
| **Git Graph** | `mhutchie.git-graph` | Visualisation graphique des branches et commits |

---

#### 📄 Utilitaires

| Extension | Identifiant | Rôle |
|---|---|---|
| **PDF Viewer** | `tomoki1207.pdf` | Prévisualisation des PDFs dans VS Code |
| **Dev Containers** | `ms-azuretools.vscode-containers` | Développement dans des conteneurs Docker |

---

#### 🤖 Intelligence artificielle (optionnel)

| Extension | Identifiant | Rôle |
|---|---|---|
| **GitHub Copilot Chat** | `github.copilot-chat` | Suggestions de code et chat IA (compte GitHub requis) |

---

#### Installation en une commande (depuis le terminal WSL dans VS Code)

Une fois connecté à WSL (étape 6), lancez cette commande dans le terminal intégré pour installer les extensions côté WSL :

```bash
code --install-extension ms-python.python \
     --install-extension ms-python.vscode-pylance \
     --install-extension ms-python.vscode-python-envs \
     --install-extension ms-toolsai.jupyter \
     --install-extension charliermarsh.ruff \
     --install-extension mhutchie.git-graph \
     --install-extension tomoki1207.pdf
```

> ⚠️ Cette commande installe les extensions **dans WSL**. Le bandeau `WSL: Ubuntu-24.04` doit être visible en bas à gauche de VS Code.

---

## Étape 6 — Ouvrir un dossier Linux dans VS Code

C'est l'étape clé : VS Code s'exécute sous **Windows** mais édite et exécute le code **dans** WSL.

### Option A — Depuis le terminal Ubuntu (recommandé)

Ouvrez Ubuntu (menu Démarrer → Ubuntu) et naviguez dans votre projet :

```bash
cd ~
mkdir mon_projet && cd mon_projet
code .
```

La commande `code .` ouvre VS Code **connecté à WSL** — vous verrez `[WSL: Ubuntu-24.04]` dans le coin inférieur gauche.

![VS Code connecté à WSL - bandeau vert en bas à gauche](Images/06_vscode_wsl_connected.png)

---

### Option B — Depuis VS Code (bouton Remote)

1. Cliquez sur le bouton **><** vert en bas à gauche de VS Code
2. Sélectionnez **Connect to WSL**
3. Puis **File → Open Folder** et naviguez dans `/home/votre_nom/`

![Bouton Remote WSL dans VS Code](Images/06_vscode_remote_button.png)

---

### Option C — Depuis l'explorateur Windows

Collez `\\wsl$\Ubuntu-24.04\home\votre_nom\` dans la barre d'adresse de l'Explorateur, puis clic droit → **Ouvrir avec Code**.

![Accès au système de fichiers WSL depuis l'explorateur](https://learn.microsoft.com/fr-fr/windows/wsl/media/windows-file-explorer.png)

> ⚠️ **Bonne pratique** : stockez toujours vos fichiers de projet **dans WSL** (`/home/...`), pas sur `C:\Users\...`. Les performances sont nettement meilleures pour les outils Linux.

---

## Étape 7 — Vérification finale

Dans le terminal intégré de VS Code (`Ctrl+ù` ou `Ctrl+backtick`), vérifiez que vous êtes bien dans WSL :

```bash
uname -a        # doit afficher Linux ... Microsoft
lsb_release -a  # doit afficher Ubuntu 24.04
pwd             # doit afficher /home/votre_nom/...
```

Résultat attendu :

```
Linux DESKTOP-XXXX 5.15.xxx-microsoft-standard-WSL2 ... GNU/Linux
Distributor ID: Ubuntu
Release:        24.04
Codename:       noble
```

![Terminal VS Code dans WSL montrant uname -a](Images/07_verification.png)

---

## Récapitulatif des commandes utiles

| Commande (PowerShell/CMD) | Description |
|---|---|
| `wsl --install -d Ubuntu-24.04` | Installer Ubuntu 24.04 |
| `wsl --list --verbose` | Lister les distributions et leur version WSL |
| `wsl --set-default Ubuntu-24.04` | Définir Ubuntu 24.04 comme distribution par défaut |
| `wsl --shutdown` | Arrêter toutes les distributions WSL |
| `wsl --update` | Mettre à jour le noyau WSL |

| Commande (dans Ubuntu) | Description |
|---|---|
| `code .` | Ouvrir le dossier courant dans VS Code (via WSL) |
| `explorer.exe .` | Ouvrir le dossier courant dans l'Explorateur Windows |
| `sudo apt update && sudo apt upgrade` | Mettre à jour Ubuntu |

---

## Résolution des problèmes courants

**`wsl --install` affiche l'aide WSL au lieu d'installer**  
→ WSL est déjà activé. Utilisez directement : `wsl --install -d Ubuntu-24.04`

**Erreur "Virtual Machine Platform not enabled"**  
→ Dans PowerShell administrateur : `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart` puis redémarrer.

**`code .` ne lance pas VS Code**  
→ VS Code n'est pas installé, ou il faut relancer Ubuntu après l'installation de VS Code.

**Le bandeau VS Code indique `WSL: Ubuntu` au lieu de `WSL: Ubuntu-24.04`**  
→ Normal si Ubuntu 24.04 est votre seule distribution. Tout fonctionne.

---

## Prochaine étape

Une fois WSL + VS Code installés, vous pouvez suivre le guide d'installation OpenFOAM :  
→ [`../MecaFlux/InstallOpenFoam/Install_OpenFoam2412.md`](../MecaFlux/InstallOpenFoam/Install_OpenFoam2412.md)
