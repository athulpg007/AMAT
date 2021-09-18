"""
test_wernerBraun2019.py

Compare results from Werner and Braun [2019, JSR]

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

class WernerBraun2019(unittest.TestCase):

	def test_aerocapture_vehicle(self):

		planet = Planet('EARTH')
		planet.loadAtmosphereModel('../atmdata/Earth/earth-gram-avg.dat', 0 , 1 ,2, 3)
		planet.h_skip = 125.0E3

		vehicle=Vehicle('EarthSmallSat', 25.97, 66.4, 0.0, np.pi*0.25**2, 0.0, 0.0563, planet)
		vehicle.setInitialState(125.0,0.0,0.0,9.8,0.0,-5.00,0.0,0.0)
		vehicle.setSolverParams(1E-6)
		vehicle.setDragModulationVehicleParams(66.4,4.72)

		print("Computing aerocapture corridor bounds from Werner and Braun [JSR, 2019]...")
		underShootLimit, exitflag_us = vehicle.findUnderShootLimitD(2400.0, 0.1, -30.0,-2.0, 1E-10, 1760.0)
		overShootLimit , exitflag_os =  vehicle.findOverShootLimitD(2400.0, 0.1, -30.0,-2.0, 1E-10, 1760.0)

		# check exitflag_os, exitflag_us = 1 (indicates AMAT found a solution)
		self.assertEqual(exitflag_os, 1)
		self.assertEqual(exitflag_us, 1)

		self.assertAlmostEqual(overShootLimit,  -4.6496, places=3)
		self.assertAlmostEqual(underShootLimit, -5.1410, places=3)

		# Set target orbit = 180 km x 1760, tolerance = 50 km
		vehicle.setTargetOrbitParams(180.0, 1760.0, 50.0)

		# Set entry phase parameters
		# v_switch_kms = 5.0, lowAlt_km = 50.0,
		# numPoints_lowAlt = 101, hdot_threshold = -200.0 m/s.
		# These are somewhat arbitrary based on experience.
		vehicle.setDragEntryPhaseParams(5.0, 50.0, 101, -200.0)

		# Set vehicle initial state to mid corridor EFPA
		vehicle.setInitialState(125.0,0.0,0.0,9.8,0.0,-4.90,0.0,0.0)

		# Propogate a single vehicle trajectory
		vehicle.propogateGuidedEntryD(1.0,1.0,0.1,2400.0)

		self.assertAlmostEqual(min(vehicle.h_kmc), 124.06, delta=2)
		self.assertAlmostEqual(max(vehicle.acc_net_g_full), 3.37, delta=0.3)
		self.assertAlmostEqual(max(vehicle.q_stag_total_full), 378.55, delta=50)

if __name__ == '__main__':
	unittest.main()

