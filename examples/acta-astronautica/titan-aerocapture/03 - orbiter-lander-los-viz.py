import numpy as np
from mayavi import mlab

from AMAT.approach import Approach
from AMAT.orbiter import PropulsiveOrbiter
from AMAT.visibility import LanderToOrbiter

approach = Approach("EARTH", v_inf_vec_icrf_kms=np.array([1, 1, 0]), rp=(6371+650)*1e3, psi=3*np.pi/2)
orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=650)
orbiter.compute_timed_orbit_trajectory(t_seconds=86400, num_points=1001)

visibility = LanderToOrbiter(planet="EARTH", latitude=0.00, orbiter=orbiter, t_seconds=86400, num_points=1001)


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

mlab.figure(bgcolor=(0,0,0))
s1 = mlab.mesh(x, y, z, color=(0.1,0.1,0.8))
s2 = mlab.mesh(x1, y1, z1, color=(0.1,0.1,0.8), opacity=0.3)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)

p5 = mlab.plot3d(orbiter.x_orbit_arr,
				 orbiter.y_orbit_arr,
				 orbiter.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)

plt1 = mlab.points3d(orbiter.x_timed_orbit_arr[:1],
					orbiter.y_timed_orbit_arr[:1],
					orbiter.z_timed_orbit_arr[:1], scale_factor=0.10, color=(1, 0, 1))

lander_pos_x_bi_arr = visibility.lander_pos_x_bi_arr/visibility.planetObj.RP
lander_pos_y_bi_arr = visibility.lander_pos_y_bi_arr/visibility.planetObj.RP
lander_pos_z_bi_arr = visibility.lander_pos_z_bi_arr/visibility.planetObj.RP

plt2 = mlab.points3d(lander_pos_x_bi_arr[:1],
					lander_pos_y_bi_arr[:1],
					lander_pos_z_bi_arr[:1], scale_factor=0.10, color=(0, 1, 0))

@mlab.animate(delay=10)
def anim():
	f = mlab.gcf()
	while True:
		for (x1, y1, z1, x2, y2, z2) in zip(orbiter.x_timed_orbit_arr, orbiter.y_timed_orbit_arr, orbiter.z_timed_orbit_arr,
											lander_pos_x_bi_arr, lander_pos_y_bi_arr, lander_pos_z_bi_arr):
			#print('Updating scene...')
			plt1.mlab_source.set(x=x1, y=y1, z=z1)
			plt2.mlab_source.set(x=x2, y=y2, z=z2)
			f.scene.render()
			yield


anim()
mlab.show()