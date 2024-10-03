import sys
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sys.path.append("../..")
import libraries

plot_dict = {
    "energy": "Energy",
    "cos_zenith": "Cosine Zenith",
}

def _hist_1d_plot(
        df,
        variable,
        smearing_level,
        binning,
):
    fig, ax = plt.subplots()
    sns.histplot(
        data=df,
        x=f"{variable}_true",
        bins=binning,
        element="step",
        hatch = "|",
        label=f"True {plot_dict[variable]}",
        ax=ax
    )
    sns.histplot(
        data=df,
        x=f"{variable}_smeared",
        bins=binning,
        element="step",
        hatch = "///",
        label=f"Smeared {plot_dict[variable]}",
        ax=ax
    )
    if (smearing_level == "antares"):
        ax.set_title(f"{plot_dict[variable]} at ANTARES-level Smearing")
    else:
        ax.set_title(f"{plot_dict[variable]} at {smearing_level} % Smearing")
    ax.set_ylabel("Counts")
    if (variable == "energy"):
        ax.set_xscale("log")
        ax.set_xlabel(f"{plot_dict[variable]} [GeV]")
    else:
        ax.set_xlabel(f"True {plot_dict[variable]}")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(f"../plots/smearing/{variable}_1dhisto_smearing_{smearing_level}.png")
    plt.close()

def _hist_2d_plot(
        df,
        variable,
        smearing_level,
        binning,
):
    fig, ax = plt.subplots()
    sns.histplot(
        data=df,
        x=f"{variable}_true",
        y=f"{variable}_smeared",
        bins= (binning, binning),
        cmap="viridis",
        cbar=True,
        ax=ax
    )
    if (smearing_level == "antares"):
        ax.set_title(f"{plot_dict[variable]} at ANTARES-level Smearing")
    else:
        ax.set_title(f"{plot_dict[variable]} at {smearing_level} % Smearing")
    ax.set_xlabel(f"True {plot_dict[variable]}")
    ax.set_ylabel(f"Smeared {plot_dict[variable]}")

    if (variable == "energy"):
        ax.set_xlim([10, 100])
    else:
        ax.set_xlim([-1, 1])
    fig.tight_layout()
    fig.savefig(f"../plots/smearing/{variable}_2dhisto_smearing_{smearing_level}.png")
    plt.close()

def run_plots(
        df,
        smearing_level,
        variable,
):
    # Plotting
    print("\nStarting Plots")
    
    if variable == "energy":
        binning = np.linspace(0, 100, 15)
    else:
        binning = np.linspace(-1, 1, 15)
        
    # 1D Histograms
    print(f"Plotting 1D Histograms for {variable}")
    _hist_1d_plot(df, variable, smearing_level, binning)

    # 2D Histograms
    print(f"Plotting 2D Histograms for {variable}")
    _hist_2d_plot(df, variable, smearing_level, binning)

def main():
    # Define the path to the ROOT file
    path = "/sps/km3net/users/mchadoli/Swim/Data/events/"
    COLUMNS = [
            "energy_true",
            "cos_zenith_true",
            "energy_smeared",
            "cos_zenith_smeared", 
            ]
    
    for smearing_level in ["10", "50", "70", "100", "200", "500", "antares"]:
        print(f"\nRunning for smearing level {smearing_level} %")
        root_file = f"antares_smeared_{smearing_level}.root"

        # Load the ROOT file into a DataFrame
        df = libraries.load_large_rootfile_to_df(os.path.join(path, f"ANTARES_Smeared_{smearing_level}", root_file), columns=COLUMNS)

        # Run plots for each variable
        for variable in ["energy", "cos_zenith"]:
            run_plots(df, smearing_level, variable)

    print("Done!")

if __name__ == "__main__":
    main()