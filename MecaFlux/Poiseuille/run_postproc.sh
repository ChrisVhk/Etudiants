#!/bin/bash
# ==============================================================================
# run_postproc.sh — Post-traitement complet du TP Poiseuille
# Lance tous les scripts Python dans le bon ordre et vérifie les dépendances.
# Usage : bash run_postproc.sh
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS="$SCRIPT_DIR/scripts"
RESULTS="$SCRIPT_DIR/Results"

# ── Couleurs pour les messages ──────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC} $*"; }
warning() { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERREUR]${NC} $*"; }

# ── Vérifications préalables ────────────────────────────────────────────────
info "Vérification des prérequis..."

# Python3 disponible ?
if ! command -v python3 &>/dev/null; then
    error "python3 introuvable. Installez Python 3 et réessayez."
    exit 1
fi

# Modules Python requis ?
MISSING_MODULES=()
for mod in numpy matplotlib; do
    python3 -c "import $mod" 2>/dev/null || MISSING_MODULES+=("$mod")
done
if [[ ${#MISSING_MODULES[@]} -gt 0 ]]; then
    warning "Modules manquants : ${MISSING_MODULES[*]}"
    info "Installation via pip..."
    pip3 install --quiet "${MISSING_MODULES[@]}"
fi

# Au moins un cas simulé ?
HAS_RESULTS=false
for CASE in case0 case1 case2 case3 case4; do
    # chercher un répertoire de timestep > 0
    if find "$SCRIPT_DIR/$CASE" -mindepth 1 -maxdepth 1 -name "[1-9]*" -type d 2>/dev/null | grep -q .; then
        HAS_RESULTS=true
        break
    fi
done
if [[ "$HAS_RESULTS" == false ]]; then
    error "Aucun résultat de simulation trouvé."
    error "Lancez d'abord : bash master_setup_V2.sh && bash run_all_cases_V2.sh"
    exit 1
fi

mkdir -p "$RESULTS"

# ── Étape 1 — Analyse quantitative (Umax, ΔP vs. analytique) ───────────────
info "Étape 1/5 — Analyse quantitative (analyze_results.py)..."
python3 "$SCRIPTS/analyze_results.py" && info "  → OK" || warning "  → Erreur dans analyze_results.py (continue)"

# ── Étape 2 — Vérification de la convergence ────────────────────────────────
info "Étape 2/5 — Convergence des résidus (convergence_check.py)..."
python3 "$SCRIPTS/convergence_check.py" && info "  → OK" || warning "  → Erreur dans convergence_check.py (continue)"

# ── Étape 3 — Étude de stabilisation (cas transitoires) ─────────────────────
info "Étape 3/5 — Stabilisation temporelle (stabilization_study.py)..."
python3 "$SCRIPTS/stabilization_study.py" && info "  → OK" || warning "  → Erreur dans stabilization_study.py (continue)"

# ── Étape 4 — Profils de vitesse ────────────────────────────────────────────
info "Étape 4/5 — Profils de vitesse (plot_results.py)..."
python3 "$SCRIPTS/plot_results.py" && info "  → OK" || warning "  → Erreur dans plot_results.py (continue)"

# ── Étape 5 — Comparaison entre cas ─────────────────────────────────────────
info "Étape 5/5 — Comparaison des cas (compare_cases.py)..."
python3 "$SCRIPTS/compare_cases.py" && info "  → OK" || warning "  → Erreur dans compare_cases.py (continue)"

# ── Résumé ───────────────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════════════"
info "Post-traitement terminé. Résultats dans : $RESULTS/"
echo ""
echo "  Figures générées :"
find "$RESULTS" -name "*.png" -newer "$0" 2>/dev/null | sort | while read -r f; do
    echo "    $(basename "$f")"
done
echo ""
info "Étape suivante :"
echo "  paraview --state=$SCRIPT_DIR/paraview_cases.pvsm"
echo "══════════════════════════════════════════════════════════════"
