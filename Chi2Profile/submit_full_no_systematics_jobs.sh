#!/bin/bash 

# Run multiple job scripts in parallel

# Usage: ./submit-all.sh 

# <DRY_RUN_FLAG> : 0 for submission to SLURM, 1 for frontend execution
# <SYSTEMATICS_FLAG> : 0 for no systematics, 1 for systematics
# <CHANNEL>   : "STD" or "TAU"
# <ORDERING>     : "NO" or "IO"
# <RECONSTRUCTION>: "MC" or "NNFit" or "AAFit"

CHANNEL=("STD" "TAU")
ORDERING=("NO" "IO")
RECONSTRUCTION=("MC" "NNFit_full" "NNFit_dir" "AAFit_ann" "AAFit_dedx")
SYSTEMATICS=(0)
COUNTER=1
CUT=$1

if [ -z "$CUT" ]; then
    echo "Please provide the CUT option"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo -e "--------------------\n"
for SYS in "${SYSTEMATICS[@]}"; do
    for CHAN in "${CHANNEL[@]}"; do
        for ORD in "${ORDERING[@]}"; do
            for REC in "${RECONSTRUCTION[@]}"; do
                    echo -e "Submitting job number ${COUNTER} for $CHAN $ORD $REC"
                    ./submit.sh 0 ${SYS} $CHAN $ORD $REC $CUT 0 0 0
                    COUNTER=$((COUNTER+1))
            done
        done
    done
done    