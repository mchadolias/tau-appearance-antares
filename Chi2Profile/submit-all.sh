#!/bin/bash 

# Run multiple job scripts in parallel

# Usage: ./submit-all.sh 

# <DRY_RUN_FLAG> : 0 for submission to SLURM, 1 for frontend execution
# <EXPERIMENT>   : "STD" or "TAU"
# <ORDERING>     : "NO" or "IO"
# <RECONSTRUCTION>: "MC" or "NNFit" or "AAFit"

EXPERIMENT=("STD" "TAU")
ORDERING=("NO" "IO")
RECONSTRUCTION=("MC" "NNFit" "AAFit")

for EXP in "${EXPERIMENT[@]}"; do
    for ORD in "${ORDERING[@]}"; do
        for REC in "${RECONSTRUCTION[@]}"; do
            echo "Submitting job for $EXP $ORD $REC"
            ./submit.sh 0 $EXP $ORD $REC
        done
    done
done