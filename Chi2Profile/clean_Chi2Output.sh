#!/bin/bash
#
# This script cleans the output of the Chi2Profile code & creates the directories again
# It is used to clean the output of the Chi2Profile code

# Go to the directory of the script
cd $WORK/master_thesis/tau_appearance/Chi2Profile

# Remove the output directory
rm -r output 
rm -r json 

python3 create_output_directories.py --cut ${1}
python3 create_all_json_files.py

echo -e "\nFinished cleaning the output of the Chi2Profile code"