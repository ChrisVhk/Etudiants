#!/bin/bash

################################################################################
#   01_setup.sh — Crée tous les cas (case0 à case5)                           #
#   TP Hagen-Poiseuille — OpenFOAM 2412                                       #
#   Appelé par : bash tp_poiseuille.sh 1  (ou directement)                    #
################################################################################

set -euo pipefail

GREEN='\033[0;32m'; BLUE='\033[0;34m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()  { echo -e "${GREEN}✅ $1${NC}"; }
err() { echo -e "${RED}❌ $1${NC}"; exit 1; }
hdr() { echo -e "\n${BLUE}========================================${NC}\n${BLUE}  $1${NC}\n${BLUE}========================================${NC}\n"; }
inf() { echo -e "${YELLOW}ℹ️  $1${NC}"; }

inf "Répertoire de travail : $(pwd)"

# ============================================================
# VÉRIFICATIONS
# ============================================================
hdr "VÉRIFICATIONS"
command -v blockMesh  &>/dev/null || err "OpenFOAM non trouvé. Source le bashrc OpenFOAM d'abord."
command -v icoFoam    &>/dev/null || err "icoFoam non trouvé."
command -v simpleFoam &>/dev/null || err "simpleFoam non trouvé."
command -v potentialFoam &>/dev/null || err "potentialFoam non trouvé."
ok "OpenFOAM trouvé"

# ============================================================
# CRÉATION STRUCTURE
# ============================================================
hdr "CRÉATION STRUCTURE"
for case in case0 case1 case2 case3; do
    rm -rf "$case"
    mkdir -p "$case"/{system,constant,0}
done
ok "Dossiers case0 à case3 créés"

# ============================================================
# FONCTION : écrire blockMeshDict (L et NX paramétrables)
# Usage : write_blockMeshDict <case> <L_m> <NX>
# ============================================================
write_blockMeshDict() {
    local CASE=$1
    local LVAL=${2:-10}
    local NX=${3:-100}
    cat > "$CASE/system/blockMeshDict" << EOF
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

convertToMeters 1;

vertices
(
    (0      -0.5  0)
    ($LVAL  -0.5  0)
    ($LVAL   0.5  0)
    (0       0.5  0)
    (0      -0.5  0.1)
    ($LVAL  -0.5  0.1)
    ($LVAL   0.5  0.1)
    (0       0.5  0.1)
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ($NX 10 1) simpleGrading (1 1 1)
);

edges ();

boundary
(
    inlet
    {
        type patch;
        faces ((0 4 7 3));
    }
    outlet
    {
        type patch;
        faces ((1 2 6 5));
    }
    top
    {
        type wall;
        faces ((3 7 6 2));
    }
    bottom
    {
        type wall;
        faces ((0 1 5 4));
    }
    front
    {
        type empty;
        faces ((0 3 2 1));
    }
    back
    {
        type empty;
        faces ((4 5 6 7));
    }
);

mergePatchPairs ();
EOF
}

# ============================================================
# FONCTION : écrire fvSchemes pour icoFoam (transient)
# ============================================================
write_fvSchemes_ico() {
    local CASE=$1
    cat > "$CASE/system/fvSchemes" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSchemes;
}

ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;
    div(phi,U)      Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}

fluxRequired
{
    default         no;
    p               ;
}
EOF
}

# ============================================================
# FONCTION : écrire fvSchemes pour simpleFoam (steady)
# ============================================================
write_fvSchemes_simple() {
    local CASE=$1
    cat > "$CASE/system/fvSchemes" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSchemes;
}

ddtSchemes
{
    default         steadyState;
}

gradSchemes
{
    default         Gauss linear;
    grad(U)         Gauss linear;
}

divSchemes
{
    default                           none;
    div(phi,U)                        Gauss linearUpwind grad(U);
    div((nuEff*dev2(T(grad(U)))))     Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear orthogonal;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         orthogonal;
}

fluxRequired
{
    default         no;
    p               ;
}
EOF
}

# ============================================================
# FONCTION : écrire fvSolution pour icoFoam (PISO)
# ============================================================
write_fvSolution_ico() {
    local CASE=$1
    cat > "$CASE/system/fvSolution" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSolution;
}

