import numpy as np
from mayavi import mlab

from AMAT.approach import Approach
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle
from AMAT.orbiter import Orbiter, PropulsiveOrbiter
from astropy.time import Time
from AMAT.arrival import Arrival

arrival = Arrival()
arrival.set_vinf_vec_from_lambert_arc(lastFlybyPlanet='EARTH',
                                      arrivalPlanet='MARS',
                                      lastFlybyDate=Time("2020-07-30 00:00:00", scale='tdb'),
                                      arrivalDate=Time("2021-02-18 00:00:00", scale='tdb'),
									  ephem_file='../../../spice-data/de432s.bsp')


probe = Approach("MARS",v_inf_vec_icrf_kms=np.array([ 2.23930484,  1.20086474, -0.73683366]),
                        rp=(3389.5+52)*1e3, psi=3*np.pi/2,
                        is_entrySystem=True, h_EI=120e3)

theta_star_arr_probe1 = np.linspace(-1.9, probe.theta_star_entry, 101)
pos_vec_bi_arr_probe1 = probe.pos_vec_bi(theta_star_arr_probe1) / 3389.5e3


space = Approach("MARS",
                    v_inf_vec_icrf_kms=np.array([ 2.23930484,  1.20086474, -0.73683366]),
                    rp=(3389.5+250)*1e3, psi=np.pi)


north_pole_bi_vec = probe.ICRF_to_BI(arrival.north_pole)

theta_star_arr_probe = np.linspace(-2, probe.theta_star_entry, 101)
pos_vec_bi_arr_probe = probe.pos_vec_bi(theta_star_arr_probe)/3389.5e3


theta_star_arr_space = np.linspace(-2, 0.0, 101)
pos_vec_bi_arr_space = space.pos_vec_bi(theta_star_arr_space)/3389.5e3

x_arr_probe = pos_vec_bi_arr_probe[0][:]
y_arr_probe = pos_vec_bi_arr_probe[1][:]
z_arr_probe = pos_vec_bi_arr_probe[2][:]

x_arr_space = pos_vec_bi_arr_space[0][:]
y_arr_space = pos_vec_bi_arr_space[1][:]
z_arr_space = pos_vec_bi_arr_space[2][:]


planet = Planet('MARS')
planet.loadAtmosphereModel('../../../atmdata/Mars/mars-gram-avg.dat', 0 , 1 ,2, 3)
planet.h_skip = 120.0E3

# Set up a vehicle object
vehicle1=Vehicle('MarsSmallSat1', 37, 20, 0.0, 1.767, 0.0, 0.1, planet)
vehicle1.setSolverParams(1E-6)
vehicle1.setDragModulationVehicleParams(20, 7.5)

# propagate a guided trajectory
# Set planet.h_low to 10 km, if vehicle dips below this level
# trajctory is terminated.
planet.h_low=10.0E3

# Set target orbit = 2000 km x 2000 km, tolerance = 20 km
# target apo intentionally set to slightly higher value to account for bias in guidance
vehicle1.setTargetOrbitParams(200.0, 2500.0, 20.0)

# Set entry phase parameters
# v_switch_kms = 2.0, lowAlt_km = 20.0,
# numPoints_lowAlt = 101, hdot_threshold = -200.0 m/s.
# These are somewhat arbitary based on experience.
vehicle1.setDragEntryPhaseParams(2.0, 20.0, 101, -200.0)

# Set beta_1 and beta_ratio
vehicle1.setDragModulationVehicleParams(20, 7.5)

# Set vehicle initial state
vehicle1.setInitialState(120.0, -89.76, -0.71, 5.3581, 1.60, -9.2475, 0.0, 0.0)
# Propogate a single vehicle trajectory
vehicle1.propogateGuidedEntryD2(1.0,1.0,0.1,2400.0)

orbiter = Orbiter(vehicle1, 200.0)
orbiter2 = PropulsiveOrbiter(approach=space, apoapsis_alt_km=70e3)


u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1 * np.outer(np.cos(u), np.sin(v))
y = 1 * np.outer(np.sin(u), np.sin(v))
z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))

x1 = 1.040381198513972*np.outer(np.cos(u), np.sin(v))
y1 = 1.040381198513972*np.outer(np.sin(u), np.sin(v))
z1 = 1.040381198513972*np.outer(np.ones(np.size(u)), np.cos(v))


x_ring_1 = 1.1*np.cos(u)
y_ring_1 = 1.1*np.sin(u)
z_ring_1 = 0.0*np.cos(u)

x_ring_2 = 1.2*np.cos(u)
y_ring_2 = 1.2*np.sin(u)
z_ring_2 = 0.0*np.cos(u)

mlab.figure(bgcolor=(0,0,0))
s1 = mlab.mesh(x, y, z, color=(0.7,0.3,0.0))
s2 = mlab.mesh(x1, y1, z1, color=(0.7, 0.3,0.0), opacity=0.3)
#r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)

p1 = mlab.plot3d(x_arr_probe, y_arr_probe, z_arr_probe, color=(1, 1, 1), line_width=3, tube_radius=None)
p2 = mlab.plot3d(x_arr_space, y_arr_space, z_arr_space, color=(0, 0, 1), line_width=3, tube_radius=None)

p3 = mlab.plot3d(orbiter.x_coast_arr,
				 orbiter.y_coast_arr,
				 orbiter.z_coast_arr, color=(1, 1, 0), line_width=3, tube_radius=None)

p4 = mlab.plot3d(orbiter.x_orbit_arr,
				 orbiter.y_orbit_arr,
				 orbiter.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p5 = mlab.plot3d(orbiter2.x_orbit_arr,
				 orbiter2.y_orbit_arr,
				 orbiter2.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)


mlab.show()
