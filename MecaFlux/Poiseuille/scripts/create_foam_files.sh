#!/usr/bin/env bash
set -euo pipefail

# Resolve Poiseuille root from the script location so it works from any cwd.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POISEUILLE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Cree un fichier .foam dans chaque cas (si non deja present)
for c in case0 case1 case2 case3 case4; do
  touch "$POISEUILLE_DIR/$c/$c.foam"
done

echo "Fichiers .foam verifies/crees pour case0..case4 dans: $POISEUILLE_DIR"
