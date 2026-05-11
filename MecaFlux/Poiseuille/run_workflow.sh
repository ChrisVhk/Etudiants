#!/bin/bash
# ==============================================================================
# run_workflow.sh — Pipeline complet TP Poiseuille
#
# Étapes :
#   1. Nettoyage complet (cas, résultats, logs)
#   2. Génération des cas (master_setup_V2.sh)
#   3. Simulation     (run_all_cases_V2.sh)
#   4. Post-traitement (run_postproc.sh)
#
# Usage :
#   bash run_workflow.sh            # pipeline complet
#   bash run_workflow.sh --no-clean # skip l'étape nettoyage
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Couleurs ────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; BLUE='\033[0;34m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
BOLD='\033[1m'; NC='\033[0m'

step()    { echo -e "\n${BLUE}${BOLD}══════════════════════════════════════════════════${NC}"; \
            echo -e "${BLUE}${BOLD}  ÉTAPE $1 — $2${NC}"; \
            echo -e "${BLUE}${BOLD}══════════════════════════════════════════════════${NC}\n"; }
ok()      { echo -e "${GREEN}✅ $*${NC}"; }
info()    { echo -e "${YELLOW}ℹ  $*${NC}"; }
error()   { echo -e "${RED}❌ $*${NC}"; exit 1; }

# ── Options ──────────────────────────────────────────────────────────────────
DO_CLEAN=true
for arg in "$@"; do
    [[ "$arg" == "--no-clean" ]] && DO_CLEAN=false
done

START_TIME=$(date +%s)

echo -e "\n${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       TP POISEUILLE — WORKFLOW COMPLET           ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
[[ "$DO_CLEAN" == false ]] && info "Mode --no-clean : nettoyage désactivé"

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — NETTOYAGE
# ═══════════════════════════════════════════════════════════════════════════
if [[ "$DO_CLEAN" == true ]]; then
    step 1 "NETTOYAGE"

    info "Suppression des répertoires de cas..."
    for CASE in case0 case1 case2 case3 case4; do
        CASE_PATH="$SCRIPT_DIR/$CASE"
        if [[ -d "$CASE_PATH" ]]; then
            rm -rf "$CASE_PATH"
            info "  → $CASE supprimé"
        fi
    done

    info "Nettoyage des résultats..."
    rm -rf "$SCRIPT_DIR/Results/paraview_images"/*.png 2>/dev/null || true

    ok "Nettoyage complet"
else
    step 1 "NETTOYAGE (ignoré — --no-clean)"
    info "Nettoyage désactivé, les cas existants seront conservés."
fi

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — GÉNÉRATION DES CAS
# ═══════════════════════════════════════════════════════════════════════════
step 2 "GÉNÉRATION DES CAS"

[[ -f "$SCRIPT_DIR/master_setup_V2.sh" ]] || error "master_setup_V2.sh introuvable dans $SCRIPT_DIR"

cd "$SCRIPT_DIR"
bash master_setup_V2.sh || error "Échec de master_setup_V2.sh"
ok "Génération des cas terminée"

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 — SIMULATION
# ═══════════════════════════════════════════════════════════════════════════
step 3 "SIMULATION (blockMesh + solveurs)"

[[ -f "$SCRIPT_DIR/run_all_cases_V2.sh" ]] || error "run_all_cases_V2.sh introuvable dans $SCRIPT_DIR"

cd "$SCRIPT_DIR"
bash run_all_cases_V2.sh || error "Échec de run_all_cases_V2.sh"
ok "Simulations terminées"

# ═══════════════════════════════════════════════════════════════════════════
# ÉTAPE 4 — POST-TRAITEMENT
# ═══════════════════════════════════════════════════════════════════════════
step 4 "POST-TRAITEMENT"

[[ -f "$SCRIPT_DIR/run_postproc.sh" ]] || error "run_postproc.sh introuvable dans $SCRIPT_DIR"

cd "$SCRIPT_DIR"
bash run_postproc.sh || error "Échec de run_postproc.sh"

# ═══════════════════════════════════════════════════════════════════════════
# BILAN FINAL
# ═══════════════════════════════════════════════════════════════════════════
END_TIME=$(date +%s)
ELAPSED=$(( END_TIME - START_TIME ))
MINUTES=$(( ELAPSED / 60 ))
SECONDS=$(( ELAPSED % 60 ))

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║           WORKFLOW TERMINÉ AVEC SUCCÈS          ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
ok "Durée totale : ${MINUTES}m ${SECONDS}s"
echo ""
info "Pour visualiser dans ParaView :"
echo "    paraview --state=$SCRIPT_DIR/paraview_cases.pvsm"
echo ""
