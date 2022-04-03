"""
test_vehicle.py

Tests for Vehicle class

"""

import unittest
import numpy as np

class TestImportVehicle(unittest.TestCase):
	def test_import_vehicle(self):
		try:
			from AMAT.planet import Planet
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import Planet from AMAT.planet")

		try:
			from AMAT.vehicle import Vehicle
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import Vehicle from AMAT.vehicle")


try:
	from AMAT.planet import Planet
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Planet from AMAT.planet")

try:
	from AMAT.vehicle import Vehicle
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Vehicle from AMAT.vehicle")

class TestBallisticEntries(unittest.TestCase):
	"""
	Create vehicles and propagate a few ballistic planetary
	entry vehicle trajectories.
	"""

	def test_create_vehicle_pioneer_venus(self):
		"""
		Creates a test vehicle flying in Venus atmosphere
		"""
		planet1 = Planet("VENUS")
		# load atmosphere models
		try:
			planet1.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0, 1, 2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		# pv-large probe
		vehicle1 = Vehicle('PV-Large', 316, 188, 0.00, 1.59, 0.0, 0.36, planet1)

		vehicle1.setInitialState(180.0, 0.0, 0.0, 11.54, 0.0, -32.4, 0.0, 0.0)
		vehicle1.setSolverParams(1E-6)
		vehicle1.propogateEntry(3600.0, 0.1, 0.0)

		# Check computed peak heating and peak g-load values
		self.assertAlmostEqual(max(vehicle1.q_stag_total), 4935, delta=100)
		self.assertAlmostEqual(max(vehicle1.acc_net_g), 287, delta=10)
		# Check vehicle.exitflag == -1 (indicates vehicle reached "trap" altitude)
		self.assertEqual(vehicle1.exitflag, -1.0)

	def test_create_vehicle_stardust_earth(self):
		planet2 = Planet("EARTH")
		planet2.h_skip = 125.0E3

		try:
			planet2.loadAtmosphereModel('../atmdata/Earth/earth-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		vehicle2 = Vehicle('Stardust', 45.8, 60.0, 0.00, 0.52, 0.0, 0.23, planet2)  # stardust
		vehicle2.setInitialState(125.0, 0.0, 0.0, 12.6, 0.0, -8.2, 0.0, 0.0)
		vehicle2.setSolverParams(1E-6)
		vehicle2.propogateEntry(1800.0, 0.1, 0.0)

		self.assertAlmostEqual(max(vehicle2.q_stag_total), 824, delta=100)
		self.assertAlmostEqual(max(vehicle2.acc_net_g), 32, delta=4)
		self.assertEqual(vehicle2.exitflag, -1.0)

	def test_create_vehicle_curiosity_mars(self):
		planet3 = Planet("MARS")
		planet3.h_skip = 126.0E3
		planet3.h_trap = 2.0E3

		try:
			planet3.loadAtmosphereModel('../atmdata/Mars/mars-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")


		vehicle3=Vehicle('Curiosity', 3257.0, 146.0, 0.00, np.pi*4.5**2.0, 0.0, 1.125, planet3) # curiosity
		vehicle3.setInitialState(125.0,0.0,0.0,6.08,0.0,-15.48,0.0,0.0)
		vehicle3.setSolverParams(1E-6)
		vehicle3.propogateEntry(1800.0,0.1,0.0)

		self.assertAlmostEqual(max(vehicle3.q_stag_total), 81, delta=10)
		self.assertAlmostEqual(max(vehicle3.acc_net_g), 13, delta=3)
		self.assertEqual(vehicle3.exitflag, -1.0)



if __name__ == '__main__':
	unittest.main()

		





