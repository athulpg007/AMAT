from mayavi import mlab
import numpy as np

from AMAT.approach import Approach

probe1 = Approach("NEPTUNE",
                    v_inf_vec_icrf_kms=np.array([17.78952518, 8.62038536, 3.15801163]),
                    rp=(24764 + 400) * 1e3, psi=3* np.pi/2,
                    is_entrySystem=True, h_EI=1000e3)

probe2 = Approach("NEPTUNE",
                    v_inf_vec_icrf_kms=np.array([17.78952518, 8.62038536, 3.15801163]),
                    rp=(24764 + 400) * 1e3, psi=np.pi,
                    is_entrySystem=True, h_EI=1000e3)


theta_star_arr_probe1 = np.linspace(-1.8, probe1.theta_star_entry, 101)
pos_vec_bi_arr_probe1 = probe1.pos_vec_bi(theta_star_arr_probe1)/24764e3


theta_star_arr_probe2 = np.linspace(-1.8, probe2.theta_star_entry, 101)
pos_vec_bi_arr_probe2 = probe2.pos_vec_bi(theta_star_arr_probe2)/24764e3

x_arr_probe1 = pos_vec_bi_arr_probe1[0][:]
y_arr_probe1 = pos_vec_bi_arr_probe1[1][:]
z_arr_probe1 = pos_vec_bi_arr_probe1[2][:]

x_arr_probe2 = pos_vec_bi_arr_probe2[0][:]
y_arr_probe2 = pos_vec_bi_arr_probe2[1][:]
z_arr_probe2 = pos_vec_bi_arr_probe2[2][:]


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
s1 = mlab.mesh(x, y, z, color=(0,0,1))
s2 = mlab.mesh(x1, y1, z1, color=(0,0,1), opacity=0.3)
r1 = mlab.plot3d(x_ring_1, y_ring_1, z_ring_1, color=(1,1,1), line_width=1, tube_radius=None)
r2 = mlab.plot3d(x_ring_2, y_ring_2, z_ring_2, color=(1,1,1), line_width=1, tube_radius=None)

p1 = mlab.plot3d(x_arr_probe1, y_arr_probe1, z_arr_probe1, color=(1,0,0), line_width=3, tube_radius=None)
p2 = mlab.plot3d(x_arr_probe2, y_arr_probe2, z_arr_probe2, color=(0,1,0), line_width=3, tube_radius=None)

mlab.show()
