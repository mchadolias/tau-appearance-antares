#!/bin/sh
### usage:
###       ./submit.sh <DRY_RUN_FLAG> <ROOT_FILE> <H5_FILE> 
###
###      
#
### set this to 1 for a DRY RUN, i.e. without submission to SLURM
DRY_RUN=$1
ROOT_FILE=$2
H5_FILE=$3
TASK=$4

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)

### PROJECT DIR for logs and the worker script
if [ -z "$THIS_INPUT_PROJ_DIR" ]; then
    THIS_PROJ_DIR=/home/saturn/capn/$USER/master_thesis/tau_appearance/reconstruction_perfomance
else
    THIS_PROJ_DIR=$THIS_INPUT_PROJ_DIR
fi


### JOBNAME
JOBNAME="job_num_files_${ROOT_FILE%.root}"

### LOGs
if [ ! -d ${THIS_PROJ_DIR}/logs ]; then
    mkdir ${THIS_PROJ_DIR}/logs
fi

WORKER_SCRIPT=${THIS_PROJ_DIR}/job_add_branch_flavour.sh


if [[ "$DRY_RUN" -eq 0 ]]; then
### SUBMISSION TO SLURM
echo "sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--export=ALL,\
--ROOT_FILE=${ROOT_FILE}, \
--H5_FILE=${H5_FILE} \
--TASK=${TASK} \
         ${WORKER_SCRIPT}"

sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--mail-user=michael.chadolias@fau.de \
--export=ALL,\
H5_FILE=$H5_FILE,\
ROOT_FILE=$ROOT_FILE,\
TASK=$TASK,\
         ${WORKER_SCRIPT}

elif [[ "$DRY_RUN" -eq 1 ]]; then
### FRONTEND EXECUTION
    echo -e "FRONTEND EXECUTION \n ----------------------------------"
    export ROOT_FILE=${ROOT_FILE} 
    export H5_FILE=${H5_FILE}
    export TASK=${TASK}
    ${WORKER_SCRIPT}
else
    echo -e "Test run with following parameters: \n \
            WORKER_SCRIPT:${WORKER_SCRIPT} \n \
            ROOT_FILE:${ROOT_FILE} \n \
            H5_FILE:${H5_FILE} \n \
            TASK:${TASK}"

fi
