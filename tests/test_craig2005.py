"""
test_craigLyne2005.py

Compare results from Craig and Lyne [2005, JSR]

"""

import unittest

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
		overShootLimit, exitflag_os  = vehicle1.findOverShootLimit (2400.0, 1.0, -20.0, -4.0, 1E-2, 407.0)
		underShootLimit,exitflag_us  = vehicle1.findUnderShootLimit(2400.0, 1.0, -20.0, -4.0, 1E-2, 407.0)

		# check exitflag_os, exitflag_us = 1 (indicates AMAT found a solution)
		self.assertEqual(exitflag_os, 1)
		self.assertEqual(exitflag_us, 1)

		# compare with values from Fig. 2 Craig and Lyne [JSR, 2005] @ V = 12 km/s
		self.assertAlmostEqual(overShootLimit,  -7.0468, places=2)
		self.assertAlmostEqual(underShootLimit, -9.4396, places=2)


if __name__ == '__main__':
	unittest.main()

		

