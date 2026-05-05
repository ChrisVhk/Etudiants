#!/bin/bash

################################################################################
#        WORKFLOW FINAL — Hagen-Poiseuille OpenFOAM 2412
#
#  Usage:
#    ./Workflow_final.sh          → menu interactif
#    ./Workflow_final.sh all      → toutes les étapes
#    ./Workflow_final.sh 0        → install dépendances (venv)
#    ./Workflow_final.sh 1        → master_setup_V2.sh
#    ./Workflow_final.sh 2        → run_all_cases_V2.sh
#    ./Workflow_final.sh 3        → analyze_results.py
#    ./Workflow_final.sh 4        → plot_results.py
#    ./Workflow_final.sh 5        → compare_cases.py
#    ./Workflow_final.sh 6        → extract_profile.py
#    ./Workflow_final.sh 7        → convergence_check.py
#    ./Workflow_final.sh 8        → ParaView
#    ./Workflow_final.sh 3-7      → étapes 3 à 7
#    ./Workflow_final.sh 1,2,5    → étapes 1, 2 et 5
################################################################################

################################################################################
#  Workflow_final.sh — Hagen-Poiseuille OpenFOAM 2412
#  Usage : ./Workflow_final.sh [0|1|2|3|4|5|6|7|8|all]
################################################################################

set -euo pipefail

# ── Couleurs ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() { echo -e "\n${CYAN}═══ $1 ═══${NC}"; }
print_ok()     { echo -e "${GREEN}✅ $1${NC}"; }
print_err()    { echo -e "${RED}❌ $1${NC}"; }
print_info()   { echo -e "${BLUE}ℹ️  $1${NC}"; }
print_warn()   { echo -e "${YELLOW}⚠️  $1${NC}"; }

# ── Chemins ───────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON="$VENV_DIR/bin/python3"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

# ── Étape 0 : venv + dépendances Python via apt ───────────────────────────────
step_0() {
    print_header "0 — Installation dépendances Python (venv)"

    # ── 1. Installer les paquets Python système via apt (bypass SSL PyPI) ──
    print_info "Installation des paquets Python via apt (bypass SSL réseau)..."
    sudo apt-get install -y \
        python3-numpy \
        python3-matplotlib \
        python3-scipy \
        python3-pandas \
        python3-venv \
        python3-pip \
        > /dev/null 2>&1
    print_ok "Paquets système installés via apt"

    # ── 2. Créer ou réparer le venv avec --system-site-packages ──────────
    if [ -d "$VENV_DIR" ] && [ ! -f "$PYTHON" ]; then
        print_info "venv incomplet détecté — suppression..."
        rm -rf "$VENV_DIR"
    fi

    if [ ! -d "$VENV_DIR" ]; then
        print_info "Création du venv (avec accès paquets système)..."
        python3 -m venv --system-site-packages "$VENV_DIR" || {
            print_err "Échec création venv"
            exit 1
        }
        print_ok "venv créé : $VENV_DIR"
    else
        # Vérifier que le venv existant a bien --system-site-packages
        if ! "$PYTHON" -c "import numpy" 2>/dev/null; then
            print_warn "venv existant sans accès système — recréation..."
            rm -rf "$VENV_DIR"
            python3 -m venv --system-site-packages "$VENV_DIR" || {
                print_err "Échec recréation venv"
                exit 1
            }
            print_ok "venv recréé : $VENV_DIR"
        else
            print_info "venv déjà existant et fonctionnel"
        fi
    fi

    # ── 3. Vérification réelle des imports ────────────────────────────────
    if "$PYTHON" -c "import numpy, matplotlib, scipy, pandas" 2>/dev/null; then
        print_ok "Dépendances vérifiées : numpy matplotlib scipy pandas"
    else
        print_err "Dépendances manquantes malgré l'installation apt"
        print_info "Diagnostic :"
        "$PYTHON" -c "import numpy" 2>&1 || true
        "$PYTHON" -c "import matplotlib" 2>&1 || true
        "$PYTHON" -c "import scipy" 2>&1 || true
        "$PYTHON" -c "import pandas" 2>&1 || true
        exit 1
    fi
}

