import numpy as np
from mayavi import mlab

from AMAT.approach import Approach
from AMAT.orbiter import PropulsiveOrbiter
from AMAT.visibility import LanderToOrbiter, OrbiterToPlanet

approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]), rp=(2575+1500)*1e3, psi=3*np.pi/2)
orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
orbiter.compute_timed_orbit_trajectory(t_seconds=86400*16, num_points=2001)
visibility = LanderToOrbiter(planet="TITAN", latitude=3.00, orbiter=orbiter, t_seconds=86400 * 16, num_points=2001)

orbiter2 = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
orbiter2.compute_timed_orbit_trajectory(t_seconds=86400*16, num_points=2001)
visibility2 = OrbiterToPlanet(target_planet="EARTH", observer_planet="TITAN",
								 orbiter=orbiter2, date="2034-03-28 00:00:00", t_seconds=86400*16, num_points=2001)


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
s1 = mlab.mesh(x, y, z, color=(0.5,0.5,0.0))
s2 = mlab.mesh(x1, y1, z1, color=(0.5,0.5,0.0), opacity=0.3)

# p6 = mlab.plot3d([0, 3*visibility2.obs_tar_pos_vec_bi_unit[0]],
# 				 [0, 3*visibility2.obs_tar_pos_vec_bi_unit[1]],
# 				 [0, 3*visibility2.obs_tar_pos_vec_bi_unit[2]], color=(1,0,0), tube_radius=0.01)

r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)



p5 = mlab.plot3d(orbiter.x_orbit_arr,
				 orbiter.y_orbit_arr,
				 orbiter.z_orbit_arr, color=(1, 0, 1), line_width=3, tube_radius=None)



plt1 = mlab.points3d(orbiter.x_timed_orbit_arr[:1],
					orbiter.y_timed_orbit_arr[:1],
					orbiter.z_timed_orbit_arr[:1], scale_factor=0.20, color=(1, 0, 1))

lander_pos_x_bi_arr = visibility.lander_pos_x_bi_arr/visibility.planetObj.RP
lander_pos_y_bi_arr = visibility.lander_pos_y_bi_arr/visibility.planetObj.RP
lander_pos_z_bi_arr = visibility.lander_pos_z_bi_arr/visibility.planetObj.RP

plt2 = mlab.points3d(lander_pos_x_bi_arr[:1],
					lander_pos_y_bi_arr[:1],
					lander_pos_z_bi_arr[:1], scale_factor=0.10, color=(0, 1, 0))


plt3 = mlab.plot3d([lander_pos_x_bi_arr[:1], orbiter.x_timed_orbit_arr[:1]],
					   [lander_pos_y_bi_arr[:1], orbiter.y_timed_orbit_arr[:1]],
					   [lander_pos_z_bi_arr[:1], orbiter.z_timed_orbit_arr[:1]], color=(0,1,0), tube_radius=0.01)


@mlab.animate(delay=30)
def anim():
	f = mlab.gcf()
	while True:
		for (x1, y1, z1, x2, y2, z2, elev) in zip(orbiter.x_timed_orbit_arr,
											orbiter.y_timed_orbit_arr,
											orbiter.z_timed_orbit_arr,
											lander_pos_x_bi_arr,
											lander_pos_y_bi_arr,
											lander_pos_z_bi_arr,
											visibility.elevation_array):
			plt1.mlab_source.set(x=x1, y=y1, z=z1)
			plt2.mlab_source.set(x=x2, y=y2, z=z2)
			if elev > 0:
				plt3.mlab_source.set(x=[x2, x1], y=[y2, y1], z=[z2, z1])
			else:
				plt3.mlab_source.set(x=[0, 0], y=[0, 0], z=[0, 0])
			f.scene.render()
			yield


anim()
mlab.show()