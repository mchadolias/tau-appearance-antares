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
RECONSTRUCTION="Smeared"
SMEARING_LEVEL=("10" "50" "70" "100" "200" "500" "antares" "orca6" "orca115")
CUT=$1
SYSTEMATICS=("0")
COUNTER=1
ASSYMETRIC_FACTOR_DIR="1.0"

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
            for SMEAR in "${SMEARING_LEVEL[@]}"; do
                echo "SMEAR: $SMEAR"
                
                if [ "$SMEAR" == "antares" ] || [ "$SMEAR" == "orca6" ] || [ "$SMEAR" == "orca115" ]; then
                    ASSYMETRIC_FACTOR_ENERGY="1.0"
                else
                    ASSYMETRIC_FACTOR_ENERGY="3.0"
                fi

                echo -e "Submitting job number ${COUNTER} for $CHAN $ORD $RECONSTRUCTION $SMEAR"
                ./submit.sh 0 ${SYS} $CHAN $ORD $RECONSTRUCTION $CUT $SMEAR $ASSYMETRIC_FACTOR_DIR $ASSYMETRIC_FACTOR_ENERGY
                COUNTER=$((COUNTER+1))
            done
        done
    done
done  