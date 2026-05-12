#!/usr/bin/env bash
# ==============================================================================
# 04_clean.sh — Nettoyage du TP Poiseuille
#
# Supprime tout ce qui est généré par tp_poiseuille.sh :
#   • case0/ à case5/          (créés par 01_setup.sh)
#   • Results/*.png, *.csv     (créés par 03_postprocess.sh)
#   • venv/                    (créé par tp_poiseuille.sh étape 0)
#   • scripts/__pycache__/     (créé par Python)
#
# Usage :
#   bash 04_clean.sh            # demande confirmation
#   bash 04_clean.sh --yes      # pas de confirmation
#   bash 04_clean.sh --dry-run  # affiche ce qui serait supprimé
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Couleurs ──────────────────────────────────────────────────────────────────
BLUE='\033[1;34m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${BLUE}[clean]${NC} $*"; }
ok()    { echo -e "${GREEN}  ✓${NC}  $*"; }
warn()  { echo -e "${YELLOW}  ⚠${NC}  $*"; }
err()   { echo -e "${RED}  ✗${NC}  $*" >&2; exit 1; }

# ── Options ───────────────────────────────────────────────────────────────────
DRY=false
YES=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY=true ;;
        --yes|-y)  YES=true ;;
        -h|--help)
            grep '^#' "$0" | head -20 | sed 's/^# \{0,2\}//'
            exit 0 ;;
        *) err "Option inconnue : $arg" ;;
    esac
done

# ── Inventaire de ce qui sera supprimé ────────────────────────────────────────
CASES=()
for i in 0 1 2 3 4 5; do
    [[ -d "$SCRIPT_DIR/case$i" ]] && CASES+=("case$i")
done

HAS_RESULTS=false
ls "$SCRIPT_DIR/Results/"*.png "$SCRIPT_DIR/Results/"*.csv &>/dev/null && HAS_RESULTS=true || true

HAS_VENV=false
[[ -d "$SCRIPT_DIR/venv" ]] && HAS_VENV=true

HAS_PYCACHE=false
[[ -d "$SCRIPT_DIR/scripts/__pycache__" ]] && HAS_PYCACHE=true

# ── Affichage du bilan ────────────────────────────────────────────────────────
echo ""
info "Éléments à supprimer :"
if [[ ${#CASES[@]} -gt 0 ]]; then
    echo "    Cas OpenFOAM : ${CASES[*]}"
else
    warn "Aucun répertoire case* trouvé"
fi
[[ "$HAS_RESULTS"  == true ]] && echo "    Résultats    : Results/*.png, Results/*.csv" || warn "Results/ — rien à supprimer"
[[ "$HAS_VENV"     == true ]] && echo "    Venv Python  : venv/" || warn "venv/ — introuvable"
[[ "$HAS_PYCACHE"  == true ]] && echo "    Cache Python : scripts/__pycache__/" || warn "__pycache__/ — introuvable"
echo ""

[[ "$DRY" == true ]] && { warn "Mode DRY-RUN — rien de supprimé"; exit 0; }

# ── Confirmation ──────────────────────────────────────────────────────────────
if [[ "$YES" == false ]]; then
    echo -e "${YELLOW}Confirmer la suppression ? [oui/NON]${NC} \c"
    read -r CONFIRM
    [[ "$CONFIRM" =~ ^[Oo][Uu][Ii]$ ]] || { info "Annulé."; exit 0; }
fi

# ── Suppression ───────────────────────────────────────────────────────────────
echo ""
info "Nettoyage en cours..."

# Cas OpenFOAM
for c in "${CASES[@]}"; do
    rm -rf "$SCRIPT_DIR/$c"
    ok "$c/ supprimé"
done

# Résultats post-traitement
if [[ "$HAS_RESULTS" == true ]]; then
    rm -f "$SCRIPT_DIR/Results/"*.png "$SCRIPT_DIR/Results/"*.csv
    ok "Results/*.png et *.csv supprimés"
fi

# Venv Python
if [[ "$HAS_VENV" == true ]]; then
    rm -rf "$SCRIPT_DIR/venv"
    ok "venv/ supprimé"
fi

# Cache Python
if [[ "$HAS_PYCACHE" == true ]]; then
    rm -rf "$SCRIPT_DIR/scripts/__pycache__"
    ok "scripts/__pycache__/ supprimé"
fi

echo ""
ok "Nettoyage terminé — prêt pour un nouveau run : bash tp_poiseuille.sh all"
