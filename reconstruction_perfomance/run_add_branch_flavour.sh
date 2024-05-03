echo "Running add_column_test.py"
module load python

# Define the name of the Anaconda environment to activate
ENVNAME="master_thesis"

# Define the path to the Anaconda installation's 'bin' directory2
ANACONDAPATH="/home/saturn/capn/mppi133h/software/private/conda/envs/master_thesis/bin"
WORKDIR="/home/saturn/capn/mppi133h/master_thesis/tau_appearance/reconstruction_perfomance"
ROOT_FILE="$1"
H5_FILE="$2"

# Add the Anaconda installation's 'bin' directory to the PATH variable
export PATH="$ANACONDAPATH:$PATH"

# Activate the conda environment
source activate "$ENVNAME"
which python

cd ${WORKDIR}
COMMAND="python3 scripts/add_new_branches.py --r ${ROOT_FILE} --h5 ${H5_FILE}"

echo " Executing command: "
echo -e "\n ========================================================="
echo " ${COMMAND}"
echo -e " =========================================================\n"

eval "${COMMAND}"

if [[ $? == 0 ]]; then
    echo " Code executed successfully"
else
    echo " Unexpected error! See error log!"
fi

echo -e "\n DONE! \n"