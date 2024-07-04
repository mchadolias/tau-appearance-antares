#!/bin/bash
#
# Script to run the Chi2Profile code
#
# Usage: ./run_MC.sh [EXPERIMENT] [TYPE] [ORDERING]
#
# Author: Michael Chadolias

# Load modules
source $HOME/bash_scripts/init.sh
source $HOME/bash_scripts/swim_env.sh

# Go to the directory of the script
cd "$(dirname "$0")"

# Compile the code
make clean && make

# Check number of arguments 
if [ "$#" -ne 4 ]; then
    echo "Illegal number of parameters"
    echo "Usage: ./run.sh [EXPERIMENT] [TYPE] [ORDERING] [RECONSTRUCTION]"
    echo "EXPERIMENT: STD or TAU"
    echo "TYPE: Free or Fixed"
    echo "ORDERING: NO or IO"
    echo "RECONSTRUCTION: MC or NNFit or AAFit"
    exit
fi

BINNING="./json/ANTARES/binning_ANTARES.json"
EXPERIMENT=$1 # "STD" or "TAU"
TYPE=$2 # "free" or "fixed"
ORDERING=$3 # "NO" or "IO"
RECONSTRUCTION=$4 # "MC" or "NNFit" or "AAFit"

### Define all json files
# Define variables json file
if [ $EXPERIMENT == "STD" ]; then
    VARIABLES="./json/ANTARES/variables_ANTARES.json"
elif [ $EXPERIMENT == "TAU" ]; then
    VARIABLES="./json/ANTARES/variables_ANTARES_TAU.json"
else
    echo "EXPERIMENT type not recognized"
    exit
fi

# Define classes json file
if [ $RECONSTRUCTION == "MC" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_MC.json"
elif [ $RECONSTRUCTION == "NNFit" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_NNFit.json"
elif [ $RECONSTRUCTION == "AAFit" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_AAFit.json"
else
    echo "RECONSTRUCTION type not recognized"
    exit
fi

# Define parametes json file
if [[ $ORDERING == "NO" && $TYPE == "free" ]]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${TYPE}.json"
elif [[ $ORDERING == "NO" && $TYPE == "fixed" ]]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${TYPE}.json"
elif [[ $ORDERING == "IO" && $TYPE == "free" ]]; then
    PARAMS="./json/PARAMETERS/parameters_Data_IO_Model_${ORDERING}_${TYPE}.json"
elif [[ $ORDERING == "IO" && $TYPE == "fixed" ]]; then
    PARAMS="./json/PARAMETERS/parameters_Data_IO_Model_${ORDERING}_${TYPE}.json"
else
    echo "ORDERING or TYPE not recognized"
    exit
fi

# Define user json file
USER="./json/USER/User_${RECONSTRUCTION}_${EXPERIMENT}_${ORDERING}_${TYPE}.json"

## Run script
./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER

echo "============ Finished ============"