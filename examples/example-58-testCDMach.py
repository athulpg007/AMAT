from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import numpy as np
from scipy.interpolate import interp1d

planet = Planet("EARTH")
planet.loadAtmosphereModel("../atmdata/Earth/earth-gram-avg.dat", 0, 1, 2, 3)

vehicle1 = Vehicle("Apollo-AS-201-A", 5400.0, 400.0, 0.3, 12.0, 0.0, 3.0, planet)
vehicle2 = Vehicle("Apollo-AS-201-B", 5400.0, 400.0, 0.3, 12.0, 0.0, 3.0, planet, userDefinedCDMach=True)
vehicle3 = Vehicle("Apollo-AS-201-C", 5400.0, 400.0, 0.3, 12.0, 0.0, 3.0, planet, userDefinedCDMach=True)

# Example of user defined function for CD(M)
def f(M):
	return 0.9 + 0.5 * np.tanh(M - 1.0)

# Example of user defined function derived from look up table for Mach no. vs CD
xx = np.linspace(0,30,101) # replace with mach no. array, if needed
yy = f(xx)                 # replace with CD array, if needed

# create interpolation function
f_int = interp1d(xx, yy, kind="linear", fill_value=(xx[0], xx[-1]), bounds_error=False)

# vectorize interpolation function
def g(x):
	# return scalar for scalar input
	if np.size(x) == 1:
		return float(f_int(x))
	# return array for array input
	else:
		return f_int(x)

#set user-defined Mach number function
vehicle2.setCDMachFunction(f)
vehicle3.setCDMachFunction(g)

vehicle1.setInitialState(120.0, 0.0, 0.0, 7.67, 0.0, -9.03, 0.0, 0.0)
vehicle2.setInitialState(120.0, 0.0, 0.0, 7.67, 0.0, -9.03, 0.0, 0.0)
vehicle3.setInitialState(120.0, 0.0, 0.0, 7.67, 0.0, -9.03, 0.0, 0.0)

vehicle1.setSolverParams(1e-6)
vehicle2.setSolverParams(1e-6)
vehicle3.setSolverParams(1e-6)

vehicle1.propogateEntry(2400.0, 0.1, 60.0)
vehicle2.propogateEntry(2400.0, 0.1, 60.0)
vehicle3.propogateEntry(2400.0, 0.1, 60.0)

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))

plt.plot(vehicle1.v_kmsc, vehicle1.h_kmc, 'k',   linewidth=2.0, label='Vehicle1')
plt.plot(vehicle2.v_kmsc, vehicle2.h_kmc, 'r-',  linewidth=2.0, label='Vehicle2')
plt.plot(vehicle3.v_kmsc, vehicle3.h_kmc, 'b--', linewidth=2.0, label='Vehicle3')

plt.xlabel('Speed, km/s',fontsize=14)
plt.ylabel('Altitude, km', fontsize=14)
ax=plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
ax.tick_params(axis='x',labelsize=14)
ax.tick_params(axis='y',labelsize=14)
plt.legend(loc='upper left', fontsize=14)

plt.show()











