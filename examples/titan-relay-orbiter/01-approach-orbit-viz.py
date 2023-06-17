from mayavi import mlab
import numpy as np
from AMAT.approach import Approach
from AMAT.orbiter import Orbiter, PropulsiveOrbiter
from astropy.time import Time
from AMAT.arrival import Arrival


space = Approach("TITAN",
                    v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]),
                    rp=(2575+1700)*1e3, psi=0.95*np.pi)

orbiter2 = PropulsiveOrbiter(approach=space, apoapsis_alt_km=1700)

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 1*np.outer(np.cos(u), np.sin(v))
y = 1*np.outer(np.sin(u), np.sin(v))
z = 1*np.outer(np.ones(np.size(u)), np.cos(v))

x1 = 1.2*np.outer(np.cos(u), np.sin(v))
y1 = 1.2*np.outer(np.sin(u), np.sin(v))
z1 = 1.2*np.outer(np.ones(np.size(u)), np.cos(v))


x_ring_1 = 1.3*np.cos(u)
y_ring_1 = 1.3*np.sin(u)
z_ring_1 = 0.0*np.cos(u)

x_ring_2 = 1.4*np.cos(u)
y_ring_2 = 1.4*np.sin(u)
z_ring_2 = 0.0*np.cos(u)

mlab.figure(bgcolor=(0,0,0))
s1 = mlab.mesh(x, y, z, color=(0.5,0.5,0.0))
s2 = mlab.mesh(x1, y1, z1, color=(0.5,0.5,0.0), opacity=0.5)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)
#r2 = mlab.plot3d(x_ring_2, y_ring_2, z_ring_2, color=(1,1,1), line_width=1, tube_radius=None)

p5 = mlab.plot3d(orbiter2.x_orbit_arr,
				 orbiter2.y_orbit_arr,
				 orbiter2.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)

mlab.show()