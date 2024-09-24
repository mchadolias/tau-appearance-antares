#!/bin/bash 

# Run multiple job scripts in parallel

# Usage: ./submit-all.sh 

# <DRY_RUN_FLAG> : 0 for submission to SLURM, 1 for frontend execution
# <SYSTEMATICS_FLAG> : 0 for no systematics, 1 for systematics
# <CHANNEL>   : "STD" or "TAU"
# <ORDERING>     : "NO" or "IO"
# <RECONSTRUCTION>: "MC" or "NNFit" or "AAFit"

CHANNEL=("STD")
ORDERING=("NO")
RECONSTRUCTION=("Smeared" "MC" "NNFit_full") 
SMEARING_LEVEL=("10" "50" "70" "100" "200" "500" "antares")
SYSTEMATICS=(0)
COUNTER=1

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo -e "--------------------\n"
for SYS in "${SYSTEMATICS[@]}"; do
    for CHAN in "${CHANNEL[@]}"; do
        for ORD in "${ORDERING[@]}"; do
            for REC in "${RECONSTRUCTION[@]}"; do

                if [[ "$REC" == "Smeared" ]]; then
                    for SMEAR in "${SMEARING_LEVEL[@]}"; do
                        echo -e "Submitting job number ${COUNTER} for $CHAN $ORD $REC $SMEAR"
                        ./submit.sh 0 ${SYS} $CHAN $ORD $REC "muon_free" $SMEAR
                        COUNTER=$((COUNTER+1))
                    done
                else
                    echo -e "Submitting job number ${COUNTER} for $CHAN $ORD $REC"
                    ./submit.sh 0 ${SYS} $CHAN $ORD $REC "muon_free" 0
                    COUNTER=$((COUNTER+1))
                fi
            done
        done
    done
done    