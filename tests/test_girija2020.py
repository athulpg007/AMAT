"""
test_girija2020.py

Compare results from Girija et al. [2020, JSR]

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

try:
    from AMAT.launcher import Launcher
except ModuleNotFoundError:
    raise ModuleNotFoundError("Cannot import Launcher from AMAT.Launcher")


class Girija2020(unittest.TestCase):

	def test_aerocapture_vehicle(self):

		planet = Planet("NEPTUNE")

		try:
			planet.loadAtmosphereModel('../atmdata/Neptune/neptune-gram-avg.dat', 0 , 7 ,6, 5 , heightInKmFlag=True)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		# select L/D = 0.4 and Vinf_arrival = 20 km/s from feasibility chart

		# C3 of selected trajectory = 111 km2/s2
		# selected launch vehicle = SLS-Block-1B with kick stage

		# compute launch vehicle capability
		launcher = Launcher( launcherID='sls-block-1B-with-kick',
							 datafile='../launcher-data/sls-block-1B-with-kick.csv')
		launch_mass = launcher.launchMass(111.0)
		assert abs(launch_mass - 6600) < 100

		# vehicle and entry state description from Girija et al. [JSR, 2021]
		vehicle = Vehicle('Trident', 1000.0, 200.0, 0.40, 3.1416, 0.0, 1.00, planet)
		vehicle.setInitialState(1000.0, 0.0, 0.0, 28.00, 0.0,-10.00, 0.0, 0.0)
		vehicle.setSolverParams(1E-6)

		print("Computing aerocapture corridor bounds from Girija et al. [JSR, 2020]...")
		overShootLimit, exitflag_os  = vehicle.findOverShootLimit (2400.0, 1.0, -20.0, -4.0, 1E-2, 400.0e3)
		underShootLimit,exitflag_us  = vehicle.findUnderShootLimit(2400.0, 1.0, -20.0, -4.0, 1E-2, 400.0e3)

		# NOTE: This result does not include the effect of planetary rotation on
		# entry speed. Use findOverShootLimit2 and findUnderShootLimit2 to include these
		# effects on the corridor location.

		# check exitflag_os, exitflag_us = 1 (indicates AMAT found a solution)
		self.assertEqual(exitflag_os, 1)
		self.assertEqual(exitflag_us, 1)

		# compare with values from Fig. 2 
		self.assertAlmostEqual(overShootLimit,  -12.7393, places=2)
		self.assertAlmostEqual(underShootLimit, -13.7081, places=2)


if __name__ == '__main__':
	unittest.main()