solvers
{
    p
    {
        solver          GAMG;
        smoother        GaussSeidel;
        tolerance       1e-7;
        relTol          0.01;
        nPreSweeps      0;
        nPostSweeps     2;
        nFinestSweeps   2;
        cacheAgglomeration on;
        agglomerator    faceAreaPair;
        nCellsInCoarsestLevel 10;
        mergeLevels     1;
    }

    pFinal
    {
        solver          GAMG;
        smoother        GaussSeidel;
        tolerance       1e-7;
        relTol          0;
        nPreSweeps      0;
        nPostSweeps     2;
        nFinestSweeps   2;
        cacheAgglomeration on;
        agglomerator    faceAreaPair;
        nCellsInCoarsestLevel 10;
        mergeLevels     1;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        nSweeps         1;
        tolerance       1e-8;
        relTol          0.1;
    }
}

PISO
{
    nCorrectors              2;
    nNonOrthogonalCorrectors 0;
}
EOF
}

# ============================================================
# FONCTION : écrire fvSolution pour simpleFoam (SIMPLE)
# ============================================================
write_fvSolution_simple() {
    local CASE=$1
    cat > "$CASE/system/fvSolution" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSolution;
}

solvers
{
    p
    {
        solver          GAMG;
        smoother        GaussSeidel;
        tolerance       1e-7;
        relTol          0.01;
        nPreSweeps      0;
        nPostSweeps     2;
        nFinestSweeps   2;
        cacheAgglomeration on;
        agglomerator    faceAreaPair;
        nCellsInCoarsestLevel 10;
        mergeLevels     1;
    }

    U
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        nSweeps         1;
        tolerance       1e-8;
        relTol          0.1;
    }
}

SIMPLE
{
    nNonOrthogonalCorrectors 0;
    residualControl
    {
        p               1e-4;
        U               1e-4;
    }
}

relaxationFactors
{
    fields    { p  0.3; }
    equations { U  0.7; }
}
EOF
}

# ============================================================
# FONCTION : écrire transportProperties (commun à tous)
# ============================================================
write_transportProperties() {
    local CASE=$1
    cat > "$CASE/constant/transportProperties" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}

transportModel  Newtonian;
nu              nu [0 2 -1 0 0 0 0] 0.001;
rho             rho [1 -3 0 0 0 0 0] 1000;
EOF
}

# ============================================================
# FONCTION : écrire turbulenceProperties (commun à tous)
# ============================================================
write_turbulenceProperties() {
    local CASE=$1
    cat > "$CASE/constant/turbulenceProperties" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      turbulenceProperties;
}

simulationType  laminar;
EOF
}

# ============================================================
# FONCTION : écrire 0/p (commun à tous)
# ============================================================
write_p() {
    local CASE=$1
    cat > "$CASE/0/p" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            zeroGradient;
    }
    outlet
    {
        type            fixedValue;
        value           uniform 0;
    }
    top
    {
        type            zeroGradient;
    }
    bottom
    {
        type            zeroGradient;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}
EOF
}

# ============================================================
# FONCTION : écrire 0/U avec vitesse paramétrable
# ============================================================
write_U() {
    local CASE=$1
    local VELOCITY=$2
    cat > "$CASE/0/U" << EOF
FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform ($VELOCITY 0 0);
    }
    outlet
    {
        type            zeroGradient;
    }
    top
    {
        type            noSlip;
    }
    bottom
    {
        type            noSlip;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}
EOF
}

# ============================================================
# CASE0 : icoFoam - 1.0 m/s (référence)
# ============================================================
hdr "CASE0 : icoFoam - 1.0 m/s (référence)"

write_blockMeshDict        case0  100  1000
write_fvSchemes_ico        case0
write_fvSolution_ico       case0
write_transportProperties  case0
write_turbulenceProperties case0
write_p                    case0
write_U                    case0  1.0

cat > "case0/system/controlDict" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     icoFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         200;
deltaT          0.05;
writeControl    timeStep;
writeInterval   400;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF
ok "case0 configuré (icoFoam, 1.0 m/s)"

