import time
from datetime import timedelta
import argparse
from file_management import read_txt_file, load_dataframes, save_to_hdf5

def argument_parser():    
    parser = argparse.ArgumentParser(description="Application to do merge hdf5 files to more managable.")

    parser.add_argument("--t", type=str, dest="list_name", 
                        help="The name of the list containing the HDF5 files.",
                        default="list_test.txt")
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # Load the data
    print("Loading the data...")
    ctime = time.time()
    
    # Parse the arguments
    args = argument_parser()
    list_name = args.list_name
    
    # Read the list of files
    filelist = read_txt_file(list_name)
    
    # Check if the filelist is empty
    if len(filelist) == 0:
        print("The filelist is empty.")
        exit()
        
    # Import the data
    print("Importing the data...")
    print(f"NNfit data: {list_name}")
    print(f"Number of files: {len(filelist)}")
    print("\nStarting the loop..\n")
    df_nnfit = load_dataframes(filelist)
    
    # Extract the data to a new hdf5 file
    print("Extracting the data...")
    save_to_hdf5(df_nnfit, f'nnfit_{list_name.split(".")[0]}.hdf5')
        
    # Save the data
    print("Saving the data...", timedelta(seconds=time.time()-ctime))

