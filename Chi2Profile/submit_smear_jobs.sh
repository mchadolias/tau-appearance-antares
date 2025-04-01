#!/bin/bash 

# Run multiple job scripts in parallel

# Usage: ./submit_smear_jobs.sh <CUT>

# Set the parameters
# CUT=$1 # The cut option is passed as an argument

CHANNEL=("STD")
ORDERING=("NO")
RECONSTRUCTION="Smeared"
SMEARING_LEVEL=("10" "30" "50" "70" "90" "100" "antares" "orca6" "orca115")
CUT=$1
SYSTEMATICS=("1" "0")
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
                ./submit.sh 0 ${SYS} $CHAN $ORD $RECONSTRUCTION $CUT $SMEAR $ASSYMETRIC_FACTOR_DIR $ASSYMETRIC_FACTOR_ENERGY "ideal"
                COUNTER=$((COUNTER+1))
            done
        done
    done
done  