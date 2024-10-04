#!/bin/bash 

# Run multiple job scripts in parallel

CHANNEL="STD"
ORDERING="NO"
RECONSTRUCTION="Smeared"
SMEARING_LEVEL="antares"
CUT=$1
SYSTEMATICS="0"
COUNTER=1
ASSYMETRIC_FACTOR_DIR=("1.0" "0.9" "0.8" "0.7" "0.6" "0.5")
ASSYMETRIC_FACTOR_ENERGY=("1.0" "0.9" "0.8" "0.7" "0.6" "0.5")

if [ -z "$CUT" ]; then
    echo "Please provide the CUT option"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo -e "--------------------\n"

for DIR in "${ASSYMETRIC_FACTOR_DIR[@]}"; do
    for ENERGY in "${ASSYMETRIC_FACTOR_ENERGY[@]}"; do

        # Skip the job submission if the asymetric factor for both cases
        if [ "$DIR" == "1.0" ] && [ "$ENERGY" == "1.0" ]; then
            echo -e "Skipping job since this is the default case and already been submitted"
        else
            echo -e "Submitting job number ${COUNTER} for $CHANNEL $ORDERING $RECONSTRUCTION $SMEARING_LEVEL $DIR $ENERGY"
            #./submit.sh 0 $SYSTEMATICS $CHANNEL $ORDERING $RECONSTRUCTION $CUT $SMEARING_LEVEL $DIR $ENERGY
            COUNTER=$((COUNTER+1))
        fi
    done
done