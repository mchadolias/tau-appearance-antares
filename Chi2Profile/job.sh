#!/bin/bash
#
# Job script to run the Chi2Profile code
#

### SLURM

#SBATCH --ntasks=1                    # Run a single task (by default tasks == CPU)
#SBATCH --mem=3G                      # GB
#SBATCH --time=01-00:00:00               #
#SBATCH --mail-user=mchadolias@km3net.de   # Where to send mail
#SBATCH --mail-type=FAIL,TIME_LIMIT              # Mail events (NONE, BEGIN, END, FAIL, ALL)

echo "Starting script:" $(basename $BASH_SOURCE)
echo "CHANNEL: $CHANNEL"
echo "ORDERING: $ORDERING"
echo "RECONSTRUCTION: $RECONSTRUCTION"
echo "SYSTEMATICS: $SYSTEMATICS"
echo "CUT: $CUT"
echo "SMEARING_LEVEL: $SMEARING_LEVEL"

if [ $SYSTEMATICS == "0" ]; then
    SYSTEMATICS="no_systematics"
    echo "SYSTEMATICS: $SYSTEMATICS"
else
    SYSTEMATICS="systematics"
fi
echo -e "============================== \n"

# Go to the directory of the script
cd $WORK/master_thesis/tau_appearance/
ROOT_PATH=$WORK/Swim/Data/events/ANTARES

if [ $DRY_RUN == "0" ]; then
    module load python
fi

# Create json files
echo -e "\nCreating json files"
echo "=============================="
cd ./Chi2Profile

python3 create_json_file.py  \
        --channel $CHANNEL  \
        --order $ORDERING  \
        --reco $RECONSTRUCTION \
        --cut $CUT \
        --systematics $SYSTEMATICS \
        --smear_level $SMEARING_LEVEL 

echo -e "\nCreating output directories"
python3 create_directories.py --cut $CUT


# Load modules
echo -e "\nLoading modules"
echo "=============================="
echo "Preparing SWIM environment"
source $HOME/bash_scripts/swim_env.sh

# Return to the main directory
cd $WORK/master_thesis/tau_appearance/

# Check if the ROOT file exists
echo -e "\nChecking if the ROOT file exists"
echo "=============================="
if [ $RECONSTRUCTION == "Smeared" ]; then
    if [ -f "$ROOT_PATH/antares_w_nnfit_FINAL1_smeared_${SMEARING_LEVEL}.root" ]; then
        echo "ROOT file: antares_w_nnfit_FINAL1_smeared_${SMEARING_LEVEL}.root already exists"
    else
        echo "ROOT file does not exist, running Smearing code"
        echo "SMEARING_LEVEL: $SMEARING_LEVEL"

        INPUT_FILE="$ROOT_PATH/antares_w_nnfit_FINAL1.root"
        OUTPUT_FILE="$ROOT_PATH/antares_w_nnfit_FINAL1_smeared_${SMEARING_LEVEL}.root"

        if [ $SMEARING_LEVEL == "antares" ]; then
            RESOLUTION_FLAG="Y"
        else
            RESOLUTION_FLAG="N"
        fi

        ./Smearing/bin/Smearing $INPUT_FILE $OUTPUT_FILE $SMEARING_LEVEL $RESOLUTION_FLAG

        echo "ROOT file: antares_w_nnfit_FINAL1_smeared_${SMEARING_LEVEL}.root created"
        echo "Add CAN to the root file"
        ./Smearing/bin/addCanANTARES $OUTPUT_FILE
    fi
else 
    echo "ROOT file: antares_w_nnfit_FINAL1.root already exists"
fi 

### Define all json files
cd ./Chi2Profile

# Define binning json file
BINNING="./json/ANTARES/binning_ANTARES_16.json"

