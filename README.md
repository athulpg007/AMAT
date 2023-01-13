# AMAT

Aerocapture Mission Analysis Tool (AMAT) is designed to provide rapid mission 
analysis capability for aerocapture and atmospheric Entry, Descent, and Landing (EDL) 
mission concepts to the planetary science community. AMAT was developed at the 
[Advanced Astrodynamics Concepts (AAC)](https://engineering.purdue.edu/AAC/) 
research group at Purdue University.

See [AMAT documentation](https://amat.readthedocs.io) for more details. 

[![Documentation Status](https://readthedocs.org/projects/amat/badge/?version=master)](https://amat.readthedocs.io/en/master/?badge=master) [![DOI](https://joss.theoj.org/papers/10.21105/joss.03710/status.svg)](https://doi.org/10.21105/joss.03710) [![PyPI version](https://badge.fury.io/py/AMAT.svg)](https://badge.fury.io/py/AMAT)

If you find AMAT useful in your work, please consider citing us: 
Girija et al., (2021). AMAT: A Python package for rapid conceptual design of 
aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a 
Jupyter environment. *Journal of Open Source Software*, 6(67), 3710, 
[DOI: 10.21105/joss.03710](https://doi.org/10.21105/joss.03710)


## Capabilities

AMAT allows the user to simulate atmospheric entry trajectories, compute deceleration
and heating loads, compute aerocapture entry corridors and simulate aerocapture 
trajectories. AMAT supports analysis for all atmosphere-bearing destinations 
in the Solar System: Venus, Earth, Mars, Jupiter, Saturn, Titan, Uranus, and Neptune.
AMAT allows the calculation of launch performance for a set of launch vehicles. 
AMAT allows the calculation of V-inf vector from a Lambert arc for an interplanetary
transfer. AMAT allows calculation of planetary approach trajectories for orbiters and entry 
systems from a given V_inf vector, B-plane targeting, and deflection maneuvers. 
AMAT allows the calculation of visibility of landers to Earth and relay orbiters
and compute telecom link budgets. 

### Venus Aerocapture Trajectories
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/craig-lyne-altitude-higher-res-lower-size.png)
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/craig-lyne-heating-higher-res-lower-size.png)
### Neptune Aerocapture Feasibility Chart
![Neptune Aerocapture Feasibility](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2019b-higher-res-lower-size.png)
### Monte Carlo Simulations
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-fig-13-N5000.png)
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-apo-histogram-N5000.png)


### Examples

AMAT comes with a number of example 
[Jupyter notebooks](https://amat.readthedocs.io/en/master/jupyter_link.html) to help users get started. The examples inculde:

1. Venus aerocapture assesssment study
2. Titan aerocapture assessment study
3. Neptune aerocapture using blunt-body aeroshells
4. Drag modulation aerocapture asssessment
5. Planetary probe entry at various Solar System destinations

## Features

* Easy installation,
* Many examples and recreation of results from published literature
* Extensive documented source code
* Can be used for probe and lander Entry, Descent, Landing (EDL) calculations
* Comes with a standard set of nominal atmospheric models

## Installation 

Note: AMAT is currently supported on Python ``3.8``, ``3.9``, and ``3.10``.

There are two ways to install AMAT. 

### Option 1: Install from pip (recommended for most users)

This is the recommended method if you do not plan or need to make changes 
to the source code.

Note: Python Package Index limits the amount of additional data that can be 
packaged in the distribution, hence all data cannot be included in the built version. 
You will need to clone the GitHub repository to get the required 
data files, examples, and start using AMAT.

Create a virtual environment and activate it. It is strongly recommended you install
AMAT inside a virtual environment to prevent it from affecting your global python
packages. 

Change directory to where you want the virtual environment to be created.
  * ```$ cd home/path```

#### On Linux/MacOS machines:
  * ```$ python3 -m venv env1```
  * ```$ source env1/bin/activate```

####On Windows machines (from Anaconda Prompt):
  * ```$ conda create --name env1```
  * ```$ conda activate env1```
  * ```$ conda install pip```

#### Clone the repository and install AMAT:
  * ```$ git clone https://github.com/athulpg007/AMAT.git```
  * ```$ pip install AMAT```
  

Once AMAT is installed, run an example Jupyter notebook to check everything works correctly.
  * ```$ cd AMAT/examples```
  * ```$ jupyter-notebook```

Note that you will need jupyterlab and pandas (for some examples) to run 
the example notebooks. Use ```pip install jupyterlab pandas``` to 
install Jupyter and pandas if it is not already installed on your system. 
This will display the full list of example Jupyter notebooks included with AMAT.  
Open and run the ```example-01-hello-world``` notebook to get started with AMAT.

### Option 2: Install from setup.py (recommended for developers)

This is the recommended method if you need to make changes to the source code.

Create a virtual environment and activate it 
following the steps at the beginning of Option 1.

Clone the GitHub repository and install AMAT using setup.py. The -e editable 
flag allows changes you make to take effect when using AMAT.
  * ```$ git clone https://github.com/athulpg007/AMAT.git```
  * ```$ cd AMAT```
  * ```$ python setup.py install -e```
  * ```$ cd examples```
  * ```$ jupyter-notebook```
  

Note that you will need jupyterlab and pandas (for some examples) 
to run the example notebooks. Use ```pip install jupyterlab pandas``` 
to install Jupyter and pandas if it is not already installed on your system. 


If you want to create a new distribution package:
  * ```$ python3 setup.py sdist bdist_wheel```

To build docs locally if you made changes to the source code 
(you must have the dependencies in ```docs/requirements.txt``` installed):
  * ```$ cd AMAT/docs```
  * ```$ make html```
  
## License

AMAT is an open source project licensed under the GNU General 
Public License Version 3.

## Credits

Parts of the AMAT source code were originally developed in support of contracts between AAC and the Jet Propulsion Laboratory for various aerocapture mission studies between 2016 and 2020. Samples of atmospheric data from Global Reference Atmospheric Model (GRAM) software is used for illustration purpose only, and was developed by NASA Marshall Space Flight Center. The use of these GRAM models does not imply endorsement by NASA in any way whatsoever. A minimal working set of atmospheric profiles is included with AMAT to run the example notebooks. A minimal working interplanetary trajctory dataset is included with AMAT. The dataset was generated at Purdue University using the STOUR software package by Alec Mudek, and is also derived from trajectories published in the NASA Ice Giants Pre-Decadal Mission Study. The author plans to augment the interplanetary dataset with more publicly available information as it becomes available.

## Support and Contribution

If you wish to contribute or report an issue, feel free to [contact me](mailto:athulpg007@gmail.com) or to use the [issue tracker](https://github.com/athulpg007/AMAT/issues) and [pull requests](https://github.com/athulpg007/AMAT/pulls) from the [code repository](https://github.com/athulpg007/AMAT).

If you wish to make a contribution, you can do as follows:

 * fork the GitHub repository 
 * create a feature branch from *master* 
 * add your feature and document it
 * add tests to verify your feature is implemented correctly
 * run all the tests to verify your change does not break something else
 * open a pull request

## Extras

The AMAT repository includes representative atmospheric profiles for 
Solar System bodies, an Excel sheet with a comprehensive literature review of 
aerocapture, sample feasibility charts for aerocapture at all destinations, 
reference journal articles (by the author).

## Reference Articles

Results from these articles are used as benchmark examples.

1. Craig, Scott, and James Evans Lyne. "Parametric Study of Aerocapture for Missions to Venus." Journal of Spacecraft and Rockets Vol. 42, No. 6, pp. 1035-1038. [DOI: 10.2514/1.2589](https://arc.aiaa.org/doi/10.2514/1.2589)

2. Putnam and Braun, "Drag-Modulation Flight-Control System Options for Planetary Aerocapture", Journal of Spacecraft and Rockets, Vol. 51, No. 1, 2014. [DOI:10.2514/1.A32589](https://arc.aiaa.org/doi/10.2514/1.A32589)

3. Lu, Ye, and Sarag J. Saikia. "Feasibility Assessment of Aerocapture for Future Titan Orbiter Missions." Journal of Spacecraft and Rockets Vol. 55, No. 5, pp. 1125-1135. [DOI: 10.2514/1.A34121](https://arc.aiaa.org/doi/10.2514/1.A34121)

4. Girija, A. P., Lu, Y., & Saikia, S. J. "Feasibility and Mass-Benefit Analysis of Aerocapture for Missions to Venus". Journal of Spacecraft and Rockets, Vol. 57, No. 1, pp. 58-73. [DOI: 10.2514/1.A34529](https://arc.aiaa.org/doi/10.2514/1.A34529)

5. Girija, A. P. et al. "Feasibility and Performance Analysis of Neptune
Aerocapture Using Heritage Blunt-Body Aeroshells", Journal of Spacecraft and Rockets, Vol. 57, No. 6, pp. 1186-1203. [DOI: 10.2514/1.A34719](https://arc.aiaa.org/doi/full/10.2514/1.A34719)

6. Girija A. P. et al. "Quantitative Assessment of Aerocapture and Applications to Future Missions", Journal of Spacecraft and Rockets, 2022.
[DOI: 10.2514/1.A35214](https://arc.aiaa.org/doi/full/10.2514/1.A35214)