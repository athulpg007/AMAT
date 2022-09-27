from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import numpy as np
from scipy import interpolate
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon

# Set up the planet and atmosphere model.
planet=Planet("MARS")
planet.loadAtmosphereModel('../../../atmdata/Mars/mars-gram-avg.dat', 0 , 1 ,2, 3)
planet.h_skip = 120e3
planet.h_low=10.0E3

# Set up the drag modulation vehicle.
vehicle=Vehicle('MarsSmallSat1', 34, 20, 0.0, np.pi*1.5**2, 0.0, 0.1, planet)

vehicle.setInitialState(120.0, 88.15, -0.71, 5.3586, 9.3778,-9.25, 0.0,0.0)
vehicle.setSolverParams(1E-6)
vehicle.setDragModulationVehicleParams(20, 7.5)

# Set up the drag modulation entry phase guidance parameters.
vehicle.setDragEntryPhaseParams(2.0, 15.0, 101, -200.0)

# Set the target orbit parameters.
vehicle.setTargetOrbitParams(200.0, 2100.0, 20.0)

# Define the path to atmospheric files to be used for the Monte Carlo simulations.
atmfiles = ['../../../atmdata/Mars/LAT00N-N1000.txt']

# Set up the Monte Carlo simulation for drag modulation.
# NPOS = 156, NMONTE = 1000
# Target EFPA = -12.05 deg
# EFPA 1-sigma error = +/- 0.067 deg
# Nominal beta_1 = 66.4 kg/m2
# beta_1 1-sigma = 0.0
# guidance time step for entry = 1.0s (Freq. = 1 Hz)
# guidance time step after jettison = 1.0 s
# max. solver time step = 0.1 s
# max. time used by solver = 2400 s

vehicle.setupMonteCarloSimulationD(156, 1000, atmfiles, 0 , 1, 2, 3, 4, True,
                                   -9.25,  0.0666, 20.0, 0.0,
                                    1.0, 1.0, 0.1, 2400.0)
# Run 1000 trajectories
vehicle.runMonteCarloD2(1000, '../../../data/acta-astronautica/smallsat-mission-concepts/mars/MCB-Mars')
