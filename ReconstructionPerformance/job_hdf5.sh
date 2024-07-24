#!/bin/bash
# 
# Usage:
#       ./job_hdf5.sh <list_name>
#
# Description:
#       This script is used to submit a job to the cluster. It is used to run the merged_nnfit.py script
#       for a given list of files. The list of files is given as an argument to the script.

LIST_NAME=$1
SCRIPT="${WRKDIR}/scripts/merge_nnfit.py"

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo "Script to run: ${SCRIPT}"
echo "List name: ${LIST_NAME}"

# Load the python/conda environment
module load python/3.7.5

# Check if the script exists
[[ ! -f "${SCRIPT}" ]] && { echo "Script not found! Exiting!"; exit; }

COMMAND="python ${SCRIPT} --t ${LIST_NAME}"

echo " Executing command: "
echo -e "\n ========================================================="
echo " ${COMMAND}"
echo -e " =========================================================\n"

eval "${COMMAND}"

if [[ $? == 0 ]]; then
    echo " Code exacuted successfully"
else
    echo " Unexpected error! See error log!"
fi

echo -e "\n DONE! \n"