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

	def test_create_launcher(self):

		"""
		Performance query for a few launch vehicles.
		"""

		Launcher1 = Launcher('atlasV401')
		Launcher2 = Launcher('atlasV551')
		Launcher3 = Launcher('falconH')
		Launcher4 = Launcher('sls-block-1B')

		# Compare with numbers from https://elvperf.ksc.nasa.gov/Pages/Query.aspx
		self.assertAlmostEqual(Launcher1.performanceQuery(16), 2088, delta=20)
		self.assertAlmostEqual(Launcher2.performanceQuery(16), 4501, delta=20)
		self.assertAlmostEqual(Launcher3.performanceQuery(16), 11004, delta=20)
		self.assertAlmostEqual(Launcher4.performanceQuery(100), 5039, delta=100)

if __name__ == '__main__':
	unittest.main()










