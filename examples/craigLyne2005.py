from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

import matplotlib.pyplot as plt
from matplotlib import rcParams

# Create a planet object
planet=Planet("VENUS")    

# Load an nominal atmospheric profile with height, temp, pressure, density data
planet.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)

# Create a vehicle object flying in the target planet atmosphere
vehicle=Vehicle('Apollo', 300.0, 78.0, 0.35, 3.1416, 0.0, 1.54, planet)

# Set vehicle conditions at entry interface
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,-4.5,0.0,0.0)
vehicle.setSolverParams(1E-6)
# Compute the overshoot and undershoot limit EFPA
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

# Reset initial conditions and propogate undershoot trajectory
vehicle.setInitialState(180.0,0.0,0.0,12.0,0.0,underShootLimit,0.0,0.0)
vehicle.propogateEntry (2400.0,0.1,0.0)

# Extract and save variable to plot
t_min_us         = vehicle.t_minc
h_km_us          = vehicle.h_kmc
acc_net_g_us     = vehicle.acc_net_g
q_stag_con_us    = vehicle.q_stag_con
q_stag_rad_us    = vehicle.q_stag_rad

'''
Create fig #1 - altitude history of aerocapture maneuver
'''

fig = plt.figure()
fig.set_size_inches([3.25,3.25])
plt.rc('font',family='Times New Roman')
params = {'mathtext.default': 'regular' }          
plt.rcParams.update(params)
plt.plot(t_min_os , h_km_os, linestyle='solid' , color='xkcd:blue',linewidth=2.0,  label='Overshoot')
plt.plot(t_min_us , h_km_us, linestyle='solid' , color='xkcd:green',linewidth=2.0,  label='Undershoot')

plt.xlabel('Time, min',fontsize=10)
plt.ylabel("Altitude, km",fontsize=10)

ax = plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
plt.tick_params(direction='in')
plt.tick_params(axis='x',labelsize=10)
plt.tick_params(axis='y',labelsize=10)

plt.legend(loc='lower right', fontsize=8)


plt.savefig('../plots/craig-lyne-altitude.png',bbox_inches='tight')
plt.savefig('../plots/craig-lyne-altitude.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/craig-lyne-altitude.eps', dpi=300,bbox_inches='tight')

plt.show()

fig = plt.figure()
fig.set_size_inches([3.25,3.25])
plt.rc('font',family='Times New Roman')
plt.plot(t_min_os , acc_net_g_os, linestyle='solid' , color='xkcd:blue',linewidth=1.0,  label='Overshoot')
plt.plot(t_min_us , acc_net_g_us, linestyle='solid' , color='xkcd:green',linewidth=1.0,  label='Undershoot')

plt.xlabel('Time, min',fontsize=10)
plt.ylabel("Deceleration, Earth g",fontsize=10)

ax = plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
plt.tick_params(direction='in')
plt.tick_params(axis='x',labelsize=10)
plt.tick_params(axis='y',labelsize=10)

plt.legend(loc='upper right', fontsize=8)


plt.savefig('../plots/craig-lyne-deceleration.png',bbox_inches='tight')
plt.savefig('../plots/craig-lyne-deceleration.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/craig-lyne-deceleration.eps', dpi=300,bbox_inches='tight')

plt.show()

fig = plt.figure()
fig.set_size_inches([3.25,3.25])
plt.rc('font',family='Times New Roman')
plt.plot(t_min_os , q_stag_con_os, linestyle='solid' , color='xkcd:blue',linewidth=1.0,  label='Overshoot convective')
plt.plot(t_min_os , q_stag_rad_os, linestyle='solid' , color='xkcd:red',linewidth=1.0,  label='Overshoot radiative')
plt.plot(t_min_us , q_stag_con_us, linestyle='solid' , color='xkcd:magenta',linewidth=1.0,  label='Undershoot convective')
plt.plot(t_min_us , q_stag_rad_us, linestyle='solid' , color='xkcd:green',linewidth=1.0,  label='Undershoot radiative')

plt.xlabel('Time, min',fontsize=10)
plt.ylabel("Stagnation-point heat rate, "+r'$W/cm^2$',fontsize=10)

ax = plt.gca()
ax.tick_params(direction='in')
ax.yaxis.set_ticks_position('both')
ax.xaxis.set_ticks_position('both')
plt.tick_params(direction='in')
plt.tick_params(axis='x',labelsize=10)
plt.tick_params(axis='y',labelsize=10)

plt.legend(loc='upper right', fontsize=8)


plt.savefig('../plots/craig-lyne-heating.png',bbox_inches='tight')
plt.savefig('../plots/craig-lyne-heating.pdf', dpi=300,bbox_inches='tight')
plt.savefig('../plots/craig-lyne-heating.eps', dpi=300,bbox_inches='tight')

plt.show()







