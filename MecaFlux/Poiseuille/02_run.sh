#!/bin/bash

################################################################################
#   02_run.sh — Exécute blockMesh + solveur + foamToVTK                       #
#   pour case0 à case5                                                        #
#   Appelé par : bash tp_poiseuille.sh 2  (ou directement)                    #
################################################################################

set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()  { echo -e "${GREEN}✅ $1${NC}"; }
err() { echo -e "${RED}❌ $1${NC}"; exit 1; }
hdr() { echo -e "\n${BLUE}========================================${NC}\n${BLUE}  $1${NC}\n${BLUE}========================================${NC}\n"; }
inf() { echo -e "${YELLOW}ℹ️  $1${NC}"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Tableau des solveurs par case
declare -A SOLVER
SOLVER[case0]="icoFoam"
SOLVER[case1]="icoFoam"
SOLVER[case2]="icoFoam"
SOLVER[case3]="simpleFoam"
SOLVER[case4]="potentialFoam"
SOLVER[case5]="icoFoam"   # Canal long L=100m — Poiseuille établi

# ============================================================
# VÉRIFICATIONS
# ============================================================
hdr "VÉRIFICATIONS"
for case in case0 case1 case2 case3 case4 case5; do
    [ -d "$SCRIPT_DIR/$case" ] || err "$case introuvable. Lance d'abord : bash 01_setup.sh"
done
ok "Tous les cases présents"

# ============================================================
# BOUCLE PRINCIPALE
# ============================================================
for case in case0 case1 case2 case3 case4 case5; do

    SOLVER_NAME="${SOLVER[$case]}"
    LOG="log.$SOLVER_NAME"

    hdr "TRAITEMENT : $case ($SOLVER_NAME)"
    cd "$SCRIPT_DIR/$case"

    # --- Nettoyage (timesteps uniquement, PAS le dossier 0/) ---
    inf "Nettoyage des anciens résultats..."
    find . -maxdepth 1 -type d -name '[1-9]*' -exec rm -rf {} + 2>/dev/null || true
    rm -rf postProcessing VTK "$LOG" 2>/dev/null || true
    ok "Nettoyage OK"

    # --- blockMesh ---
    inf "Génération du maillage (blockMesh)..."
    blockMesh > log.blockMesh 2>&1 \
        && ok "blockMesh OK" \
        || { echo ""; tail -10 log.blockMesh; err "blockMesh échoué → voir $case/log.blockMesh"; }

    # --- Solveur ---
    inf "Lancement $SOLVER_NAME..."
    $SOLVER_NAME > "$LOG" 2>&1 \
        && ok "$SOLVER_NAME OK" \
        || { echo ""; tail -15 "$LOG"; err "$SOLVER_NAME échoué → voir $case/$LOG"; }

    # --- Vérification FOAM exiting ---
    if grep -q "FOAM exiting" "$LOG" 2>/dev/null; then
        tail -15 "$LOG"
        err "FOAM exiting détecté dans $case/$LOG"
    fi

    # --- Compter les timesteps ---
    # potentialFoam écrit dans 0/ → vérifier 0/U, sinon compter dossiers
    if grep -q 'potentialFoam' system/controlDict 2>/dev/null; then
        [ -f '0/U' ] && N_STEPS=1 || N_STEPS=0
    else
        N_STEPS=$(find . -maxdepth 1 -type d -name '[1-9]*' | wc -l)
    fi
    ok "$N_STEPS timesteps créés"

    # --- foamToVTK ---
    inf "Conversion VTK..."
    foamToVTK > log.foamToVTK 2>&1 \
        && ok "foamToVTK OK" \
        || inf "foamToVTK échoué (non bloquant)"

    cd "$SCRIPT_DIR"

done

# ============================================================
# RÉSUMÉ FINAL
# ============================================================
hdr "RÉSUMÉ FINAL"
echo ""
printf "  %-8s %-12s %-8s %-10s %-8s\n" "Case" "Solveur" "Steps" "Log" "VTK"
printf "  %-8s %-12s %-8s %-10s %-8s\n" "--------" "------------" "--------" "----------" "--------"

for case in case0 case1 case2 case3 case4 case5; do
    SOLVER_NAME="${SOLVER[$case]}"
    LOG="$SCRIPT_DIR/$case/log.$SOLVER_NAME"
    if grep -q 'potentialFoam' "$SCRIPT_DIR/$case/system/controlDict" 2>/dev/null; then
        [ -f "$SCRIPT_DIR/$case/0/U" ] && N_STEPS=1 || N_STEPS=0
    else
        N_STEPS=$(find "$SCRIPT_DIR/$case" -maxdepth 1 -type d -name '[1-9]*' 2>/dev/null | wc -l)
    fi
    VTK_OK="❌"
    LOG_OK="❌"
    [ -d "$SCRIPT_DIR/$case/VTK" ] && VTK_OK="✅"
    [ -f "$LOG" ] && ! grep -q "FOAM exiting" "$LOG" && LOG_OK="✅"
    printf "  %-8s %-12s %-8s %-10s %-8s\n" "$case" "$SOLVER_NAME" "$N_STEPS" "$LOG_OK" "$VTK_OK"
done

echo ""
ok "02_run.sh terminé !"
