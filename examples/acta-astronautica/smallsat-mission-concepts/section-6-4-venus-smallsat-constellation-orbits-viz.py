from mayavi import mlab
import numpy as np
from tvtk.tools import visual
from AMAT.approach import Approach
from astropy.time import Time
from AMAT.arrival import Arrival
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle
from AMAT.orbiter import Orbiter, PropulsiveOrbiter

def Arrow_From_A_to_B(x1, y1, z1, x2, y2, z2):
    ar1 = visual.arrow(x=x1, y=y1, z=z1)
    ar1.length_cone = 0.4

    arrow_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    ar1.actor.scale = [arrow_length, arrow_length, arrow_length]
    ar1.pos = ar1.pos / arrow_length
    ar1.axis = [x2 - x1, y2 - y1, z2 - z1]
    return ar1

arrival = Arrival()
arrival.set_vinf_vec_from_lambert_arc(lastFlybyPlanet='EARTH',
                                      arrivalPlanet='VENUS',
                                      lastFlybyDate=Time("2010-05-10 00:00:00", scale='tdb'),
                                      arrivalDate=Time("2010-12-06 00:00:00", scale='tdb'))



probe1 = Approach("VENUS", v_inf_vec_icrf_kms=arrival.v_inf_vec,
                            rp=(6051.8+103.85)*1e3, psi=0.94*np.pi,
                            is_entrySystem=True, h_EI=150e3)

space5 = Approach("VENUS",
                    v_inf_vec_icrf_kms=np.array([-3.26907094,  0.67649494, -1.0697747 ]),
                    rp=(6051.8+103.85)*1e3, psi=0.94*np.pi)

space4 = Approach("VENUS",
                    v_inf_vec_icrf_kms=np.array([-3.26907094,  0.67649494, -1.0697747 ]),
                    rp=(6051.8+103.85)*1e3, psi=0.97*np.pi)

space3 = Approach("VENUS",
                    v_inf_vec_icrf_kms=np.array([-3.26907094,  0.67649494, -1.0697747 ]),
                    rp=(6051.8+103.85)*1e3, psi=1.00*np.pi)

space2 = Approach("VENUS",
                    v_inf_vec_icrf_kms=np.array([-3.26907094,  0.67649494, -1.0697747 ]),
                    rp=(6051.8+103.85)*1e3, psi=1.03*np.pi)

space1 = Approach("VENUS",
                    v_inf_vec_icrf_kms=np.array([-3.26907094,  0.67649494, -1.0697747 ]),
                    rp=(6051.8+103.85)*1e3, psi=1.05988*np.pi)


space = Approach("VENUS", v_inf_vec_icrf_kms=arrival.v_inf_vec, rp=(6051.8 + 400) * 1e3, psi=1.00*np.pi)



theta_star_arr_space = np.linspace(-2.00, 0.0, 101)
pos_vec_bi_arr_space = space.pos_vec_bi(theta_star_arr_space)/6051.8e3

x_arr_space = pos_vec_bi_arr_space[0][:]
y_arr_space = pos_vec_bi_arr_space[1][:]
z_arr_space = pos_vec_bi_arr_space[2][:]

north_pole_bi_vec = probe1.ICRF_to_BI(arrival.north_pole)



orbiter5 = PropulsiveOrbiter(approach=space5, apoapsis_alt_km=2000)
orbiter4 = PropulsiveOrbiter(approach=space4, apoapsis_alt_km=2000)
orbiter3 = PropulsiveOrbiter(approach=space3, apoapsis_alt_km=2000)
orbiter2 = PropulsiveOrbiter(approach=space2, apoapsis_alt_km=2000)
orbiter1 = PropulsiveOrbiter(approach=space1, apoapsis_alt_km=2000)
orbiter = PropulsiveOrbiter(approach=space, apoapsis_alt_km=150000)

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1*np.outer(np.cos(u), np.sin(v))
y = 1*np.outer(np.sin(u), np.sin(v))
z = 1*np.outer(np.ones(np.size(u)), np.cos(v))

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
s1 = mlab.mesh(x, y, z, color=(0.34,0.33,0.33))
s2 = mlab.mesh(x1, y1, z1, color=(0.34, 0.33,0.33), opacity=0.0)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)
#r2 = mlab.plot3d(x_ring_2, y_ring_2, z_ring_2, color=(1,1,1), line_width=1, tube_radius=None)

# p1 = mlab.plot3d(x_arr_probe1, y_arr_probe1, z_arr_probe1, color=(0,1,0), line_width=3, tube_radius=None)
# p2 = mlab.plot3d(x_arr_probe2, y_arr_probe2, z_arr_probe2, color=(0,1,0), line_width=3, tube_radius=None)
# p3 = mlab.plot3d(x_arr_probe3, y_arr_probe3, z_arr_probe3, color=(0,1,0), line_width=3, tube_radius=None)
# p4 = mlab.plot3d(x_arr_probe4, y_arr_probe4, z_arr_probe4, color=(0,1,0), line_width=3, tube_radius=None)
# p5 = mlab.plot3d(x_arr_probe5, y_arr_probe5, z_arr_probe5, color=(0,1,0), line_width=3, tube_radius=None)
# o1 = mlab.plot3d(x_arr_space, y_arr_space, z_arr_space, color=(0,0,1), line_width=3, tube_radius=None)



p5o = mlab.plot3d(orbiter5.x_orbit_arr,
				 orbiter5.y_orbit_arr,
				 orbiter5.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p4o = mlab.plot3d(orbiter4.x_orbit_arr,
				 orbiter4.y_orbit_arr,
				 orbiter4.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p3o = mlab.plot3d(orbiter3.x_orbit_arr,
				 orbiter3.y_orbit_arr,
				 orbiter3.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)


p2o = mlab.plot3d(orbiter2.x_orbit_arr,
				 orbiter2.y_orbit_arr,
				 orbiter2.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p1o = mlab.plot3d(orbiter1.x_orbit_arr,
				 orbiter1.y_orbit_arr,
				 orbiter1.z_orbit_arr, color=(0, 1, 0), line_width=3, tube_radius=None)

p0 = mlab.plot3d(orbiter.x_orbit_arr,
				 orbiter.y_orbit_arr,
				 orbiter.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)


mlab.plot3d([0, 1.2 * north_pole_bi_vec[0]],
                   [0, 1.2 * north_pole_bi_vec[1]],
                   [0, 1.2 * north_pole_bi_vec[2]])

# mlab.plot3d([0, 1.5 * probe1.S_vec_bi_unit[0]],
#                    [0, 1.5 * probe1.S_vec_bi_unit[1]],
#                    [0, 1.5 * probe1.S_vec_bi_unit[2]], color=(0, 1, 0))
#
# mlab.plot3d([0, 1.5 * probe1.R_vec_bi_unit[0]],
#                    [0, 1.5 * probe1.R_vec_bi_unit[1]],
#                    [0, 1.5 * probe1.R_vec_bi_unit[2]], color=(1, 0, 0))
#
# mlab.plot3d([0, 1.5 * probe1.T_vec_bi_unit[0]],
#                    [0, 1.5 * probe1.T_vec_bi_unit[1]],
#                    [0, 1.5 * probe1.T_vec_bi_unit[2]], color=(0, 0, 1))
#

mlab.show()
