import os
import uproot
import pandas as pd
import time
from datetime import timedelta
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def get_trackmask(df):
    cc_ma = df["is_cc"] == True
    numu_ma = get_numumask(df)

    track_tau = df["interaction_type"] == 2
    tau_ma = get_nutaumask(df)

    track_ma = (cc_ma & numu_ma) | (track_tau & tau_ma)

    return track_ma


def get_showermask_cc(df):
    nue_mask = get_nuemask(df)
    nutau_mask = get_nutaumask(df)

    CCshower = df["interaction_type"] == 3 
    is_cc = df["is_cc"] == True

    shower_cc = (nue_mask | nutau_mask & CCshower) & is_cc
    
    return shower_cc

def get_showermask_nc(df):
    nue_mask =  get_nuemask(df)
    numu_mask = get_numumask(df)
    nutau_mask =  get_nutaumask(df)
    nu_mask = nue_mask | numu_mask | nutau_mask

    nc_ma = (df["is_cc"] == False) & nu_mask

    return nc_ma 
        
def get_nutaumask(df):
    nutau_mask = abs(df["Type"]) == 16

    return nutau_mask

def get_numumask(df):
    numu_mask = abs(df["Type"]) == 14

    return numu_mask

def get_nuemask(df):
    nue_mask = abs(df["Type"]) == 12

    return nue_mask



def load_large_rootfile_to_df(rootfile, columns=None, tree="sel", chunksize=100_000):
    """
    Load a large ROOT file into a pandas DataFrame while optimizing memory usage.

    Parameters:
    file_path (str): The path to the ROOT file.
    tree_name (str): The name of the TTree to load.
    columns (list, optional): A list of columns to load. If None, all columns will be loaded.
    chunksize (int, optional): The number of rows to load in each chunk.

    Returns:
    A pandas DataFrame containing the data from the TTree.
    """
    df_list = []
    
    print(f"Loading the ROOT file: {rootfile}")
    ctime = time.time()
    
    # Open the ROOT file and get the TTree object
    with uproot.open(rootfile) as f:

        # Specify the columns to load
        if columns is None:
            columns = f[tree].keys()

        # Load the data in chunks
        for i in tqdm(range(0, f[tree].num_entries, chunksize)):
            df = f["sel"].arrays(columns, library="pd", entry_start=i, entry_stop=i+chunksize)
            
            # Append the chunk to the list
            df_list.append(df)
    
    print(f"ROOT file imported as a Dataframe in: {timedelta(seconds=time.time()-ctime)}")
    # Concatenate the chunks into a single DataFrame
    return pd.concat(df_list, ignore_index=True)

def energy_resolution_fit(
    df,
):

    # Define energy bins
    energy_bins = np.round(np.geomspace(10, 100, 15), 4)
    energy_bins = np.append(energy_bins, 1e3)

    # find the mean and std of the energy resolution in each bin and save it in a DataFrame
    energy_resolutions = []
    for i in range(len(energy_bins) - 1):
        energy_bin = df[(df["energy_true"] > energy_bins[i]) & (df["energy_true"] < energy_bins[i+1])]
        mean = energy_bin["EnergyResolution"].mean()
        std = energy_bin["EnergyResolution"].std()
        energy_resolutions.append({"energy_bin": energy_bins[i], "mean": mean, "std": std})
    
    energy_resolutions = pd.DataFrame(energy_resolutions)


    return energy_resolutions


def plot_energy_resolution(
    df,
    energy_resolutions,
):
    """
    Plot the energy resolution of the detector as a function of the true energy.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    energy_resolutions (pd.DataFrame): The DataFrame containing the energy resolutions.

    """

    # Plot the energy resolution as a function of the true energy
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.errorbar(
        energy_resolutions["energy_bin"],
        energy_resolutions["mean"],
        yerr=energy_resolutions["std"],
        fmt="o",
        color="black",
        label="Energy resolution",
    )
    ax.hist2d(
        df["energy_true"],
        df["EnergyResolution"],
        bins=(100, 100),
        cmap="viridis",
        cmin=1,
        label="Energy resolution distribution",
    )
    ax.set_xscale("log")
    ax.set_xlabel("True energy (GeV)")
    ax.set_ylabel("Energy resolution")
    ax.set_title("Energy resolution of the detector")
    ax.legend()
    plt.show()



def energy_resolution_function(
    energy_true,
    energy_reco,
):
    """
    Function to fit the energy resolution of a detector.

    Parameters:
    energy_true (float): The true energy of the particle.
    energy_reco (float): The reconstructed energy of the particle.

    Returns:
    The energy resolution of the detector.
    """
    return (energy_reco - energy_true) / energy_true

if __name__ == "__main__":
    # Define the path to the ROOT file
    path = "/sps/km3net/users/mchadoli/ANTARES/mc/cut_selection/100GeV"
    root_file = "full_nutau_low_updated.root"
    COLUMNS = ["interaction_type", "is_cc", "type", "energy_true", "NNFitTrack_Log10Energy", "NNFitShower_Log10Energy"]

    # Load the ROOT file into a DataFrame
    df = load_large_rootfile_to_df(os.path.join(path, root_file), columns=COLUMNS)
    df["NNFitShower_Energy"] = 10**df["NNFitShower_Log10Energy"]


    # TODO: See if there is a huge difference between shower/track topology

    # Create energy resolution column
    df["EnergyResolution"] = energy_resolution_function(df["energy_true"], df["NNFitShower_Energy"])


    # Energy resolution fit
    energy_resolutions = energy_resolution_fit(df)