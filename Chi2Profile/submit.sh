#!/bin/sh
### usage:
###       ./submit.sh <DRY_RUN_FLAG> <EXPERIMENT> <ORDERING> <RECONSTRUCTION>
###
###      <DRY_RUN_FLAG> : 0 for submission to SLURM, 1 for frontend execution
###      <EXPERIMENT>   : "STD" or "TAU"
###      <ORDERING>     : "NO" or "IO"
###      <RECONSTRUCTION>: "MC" or "NNFit" or "AAFit"
###
### example: ./submit.sh 0 STD NO MC
#
### set this to 1 for a DRY RUN, i.e. without submission to SLURM
DRY_RUN=$1
EXPERIMENT=$2 # "STD" or "TAU"
ORDERING=$3 # "NO" or "IO"
RECONSTRUCTION=$4 # "MC" or "NNFit" or "AAFit"

if [ -z "$EXPERIMENT" ] || [ -z "$ORDERING" ] || [ -z "$RECONSTRUCTION" ]; then
    echo "Please provide all the necessary arguments"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo "DRY_RUN: $DRY_RUN"
echo "EXPERIMENT: $EXPERIMENT"
echo "ORDERING: $ORDERING"
echo -e "RECONSTRUCTION: $RECONSTRUCTION\n"

### PROJECT DIR for logs and the worker script
if [ -z "$THIS_INPUT_PROJ_DIR" ]; then
    THIS_PROJ_DIR=$WORK/master_thesis/tau_appearance/Chi2Profile
else
    THIS_PROJ_DIR=$THIS_INPUT_PROJ_DIR
fi


### JOBNAME
JOBNAME="job_chi2_${EXPERIMENT}_${ORDERING}_${RECONSTRUCTION}"

### LOGs
if [ ! -d ${THIS_PROJ_DIR}/logs ]; then
    mkdir ${THIS_PROJ_DIR}/logs
fi

WORKER_SCRIPT=${THIS_PROJ_DIR}/job.sh


if [[ "$DRY_RUN" -eq 0 ]]; then
### SUBMISSION TO SLURM
echo "sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--export=ALL,\
--EXPERIMENT=${EXPERIMENT},\
--ORDERING=${ORDERING},\
--RECONSTRUCTION=${RECONSTRUCTION},\
         ${WORKER_SCRIPT}"

sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--mail-user=mchadolias@km3net.de \
--export=ALL,\
EXPERIMENT=${EXPERIMENT},\
ORDERING=${ORDERING},\
RECONSTRUCTION=${RECONSTRUCTION} \
         ${WORKER_SCRIPT}

elif [[ "$DRY_RUN" -eq 1 ]]; then
### FRONTEND EXECUTION
    echo -e "FRONTEND EXECUTION \n ----------------------------------"
    export EXPERIMENT=${EXPERIMENT} ORDERING=${ORDERING} RECONSTRUCTION=${RECONSTRUCTION}
    ${WORKER_SCRIPT}
else
    echo -e "Test run with following parameters: \n \
            WORKER_SCRIPT:${WORKER_SCRIPT} \n \
            EXPERIMENT:${EXPERIMENT} \n \
            ORDERING:${ORDERING} \n \
            RECONSTRUCTION:${RECONSTRUCTION}"
fi
