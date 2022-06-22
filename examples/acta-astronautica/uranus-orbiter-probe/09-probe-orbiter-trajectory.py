import numpy as np
from mayavi import mlab

from AMAT.approach import Approach
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle
from AMAT.orbiter import Orbiter

probe1 = Approach("URANUS",
				  v_inf_vec_icrf_kms=np.array([-9.62521831, 16.51192666, 7.46493598]),
				  rp=(25559 + 345) * 1e3, psi=np.pi,
				  is_entrySystem=True, h_EI=1000e3)

theta_star_arr_probe1 = np.linspace(-1.8, probe1.theta_star_entry, 101)
pos_vec_bi_arr_probe1 = probe1.pos_vec_bi(theta_star_arr_probe1) / 25559e3

x_arr_probe1 = pos_vec_bi_arr_probe1[0][:]
y_arr_probe1 = pos_vec_bi_arr_probe1[1][:]
z_arr_probe1 = pos_vec_bi_arr_probe1[2][:]

planet = Planet("URANUS")
planet.h_skip = 1000e3
planet.loadAtmosphereModel('../../../atmdata/Uranus/uranus-gram-avg.dat', 0, 1, 2, 3, heightInKmFlag=True)
planet.h_low = 120e3
planet.h_trap = 100e3

vehicle = Vehicle('Titania', 3200.0, 146, 0.24, np.pi * 4.5 ** 2.0, 0.0, 1.125, planet)
vehicle.setInitialState(1000.0, -15.22, 75.55, 29.2877, 88.687, -11.0088, 0.0, 0.0)
vehicle.setSolverParams(1E-6)
vehicle.propogateEntry2(2400.0, 0.1, 180.0)

orbiter = Orbiter(vehicle, 4000.0)
orbiter.compute_probe_targeting_trajectory(178 * np.pi / 180, -90)
orbiter.compute_orbiter_deflection_trajectory(182 * np.pi / 180, 89.38)

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1 * np.outer(np.cos(u), np.sin(v))
y = 1 * np.outer(np.sin(u), np.sin(v))
z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))

x1 = 1.040381198513972 * np.outer(np.cos(u), np.sin(v))
y1 = 1.040381198513972 * np.outer(np.sin(u), np.sin(v))
z1 = 1.040381198513972 * np.outer(np.ones(np.size(u)), np.cos(v))

x_ring_1 = 1.4 * np.cos(u)
y_ring_1 = 1.4 * np.sin(u)
z_ring_1 = 0.0 * np.cos(u)

x_ring_2 = 1.6 * np.cos(u)
y_ring_2 = 1.6 * np.sin(u)
z_ring_2 = 0.0 * np.cos(u)

mlab.figure(bgcolor=(0, 0, 0))
s1 = mlab.mesh(x, y, z, color=(0.10, 0.55, 0.35))
s2 = mlab.mesh(x1, y1, z1, color=(0.2, 0.4, 0.4), opacity=0.3)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1, 1, 1), line_width=1, tube_radius=None)
r2 = mlab.plot3d(x_ring_2, y_ring_2, z_ring_2, color=(1, 1, 1), line_width=1, tube_radius=None)

#p1 = mlab.plot3d(x_arr_probe1, y_arr_probe1, z_arr_probe1, color=(1, 1, 1), line_width=3, tube_radius=None)

#p2 = mlab.plot3d(orbiter.x_coast_arr,
#				 orbiter.y_coast_arr,
#				 orbiter.z_coast_arr, color=(1, 1, 0), line_width=3, tube_radius=None)

p3 = mlab.plot3d(orbiter.x_orbit_arr[0: int(len(orbiter.x_orbit_arr/2))],
				 orbiter.y_orbit_arr[0: int(len(orbiter.x_orbit_arr/2))],
				 orbiter.z_orbit_arr[0: int(len(orbiter.x_orbit_arr/2))], color=(1, 0, 1), line_width=3, tube_radius=None)

p4 = mlab.plot3d(orbiter.x_probe_orbit_arr,
				 orbiter.y_probe_orbit_arr,
				 orbiter.z_probe_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

#p4 = mlab.plot3d(orbiter.x_orbiter_defl_arr,
#				 orbiter.y_orbiter_defl_arr,
#				 orbiter.z_orbiter_defl_arr, color=(0, 1, 0), line_width=3, tube_radius=None)


mlab.show()
