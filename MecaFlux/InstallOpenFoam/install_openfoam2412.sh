#!/usr/bin/env bash
# install_openfoam2412.sh — Installation OpenFOAM 2412 + ParaView (Ubuntu 22/24)
# Usage : bash install_openfoam2412.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

# ── Couleurs ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

ok()   { echo -e "${GREEN}  ✓${NC}  $*"; }
err()  { echo -e "${RED}  ✗  $*${NC}" >&2; exit 1; }
warn() { echo -e "${YELLOW}  ⚠${NC}  $*"; }
info() { echo -e "${BLUE}[install]${NC} $*"; }
step() { echo -e "\n${BOLD}── $* ──${NC}"; }

# ── Prérequis système ─────────────────────────────────────────────────────────
step "Vérification du système"

[[ "$(id -u)" -eq 0 ]] && err "Ne pas lancer en root. Utiliser un utilisateur normal avec sudo."

if ! command -v lsb_release &>/dev/null; then
    err "lsb_release introuvable. Ce script nécessite Ubuntu 22.04 ou 24.04."
fi

DISTRIB="$(lsb_release -is)"
CODENAME="$(lsb_release -cs)"
[[ "$DISTRIB" == "Ubuntu" ]] || err "Système détecté : $DISTRIB. Ce script est prévu pour Ubuntu."

case "$CODENAME" in
    jammy|noble) ok "Ubuntu $CODENAME ($DISTRIB) — compatible" ;;
    *) warn "Ubuntu $CODENAME non testé — le script continue mais des erreurs sont possibles." ;;
esac

# ── Étape 1 : Dépôt OpenFOAM ─────────────────────────────────────────────────
step "1/5 — Dépôt OpenFOAM (openfoam.com)"

REPO_FILE="/etc/apt/sources.list.d/openfoam.list"
REPO_URL="https://dl.openfoam.com"

if [[ -f "$REPO_FILE" ]] || grep -rqs "openfoam.com" /etc/apt/sources.list.d/ 2>/dev/null; then
    ok "Dépôt OpenFOAM déjà configuré — étape ignorée"
else
    info "Ajout du dépôt OpenFOAM..."
    if ! wget -q --spider "$REPO_URL" 2>/dev/null; then
        err "Impossible de joindre $REPO_URL — vérifiez votre connexion Internet."
    fi
    wget -q -O - "$REPO_URL/add-debian-repo.sh" | sudo bash
    ok "Dépôt ajouté"
fi

# ── Étape 2 : Mise à jour apt ─────────────────────────────────────────────────
step "2/5 — Mise à jour des paquets (apt update)"

info "Cela peut prendre 1–2 minutes..."
sudo apt-get update -qq
ok "Index apt à jour"

# ── Étape 3 : OpenFOAM 2412 ───────────────────────────────────────────────────
step "3/5 — Installation OpenFOAM 2412"

OF_BASHRC="/usr/lib/openfoam/openfoam2412/etc/bashrc"

if [[ -f "$OF_BASHRC" ]]; then
    ok "openfoam2412 déjà installé — étape ignorée"
else
    if ! apt-cache show openfoam2412-default &>/dev/null; then
        err "Paquet openfoam2412-default introuvable. Vérifiez que le dépôt a bien été ajouté (étape 1)."
    fi
    info "Installation openfoam2412-default (plusieurs centaines de Mo)..."
    sudo apt-get install -y openfoam2412-default
    ok "openfoam2412 installé"
fi

# ── Étape 4 : ParaView ────────────────────────────────────────────────────────
step "4/5 — Installation ParaView"

# Note : paraviewopenfoam2412-default n'est plus disponible dans les dépôts
# depuis 2025. On utilise le ParaView Ubuntu standard, compatible avec les
# fichiers OpenFOAM via le reader .foam / foamToVTK.
if command -v paraview &>/dev/null; then
    PV_VER="$(paraview --version 2>/dev/null | head -1 || echo 'version inconnue')"
    ok "ParaView déjà installé : $PV_VER"
else
    info "Installation paraview..."
    sudo apt-get install -y paraview
    ok "ParaView installé"
fi

# ── Étape 5 : Environnement ~/.bashrc ─────────────────────────────────────────
step "5/5 — Configuration de l'environnement shell"

SOURCE_LINE="source $OF_BASHRC"

if grep -qF "openfoam2412" "$HOME/.bashrc" 2>/dev/null; then
    ok ".bashrc déjà configuré — étape ignorée"
else
    echo "" >> "$HOME/.bashrc"
    echo "# OpenFOAM 2412" >> "$HOME/.bashrc"
    echo "$SOURCE_LINE" >> "$HOME/.bashrc"
    ok ".bashrc mis à jour"
fi

# ── Validation ────────────────────────────────────────────────────────────────
step "Validation de l'installation"

# Charger l'environnement pour les tests
# set -euo pipefail est suspendu : le bashrc OpenFOAM génère une erreur
# pop_var_context dans un sous-shell non-interactif (comportement connu, bénin)
set +euo pipefail
# shellcheck source=/dev/null
source "$OF_BASHRC" 2>/dev/null || true
set -euo pipefail

ERRORS=0

# foamVersion est une fonction shell (pas un binaire) — vérifier via le bashrc
OF_VERSION="$(bash --norc -c "source '$OF_BASHRC' 2>/dev/null; foamVersion 2>/dev/null" || true)"
if [[ -n "$OF_VERSION" ]]; then
    ok "foamVersion : $OF_VERSION"
else
    # Fallback : lire la version depuis le chemin du bashrc
    OF_VER_FALLBACK="$(basename "$(dirname "$(dirname "$OF_BASHRC")")")" 
    ok "OpenFOAM installé : $OF_VER_FALLBACK (foamVersion disponible après 'exec bash')"
fi

for CMD in blockMesh simpleFoam icoFoam foamToVTK; do
    if command -v "$CMD" &>/dev/null; then
        ok "$CMD trouvable"
    else
        warn "$CMD introuvable"
        ERRORS=$((ERRORS + 1))
    fi
done

if foamInstallationTest &>/dev/null; then
    ok "foamInstallationTest : OK"
else
    warn "foamInstallationTest a signalé des avertissements — cf. détails ci-dessous :"
    foamInstallationTest 2>&1 | grep -E "(ERROR|WARN|Critical|ok)" | head -10 || true
fi

# ── Bilan ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "────────────────────────────────────────"
if [[ "$ERRORS" -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}  Installation terminée avec succès.${NC}"
else
    echo -e "${YELLOW}${BOLD}  Installation terminée avec $ERRORS avertissement(s).${NC}"
fi
echo -e "────────────────────────────────────────"
echo ""
echo -e "  ${BOLD}Prochaines étapes :${NC}"
echo -e "  1. Ouvrir un ${BOLD}nouveau terminal${NC} (ou relancer bash : ${BOLD}exec bash${NC})"
echo -e "  2. Vérifier avec : ${BOLD}foamVersion${NC}"
echo -e "  3. Lancer le TP  : ${BOLD}cd MecaFlux/Poiseuille && bash tp_poiseuille.sh all${NC}"
echo ""
