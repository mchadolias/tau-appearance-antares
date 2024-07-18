#!/bin/bash

# Run plotter for all possible combinations of experiment, ordering and reconstruction
RECOS=("MC" "NNFit_full" "NNFit_dir" "AAFit_ann" "AAFit_dedx")
CHANNELS=("STD" "TAU")
ORDERINGS=("NO" "IO")


# Go to the directory of the script
cd "$(dirname "$0")"

echo "Running for different recos"
for CHANNEL in "${CHANNELS[@]}"; do
    for RECO in "${RECOS[@]}"; do
        echo -e "\n--------------------"
        echo -e "Run python script for $RECO"
        python3 plotter.py --type reconstruction --reco $RECO --probe $CHANNEL
    done
done

echo "Running for different orderings"
echo -e "\n--------------------"
echo -e "Run python script for $ORDERING"
python3 plotter.py --type ordering 

echo "Running for different channels"
for RECO in "${RECOS[@]}"; do
    for CHANNEL in "${CHANNELS[@]}"; do
        echo -e "\n--------------------"
        echo -e "Run python script for $CHANNEL"
        python3 plotter.py --type study --probe $CHANNEL --reco $RECO
    done
done
echo "=========== DONE ==========="