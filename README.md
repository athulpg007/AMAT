# AMAT

Aerocapture Mission Analysis Tool (AMAT) is designed to provide rapid mission analysis capability for aerocapture and Entry, Descent, and Landing (EDL) mission concepts to the planetary science community. AMAT was developed at the [Advanced Astrodynamics Concepts (AAC)](https://engineering.purdue.edu/AAC/) research group at Purdue University.


See [AMAT documentation](https://amat.readthedocs.io) for more details. 

[![Documentation Status](https://readthedocs.org/projects/amat/badge/?version=master)](https://amat.readthedocs.io/en/master/?badge=master) 


Please note the public release version has a minimal working interplanetary dataset to run some of the example Jupyter notebooks because of data sharing policies of external collaborators.

## Capabilities

AMAT allows the user to perform low-fidelity broad sweep parametric studies; as well as high fidelity Monte Carlo simulations to quantify aerocapture performance. AMAT supports analysis for all atmosphere-bearing destinations in the Solar System: Venus, Earth, Mars, Jupiter, Saturn, Titan, Uranus, and Neptune.

### Venus Aerocapture Trajectories
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/craig-lyne-altitude-higher-res-lower-size.png)
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/craig-lyne-heating-higher-res-lower-size.png)
### Neptune Aerocapture Feasibility Chart
![Neptune Aerocapture Feasibility](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2019b-higher-res-lower-size.png)
### Monte Carlo Simulations
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-fig-13-N5000.png)
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-apo-histogram-N5000.png)


## What kind of problems can AMAT solve?

AMAT can be used to quickly assess the feasibility of an aerocapture mission concept using aerocapture feasibiility charts, and perform trade studies involving vehicle type, control authority, thermal protection system materials, and useful delivered mass to orbit. AMAT can also be used to set up and run high-fidelity Monte Carlo simulations of aerocapture trajectories considering delivery errors, atmospheric uncertainties, and aerodynamic uncertainties to evaluate system performance under uncertainty.

### Examples

