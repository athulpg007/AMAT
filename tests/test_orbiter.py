"""
test_orbiter.py

Tests for Orbiter class

"""
import numpy as np

from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

class TestImportOrbiter():
	def test_import_orbiter(self):
		try:
			from AMAT.orbiter import Orbiter
			return True
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import Orbiter from AMAT.orbiter")
			assert False

try:
	from AMAT.orbiter import Orbiter
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Orbiter from AMAT.orbiter")

class TestCoast:

	planet = Planet("URANUS")
	planet.h_skip = 1000e3
	planet.loadAtmosphereModel('../atmdata/Uranus/uranus-gram-avg.dat', 0, 1, 2, 3, heightInKmFlag=True)
	planet.h_low = 120e3
	planet.h_trap = 100e3

	vehicle = Vehicle('Titania', 3200.0, 146, 0.24, np.pi * 4.5 ** 2.0, 0.0, 1.125, planet)
	vehicle.setInitialState(1000.0, -15.22, 75.55, 29.2877, 88.687, -11.0088, 0.0, 0.0)
	vehicle.setSolverParams(1E-6)
	vehicle.propogateEntry2(2400.0, 0.1, 180.0)

	coast = Orbiter(vehicle, 4000.0)


	def test_compute_exit_state_atm_relative(self):

		assert abs((self.coast.terminal_r - self.planet.RP)/1e3 - 1000) < 1.0
		assert abs((self.coast.terminal_theta) * 180/np.pi + 190.81) < 0.1
		assert abs((self.coast.terminal_phi) * 180 / np.pi - 63.80) < 0.1
		assert abs((self.coast.terminal_v) / 1e3 - 20.41) < 0.1
		assert abs((self.coast.terminal_g) * 180 / np.pi - 8.78) < 0.1
		assert abs((self.coast.terminal_psi) * 180 / np.pi - 273.297) < 0.1

	def test_compute_exit_state_inertial(self):
		assert abs((self.coast.terminal_r_bi - self.planet.RP) / 1e3 - 1000) < 1.0
		assert abs((self.coast.terminal_theta_bi) * 180 / np.pi + 190.81) < 0.1
		assert abs((self.coast.terminal_phi_bi) * 180 / np.pi - 63.80) < 0.1
		assert abs((self.coast.terminal_v_bi) / 1e3 - 20.382) < 0.1
		assert abs((self.coast.terminal_g_bi) * 180 / np.pi - 8.8035) < 0.1
		assert abs((self.coast.terminal_psi_bi) * 180 / np.pi - 273.297) < 0.1

	def test_compute_theta_star_exit(self):
		assert abs(self.coast.theta_star_exit*180/np.pi - 18.5214165) < 1e-2






