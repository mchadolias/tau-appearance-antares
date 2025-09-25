import scienceplots
import matplotlib.pyplot as plt

def _set_style(
        file,
):
    if file == "notebook":
        plt.style.use(['science',"grid","notebook","bright"])
    else:
        plt.style.use(['science',"grid","bright", "no-latex"])


def _set_size():
    plt.rcParams.update({
        "figure.figsize": (8, 6),
        "font.size": 14,
        "font.family": "serif",
        "lines.linewidth": 2,
        "lines.markersize": 5,
        "axes.titlesize": 16,
        "axes.labelsize": 15,
        "legend.fontsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    })

def customize_style(
        file,
):
    _set_style(file)
    _set_size()
