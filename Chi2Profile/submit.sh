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
RECONSTRUCTION=$5 # "MC" or "NNFit_full" or "NNFit_dir" or "AAFit_ann" or "AAFit_dedx" or "Smeared"
CUT_OPTION=$6 # example: "muon_free"
SMEARING_LEVEL=$7 # example: "10" or "50" or "100" or "200" or "500" or "km3net"

if [ -z "$CHANNEL" ] || [ -z "$ORDERING" ] || [ -z "$RECONSTRUCTION" ] || [ -z "$CUT_OPTION" ] || [ -z "$SMEARING_LEVEL" ]; then
    echo "Please provide all the necessary arguments"
    exit
fi

echo -e "\n--------------------"
echo "Starting script:" $(basename $BASH_SOURCE)
echo "DRY_RUN: $DRY_RUN"
echo "SYSTEMATICS: $SYSTEMATICS_FLAG"
echo "CHANNEL: $CHANNEL"
echo "ORDERING: $ORDERING"
echo "RECONSTRUCTION: $RECONSTRUCTION"
echo "CUT_OPTION: $CUT_OPTION"
echo "SMEARING_LEVEL: $SMEARING_LEVEL"
echo -e "--------------------\n"


### PROJECT DIR for logs and the worker script
if [ -z "$THIS_INPUT_PROJ_DIR" ]; then
    THIS_PROJ_DIR=$WORK/master_thesis/tau_appearance/Chi2Profile
else
    THIS_PROJ_DIR=$THIS_INPUT_PROJ_DIR
fi


### JOBNAME
JOBNAME="job_swim_${CHANNEL}_${ORDERING}_${RECONSTRUCTION}_${CUT_OPTION}_${SYSTEMATICS_FLAG}_${SMEARING_LEVEL}"

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
--DRY_RUN=${DRY_RUN},\
--RECONSTRUCTION=${RECONSTRUCTION},\
--SMEARING_LEVEL=${SMEARING_LEVEL} \
         ${WORKER_SCRIPT}"

sbatch \
--job-name=${JOBNAME} \
--output=logs/conv_${JOBNAME}_%j.log \
--mail-user=mchadolias@km3net.de \
--mail-type=FAIL,TIME_LIMIT,END \
--export=ALL,\
SYSTEMATICS=${SYSTEMATICS_FLAG},\
CHANNEL=${CHANNEL},\
ORDERING=${ORDERING},\
CUT=${CUT_OPTION},\
DRY_RUN=${DRY_RUN},\
RECONSTRUCTION=${RECONSTRUCTION},\
SMEARING_LEVEL=${SMEARING_LEVEL} \
         ${WORKER_SCRIPT}

elif [[ "$DRY_RUN" -eq 1 ]]; then
### FRONTEND EXECUTION
    echo -e "FRONTEND EXECUTION \n----------------------------------"
    export CHANNEL=${CHANNEL} \
           ORDERING=${ORDERING} \
           RECONSTRUCTION=${RECONSTRUCTION} \
           SYSTEMATICS=${SYSTEMATICS_FLAG} \
           CUT=${CUT_OPTION} \
           SMEARING_LEVEL=${SMEARING_LEVEL} \
           DRY_RUN=${DRY_RUN}
    ${WORKER_SCRIPT}
else
    echo -e "Test run with following parameters: \n \
            WORKER_SCRIPT:${WORKER_SCRIPT} \n \
            CHANNEL:${CHANNEL} \n \
            ORDERING:${ORDERING} \n \
            SYSTEMATICS:${SYSTEMATICS_FLAG} \n \
            CUT:${CUT_OPTION} \n \
            RECONSTRUCTION:${RECONSTRUCTION} \n \
            SMEARING_LEVEL:${SMEARING_LEVEL} \n "
fi
