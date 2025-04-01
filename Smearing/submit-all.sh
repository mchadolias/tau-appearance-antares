#!/bin/bash
DRY_RUN=2
SMEARING_PERCENTAGE=(10 50 100 200 500)

echo "Submitting jobs: DRY_RUN=$DRY_RUN" 
for i in "${SMEARING_PERCENTAGE[@]}"
do
    echo "Submitting job for SMEARING_PERCENTAGE: $i"
    ./submit.sh $DRY_RUN $i N
done