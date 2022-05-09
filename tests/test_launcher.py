"""
test_launcher.py

Basic test for AMAT.launcher

"""

import unittest

try:
	from AMAT.launcher import Launcher
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Launcher from AMAT.Launcher")


class TestLauncher(unittest.TestCase):

	def test_atlas_V_401(self):
		"""
		Performance query for a few launch vehicles.
		"""

		launcher = Launcher('atlasV401', datafile='../launcher-data/atlas-v401.csv')
		# Compare with numbers from https://elvperf.ksc.nasa.gov/Pages/Query.aspx
		self.assertAlmostEqual(launcher.launchMass(16), 2088, delta=20)


	def test_atlas_V_551(self):
		"""
		Performance query for a few launch vehicles.
		"""

		launcher = Launcher('atlasV401', datafile='../launcher-data/atlas-v551.csv')
		# Compare with numbers from https://elvperf.ksc.nasa.gov/Pages/Query.aspx
		self.assertAlmostEqual(launcher.launchMass(16), 4325, delta=20)

if __name__ == '__main__':
	unittest.main()










