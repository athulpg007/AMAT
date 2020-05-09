from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os


# Create a planet object
planet=Planet("VENUS")    

# Load an nominal atmospheric profile with height, temp, pressure, density data
planet.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)

planet.h_skip = 150000.0 
# Create a vehicle object flying in the target planet atmosphere
vehicle=Vehicle('DMVehicle', 1500.0, 50.0, 0.0, 3.1416, 0.0, 0.10, planet)

# Set vehicle conditions at entry interface
vehicle.setInitialState(150.0,0.0,0.0,11.0,0.0,-4.5,0.0,0.0)
vehicle.setSolverParams(1E-6)

VAI_array = np.linspace(11,14,7)
BR_array  = np.array([2.0,5.0,10.0,20.0])

os.makedirs('../data/putnamBraun2013')

np.savetxt('../data/putnamBraun2013/VAI_array.txt',VAI_array)	
np.savetxt('../data/putnamBraun2013/BR_array.txt' , BR_array)

TCW_array1 = np.zeros((len(VAI_array),len(BR_array))) 
TCW_array2 = np.zeros((len(VAI_array),len(BR_array))) 

beta11 = 5.0
beta12 = 10.0


print('Running beta1=5.0')

for i in range(0,len(VAI_array)):
	for j in range(0,len(BR_array)):
		vehicle.setInitialState(150.0,0.0,0.0,VAI_array[i],0.0,-4.5,0.0,0.0)
		vehicle.setDragModulationVehicleParams(beta11,BR_array[j])
		TCW_array1[i,j] = vehicle.computeTCWD(2400.0, 0.1,-80.0,-4.0,1E-10,400.0)
		print('VAI: '+str(VAI_array[i])+' km/s, BETA RATIO: '+str(BR_array[j])+' TCW: '+str(TCW_array1[i,j])+' deg.')

np.savetxt('../data/putnamBraun2013/TCW_array1.txt', TCW_array1)

print('Running beta1=10.0')
for i in range(0,len(VAI_array)):
	for j in range(0,len(BR_array)):
		vehicle.setInitialState(150.0,0.0,0.0,VAI_array[i],0.0,-4.5,0.0,0.0)
		vehicle.setDragModulationVehicleParams(beta12,BR_array[j])
		TCW_array2[i,j] = vehicle.computeTCWD(2400.0, 0.1,-80.0,-4.0,1E-10,400.0)
		print('VAI: '+str(VAI_array[i])+' km/s, BETA RATIO: '+str(BR_array[j])+' TCW: '+str(TCW_array2[i,j])+' deg.')

np.savetxt('../data/putnamBraun2013/TCW_array2.txt', TCW_array2)
print('Done!')


VAI_array  = np.loadtxt('../data/putnamBraun2013/VAI_array.txt')
BR_array   = np.loadtxt('../data/putnamBraun2013/BR_array.txt')
TCW_array1 = np.loadtxt('../data/putnamBraun2013/TCW_array1.txt')
TCW_array2 = np.loadtxt('../data/putnamBraun2013/TCW_array2.txt')

fig = plt.figure()
fig.set_size_inches([3.25,3.25])
plt.rc('font',family='Times New Roman')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)

plt.plot(VAI_array, TCW_array1[:,0], linestyle='-', linewidth=0.75, marker='s',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array1[:,1], linestyle='-', linewidth=0.75, marker='^',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array1[:,2], linestyle='-', linewidth=0.75, marker='o',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array1[:,3], linestyle='-', linewidth=0.75, marker='v',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)

plt.plot(VAI_array, TCW_array2[:,0], linestyle='--', linewidth=0.75, marker='s',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array2[:,1], linestyle='--', linewidth=0.75, marker='^',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array2[:,2], linestyle='--', linewidth=0.75, marker='o',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)
plt.plot(VAI_array, TCW_array2[:,3], linestyle='--', linewidth=0.75, marker='v',ms=6, markerfacecolor="None", markeredgecolor='black', markeredgewidth=0.75, color='black', clip_on=False)

plt.xlabel('Entry velocity, km/s', fontsize=10)
plt.ylabel('Corridor width, deg',fontsize=10)
plt.yticks(np.arange(0, 0.9, step=0.2))
plt.xticks(np.arange(11.0, 14.5, step=1.0))

plt.xlim([11.0,14.0])
plt.ylim([0.0,  0.8])

ax = plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
plt.tick_params(direction='in')
plt.tick_params(axis='x',labelsize=10)
plt.tick_params(axis='y',labelsize=10)


plt.savefig('../plots/putnam-braun-2013.png',bbox_inches='tight')
plt.savefig('../plots/putnam-braun-2013.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/putnam-braun-2013.eps', dpi=300,bbox_inches='tight')

plt.show()