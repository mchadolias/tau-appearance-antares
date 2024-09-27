import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import numpy as np
import uproot
import argparse
from itertools import product
import os
import scienceplots

# Set the style of the plots
plt.style.use(['science', "grid","no-latex"])   
plt.rcParams['savefig.dpi'] = 1000
plt.rcParams.update({
    'axes.titlesize': 20,
    'axes.labelsize': 15,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})

text_conversion = {
    "STD": "CC",
    "TAU": "NC+CC",
    "NO": "Normal Ordering",
    "IO": "Inverted Ordering",
    "MC": "Monte-Carlo truth",
    "AAFit": "AAFit",
    "NNFit": "NNFit",
    "AAFit_dedx": "AAFit dedx",
    "AAFit_ann": "AAFit ANN",
    "NNFit_full": "NNFit",
    "NNFit_dir": "NNFit direction reco only",
    "10_percent": "10 %",
    "50_percent": "50 %",
    "70_percent": "70 %",
    "100_percent": "100 %",
    "200_percent": "200 %",
    "500_percent": "500 %",
    "antares": "ANTARES level"
}

def ArgumentParser():
    parser = argparse.ArgumentParser(description='Plotter for chi2 profile')
    parser.add_argument('--type', type=str, default='reconstruction', 
                        help="Select type of plot to be made: reconstruction or study or smeared")
    parser.add_argument('--reco', type=str, 
                        help="Choose the reconstruction algorithm used to reconstruct the events")
    parser.add_argument('--channel', type=str,
                        help="Choose which channel to channel. STD corresponds to CC and TAU corresponds to NC")
    parser.add_argument('--path', type=str, 
                        default="/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/",
                        help="Path to the root files")
    parser.add_argument('--systematic', type=str, default="no_systematics",
                        help="Choose if the systematic uncertainties are included or not")
    parser.add_argument('--cut', type=str, default="muon_free",
                        help="Choose if the muons are included or not")
    args = parser.parse_args()
    return args

def _root_to_tables(root_file, tree_name = "outTree", columns = ["chi2","TauNorm"]):
    
    # Load the root file
    with uproot.open(root_file) as f:
        data = f[tree_name].arrays(columns, library="numpy")
    return data

def load_data(
    channel,
    order,
    path,
    reco = None,
):
    # Load the data
    if reco is None:
        data_fixed = _root_to_tables(os.path.join(path, channel, order,
                                            f"fixed/Chi2Profile_TauNorm_{channel}_{order}_fixed_FitTwoOctants.root"))
        data_free = _root_to_tables(os.path.join(path, channel, order,
                                            f"free/Chi2Profile_TauNorm_{channel}_{order}_free_FitTwoOctants.root"))
    else:
        print(f"Loading data for {reco} {channel} {order}...")
        data_fixed = _root_to_tables(os.path.join(path, reco, channel, order,
                                            f"fixed/Chi2Profile_TauNorm_{channel}_{order}_fixed_FitTwoOctants.root"))
        data_free = _root_to_tables(os.path.join(path, reco, channel, order,
                                            f"free/Chi2Profile_TauNorm_{channel}_{order}_free_FitTwoOctants.root"))

    return data_fixed, data_free

def square_root(
    data_list: list,
):
    return [np.sqrt(x) if x > 0 else 0 for x in data_list]

def plot_chi2(
    type,
    channel,
    reco,
    systematic,
    cut,
    save_path,
    path = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/",
):
    # Set data path
    path = os.path.join(path, "output", "ANTARES", cut)

    # Define the mass ordering
    ordering = ["NO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=12)
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    print(f"Plotting chi-square plots for {type} type...")
    if type == "reconstruction":
        recos = ["MC", "AAFit_dedx", "AAFit_ann", "NNFit_full", "NNFit_dir"]

        for order in ordering:
            print(f"Plotting for {order}...")
            zoomed_ax = fig.add_axes([0.6, 0.6, 0.29, 0.26])
            for reco in recos:
                data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
                print(len(data_fixed["TauNorm"]), len(data_fixed["chi2"] - data_free["chi2"]))
                ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                        'o', markersize=7, label=f"{text_conversion[reco]}")
                zoomed_ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                                 'o--', linewidth=2, markersize=5)
            zoomed_ax.set(
                xlim = (0, 2),
                ylim = (0, 100),
            )
            ax.set(
                title = f"Chi2 profile for {text_conversion[channel]} channel and \
                {text_conversion[order]}",
                ylim = (0, 750),
            )        
    elif type == "study":
        channels = ["STD", "TAU"]
        
        zoomed_ax = fig.add_axes([0.5, 0.5, 0.39, 0.36]) 
        for order, channel in product(ordering, channels):
            data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"], 
                    'o', markersize=7, label=f"{text_conversion[order]} ({text_conversion[channel]})")
            zoomed_ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                            'o--', linewidth=2, markersize=5)
        ax.set(
            title = f"Chi2 profile for {reco} reco",
        )    
    elif type == "smeared":
        channel = "STD"
        order = "NO"
        
        smear_path = os.path.join(path, "smeared")
        smear_levels = os.listdir(smear_path) ;  smear_levels.remove("km3net")
    
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for level in smear_levels:
            print(f"Loading smeared data for {text_conversion[level]} smearing level...")
            data_fixed, data_free = load_data( channel, order, os.path.join(smear_path, level, systematic))
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                    'o--', markersize=3, label=f"Smeared - {text_conversion[level]}")
            
        for reco in ["MC", "NNFit_full"]:
            data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
            ax.plot(data_fixed["TauNorm"], data_fixed["chi2"] - data_free["chi2"],
                    'o--', markersize=3, label=f"{text_conversion[reco]}")
        ax.set(
            ylim = (0, None),
            title = f"Chi-square profile for smeared events",
        )
    # General settings
    ax.set(
        xlabel="Tau Normalization ($N_{\\nu_{\\tau}}$)",
        ylabel="$\\Delta \\chi^2$",
        xlim=(0, 2),
    )
    ax.legend(prop=font, frameon=False)
    fig.tight_layout()
    if (type == "reconstruction"):
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{channel}_{order}_{reco}.png"))
    elif type == "study":
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}_{reco}.png"))
    elif type == "smeared":
        fig.savefig(os.path.join(save_path, f"Chi2Profile_{type}.png"))

            