AMAT comes with a number of example [Jupyter notebooks](https://amat.readthedocs.io/en/master/jupyter_link.html) to help users get started. The examples inculde:

1. Venus aerocapture assesssment study
2. Titan aerocapture assessment study
3. Neptune aerocapture using blunt-body aeroshells
4. Drag modulation aerocapture asssessment
5. Planetary probe entry at various Solar System destinations

## Features

* Easy installation, only standard dependencies
* Many examples and recreation of results from published literature
* Extensive documented source code
* Can be used for probe and lander Entry, Descent, Landing (EDL) calculations
* Comes with a standard set of nominal atmospheric models

## Installation 

Note: AMAT is designed to work with Python 3.0 or greater. You must have a Python 3 installation in your system.

There are three ways to install AMAT. 

### Option 1 : Install from pip (recommended)

Note: Python Package Index limits the amount of additional data that can be packaged in the distribution, hence all data cannot be included in the built version. You will need to clone the GitHub repository to get the required data files, examples, and start using AMAT.

#### For Linux machines:
  * ```$ pip install AMAT```
  * ```$ git clone https://github.com/athulpg007/AMAT.git```

If you are unable to clone the repository, you can download the repository as a .zip file from GitHub and extract it.

Once AMAT is installed, run an example Jupyter notebook to check everything works correctly.
  * ```$ cd AMAT/examples```
  * ```$ jupyter-notebook```

Note that you will need jupyterlab and pandas (for some examples) to run the example notebooks. Use ```pip install jupyterlab pandas``` to install Jupyter and pandas if it is not already installed on your system. 


This will display the full list of example Jupyter notebooks included with AMAT.  Open and run the ```example-01-hello-world``` notebook to get started with AMAT.

#### For Windows machines:

You must have Anaconda installed. Open the Anaconda Prompt terminal:
  * ```$ pip install AMAT```

Open a Windows Powershell terminal and clone the GitHub reporistory. You must have Git installed.
  * ```$ git clone https://github.com/athulpg007/AMAT.git```

Run an example Jupyter notebook. From the Anaconda Prompt terminal:
  * ```$ cd AMAT/examples```
  * ```$ jupyter-notebook```

Note that you will need jupyterlab and pandas (for some examples) to run the example notebooks. Use ```pip install jupyterlab pandas``` to install Jupyter and pandas if it is not already installed on your system. 


This will display the full list of example Jupyter notebooks included with AMAT. Open and run the ```example-01-hello-world``` notebook to get started with AMAT.


### Option 2 : Install from source

This will clone the repository from GitHub and install AMAT from the source code.

#### For Linux machines:

Make sure you have numpy, scipy, matplotlib and pandas installed. Most likely you already have these installed. If not, use the following commands to install these dependenies first. Open a terminal window (on Linux machines) and type the following commands. You must have pip installed.
  * ```$ pip install numpy scipy matplotlib pandas jupyterlab```

Clone the GitHub repository and install AMAT.
  * ```$ git clone https://github.com/athulpg007/AMAT.git```
  * ```$ cd AMAT```
  * ```$ python setup.py install```
  * ```$ cd examples```
  * ```$ jupyter-notebook```

#### For Windows machines:

Open the Anaconda Prompt terminal to install the prerequisite packages.
  * ```$ pip install numpy scipy matplotlib```

Open a Windows Powershell terminal, clone the GitHub repository and install AMAT.
  * ```$ git clone https://github.com/athulpg007/AMAT.git```
  * ```$ cd AMAT```
  * ```$ python setup.py install```
  * ```$ cd examples```
  * ```$ jupyter-notebook```

Note that you will need jupyterlab and pandas (for some examples) to run the example notebooks. Use ```pip install jupyterlab pandas``` to install Jupyter and pandas if it is not already installed on your system. 


To uninstall AMAT:

1. If you installed AMAT using pip:
  * ```$ pip uninstall AMAT```

2. If you installed AMAT from source, from the main AMAT directory:
  * ```$ python setup.py develop -u```

This will remove the AMAT installation from Python. You may simply delete the root folder where AMAT was installed to completely remove the files.


### Option 3 : Install in a virutalenv

If you plan to modifty the source code or add features, the recommended option is to to install it in a virtual environment. 

1. Change directory to where you want the virtual environment to be created.
  * ```$ cd home/path```

2. Create a virutal environment and activate it.

On Linux machines:
  * ```$ python3 -m venv env1```
  * ```$ source env1/bin/activate```

On Windows machines (from Anaconda Prompt):
  * ```$ conda create --name env1```
  * ```$ conda activate env1```
  * ```$ conda install pip```

4. Follow the steps outlined in Option #2 (build from source) to clone the repository and install AMAT. If you make changes to the source code, remove the existing installation, update the setup file with a new version number, and re-install:
  * ```$ python setup.py develop -u```
  * ```$ python setup.py install```

If you want to create a new distrubution package:
  * ```$ python3 setup.py sdist bdist_wheel```

To re-make docs if you made changes to the source code (you must have Sphinx installed):
  * ```$ cd ~root/docs```
  * ```$ sphinx-apidoc -f -o source/ ../```
  * ```$ make html```

If you added a new AMAT module, appropriate changes must be made to docs/source/AMAT.rst.

## Usage

  * ```from AMAT.planet import Planet```
  * ```from AMAT.vehicle import Vehicle```
  * ```from AMAT.launcher import Launcher```

## License

AMAT is an open source project licensed under the CC-BY-SA-4.0 License

## Credits

Parts of the AMAT source code were originally developed in support of contracts between AAC and the Jet Propulsion Laboratory for various aerocapture mission studies between 2016 and 2020. Samples of atmospheric data from Global Reference Atmospheric Model (GRAM) software is used for illustration purpose only, and was developed by NASA Marshall Space Flight Center. The use of these GRAM models does not imply endorsement by NASA in any way whatsoever. A minimal working set of atmospheric profiles is included with AMAT to run the example notebooks. A minimal working interplanetary trajctory dataset is included with AMAT. The dataset was generated at Purdue University using the STOUR software package by Alec Mudek, and is also derived from trajectories published in the NASA Ice Giants Pre-Decadal Mission Study. The author plans to augment the interplanetary dataset with more publicly available information as it becomes available.

## Extras

The AMAT repository includes representative atmospheric profiles for Solar System bodies, an Excel sheet with a comprehensive literature review of aerocapture, sample feasibility charts for aerocapture at all destinations, reference journal articles (by the author), a PDF version of the documentation, and the author's Ph.D. dissertation which provides more details on the methods and algorithms implemented in AMAT.

## Reference Articles

Results from these articles are used as benchmark examples.

1. Craig, Scott, and James Evans Lyne. "Parametric Study of Aerocapture for Missions to Venus." Journal of Spacecraft and Rockets Vol. 42, No. 6, pp. 1035-1038. [DOI: 10.2514/1.2589](https://arc.aiaa.org/doi/10.2514/1.2589)

2. Putnam and Braun, "Drag-Modulation Flight-Control System Options for Planetary Aerocapture", Journal of Spacecraft and Rockets, Vol. 51, No. 1, 2014. [DOI:10.2514/1.A32589](https://arc.aiaa.org/doi/10.2514/1.A32589)

2. Lu, Ye, and Sarag J. Saikia. "Feasibility Assessment of Aerocapture for Future Titan Orbiter Missions." Journal of Spacecraft and Rockets Vol. 55, No. 5, pp. 1125-1135. [DOI: 10.2514/1.A34121](https://arc.aiaa.org/doi/10.2514/1.A34121)

3. Girija, A. P., Lu, Y., & Saikia, S. J. "Feasibility and Mass-Benefit Analysis of Aerocapture for Missions to Venus". Journal of Spacecraft and Rockets, Vol. 57, No. 1, pp. 58-73. [DOI: 10.2514/1.A34529](https://arc.aiaa.org/doi/10.2514/1.A34529)

4. Girija, A. P. et al. "Feasibility and Performance Analysis of Neptune
Aerocapture Using Heritage Blunt-Body Aeroshells", Journal of Spacecraft and Rockets, Vol. 57, No. 6, pp. 1186-1203. [DOI: 10.2514/1.A34719](https://arc.aiaa.org/doi/full/10.2514/1.A34719)