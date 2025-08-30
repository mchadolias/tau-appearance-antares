# Tau Neutrino Appearance with ANTARES

## 📖 Overview

An open-source repository containing the SWIM-based analysis for a feasibility study of tau-neutrino appearance measurements with the ANTARES neutrino telescope. This repository accompanies the Master's thesis from FAU Erlangen-Nuremberg, supervised by PD Dr. Thomas Eberl.

---

## 📂 Repository Structure

The repository is organized into modules, each addressing a different step of the analysis:

```markdown
├── README.md <- Overview of the project, setup instructions, and usage.
│
├── LICENSE <- Open-source license for this repository.
|
├── libraries <- Collection of custom functions and classes for data handling and analysis.
│
├── ReconstructionPerformance <- Scripts to evaluate reconstruction performance,
│                              comparing AntDSTs and NNFit outputs.
│
├── CanDimension <- Scripts to add required 3D coordinate vectors to data
│                samples for constructing the detector response matrix.
│
├── Chi2Profile <- Scripts to compute χ² profiles with smeared and
│               unsmeared datasets using the SWIM framework.
│
├── Smearing <- Contains smearing strategies (flat-based, performance-based)
│             and NNFit parameterizations for reconstruction.
│
└── Plotter <- Contains plotter.py for visualizing χ² profiles 
              and significance results.
```

## ⚙️ Requirements

- **[SWIM](https://git.km3net.de/oscillation/Swim)** –  C++ framework for neutrino oscillation analyses and sensitivity studies.  
- Python 3.8+ with standard scientific libraries:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `pandas`
  - `h5py`
  - `pyyaml`
  - `tabulate`
  - `tqdm`
  - `json`

---

## 🚀 Quick Start

Clone the repository:

```bash
git clone https://github.com/mchadolias/tau-appearance-antares.git
cd tau-appearance-antares

```

Install SWIM:

```bash
git clone https://git.km3net.de/oscillation/Swim.git
cd Swim
mkdir build
cd build
cmake ..
make
```

Run the analysis based on the submission bash script:

```bash
./Chi2Profile/submit_full_no_systematics.sh
```

The results will be stored in the `output` directory.

---

## 📝 License

This repository is distributed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Special thanks to the **ANTARES Collaboration** for providing the data used in this study and the **KM3NeT Collaboration** for the SWIM framework. Further acknowledgments are in the section of the masters thesis.

---

## 📖 References

- [SWIM](https://git.km3net.de/oscillation/Swim)
- [ANTARES](https://antares.in2p3.fr/)
- [KM3NeT](https://www.km3net.org/)
- [Master's Thesis](https://ecap.nat.fau.de/wp-content/uploads/2025/03/MSc_MichailChadolias_ANTARES_TauAppearance.pdf)
- [ECAP](https://ecap.nat.fau.de/)
