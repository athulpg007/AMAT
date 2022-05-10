"""
test_launcher.py

Basic tests for AMAT.launcher

"""

import unittest

try:
	from AMAT.launcher import Launcher
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Launcher from AMAT.Launcher")


class TestLauncher(unittest.TestCase):

	def test_falcon_heavy_expendable(self):
		launcher = Launcher('Falcon Heavy Expendable', datafile='../launcher-data/falcon-heavy-expendable.csv')
		# Compare with numbers from https://elvperf.ksc.nasa.gov/Pages/Query.aspx
		self.assertAlmostEqual(launcher.launchMass(29), 8405 , delta=50)

	def test_falcon_heavy_recovery(self):
		launcher = Launcher('Falcon Heavy Reusable', datafile='../launcher-data/falcon-heavy-reusable.csv')
		# Compare with numbers from https://elvperf.ksc.nasa.gov/Pages/Query.aspx
		self.assertAlmostEqual(launcher.launchMass(29), 2850 , delta=50)

	def test_atlas_V_401(self):
		launcher = Launcher('Atlas V401', datafile='../launcher-data/atlas-v401.csv')
		self.assertAlmostEqual(launcher.launchMass(11.94), 2316 , delta=50)

	def test_atlas_V_551(self):
		launcher = Launcher('Atlas V551', datafile='../launcher-data/atlas-v551.csv')
		self.assertAlmostEqual(launcher.launchMass(11.94), 4879 , delta=50)

	def test_delta_IV_Heavy(self):
		launcher = Launcher('Delta IVH', datafile='../launcher-data/delta-IVH.csv')
		self.assertAlmostEqual(launcher.launchMass(11.94), 8153 , delta=50)

	def test_falcon_heavy_expendable_with_kick1(self):
		launcher = Launcher('Falcon Heavy Expendable with Kick', datafile='../launcher-data/falcon-heavy-expendable-w-star-48.csv')
		self.assertAlmostEqual(launcher.launchMass(29.36), 7800 , delta=100)

	def test_falcon_heavy_expendable_with_kick2(self):
		launcher = Launcher('Falcon Heavy Expendable with Kick', datafile='../launcher-data/falcon-heavy-expendable-w-star-48.csv')
		self.assertAlmostEqual(launcher.launchMass(80), 3010 , delta=200)

	def test_vulcan_6(self):
		launcher = Launcher('Vulcan-6', datafile='../launcher-data/vulcan-centaur-w-6-solids.csv')
		self.assertAlmostEqual(launcher.launchMass(29), 6328, delta=50)

	def test_vulcan_6_with_kick(self):
		launcher = Launcher('Vulcan-6-with-kick', datafile='../launcher-data/vulcan-centaur-w-6-solids-w-star-48.csv')
		self.assertAlmostEqual(launcher.launchMass(80), 2586, delta=200)

	def test_sls_block_1(self):
		launcher = Launcher('SLS-Block-1', datafile='../launcher-data/sls-block-1.csv')
		self.assertAlmostEqual(launcher.launchMass(80), 5400, delta=100)

	def test_sls_block_1B(self):
		launcher = Launcher('SLS-Block-1B', datafile='../launcher-data/sls-block-1B.csv')
		self.assertAlmostEqual(launcher.launchMass(80), 8500, delta=100)

	def test_sls_block_1B_kick(self):
		launcher = Launcher('SLS-Block-1B-with-kick', datafile='../launcher-data/sls-block-1B-with-kick.csv')
		self.assertAlmostEqual(launcher.launchMass(80), 10400, delta=100)

	def test_sls_block_1B_kick_2(self):
		launcher = Launcher(launcherID='sls-block-1B-with-kick',
							datafile='../launcher-data/sls-block-1B-with-kick.csv')
		self.assertAlmostEqual(launcher.launchMass(111.0), 6600, delta=100)


if __name__ == '__main__':
	unittest.main()










