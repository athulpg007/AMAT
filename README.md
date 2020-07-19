# AMAT

Aerocapture Mission Analysis Tool (AMAT) is designed to provide rapid mission analysis capability for aerocapture and Entry, Descent, and Landing (EDL) mission concepts to the planetary science community. 

See [AMAT documentation](https://amat.readthedocs.io) for more details. 

## Capabilities

AMAT allows the user to perform low-fidelity broad sweep parametric studies; as well as high fidelity Monte Carlo simulations to quantify aerocapture performance. AMAT supports analysis for all atmosphere-bearing destinations in the Solar System: Venus, Earth, Mars, Jupiter, Saturn, Titan, Uranus, and Neptune.

### Venus Aerocapture Trajectories
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/a1.png)
![Venus Aerocapture Trajectory and Heating](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/a2.png)
### Neptune Aerocapture Feasibility Chart
![Neptune Aerocapture Feasibility](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2019b-higher-res-lower-size.png)
### Monte Carlo Simulations
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-fig-13-N5000.png)
![Monte Carlo Simulations](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2020b-apo-histogram-N5000.png)


## What kind of problems can AMAT solve?

AMAT can be used to quickly assess the feasibility of an aerocapture mission concept using aerocapture feasibiility charts, and perform trade studies involving vehicle type, control authority, thermal protection system materials, and useful delivered mass to orbit.

### Examples

1. Venus Aerocapture Assesssment
2. Titan Aerocapture Assessment
3. Neptune Aerocapture Using Blunt-Body Aeroshells

## Features

* Easy installation, only standard dependencies
* Many examples and recreation of results from published literature
* Extensive documented source code
* Can be used for probe and lander Entry, Descent, Landing (EDL) calculations
* Comes with a standard set of nominal atmospheric models

## Installation 

Note: AMAT is designed to work with Python 3.0 or greater. You must have a Python 3 installation in your system.

There are three ways to install AMAT. 

### Option 1 : Install from source (recommended)

This allows you to download the "entire" package (with the required data files to run examples).

1. Make sure you have numpy, scipy, matplotlib and pandas installed. Most likely you already have these installed. If not, use the following commands to install these dependenies first. Open a terminal window (on Linux/Mac machines) and type the following commands. You must have pip installed.

  * ``` $ pip install numpy ``` 
  * ``` $ pip install scipy ```
  * ``` $ pip install matplotlib ```
  * ``` $ pip install pandas ```

On Windows machines, the recommended option is to use Anaconda or Canopy package manager to install these packages.

2. Navigate to the directory where you want AMAT to be installed. Open a terminal (or command window) and use the folllowing command:

  * ``` $ cd home/path ```

where home/path is to be replaced with the path to the folder where AMAT will be installed. 

3. Clone the github repository using the following command. You must have git installed.

  * ```$ git clone https://github.com/athulpg007/AMAT.git```

If you do not have git installed, you can download a .zip file from the github page and extract it. Copy the entire uncompressed folder into the directory where you want AMAT to be installed.

4. Change directory to AMAT and install package.

  * ```$ cd AMAT```
  * ```$ python setup.py install```

5. Check that you have the required data files. For example, in the root folder where AMAT is installed, you should see a folder names atmdata with data for various planets.

6. Run an example script to check everything is working.

  * ``$ cd examples``
  * ``$ ipython``
  * ``$ run example-01-hello-world.py``

7. Run example Jupyter notebooks

  * ``jupyter-notebook``

To uninstall AMAT, use

  * ``python setup.py develop -u``

This will remove the AMAT installation from Python. You may simply delete the root folder where AMAT was installed to completely remove the files.

### Option 2 : Install from pip (NOT recommended)

This allows you to download the package, but without most of the data files. You can run the program, but will need to visit the git repository later to download some of the data files and place them in an appropriate location. You will also need to change the location of data files in the example scripts if you use them.

Python Package Index limits the amount of additional data that can be packaged in the distribution, hence all data cannot be included in the built version.

  * ```$ pip install AMAT```

### Option 3 : Install in a virutalenv (for developers)

If you plan to test or develop the package, the recommended option is to to install it in a virtual environment. This allows you to discard changes and start afresh without having to do a system-wide installation.

1. Change directory to where you want the virtual environment to be created.

  * ```$ cd home/path```

2. Create a virutal environment and activate it.

  * ```$ python3 -m venv env1```
  * ```$ source env1/bin/activate```

3. Change directory to env1

  * ```$ cd env1```

4. Follow steps 1 through 5 in Option #1 : Install from source.


## Usage

  * ```from AMAT.planet import Planet```
  * ```from AMAT.vehicle import Vehicle```

## License
AMAT is an open source project licensed under the CC-BY-SA-4.0 License

## Credits
AMAT was developed at the School of Aeronautics and Astronautics at Purdue University. Samples of atmospheric data from Global Reference Atmospheric Model (GRAM) software is used for illustration purpose only, and was developed by NASA Marshall Space Flight Center. Interplanetary trajctory data was generated at Purdue University using the STOUR software package by Alec Mudek. 

## Reference Articles

Results from these articles are used as benchmark examples.

1. Craig, Scott, and James Evans Lyne. "Parametric Study of Aerocapture for Missions to Venus." Journal of Spacecraft and Rockets Vol. 42, No. 6, pp. 1035-1038.

2. Lu, Ye, and Sarag J. Saikia. "Feasibility Assessment of Aerocapture for Future Titan Orbiter Missions." Journal of Spacecraft and Rockets Vol. 55, No. 5, pp. 1125-1135.

3. Girija, A. P., Lu, Y., & Saikia, S. J. Feasibility and Mass-Benefit Analysis of Aerocapture for Missions to Venus. Journal of Spacecraft and Rockets, Vol. 57, No. 1, pp. 58-73.

4. Girija, A. P., "A Unified Framework for Aerocapture Systems Analysis, AAS 19-811, 2019 AAS/AIAA Astrodynamics Specialist Conference, Portland, ME.

5. Girija, A. P. et al. "Feasibility and Performance Analysis of Neptune
Aerocapture Using Heritage Blunt-Body Aeroshells", Journal of Spacecraft and Rockets, under review.