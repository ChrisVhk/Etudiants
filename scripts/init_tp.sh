#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./scripts/init_tp.sh <tp_name> [--from <existing_tp_or_path>] [--force]

Examples:
  ./scripts/init_tp.sh TurbulenceIntro
  ./scripts/init_tp.sh Venturi --from Poiseuille
  ./scripts/init_tp.sh Canal2D --from /abs/path/to/template --force

Behavior:
  - Creates a new TP in MecaFlux/<tp_name>
  - If --from is provided, copies the source folder content
  - Otherwise creates an empty TP skeleton with case0..case4
EOF
}

TP_NAME=""
FROM_SOURCE=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)
      shift
      [[ $# -gt 0 ]] || { echo "Error: --from requires a value"; exit 1; }
      FROM_SOURCE="$1"
      ;;
    --force)
      FORCE=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Error: unknown option: $1"
      usage
      exit 1
      ;;
    *)
      if [[ -z "$TP_NAME" ]]; then
        TP_NAME="$1"
      else
        echo "Error: too many positional arguments"
        usage
        exit 1
      fi
      ;;
  esac
  shift
done

if [[ -z "$TP_NAME" ]]; then
  usage
  exit 1
fi

if [[ "$TP_NAME" == *"/"* ]]; then
  echo "Error: tp_name must not contain '/'"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MECAFLUX_DIR="$REPO_ROOT/MecaFlux"
TARGET_DIR="$MECAFLUX_DIR/$TP_NAME"

mkdir -p "$MECAFLUX_DIR"

if [[ -e "$TARGET_DIR" && "$FORCE" != true ]]; then
  echo "Error: target already exists: $TARGET_DIR"
  echo "Use --force to overwrite it."
  exit 1
fi

if [[ "$FORCE" == true ]]; then
  rm -rf "$TARGET_DIR"
fi

if [[ -n "$FROM_SOURCE" ]]; then
  if [[ -d "$FROM_SOURCE" ]]; then
    SOURCE_DIR="$FROM_SOURCE"
  elif [[ -d "$MECAFLUX_DIR/$FROM_SOURCE" ]]; then
    SOURCE_DIR="$MECAFLUX_DIR/$FROM_SOURCE"
  else
    echo "Error: source not found: $FROM_SOURCE"
    exit 1
  fi

  mkdir -p "$TARGET_DIR"
  cp -a "$SOURCE_DIR/." "$TARGET_DIR/"
  echo "TP created from template: $TARGET_DIR"
else
  mkdir -p "$TARGET_DIR/Enonce" "$TARGET_DIR/scripts" "$TARGET_DIR/Results"

  for c in 0 1 2 3 4; do
    mkdir -p "$TARGET_DIR/case$c/0" "$TARGET_DIR/case$c/constant" "$TARGET_DIR/case$c/system"
  done

  cat > "$TARGET_DIR/README.md" <<EOF
# $TP_NAME

Nouveau TP MecaFlux initialise automatiquement.

## Structure creee
- Enonce
- scripts
- Results
- case0..case4 (0, constant, system)

## Etapes suivantes
1. Ajouter les fichiers OpenFOAM dans chaque case (0, constant, system)
2. Ajouter les scripts de lancement dans scripts
3. Documenter les consignes dans Enonce
EOF

  cat > "$TARGET_DIR/scripts/run_all_cases.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "TODO: implement run sequence for case0..case4"
EOF

  chmod +x "$TARGET_DIR/scripts/run_all_cases.sh"
  echo "Empty TP skeleton created: $TARGET_DIR"
fi

# Ensure helper script stays executable if copied from template or recreated.
if [[ -f "$TARGET_DIR/scripts/run_all_cases.sh" ]]; then
  chmod +x "$TARGET_DIR/scripts/run_all_cases.sh"
fi

echo "Done."
