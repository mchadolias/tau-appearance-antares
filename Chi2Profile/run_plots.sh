#!/bin/bash

# Load modules
module load python 

# Go to the directory of the script
cd "$(dirname "$0")"

EXPERIMENT=("STD" "TAU")
ORDERING=("NO" "IO")
RECONSTRUCTION=("MC" "NNFit" "AAFit")

COUNTER=1
for EXP in "${EXPERIMENT[@]}"; do
    for ORD in "${ORDERING[@]}"; do
        for REC in "${RECONSTRUCTION[@]}"; do
            echo -e "\n--------------------"
            echo -e "Run python script ${COUNTER} for $EXP $ORD $REC"
            python3 plot_chi_square.py --probe $EXP --ordering $ORD --reco $REC
            COUNTER=$((COUNTER+1))
        done
    done
done