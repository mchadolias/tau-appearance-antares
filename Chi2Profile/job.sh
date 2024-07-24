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

# Go to the directory of the script
cd $WORK/master_thesis/tau_appearance/Chi2Profile

# Load modules
echo "Loading modules"
source $HOME/bash_scripts/init.sh
echo "Preparing SWIM environment"
source $HOME/bash_scripts/swim_env.sh

python3 create_json_file.py --channel $CHANNEL --order $ORDERING  --reco $RECONSTRUCTION --systematics "$SYSTEMATICS"
python3 create_output_directories.py

# Compile the code
#echo "Compiling the code"
#make clean && make

echo "Starting script:" $(basename $BASH_SOURCE)
echo "CHANNEL: $CHANNEL"
echo "ORDERING: $ORDERING"
echo "RECONSTRUCTION: $RECONSTRUCTION"
echo "SYSTEMATICS: $SYSTEMATICS"


### Define all json files

# Define binning json file
BINNING="./json/ANTARES/binning_ANTARES.json"

# Define variables json file
if [ $CHANNEL == "STD" ]; then
    VARIABLES="./json/ANTARES/variables_ANTARES_STD.json"
elif [ $CHANNEL == "TAU" ]; then
    VARIABLES="./json/ANTARES/variables_ANTARES_TAU.json"
else
    echo "CHANNEL type not recognized"
    exit
fi

# Define classes json file
if [ $RECONSTRUCTION == "MC" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_MC.json"
elif [ $RECONSTRUCTION == "NNFit_full" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_NNFit_full.json"
elif [ $RECONSTRUCTION == "NNFit_dir" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_NNFit_dir.json"
elif [ $RECONSTRUCTION == "AAFit_ann" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_AAFit_ann.json"
elif [ $RECONSTRUCTION == "AAFit_dedx" ]; then
    CLASSES="./json/ANTARES/classes_ANTARES_AAFit_dedx.json"
else
    echo "RECONSTRUCTION type not recognized"
    exit
fi

if [ $SYSTEMATICS == "1" ]; then
    # Define parametes json file
    if [ $ORDERING == "NO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free_systematics.json"
    elif [ $ORDERING == "IO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free_systematics.json"
    else
        echo "ORDERING type not recognized"
        exit
    fi

    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_free_systematics.json"
else 
    # Define parametes json file
    if [ $ORDERING == "NO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free_no_systematics.json"
    elif [ $ORDERING == "IO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_free_no_systematics.json"
    else
        echo "ORDERING type not recognized"
        exit
    fi

    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_free_no_systematics.json"
fi 

## Run source-code

# --------------- Free ----------------
echo "Running MyChi2Profile with TauNorm parameter free"
echo "Parameters: $BINNING $CLASSES $VARIABLES $PARAMS $USER"
./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER


# --------------- Fixed ----------------
echo "Running MyChi2Profile with TauNorm parameter fixed"

if [ $SYSTEMATICS == "1" ]; then
    # Define parametes json file
    if [ $ORDERING == "NO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed_systematics.json"
    elif [ $ORDERING == "IO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed_systematics.json"
    else
        echo "ORDERING type not recognized"
        exit
    fi

    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_fixed_systematics.json"
else 
    # Define parametes json file
    if [ $ORDERING == "NO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed_no_systematics.json"
    elif [ $ORDERING == "IO" ]; then
        PARAMS="./json/PARAMETERS/parameters_Data_NO_Model_${ORDERING}_fixed_no_systematics.json"
    else
        echo "ORDERING type not recognized"
        exit
    fi

    # Define user json file
    USER="./json/USER/User_${RECONSTRUCTION}_${CHANNEL}_${ORDERING}_fixed_no_systematics.json"
fi

./bin/MyChi2Profile  $BINNING $CLASSES $VARIABLES $PARAMS $USER

# Plotting the Chi-Square profile
echo "Plotting the Chi-Square profile"

# Define the path to the Anaconda installation's 'bin' directory2
WORKDIR="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile"

cd ${WORKDIR}

if [ $SYSTEMATICS == "0" ]; then
    SYSTEMATICS="no_systematics"
    echo "SYSTEMATICS: $SYSTEMATICS"
else
    SYSTEMATICS="systematics"
fi

python3 plot_chi_square.py --channel $CHANNEL --ordering $ORDERING --reco $RECONSTRUCTION --systematic $SYSTEMATICS

echo "============ Finished ============"