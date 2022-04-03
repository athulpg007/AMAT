"""
test_craigLyne2005.py

Compare results from Craig and Lyne [2005, JSR]

"""

import unittest
import numpy as np

try:
    from AMAT.planet import Planet
except ModuleNotFoundError:
    raise ModuleNotFoundError("Cannot import Planet from AMAT.planet")

try:
	from AMAT.vehicle import Vehicle
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Vehicle from AMAT.vehicle")

class CraigLyne2005(unittest.TestCase):

	def test_craig_lyne_2005(self):

		planet1 = Planet("VENUS")

		try:
			planet1.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		# vehicle and entry state description from Craig and Lyne, 
		# Parametric Study of Aerocapture for Missions to Venus, 
		# Journal of Spacecraft and Rockets, 
		# Vol. 42, No. 6., 2005. DOI:10.2514/1.2589
		vehicle1=Vehicle('Apollo', 300.0, 78.0, 0.35, 3.1416, 0.0, 1.54, planet1)
		vehicle1.setInitialState(180.0,0.0,0.0,12.0,0.0,-4.5,0.0,0.0)
		vehicle1.setSolverParams(1E-6)

		print("Computing aerocapture corridor bounds from Craig and Lyne [JSR, 2005]...")
		overShootLimit, exitflag_os  = vehicle1.findOverShootLimit (2400.0,0.1,-80.0,-4.0,1E-10,407.0)
		underShootLimit,exitflag_us  = vehicle1.findUnderShootLimit(2400.0,0.1,-80.0,-4.0,1E-10,407.0)

		# check exitflag_os, exitflag_us = 1 (indicates AMAT found a solution)
		self.assertEqual(exitflag_os, 1)
		self.assertEqual(exitflag_us, 1)

		# compare with values from Fig. 2 Craig and Lyne [JSR, 2005] @ V = 12 km/s
		self.assertAlmostEqual(overShootLimit,  -7.0519, places=4)
		self.assertAlmostEqual(underShootLimit, -9.4396, places=4)

		# Reset initial conditions and propagate overshoot trajectory
		vehicle1.setInitialState(180.0,0.0,0.0,12.0,0.0,overShootLimit,0.0,0.0)
		vehicle1.propogateEntry (2400.0,0.1,180.0)

		# Extract and save variables to plot
		t_min_os         = vehicle1.t_minc
		h_km_os          = vehicle1.h_kmc
		acc_net_g_os     = vehicle1.acc_net_g
		q_stag_con_os    = vehicle1.q_stag_con
		q_stag_rad_os    = vehicle1.q_stag_rad

		# Reset initial conditions and propagate undershoot trajectory
		vehicle1.setInitialState(180.0,0.0,0.0,12.0,0.0,underShootLimit,0.0,0.0)
		vehicle1.propogateEntry (2400.0,0.1,0.0)

		# Extract and save variable to plot
		t_min_us         = vehicle1.t_minc
		h_km_us          = vehicle1.h_kmc
		acc_net_g_us     = vehicle1.acc_net_g
		q_stag_con_us    = vehicle1.q_stag_con
		q_stag_rad_us    = vehicle1.q_stag_rad
		
		# compare with values from Fig. 4 of Craig and Lyne [JSR, 2005] 
		self.assertAlmostEqual(max(t_min_os), 22.85, places=1)
		self.assertAlmostEqual(max(t_min_us), 3.335, places=1)

		self.assertAlmostEqual(min(h_km_os), 103.16, places=1) 
		self.assertAlmostEqual(min(h_km_us), 92.712, places=1)

		# compare with values from Fig. 5 of Craig and Lyne [JSR, 2005]
		self.assertAlmostEqual(max(acc_net_g_os), 2.925, places=1)
		self.assertAlmostEqual(max(acc_net_g_us), 35.872, places=1)

		# compare with values from Fig. 6 of Craig and Lyne [JSR, 2005]
		self.assertAlmostEqual(max(q_stag_con_os), 126.16, places=1)
		self.assertAlmostEqual(max(q_stag_rad_os), 36.375, places=1)

		self.assertAlmostEqual(max(q_stag_con_us), 373.69, places=1)
		self.assertAlmostEqual(max(q_stag_rad_us), 367.33, places=1)

if __name__ == '__main__':
	unittest.main()

		

