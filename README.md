# AMAT

Aerocapture Mission Analysis Tool (AMAT) is designed to provide rapid mission analysis capability for aerocapture mission concepts to the planetary science community. 

## Capabilities

AMAT allows the user to peform low-fidelity broad sweep parametric studies; as well as high fidelity Monte Carlo simulations to quantify aerocapture performance. AMAT supports analysis for all atmosphere-bearing destinations in the Solar System except Jupiter and Saturn where aerocapture is not feasible in the near-future. AMAT includes a database of interplanetary trajectories to Venus, Uranus, and Neptune for quick reference.

### Venus Aerocapture Trajectories
![Venus Aerocapture Trajectories](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/craig-lyne-altitude.png)
### Neptune Aerocapture Feasibility Chart
![Neptune Aerocapture Feasibility](https://raw.githubusercontent.com/athulpg007/AMAT/master/plots/girijaSaikia2019b.png)
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
* Comes with a standard set of nominal atmospheric models and interplanetary trajectory catalog

## Installation 

$ pip install AMAT

## Usage

from AMAT.planet import Planet

from AMAT.vehicle import Vehicle

## License
AMAT is an open source project licensed under the CC-BY-SA-4.0 License

## Credits
AMAT was developed at the School of Aeronautics and Astronautics at Purdue University with partial support from the NASA Jet Propulsion Laboratory under Contract Number 108436. Samples of atmospheric data from Global Reference Atmospheric Model (GRAM) software is used for illustration purpose only, and was developed by NASA Marshall Space Flight Center. Interplanetary trajctory data was generated at Purdue University using the STOUR software package by Alec Mudek. The aerocapture feasibility charts were first conceived by Ye Lu at Purdue University, and then expanded upon by the author. 

The current version is a test release and is under active development and testing. Some portions of the code may not conform to PEP-8 standards, this will be rectified in a future release.

## Reference Articles

Results from these articles are used as benchmark examples.

1. Craig, Scott, and James Evans Lyne. "Parametric Study of Aerocapture for Missions to Venus." Journal of Spacecraft and Rockets Vol. 42, No. 6, pp. 1035-1038.

2. Lu, Ye, and Sarag J. Saikia. "Feasibility Assessment of Aerocapture for Future Titan Orbiter Missions." Journal of Spacecraft and Rockets Vol. 55, No. 5, pp. 1125-1135.

3. Girija, A. P., Lu, Y., & Saikia, S. J. Feasibility and Mass-Benefit Analysis of Aerocapture for Missions to Venus. Journal of Spacecraft and Rockets, Vol. 57, No. 1, pp. 58-73.

4. Girija, A. P., "A Unified Framework for Aerocapture Systems Analysis, AAS 19-811, 2019 AAS/AIAA Astrodynamics Specialist Conference, Portland, ME.

5. Girija, A. P. et al. "Feasibility and Performance Analysis of Neptune
Aerocapture Using Heritage Blunt-Body Aeroshells", Journal of Spacecraft and Rockets, under review.