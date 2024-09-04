#!/bin/sh
### usage:
###       ./submit.sh <DRY_RUN_FLAG> <CHANNEL> <ORDERING> <RECONSTRUCTION>
###
###      <DRY_RUN_FLAG> : 0 for submission to SLURM, 1 for frontend execution
###      <SYSTEMATICS_FLAG> : 0 for no systematics, 1 for systematics
###      <CHANNEL>   : "STD" or "TAU"
###      <ORDERING>     : "NO" or "IO"
###      <RECONSTRUCTION>: "MC" or "NNFit_full" or "NNFit_dir" or "AAFit_ann" or "AAFit_dedx"
###
### example: ./submit.sh 0 0 STD NO MC
#
### set this to 1 for a DRY RUN, i.e. without submission to SLURM
DRY_RUN=$1
SYSTEMATICS_FLAG=$2
CHANNEL=$3 # "STD" or "TAU"
ORDERING=$4 # "NO" or "IO"
RECONSTRUCTION=$5 # "MC" or "NNFit_full" or "NNFit_dir" or "AAFit_ann" or "AAFit_dedx"
CUT_OPTION=$6 # example: "muon_free"

if [ -z "$CHANNEL" ] || [ -z "$ORDERING" ] || [ -z "$RECONSTRUCTION" ]; then
    echo "Please provide all the necessary arguments"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo "DRY_RUN: $DRY_RUN"
echo "SYSTEMATICS: $SYSTEMATICS_FLAG"
echo "CHANNEL: $CHANNEL"
echo "ORDERING: $ORDERING"
echo -e "RECONSTRUCTION: $RECONSTRUCTION\n"

### PROJECT DIR for logs and the worker script
if [ -z "$THIS_INPUT_PROJ_DIR" ]; then
    THIS_PROJ_DIR=$WORK/master_thesis/tau_appearance/Chi2Profile
else
    THIS_PROJ_DIR=$THIS_INPUT_PROJ_DIR
fi


### JOBNAME
JOBNAME="job_chi2_${CHANNEL}_${ORDERING}_${RECONSTRUCTION}_${CUT_OPTION}_${SYSTEMATICS_FLAG}"

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
--CHANNEL=${CHANNEL},\
--ORDERING=${ORDERING},\
--SYSTEMATICS=${SYSTEMATICS_FLAG},\
--CUT=${CUT_OPTION},\
--RECONSTRUCTION=${RECONSTRUCTION},\
         ${WORKER_SCRIPT}"

sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--mail-user=mchadolias@km3net.de \
--export=ALL,\
SYSTEMATICS=${SYSTEMATICS_FLAG},\
CHANNEL=${CHANNEL},\
ORDERING=${ORDERING},\
CUT=${CUT_OPTION},\
RECONSTRUCTION=${RECONSTRUCTION} \
         ${WORKER_SCRIPT}

elif [[ "$DRY_RUN" -eq 1 ]]; then
### FRONTEND EXECUTION
    echo -e "FRONTEND EXECUTION \n ----------------------------------"
    export CHANNEL=${CHANNEL} ORDERING=${ORDERING} RECONSTRUCTION=${RECONSTRUCTION} SYSTEMATICS=${SYSTEMATICS_FLAG} CUT=${CUT_OPTION}
    ${WORKER_SCRIPT}
else
    echo -e "Test run with following parameters: \n \
            WORKER_SCRIPT:${WORKER_SCRIPT} \n \
            CHANNEL:${CHANNEL} \n \
            ORDERING:${ORDERING} \n \
            SYSTEMATICS:${SYSTEMATICS_FLAG} \n \
            CUT:${CUT_OPTION} \n \
            RECONSTRUCTION:${RECONSTRUCTION}"
fi
