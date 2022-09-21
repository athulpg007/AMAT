from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import numpy as np
from scipy import interpolate
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon

# Create a planet object
planet=Planet("VENUS")
planet.h_skip = 150000.0
planet.h_low=10.0E3

# Load an nominal atmospheric profile with height, temp, pressure, density data
planet.loadAtmosphereModel('../../../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)

# Set up a vehicle object
vehicle=Vehicle('SmallSat1', 37, 20, 0.0, 1.767, 0.0, 0.35, planet)
vehicle.setInitialState(150.0,-6.22,23.16,10.8191,89.9982,-5.30,0.0,0.0)
vehicle.setSolverParams(1E-6)
vehicle.setDragModulationVehicleParams(20, 7.5)

# Set up the drag modulation entry phase guidance parameters.
vehicle.setDragEntryPhaseParams(2.0, 20.0, 101, -200.0)

# Set the target orbit parameters.
vehicle.setTargetOrbitParams(200.0, 1800.0, 20.0)

# Define the path to atmospheric files to be used for the Monte Carlo simulations.
atmfiles = ['../../../atmdata/Venus/LAT20N.txt']

# Set up the Monte Carlo simulation for drag modulation.
# NPOS = 151, NMONTE = 200
# Target EFPA = -5.30 deg
# EFPA 1-sigma error = +/- 0.033 deg
# Nominal beta_1 = 20 kg/m2
# beta_1 1-sigma = 0.0
# guidance time step for entry = 1.0s (Freq. = 1 Hz)
# guidance time step after jettison = 1.0 s
# max. solver time step = 0.1 s
# max. time used by solver = 2400 s

vehicle.setupMonteCarloSimulationD(151, 200, atmfiles, 0 , 1, 2, 3, 4, True,
                                   -5.20,  0.0333, 20.0, 0.0,
                                    1.0, 1.0, 0.1, 2400.0)
# Run 1000 trajectories
vehicle.runMonteCarloD2(1000, '../../../data/acta-astronautica/smallsat-mission-concepts/venus/MCB-Venus')
