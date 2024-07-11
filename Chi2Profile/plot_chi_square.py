import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as font_manager
import uproot
import os
import argparse
import numpy as np

# Set the style of the plots
plt.style.use('seaborn-v0_8-paper')
#plt.rcParams['savefig.dpi'] = 1000

def ArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str, default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/output/ANTARES/")
    parser.add_argument("--reco", type=str, default="MC",
                        help="Choose the reconstruction algorithm used to reconstruct the events")
    parser.add_argument("--ordering", type=str, default="NO",
                        help="Choose the ordering of the neutrino mass hierarchy")
    parser.add_argument("--probe", type=str, default="STD",
                        help="Choose which channel to probe. STD corresponds to CC and TAU corresponds to NC")
    args = parser.parse_args()
    return args
    
def _root_to_tables(root_file, tree_name = "outTree", columns = ["chi2","TauNorm"]):
    
    # Load the root file
    with uproot.open(root_file) as f:
        data = f[tree_name].arrays(columns, library="numpy")
    return data

def plot_sigma(
    data_free,
    data_fixed,
    reco,
    probe,
    order,
    save_path = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/plots",
    ):
    
    if probe == "STD":
        channel = "CC-only"
    elif probe == "TAU":
        channel = "CC+NC"
    
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=16)
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(data_fixed["TauNorm"], np.sqrt(data_fixed["chi2"]-data_free["chi2"]), 'bo--', linewidth=2, markersize=5, label=f"Data {order} ({channel})")
    #ax.plot(data_free["TauNorm"], np.sqrt(data_free["chi2"]), "o", c = "black")
    ax.set(
        xlabel="Tau Normalization",
        ylabel="Significance ($\sigma$)",
        xlim=(0, 2),
        title = f"Sensitivity of the Tau Normalization with {reco} reco"
    )
    ax.tick_params(which='major', direction="in", top=True, left=True, right=True, width=1.5, size=6)
    ax.tick_params(which='minor', direction="in", top=True, left=True, right=True, width=1, size=4)
    ax.legend(prop=font, frameon=False)
    fig.savefig(os.path.join(save_path, f"SigmaPlots_TauNorm_{reco}_{probe}_{order}.png"))

def plot_chi2(
    data_free,
    data_fixed,
    reco,
    probe,
    order,
    save_path = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/plots",
    ):
    
    if probe == "STD":
        channel = "CC-only"
    elif probe == "TAU":
        channel = "CC+NC"
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax.plot(data_fixed["TauNorm"], data_fixed["chi2"]-data_free["chi2"], c = "black", label=f"Data {order} ({channel})")
    ax.set(
        xlabel="Tau Normalization",
        ylabel="$\chi^2$",
        xlim=(0, 2),
        title = f"Sensitivity of the Tau Normalization with {reco} reco"
    )
    ax.grid()
    ax.legend()
    fig.savefig(os.path.join(save_path, f"Chi2Plots_TauNorm_{reco}_{probe}_{order}.png"))
    

if __name__ == '__main__':
    # Load the data
    print("=============== Loading Arguments ===============")
    args = ArgumentParser()
    directory = args.directory
    reco = args.reco
    ordering = args.ordering
    probe = args.probe

    print(f"=============== Loading Data ===============")
    data_free = _root_to_tables(os.path.join(directory, reco, probe, ordering, f"free/Chi2Profile_TauNorm_{probe}_{ordering}_free_FitTwoOctants.root"))
    data_fixed = _root_to_tables(os.path.join(directory, reco, probe, ordering, f"fixed/Chi2Profile_TauNorm_{probe}_{ordering}_fixed_FitTwoOctants.root"))
    
    print(f"=============== Plotting  ===============")
    plot_chi2(data_free, data_fixed, reco, probe, ordering)
    
    plot_sigma(data_free, data_fixed, reco, probe, ordering) 
        
    print("=============== End of program ===============")
                                                 

                                                 
    
    
    
    
    
    
    