# ============================================================
# CASE1 : icoFoam - 0.5 m/s
# ============================================================
hdr "CASE1 : icoFoam - 0.5 m/s"

write_blockMeshDict        case1  50   500
write_fvSchemes_ico        case1
write_fvSolution_ico       case1
write_transportProperties  case1
write_turbulenceProperties case1
write_p                    case1
write_U                    case1  0.5

cat > "case1/system/controlDict" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     icoFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         200;
deltaT          0.05;
writeControl    timeStep;
writeInterval   400;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF
ok "case1 configuré (icoFoam, 0.5 m/s)"

# ============================================================
# CASE2 : icoFoam - 1.5 m/s
# ============================================================
hdr "CASE2 : icoFoam - 1.5 m/s"

write_blockMeshDict        case2  150  1500
write_fvSchemes_ico        case2
write_fvSolution_ico       case2
write_transportProperties  case2
write_turbulenceProperties case2
write_p                    case2
write_U                    case2  1.5

cat > "case2/system/controlDict" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     icoFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         200;
deltaT          0.05;
writeControl    timeStep;
writeInterval   400;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF
ok "case2 configuré (icoFoam, 1.5 m/s)"

# ============================================================
# CASE3 : simpleFoam - 1.5 m/s (steady-state)
# ============================================================
hdr "CASE3 : simpleFoam - 1.5 m/s (steady-state)"

write_blockMeshDict        case3  150  1500
write_fvSchemes_simple     case3
write_fvSolution_simple    case3
write_transportProperties  case3
write_turbulenceProperties case3
write_p                    case3
write_U                    case3  1.5

cat > "case3/system/controlDict" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     simpleFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         2000;
deltaT          1;
writeControl    timeStep;
writeInterval   200;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF
ok "case3 configuré (simpleFoam, 1.5 m/s)"

# ============================================================
# CASE4 : potentialFoam - tuyau + slip (écoulement potentiel)
# ============================================================
hdr "CASE4 : potentialFoam - 1.0 m/s (slip)"

rm -rf case4
mkdir -p case4/{system,constant,0}

write_blockMeshDict        case4  10   100
write_transportProperties  case4
write_turbulenceProperties case4

# --- fvSchemes (Laplace, pas de dérivée temporelle) ---
cat > "case4/system/fvSchemes" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSchemes;
}

ddtSchemes
{
    default         none;
}

gradSchemes
{
    default         Gauss linear;
}

divSchemes
{
    default         none;
}

laplacianSchemes
{
    default         Gauss linear corrected;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         corrected;
}

fluxRequired
{
    default         no;
    p               ;
}
EOF

# --- fvSolution (GAMG pour Laplace) ---
cat > "case4/system/fvSolution" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      fvSolution;
}

solvers
{
    Phi
    {
        solver          GAMG;
        smoother        GaussSeidel;
        tolerance       1e-7;
        relTol          0.01;
        nPreSweeps      0;
        nPostSweeps     2;
        cacheAgglomeration on;
        agglomerator    faceAreaPair;
        nCellsInCoarsestLevel 10;
        mergeLevels     1;
    }
}

SIMPLE
{
    nNonOrthogonalCorrectors 2;
}
EOF

# --- controlDict (potentialFoam) ---
cat > "case4/system/controlDict" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      controlDict;
}

application     potentialFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         1;
deltaT          1;
writeControl    timeStep;
writeInterval   1;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF

# --- 0/p ---
cat > "case4/0/p" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}

dimensions      [0 2 -2 0 0 0 0];

internalField   uniform 0;

boundaryField
{
    inlet
    {
        type            zeroGradient;
    }
    outlet
    {
        type            fixedValue;
        value           uniform 0;
    }
    top
    {
        type            zeroGradient;
    }
    bottom
    {
        type            zeroGradient;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}
EOF

# --- 0/U avec slip sur les parois (potentiel = inviscide) ---
cat > "case4/0/U" << 'EOF'
FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}

dimensions      [0 1 -1 0 0 0 0];

internalField   uniform (1.0 0 0);

