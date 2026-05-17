#!/usr/bin/env bash
# ============================================================
# install_python_deps.sh
# Installe les dépendances Python pour le post-traitement
# (numpy, matplotlib, scipy, pandas, reportlab)
#
# Usage :
#   bash install_python_deps.sh          # installation standard
#   bash install_python_deps.sh --check  # vérification uniquement
# ============================================================
set -euo pipefail

# ── Couleurs ──────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'
BLUE='\033[1;34m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC}  $*"; }
warn() { echo -e "${YELLOW}  ⚠${NC}  $*"; }
err()  { echo -e "${RED}  ✗${NC}  $*" >&2; exit 1; }
info() { echo -e "${BLUE}[deps]${NC} $*"; }

# ── Mode ──────────────────────────────────────────────────────────
CHECK_ONLY=false
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=true

# ── Vérifier Python 3 ─────────────────────────────────────────────
PY="$(command -v python3 2>/dev/null || true)"
[[ -n "$PY" ]] || err "python3 introuvable — installez Python 3 d'abord : sudo apt install python3"
PY_VERSION="$("$PY" --version 2>&1)"
ok "Python trouvé : $PY_VERSION"

PIP="$(command -v pip3 2>/dev/null || true)"
[[ -n "$PIP" ]] || err "pip3 introuvable — installez pip : sudo apt install python3-pip"

echo ""

# ── Paquets à installer ───────────────────────────────────────────
# Format : "nom_pip|version_min|paquet_apt"
# paquet_apt = "" si non disponible via apt
PACKAGES=(
    "numpy|1.24|python3-numpy"
    "matplotlib|3.5|python3-matplotlib"
    "scipy|1.10|python3-scipy"
    "pandas|2.0|python3-pandas"
    "reportlab|3.6|"
)

# ── Fonction de vérification d'un paquet ─────────────────────────
check_package() {
    local pkg="$1"
    local version
    version="$("$PY" -c "import $pkg; print(getattr($pkg, '__version__', getattr($pkg, 'Version', '?')))" 2>/dev/null || echo "")"
    if [[ -n "$version" ]]; then
        ok "$pkg : $version"
        return 0
    else
        warn "$pkg : non installé"
        return 1
    fi
}

# ── Mode vérification seule ───────────────────────────────────────
if [[ "$CHECK_ONLY" == true ]]; then
    info "Vérification des dépendances Python..."
    echo ""
    MISSING=0
    for entry in "${PACKAGES[@]}"; do
        pkg="${entry%%|*}"
        check_package "$pkg" || MISSING=$((MISSING + 1))
    done
    echo ""
    if [[ "$MISSING" -eq 0 ]]; then
        ok "Toutes les dépendances sont installées."
    else
        warn "$MISSING dépendance(s) manquante(s) — lancez : bash install_python_deps.sh"
        exit 1
    fi
    exit 0
fi

# ── Installation ──────────────────────────────────────────────────
info "Installation des dépendances Python (post-traitement)..."
echo ""

ERRORS=0
for entry in "${PACKAGES[@]}"; do
    pkg="${entry%%|*}"
    rest="${entry#*|}"
    ver_min="${rest%%|*}"
    apt_pkg="${rest##*|}"

    info "── $pkg (>= $ver_min) ──"

    # Vérifier si déjà installé
    current="$("$PY" -c "import $pkg; print(getattr($pkg, '__version__', getattr($pkg, 'Version', '?')))" 2>/dev/null || echo "")"
    if [[ -n "$current" ]]; then
        ok "Déjà installé : $pkg $current"
        echo ""
        continue
    fi

    # Essayer apt d'abord (si disponible)
    if [[ -n "$apt_pkg" ]]; then
        info "Tentative via apt : $apt_pkg"
        if sudo apt-get install -y "$apt_pkg" > /dev/null 2>&1; then
            ver="$("$PY" -c "import $pkg; print(getattr($pkg, '__version__', '?'))" 2>/dev/null || echo "?")"
            ok "Installé via apt : $pkg $ver"
            echo ""
            continue
        else
            warn "apt échoué — tentative via pip..."
        fi
    fi

    # Fallback : pip
    info "Installation via pip : $pkg>=$ver_min"
    # Utiliser --break-system-packages pour Ubuntu 24.04 (PEP 668)
    if "$PIP" install --quiet "$pkg>=$ver_min" 2>/dev/null \
       || "$PIP" install --quiet --break-system-packages "$pkg>=$ver_min" 2>/dev/null; then
        ver="$("$PY" -c "import $pkg; print(getattr($pkg, '__version__', getattr($pkg, 'Version', '?')))" 2>/dev/null || echo "?")"
        ok "Installé via pip : $pkg $ver"
    else
        err_msg="Échec d'installation : $pkg"
        warn "$err_msg"
        ERRORS=$((ERRORS + 1))
    fi
    echo ""
done

# ── Bilan ─────────────────────────────────────────────────────────
echo "────────────────────────────────────────"
if [[ "$ERRORS" -eq 0 ]]; then
    ok "Toutes les dépendances sont installées."
else
    warn "$ERRORS paquet(s) en erreur — vérifiez les messages ci-dessus."
fi
echo "────────────────────────────────────────"
echo ""
info "Vérification finale :"
echo ""
"$PY" -c "
import numpy as np
import matplotlib
import scipy
import pandas as pd
import reportlab
print('  numpy      :', np.__version__)
print('  matplotlib :', matplotlib.__version__)
print('  scipy      :', scipy.__version__)
print('  pandas     :', pd.__version__)
print('  reportlab  :', reportlab.Version)
" 2>/dev/null && ok "Toutes les bibliothèques importables." || warn "Certains imports ont échoué."
