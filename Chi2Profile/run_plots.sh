#!/bin/bash

# Load modules
module load python 

# Go to the directory of the script
cd "$(dirname "$0")"

SYSTEMATICS=("systematics" "no_systematics")
EXPERIMENT=("STD" "TAU")
ORDERING=("NO" "IO")
RECONSTRUCTION=("MC" "NNFit_full" "NNFit_dir" "AAFit_ann" "AAFit_dedx")

COUNTER=1
for SYS in "${SYSTEMATICS[@]}"; do
    for EXP in "${EXPERIMENT[@]}"; do
        for ORD in "${ORDERING[@]}"; do
            for REC in "${RECONSTRUCTION[@]}"; do
                echo -e "\n--------------------"
                echo -e "Run python script ${COUNTER} for $EXP $ORD $REC"
                python3 plot_chi_square.py --channel $EXP --ordering $ORD --reco $REC --systematic $SYS
                COUNTER=$((COUNTER+1))
            done
        done
    done
done