def sigma_plots(
    type,
    channel,
    reco,
    systematic,
    cut_option,
    save_path,
    path = "/sps/km3net/users/mchadoli/master_thesis/tau_appearance/Chi2Profile/",
): 
    # Set data path
    path = os.path.join(path, "output", "ANTARES", cut_option)

    # Define the mass ordering        
    ordering = ["NO", "IO"]
    
    # Define the font for legend
    font = font_manager.FontProperties(family='sans-serif', style='normal', size=10)
    
    print(f"\nPlotting sigma plots for {type}...")
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    if type == "reconstruction":
        recos = ["MC", "AAFit_dedx", "AAFit_ann", "NNFit_full", "NNFit_dir"]

        for order in ordering:
            for reco in recos:
                data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
                ax.plot(
                    data_fixed["TauNorm"], 
                    square_root(data_fixed["chi2"] - data_free["chi2"]), 
                    'o--', 
                    linewidth=2, 
                    markersize=4, 
                    label=f"{text_conversion[reco]}"
            )
        
    elif type == "study":
        channels = ["STD", "TAU"]
        
        for order, channel in product(ordering, channels):
            data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
            ax.plot(
                data_fixed["TauNorm"],
                square_root(data_fixed["chi2"] - data_free["chi2"]), 
                'o--', 
                linewidth=2, 
                markersize=5, 
                label=f"{text_conversion[order]} ({text_conversion[channel]})"
            )
    
    elif type == "smeared":
        channel = "STD"
        order = "NO"
        
        smear_path = os.path.join(path, "smeared")
        smear_levels = os.listdir(smear_path) ;  smear_levels.remove("km3net")

        for level in smear_levels:
            print(f"Loading smeared data for {text_conversion[level]} smearing level...")
            data_fixed, data_free = load_data( channel, order, os.path.join(smear_path, level, systematic))
            ax.plot(
                data_fixed["TauNorm"], 
                square_root(data_fixed["chi2"] - data_free["chi2"]),
                'o--', 
                markersize=3, 
                label=f"Smeared - {text_conversion[level]}"
            )

        for reco in ["MC", "NNFit_full"]:
            data_fixed, data_free = load_data(channel, order, os.path.join(path, "unsmeared", systematic), reco)
            ax.plot(
                data_fixed["TauNorm"], 
                square_root(data_fixed["chi2"] - data_free["chi2"]),
                'o--', 
                markersize=3, 
                label=f"{text_conversion[reco]}"
            )

    # General settings
    ax.axhline(y=3, linestyle='--', c = "black")
    ax.legend(prop=font, frameon=False, loc = 1)
    ax.axhline(y=5, linestyle='-.', c = "black")
    ax.set(
        xlabel="Tau Normalization ($N_{\\nu_{\\tau}}$)",
        ylabel="Significance ($\\sigma$)",
        xlim=(0, 2),
        ylim = (0, None),
    )
    fig.tight_layout()

    if (type == "reconstruction") or (type == "study"):
        ax.set_title(f"Sensitivity of Tau Normalization for {text_conversion[channel]} channel")
        fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}_{channel}_{order}_{reco}.png"))
    elif type == "smeared":
        ax.set_title(f"Sensitivity of Tau Normalization for smeared events")
        fig.savefig(os.path.join(save_path, f"SigmaPlots_{type}.png"))

if __name__ == '__main__':
    
    args = ArgumentParser()
    type = args.type
    path = args.path
    reco = args.reco
    channel = args.channel
    systematic = args.systematic
    cut_option = args.cut
    
    save_path = os.path.join(path, f"plots/{cut_option}/{systematic}/{type}")
    
    if type ==  "reconstruction":
        if channel is None:
            raise ValueError("Please provide the channel channel")
    elif type == "study":
        if reco is None:
            raise ValueError("Please provide the reconstruction algorithm")
        
    # Check if the paths exist
    if not os.path.exists(path):
        raise ValueError("The path for the files does not exist")
    if not os.path.exists(save_path):
        print("The path to save the plots does not exist. Creating the directory...")
        os.makedirs(save_path)
    
    # Plotting the chi2 profile
    plot_chi2(type, channel, reco, systematic, cut_option, save_path, path)

    # Plotting the significance
    sigma_plots(type, channel, reco, systematic, cut_option, save_path, path)
    
    
    