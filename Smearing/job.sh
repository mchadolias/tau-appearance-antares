#!/bin/bash
#
# Job script to run the Smearing code
#

### SLURM

#SBATCH --ntasks=1                    # Run a single task (by default tasks == CPU)
#SBATCH --mem=3G                      # GB
#SBATCH --time=01-00:00:00               #
#SBATCH --mail-user=mchadolias@km3net.de   # Where to send mail
#SBATCH --mail-type=FAIL,TIME_LIMIT              # Mail events (NONE, BEGIN, END, FAIL, ALL)

# Go to the directory of the script
cd $WORK/master_thesis/tau_appearance/Smearing

printf "\n--------------------\n"
echo "Starting script:" $(basename $BASH_SOURCE)

INPUT_FILE="$WORK/Swim/Data/events/ANTARES/antares_w_nnfit_FINAL1.root"
OUTPUT_FILE="$WORK/Swim/Data/events/ANTARES/antares_w_nnfit_FINAL1_smeared_${SMEARING_PERCENTAGE}.root"

echo "Smearing Code"
echo "===================="
./bin/Smearing $INPUT_FILE $OUTPUT_FILE $SMEARING_PERCENTAGE $USE_RESOLUTION

echo "AddCanANTARES Code"
echo "===================="
./bin/AddCanANTARES $OUTPUT_FILE 