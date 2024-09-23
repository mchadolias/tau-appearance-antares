#!/bin/bash

DRY_RUN=$1
SMEARING_PERCENTAGE=$2
USE_RESOLUTION=$3

if [ -z "$SMEARING_PERCENTAGE" ] || [ -z "$USE_RESOLUTION" ]; then
    echo "Please provide all the necessary arguments"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo "DRY_RUN: $DRY_RUN"
echo "SMEARING_PERCENTAGE: $SMEARING_PERCENTAGE"
echo "USE_RESOLUTION: $USE_RESOLUTION"

### PROJECT DIR for logs and the worker script
if [ -z "$THIS_INPUT_PROJ_DIR" ]; then
    THIS_PROJ_DIR=$WORK/master_thesis/tau_appearance/Smearing
else
    THIS_PROJ_DIR=$THIS_INPUT_PROJ_DIR
fi

### JOBNAME
JOBNAME="job_smear_${SMEARING_PERCENTAGE}_${USE_RESOLUTION}"

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
--SMEARING_PERCENTAGE=${SMEARING_PERCENTAGE},\
--USE_RESOLUTION=${USE_RESOLUTION},\
         ${WORKER_SCRIPT}"
sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--mail-user=mchadolias@km3net.de \
--export=ALL,\
SMEARING_PERCENTAGE=${SMEARING_PERCENTAGE},\
USE_RESOLUTION=${USE_RESOLUTION} \
         ${WORKER_SCRIPT}

elif [[ "$DRY_RUN" -eq 1 ]]; then
### FRONTEND EXECUTION
    export SMEARING_PERCENTAGE=${SMEARING_PERCENTAGE} USE_RESOLUTION=${USE_RESOLUTION}
    ${WORKER_SCRIPT}
else
    echo "Invalid DRY_RUN option"

    echo "Usage: $0 DRY_RUN SMEARING_PERCENTAGE USE_RESOLUTION"
    echo "Example: $0 0 0.1 Y"
fi