# ── Étape 1 : Création des cas ─────────────────────────────────────────────────
step_1() {
    print_header "1 — Création des cas (master_setup_V2.sh)"
    print_info "Répertoire de travail : $SCRIPT_DIR"
    bash "$SCRIPT_DIR/master_setup_V2.sh" || {
        print_err "Échec master_setup_V2.sh"
        exit 1
    }
    print_ok "Cas créés"
}

# ── Étape 2 : Simulations OpenFOAM ────────────────────────────────────────────
step_2() {
    print_header "2 — Simulations OpenFOAM (run_all_cases_V2.sh)"
    bash "$SCRIPT_DIR/run_all_cases_V2.sh" || {
        print_err "Échec run_all_cases_V2.sh"
        exit 1
    }
    print_ok "Simulations terminées"
}

# ── Étape 3 : Analyse ─────────────────────────────────────────────────────────
step_3() {
    print_header "3 — Analyse des résultats"
    "$PYTHON" "$SCRIPTS_DIR/analyze_results.py" || {
        print_err "Échec analyze_results.py"
        exit 1
    }
    print_ok "Analyse OK"
}

# ── Étape 4 : Graphiques ──────────────────────────────────────────────────────
step_4() {
    print_header "4 — Graphiques"
    "$PYTHON" "$SCRIPTS_DIR/plot_results.py" || {
        print_err "Échec plot_results.py"
        exit 1
    }
    print_ok "Graphiques générés"
}

# ── Étape 5 : Comparaison ─────────────────────────────────────────────────────
step_5() {
    print_header "5 — Comparaison des cas"
    "$PYTHON" "$SCRIPTS_DIR/compare_cases.py" || {
        print_err "Échec compare_cases.py"
        exit 1
    }
    print_ok "Comparaison OK"
}

# ── Étape 6 : Profils de vitesse ──────────────────────────────────────────────
step_6() {
    print_header "6 — Profils de vitesse extraits"
    "$PYTHON" "$SCRIPTS_DIR/extract_profile.py" || {
        print_err "Échec extract_profile.py"
        exit 1
    }
    print_ok "Profils OK"
}

# ── Étape 7 : Convergence ─────────────────────────────────────────────────────
step_7() {
    print_header "7 — Vérification convergence"
    "$PYTHON" "$SCRIPTS_DIR/convergence_check.py" || {
        print_err "Échec convergence_check.py"
        exit 1
    }
    print_ok "Convergence OK"
}

# ── Étape 8 : ParaView ────────────────────────────────────────────────────────
step_8() {
    print_header "8 — Visualisation ParaView"
    local series_file="$SCRIPT_DIR/case0/VTK/case0.vtm.series"
    if command -v paraview &>/dev/null; then
        if [ -f "$series_file" ]; then
            paraview "$series_file" &
            print_ok "ParaView lancé (PID $!)"
        else
            print_warn "Fichier VTK introuvable : $series_file"
            print_info "Exécute d'abord l'étape 2 (run_all_cases_V2.sh)."
        fi
    else
        print_warn "ParaView non trouvé — installez avec : sudo apt install paraview"
    fi
}

# ── Dispatch ──────────────────────────────────────────────────────────────────
case "${1:-all}" in
    0)   step_0 ;;
    1)   step_1 ;;
    2)   step_2 ;;
    3)   step_3 ;;
    4)   step_4 ;;
    5)   step_5 ;;
    6)   step_6 ;;
    7)   step_7 ;;
    8)   step_8 ;;
    all)
        step_0
        step_1
        step_2
        step_3
        step_4
        step_5
        step_6
        step_7
        step_8
        echo -e "\n${GREEN}🎉 Workflow complet terminé avec succès !${NC}"
        ;;
    *)
        echo "Usage : $0 [0|1|2|3|4|5|6|7|8|all]"
        echo ""
        echo "  0   — Installation venv + dépendances Python (via apt)"
        echo "  1   — Création des cas OpenFOAM"
        echo "  2   — Simulations (blockMesh + solveurs + VTK)"
        echo "  3   — Analyse des résultats"
        echo "  4   — Génération des graphiques"
        echo "  5   — Comparaison des cas"
        echo "  6   — Extraction profils de vitesse"
        echo "  7   — Vérification convergence"
        echo "  8   — Lancement ParaView"
        echo "  all — Tout exécuter dans l'ordre"
        exit 1
        ;;
esac
