---
title: "AMAT: A Python package for rapid conceptual design of aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a Jupyter environment"
tags:
    - Python
    - aerocapture
    - atmospheric entry
    - mission design
    - planetary probe
authors:
    - name: Athul P. Girija
      orcid: 0000-0002-9326-3293
      affiliation: "1"
    - name: Sarag J. Saikia
      affiliation: "1"
    - name: James M. Longuski
      affiliation: "1"
    - name: James A. Cutts
      affiliation: "2"
affiliations:
    - name: School of Aeronautics and Astronautics, Purdue University, West Lafayette, IN 47907, United States
      index: 1
    - name: Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA 91109, United States
      index: 2
date: 01 August 2021
bibliography: paper.bib
---

# Summary
The Aerocapture Mission Analysis Tool (**AMAT**) is a free and open-source Python package for rapid conceptual design of aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a Jupyter environment. Compared to conventional propulsive insertion, aerocapture allows interplanetary spacecraft to accomplish a near-propellantless method of orbit insertion at any planetary destination with a signficant atmosphere. While aerocapture has been studied for many decades, to our knowledge, there are no publicly available tools for rapid conceptual design of aerocapture missions. AMAT aims to fill this gap by providing scientists and mission planners an interactive design tool to quickly evaluate aerocapture mission concepts, perform parametric trade space studies, and select a baseline mission concept for higher-fidelity analysis. Atmospheric Entry, Descent, and Landing (EDL) includes the hypersonic flight regime where the entry vehicle undergoes intense heating and rapid deceleration, followed by supersonic and subsonic flight, terminal descent phase, and final touchdown. AMAT comes with a suite of tools for rapid end-to-end conceptual design of aerocapture and EDL mission concepts at any atmosphere-bearing Solar System destination.

# Statement of Need

Software tools for identification of trajectories and techniqes that enhance or enable planetary missions or substantially reduce their cost is of great importance in realizing succesful exploration missions [@Squyres2011]. While there have been some aerocapture mission analysis tools developed in the past such as ACAPS [@Leszczynski1998] and HyperPASS [@mcronald2003analysis], these tools are propreitary, and not accessible to the general public. The NASA Ice Giants Pre-Decadal Mission Study in 2016, which studied mission concepts to Uranus and Neptune in the next decade highlighted the need for a design tool to evaluate aerocapture mission concepts [@Hofstadter2017]. A NASA-led study in 2016 to assess the readiness of aerocapture also underlined the need for an integrated aerocapture mission design tool which incorporated both interplanetary trajectory and vehicle design aspects [@Spilker2018]. While several software tools for conceptual design of EDL missions such as PESST [@otero2010planetary], TRAJ [@allen2005trajectory], and SAPE [@samareh2009multidisciplinary] have been developed in the past, these programs are not publicly available.  AMAT aims to fill this gap for scientists, engineers, and academic researchers who want to quickly perform aerocapture mission analysis and atmospheric EDL as part of mission concept studies. 


# Rapid Design Capability

AMAT can be used to compute aerocapture trajectories as well as key design parameters such as deceleration and stagnation-point heat rate using just a few lines of code. The example below computes the altitude profiles and stagnation-point heat rates for lift modulation aerocapture vehicle at Venus (based on [@Craig2005]).


```
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

# Create a planet object
planet=Planet("VENUS")

# Load an nominal atmospheric profile with height, temp, pressure, density data
planet.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)

# Create a vehicle object flying in the target planet atmosphere.
# with params m = 300 kg, beta = 78.0, L/D = 0.35, A = 3.1416, AoA = 0, RN = 1.54

# These values are taken from the reference article mentioned above.
vehicle=Vehicle('Apollo', 300.0, 78.0, 0.35, 3.1416, 0.0, 1.54, planet)

# h0 = 180 km, LON = 0 deg, LAT = 0 deg
# v0 = 12 km/s, HDG = 0 deg, FPA = 0 deg
# DOWNRANGE0 = 0 deg, HEATLOAD0 = 0.

# See help(vehicle) for more details.
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,-4.5,0.0,0.0)

# Set solver tolerance = 1E-6 (recommended value)
vehicle.setSolverParams(1E-6)

# Compute the overshoot and undershoot limit EFPA

# Set max. propogation time = 2400.0 secs.
# Set max. time step = 0.1 sec.
# Set low value for guess = -80.0 deg
# Set high value for guess = -4.0 deg
# Set EFPA tolerance = 1E-10 (recommended)
# Set target apoapsis = 407 km

# Compute limiting flight-path angles for overshoot and undershoot trajectories
overShootLimit, exitflag_os  = vehicle.findOverShootLimit (2400.0,0.1,-80.0,-4.0,1E-10,407.0)
underShootLimit,exitflag_us  = vehicle.findUnderShootLimit(2400.0,0.1,-80.0,-4.0,1E-10,407.0)

# Reset initial conditions and propogate overshoot trajectory
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,overShootLimit,0.0,0.0)
vehicle.propogateEntry (2400.0,0.1,180.0)

# Extract and save variables to plot
t_min_os         = vehicle.t_minc
h_km_os          = vehicle.h_kmc
acc_net_g_os     = vehicle.acc_net_g
q_stag_con_os    = vehicle.q_stag_con
q_stag_rad_os    = vehicle.q_stag_rad

# Reset initial conditions and propogate overshoot trajectory
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,overShootLimit,0.0,0.0)
vehicle.propogateEntry (2400.0,0.1,180.0)

# Extract and save variables to plot
t_min_os         = vehicle.t_minc
h_km_os          = vehicle.h_kmc
acc_net_g_os     = vehicle.acc_net_g
q_stag_con_os    = vehicle.q_stag_con
q_stag_rad_os    = vehicle.q_stag_rad

# Reset initial conditions and propogate undershoot trajectory
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,underShootLimit,0.0,0.0)
vehicle.propogateEntry (2400.0,0.1,0.0)

# Extract and save variable to plot
t_min_us         = vehicle.t_minc
h_km_us          = vehicle.h_kmc
acc_net_g_us     = vehicle.acc_net_g
q_stag_con_us    = vehicle.q_stag_con
q_stag_rad_us    = vehicle.q_stag_rad

plt.plot(t_min_os , h_km_os, linestyle='solid' , color='xkcd:blue',linewidth=2.0,  label='Overshoot')
plt.plot(t_min_us , h_km_us, linestyle='solid' , color='xkcd:green',linewidth=2.0,  label='Undershoot')

plt.plot(t_min_os , q_stag_con_os,  label='Overshoot convective')
plt.plot(t_min_os , q_stag_rad_os,  label='Overshoot radiative')
plt.plot(t_min_us , q_stag_con_us,  label='Undershoot convective')
plt.plot(t_min_us , q_stag_rad_us,  label='Undershoot radiative')

```




# AMAT Modules

# Example Jupyter Notebooks

# Acknowledgements

# References