boundaryField
{
    inlet
    {
        type            fixedValue;
        value           uniform (1.0 0 0);
    }
    outlet
    {
        type            zeroGradient;
    }
    top
    {
        type            slip;
    }
    bottom
    {
        type            slip;
    }
    front
    {
        type            empty;
    }
    back
    {
        type            empty;
    }
}
EOF

ok "case4 configuré (potentialFoam, 1.0 m/s, slip)"


# ============================================================
# CASE 5 — icoFoam — Canal long L=200m — Re=1000
# But : montrer l'écoulement de Poiseuille PLEINEMENT ÉTABLI
# L_dev = 0.05 × Re × H = 0.05 × 1000 × 1 = 50 m → L = 4×L_dev
# ============================================================
hdr "CASE 5 — icoFoam (canal long L=200m, Re=1000 — Poiseuille pleinement établi)"
rm -rf case5
mkdir -p case5/{system,constant,0}

write_blockMeshDict  case5  200  2000

write_fvSchemes_ico   "case5"
write_fvSolution_ico  "case5"

cat > "case5/constant/transportProperties" << 'EOF'
FoamFile { version 2.0; format ascii; class dictionary; object transportProperties; }
transportModel  Newtonian;
nu              nu [ 0 2 -1 0 0 0 0 ] 0.001;
EOF

cat > "case5/constant/turbulenceProperties" << 'EOF'
FoamFile { version 2.0; format ascii; class dictionary; object turbulenceProperties; }
simulationType  laminar;
EOF

cat > "case5/system/controlDict" << 'EOF'
FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }
application     icoFoam;
startFrom       startTime;
startTime       0;
stopAt          endTime;
endTime         400;
deltaT          0.05;
writeControl    timeStep;
writeInterval   800;
purgeWrite      0;
writeFormat     ascii;
writePrecision  6;
writeCompression off;
timeFormat      general;
timePrecision   6;
runTimeModifiable true;
EOF

cat > "case5/0/p" << 'EOF'
FoamFile { version 2.0; format ascii; class volScalarField; object p; }
dimensions      [0 2 -2 0 0 0 0];
internalField   uniform 0;
boundaryField
{
    inlet   { type zeroGradient; }
    outlet  { type fixedValue; value uniform 0; }
    top     { type zeroGradient; }
    bottom  { type zeroGradient; }
    front   { type empty; }
    back    { type empty; }
}
EOF

cat > "case5/0/U" << 'EOF'
FoamFile { version 2.0; format ascii; class volVectorField; object U; }
dimensions      [0 1 -1 0 0 0 0];
internalField   uniform (1.0 0 0);
boundaryField
{
    inlet   { type fixedValue; value uniform (1.0 0 0); }
    outlet  { type zeroGradient; }
    top     { type noSlip; }
    bottom  { type noSlip; }
    front   { type empty; }
    back    { type empty; }
}
EOF

touch "case5/case5.foam"
ok "case5 configuré (icoFoam, L=200m, 1.0 m/s, noSlip, Re=1000 — Poiseuille pleinement établi, 4×L_dev)"


# ============================================================
# RÉSUMÉ FINAL
# ============================================================
hdr "RÉSUMÉ"
echo ""
echo "  case0 : icoFoam      | 1.0 m/s | L=100m  | transient  | noSlip  | endTime=200  (2×L_dev, Re=1000)"
echo "  case1 : icoFoam      | 0.5 m/s | L=50m   | transient  | noSlip  | endTime=200  (2×L_dev, Re=500)"
echo "  case2 : icoFoam      | 1.5 m/s | L=150m  | transient  | noSlip  | endTime=200  (2×L_dev, Re=1500)"
echo "  case3 : simpleFoam   | 1.5 m/s | L=150m  | steady     | noSlip  | endTime=2000 (2×L_dev, Re=1500)"
echo "  case4 : potentialFoam| 1.0 m/s | L=10m   | steady     | slip    | endTime=1"
echo "  case5 : icoFoam      | 1.0 m/s | L=200m  | transient  | noSlip  | endTime=400  (4×L_dev, Re=1000)"
echo "          → Poiseuille PLEINEMENT ÉTABLI — coupes à 25/50/75/100% du canal"
echo ""
ok "01_setup.sh terminé → lance : bash 02_run.sh"
