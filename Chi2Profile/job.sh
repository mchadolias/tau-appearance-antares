#!/bin/bash
#
# Job script to run the Chi2Profile code
#

### SLURM

#SBATCH --ntasks=1                    # Run a single task (by default tasks == CPU)
#SBATCH --mem=2G                      # GB
#SBATCH --time=01-00:00:00               #
#SBATCH --mail-user=mchadolias@km3net.de   # Where to send mail
#SBATCH --mail-type=FAIL,TIME_LIMIT              # Mail events (NONE, BEGIN, END, FAIL, ALL)

# Load modules
echo "Loading modules"
source $HOME/bash_scripts/init.sh
echo "Preparing SWIM environment"
source $HOME/bash_scripts/swim_env.sh

# Go to the directory of the script
cd $WORK/master_thesis/tau_appearance/Chi2Profile

# Compile the code
echo "Compiling the code"
make clean && make

echo "Starting script:" $(basename $BASH_SOURCE)
echo "EXPERIMENT: $EXPERIMENT"
echo "ORDERING: $ORDERING"
echo "RECONSTRUCTION: $RECONSTRUCTION"


### Define all json files

# Define binning json file
BINNING="./json/ANTARES/binning_ANTARES.json"
#BINNING="./json/ANTARES/binning_ANTARES_EffMass.json"

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
if [ $ORDERING == "NO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free.json"
elif [ $ORDERING == "IO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free.json"
else
    echo "ORDERING type not recognized"
    exit
fi

# Define user json file
USER="./json/USER/User_${RECONSTRUCTION}_${EXPERIMENT}_${ORDERING}_free.json"

## Run source-code

# --------------- Free ----------------
echo "Running MyChi2Profile with TauNorm parameter free"
echo "Parameters: $BINNING $CLASSES $VARIABLES $PARAMS $USER"
./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER


# --------------- Fixed ----------------
echo "Running MyChi2Profile with TauNorm parameter fixed"

# Define parametes json file
if [ $ORDERING == "NO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed.json"
elif [ $ORDERING == "IO" ]; then 
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed.json"
else
    echo "ORDERING or TYPE not recognized"
    exit
fi
# Define user json file
USER="./json/USER/User_${RECONSTRUCTION}_${EXPERIMENT}_${ORDERING}_fixed.json"

./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER

echo "============ Finished ============"