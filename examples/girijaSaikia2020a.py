from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import numpy as np
from scipy import interpolate
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import Polygon

# Create a planet object
planet=Planet("NEPTUNE")

# Load an nominal atmospheric profile with height, temp, pressure, density data
planet.loadAtmosphereModel('../atmdata/Neptune/neptune-gram-avg.dat', 0 , 7 , 6 , 5 , \
							heightInKmFlag=True)

# Create a vehicle object
vehicle=Vehicle('Trident', 1000.0, 200.0, 0.40, 3.1416, 0.0, 1.00, planet)

# Set vehicle conditions at entry interface
vehicle.setInitialState(1000.0, 0.0, 0.0, 28.00, 0.0,-13.85, 0.0, 0.0)
vehicle.setSolverParams(1E-6)

#vehicle.createQPlot(200,0.1,0.0)

vehicle.setMaxRollRate(30.0)
vehicle.setEquilibriumGlideParams(75.0, 3.0, 18.9, 120.0, 101, -500.0)
vehicle.setTargetOrbitParams(4000.0, 400.0E3, 10.0E3)

atmfiles = ['../atmdata/Neptune/FMINMAX-10L.txt', 
			'../atmdata/Neptune/FMINMAX-08L.txt',
			'../atmdata/Neptune/FMINMAX-06L.txt',  
			'../atmdata/Neptune/FMINMAX-04L.txt',
			'../atmdata/Neptune/FMINMAX-02L.txt',
			'../atmdata/Neptune/FMINMAX+00L.txt',  
			'../atmdata/Neptune/FMINMAX+02L.txt',
			'../atmdata/Neptune/FMINMAX+04L.txt',
			'../atmdata/Neptune/FMINMAX+06L.txt',
			'../atmdata/Neptune/FMINMAX+08L.txt', 
			'../atmdata/Neptune/FMINMAX+10L.txt']

vehicle.setupMonteCarloSimulation(1086, 200, atmfiles, 0, 1, 2, 3, 4, True, \
								 -13.85, 0.11, 0.40, 0.013, 0.5, 0.1, 2400.0) 

vehicle.runMonteCarlo(100, '../data/girijaSaikia2020a/MCB1') 

peri  = np.loadtxt('../data/girijaSaikia2020a/MCB1/terminal_periapsis_arr.txt')
apoa  = np.loadtxt('../data/girijaSaikia2020a/MCB1/terminal_apoapsis_arr.txt')

peri_dv  = np.loadtxt('../data/girijaSaikia2020a/MCB1/periapsis_raise_DV_arr.txt')

del_index1 = np.where(apoa < 0)
del_index2 = np.where(apoa>800.0E3)

del_index = np.concatenate((del_index1, del_index2), axis=1)

print('Simulation statistics')
print('----------------------------------------------')
print("No. of cases escaped :"+str(len(del_index1[0])))
print("No. of cases with apo. alt > 800.0E3 km :"+str(len(del_index2[0])))




peri_new = np.delete(peri, del_index)
apoa_new = np.delete(apoa, del_index)
peri_dv_new  = np.delete(peri_dv, del_index)


fig = plt.figure()
fig.set_size_inches([3.25,3.25])
plt.rc('font',family='Times New Roman')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.plot(peri_new, apoa_new/1000.0, 'bo', markersize=3)

plt.xlabel('Periapsis altitude, km',fontsize=10)
plt.ylabel('Apoapsis altitude x '+r'$10^3$'+', km', fontsize=10)

plt.axhline(y=350.0, linewidth=1, color='k', linestyle='dotted')
plt.axhline(y=450.0, linewidth=1, color='k', linestyle='dotted')



ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=10)
ax.tick_params(axis='y',labelsize=10)

plt.savefig('../plots/girijaSaikia2020a-fig-15-N100.png',bbox_inches='tight')
plt.savefig('../plots/girijaSaikia2020a-fig-15-N100.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/girijaSaikia2020a-fig-15-N100.eps', dpi=300,bbox_inches='tight')

fig = plt.figure()
fig.set_size_inches([3.25,3.25])
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['DejaVu Sans']
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)	

plt.hist(peri_dv_new, bins=100, color='xkcd:periwinkle')
plt.xlabel('Periapse raise '+r'$\Delta V$'+', m/s', fontsize=10)
plt.ylabel('Number of cases', fontsize=10)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=10)
ax.tick_params(axis='y',labelsize=10)

plt.savefig('../plots/girijaSaikia2020a-prm-histogram.png',bbox_inches='tight')
plt.savefig('../plots/girijaSaikia2020a-prm-histogram.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/girijaSaikia2020a-prm-histogram.eps', dpi=300,bbox_inches='tight')



plt.show()


