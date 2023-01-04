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
                                      arrivalPlanet='VENUS',
                                      lastFlybyDate=Time("2010-05-10 00:00:00", scale='tdb'),
                                      arrivalDate=Time("2010-12-06 00:00:00", scale='tdb'),
									  ephem_file='../../../spice-data/de432s.bsp')


probe = Approach("VENUS", v_inf_vec_icrf_kms=arrival.v_inf_vec,
                            rp=(6051.8+200)*1e3, psi=np.pi)


space = Approach("VENUS", v_inf_vec_icrf_kms=arrival.v_inf_vec,
                            rp=(6051.8+400)*1e3, psi=np.pi)


north_pole_bi_vec = probe.ICRF_to_BI(arrival.north_pole)





orbiter = PropulsiveOrbiter(approach=probe, apoapsis_alt_km=2e3)
orbiter2 = PropulsiveOrbiter(approach=space, apoapsis_alt_km=150e3)


u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1 * np.outer(np.cos(u), np.sin(v))
y = 1 * np.outer(np.sin(u), np.sin(v))
z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))


x1 = 1.02478929103*np.outer(np.cos(u), np.sin(v))
y1 = 1.024789291032*np.outer(np.sin(u), np.sin(v))
z1 = 1.02478929103*np.outer(np.ones(np.size(u)), np.cos(v))


x_ring_1 = 1.1*np.cos(u)
y_ring_1 = 1.1*np.sin(u)
z_ring_1 = 0.0*np.cos(u)

x_ring_2 = 1.2*np.cos(u)
y_ring_2 = 1.2*np.sin(u)
z_ring_2 = 0.0*np.cos(u)

mlab.figure(bgcolor=(0,0,0))
s1 = mlab.mesh(x, y, z, color=(0.34,0.33,0.33))
s2 = mlab.mesh(x1, y1, z1, color=(0.34, 0.33,0.33), opacity=0.3)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)



p4 = mlab.plot3d(orbiter.x_orbit_arr,
				 orbiter.y_orbit_arr,
				 orbiter.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p5 = mlab.plot3d(orbiter2.x_orbit_arr,
				 orbiter2.y_orbit_arr,
				 orbiter2.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)


mlab.plot3d([0, 1.05 * north_pole_bi_vec[0]],
                   [0, 1.05 * north_pole_bi_vec[1]],
                   [0, 1.05 * north_pole_bi_vec[2]])

mlab.show()