# Define variables json file
if [ $RECONSTRUCTION == "Smeared" ]; then
    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${SMEARING_LEVEL}_${CHANNEL}_${ORDERING}_${CUT}_${SYSTEMATICS}_free.json"

    if [ $CHANNEL == "STD" ]; then
        VARIABLES="./json/ANTARES/variables_ANTARES_STD_Smear_${SMEARING_LEVEL}.json"
    elif [ $CHANNEL == "TAU" ]; then
        VARIABLES="./json/ANTARES/variables_ANTARES_TAU_Smear_${SMEARING_LEVEL}.json"
    else
        echo "CHANNEL type not recognized"
        exit
    fi
else
    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_${CUT}_${SYSTEMATICS}_free.json"

    if [ $CHANNEL == "STD" ]; then
        VARIABLES="./json/ANTARES/variables_ANTARES_STD.json"
    elif [ $CHANNEL == "TAU" ]; then
        VARIABLES="./json/ANTARES/variables_ANTARES_TAU.json"
    else
        echo "CHANNEL type not recognized"
        exit
    fi
fi

# Define classes json file
if [ $RECONSTRUCTION == "MC" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_MC.json"
elif [ $RECONSTRUCTION == "NNFit_full" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_NNFit_full.json"
elif [ $RECONSTRUCTION == "NNFit_dir" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_NNFit_dir.json"
elif [ $RECONSTRUCTION == "AAFit_ann" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_AAFit_ann.json"
elif [ $RECONSTRUCTION == "AAFit_dedx" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_AAFit_dedx.json"
elif [ $RECONSTRUCTION == "Smeared" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_${CUT}_Smeared.json"
else
    echo "RECONSTRUCTION type not recognized"
    exit
fi

# Define parameters json file
if [ $ORDERING == "NO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${SYSTEMATICS}_free.json"
elif [ $ORDERING == "IO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${SYSTEMATICS}_free.json"
else
    echo "ORDERING type not recognized"
    exit
fi

## Check if the json files exist
if [ ! -f $BINNING ] || [ ! -f $VARIABLES ] || [ ! -f $CLASSES ] || [ ! -f $PARAMS ] || [ ! -f $USER ]; then
    echo -e "\nOne or more json files do not exist"
    echo "BINNING: $BINNING"
    echo "VARIABLES: $VARIABLES"
    echo "CLASSES: $CLASSES"
    echo "PARAMS: $PARAMS"
    echo "USER: $USER"
    exit
fi

## Run source-code
# --------------- Free ----------------
echo -e "\nRunning MyChi2Profile with TauNorm parameter free"
echo "=============================="
echo "===> Freeing TauNorm parameter"
echo "Parameters:"
echo "BINNING: $BINNING"
echo "VARIABLES: $VARIABLES"
echo "CLASSES: $CLASSES"
echo "PARAMS: $PARAMS"
echo -e "USER: $USER \n"

./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER


# --------------- Fixed ----------------
echo -e "\nRunning MyChi2Profile with TauNorm parameter fixed"
echo "=============================="
echo "===> Fixing TauNorm parameter"

# Change parameters json file
if [ $ORDERING == "NO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${SYSTEMATICS}_fixed.json"
elif [ $ORDERING == "IO" ]; then
    PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_${SYSTEMATICS}_fixed.json"
else
    echo "ORDERING type not recognized"
    exit
fi

# Change user json file
if [ $RECONSTRUCTION == "Smeared" ]; then
    USER="./json/USER/User_${RECONSTRUCTION}_${SMEARING_LEVEL}_${CHANNEL}_${ORDERING}_${CUT}_${SYSTEMATICS}_fixed.json"
else
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_${CUT}_${SYSTEMATICS}_fixed.json"
fi

## Check if the json files exist
if [ ! -f $PARAMS ] || [ ! -f $USER ]; then
    echo -e "\nOne or more json files do not exist"
    echo "PARAMS: $PARAMS"
    echo "USER: $USER"
    exit
fi

echo "Parameters:"
echo "PARAMS: $PARAMS"
echo -e "USER: $USER \n"

./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER

echo -e "\n============ Finished ============"