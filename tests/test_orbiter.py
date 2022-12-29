"""
test_orbiter.py

Tests for Orbiter class

"""
import numpy as np

from AMAT.planet import Planet
from AMAT.vehicle import Vehicle


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

	orbiter = Orbiter(vehicle, 4000.0)
	orbiter.compute_probe_targeting_trajectory(178 * np.pi / 180, -90)
	orbiter.compute_orbiter_deflection_trajectory(182 * np.pi / 180, 90)


	def test_compute_exit_state_atm_relative(self):

		assert abs((self.orbiter.terminal_r - self.planet.RP) / 1e3 - 1000) < 1.0
		assert abs((self.orbiter.terminal_theta) * 180 / np.pi + 190.81) < 0.1
		assert abs((self.orbiter.terminal_phi) * 180 / np.pi - 63.80) < 0.1
		assert abs((self.orbiter.terminal_v) / 1e3 - 20.41) < 0.1
		assert abs((self.orbiter.terminal_g) * 180 / np.pi - 8.78) < 0.1
		assert abs((self.orbiter.terminal_psi) * 180 / np.pi - 273.297) < 0.1

	def test_compute_exit_state_inertial(self):
		assert abs((self.orbiter.terminal_r_bi - self.planet.RP) / 1e3 - 1000) < 1.0
		assert abs((self.orbiter.terminal_theta_bi) * 180 / np.pi + 190.81) < 0.1
		assert abs((self.orbiter.terminal_phi_bi) * 180 / np.pi - 63.80) < 0.1
		assert abs((self.orbiter.terminal_v_bi) / 1e3 - 20.382) < 0.1
		assert abs((self.orbiter.terminal_g_bi) * 180 / np.pi - 8.8035) < 0.1
		assert abs((self.orbiter.terminal_psi_bi) * 180 / np.pi - 273.297) < 0.1

	def test_compute_theta_star_exit(self):
		assert abs(self.orbiter.theta_star_exit * 180 / np.pi - 18.5214165) < 1e-2


	def test_probe_delivery(self):
		assert abs(self.orbiter.h_periapsis_probe/1e3 - -743.23) < 1e-2

	def test_inertial_entry_speed(self):
		assert abs(self.orbiter.v_bi_mag_probe_entry / 1e3 - 20.3808330) < 1e-6

	def test_inertial_gamma_entry(self):
		assert abs(self.orbiter.gamma_inertial_probe_entry*180/np.pi - -14.482985116) < 1e-6

	def test_atm_relative_entry_speed(self):
		assert abs(self.orbiter.v_mag_probe_entry_atm/1e3 - 20.4058249) < 1e-6

	def test_atm_gamma_entry(self):
		assert abs(self.orbiter.gamma_atm_probe_entry*180/np.pi - -14.14625695788) < 1e-6

	def test_atm_heading_entry(self):
		assert abs(self.orbiter.heading_atm_probe_entry*180/np.pi - 87.162773860) < 1e-6

	def test_probe_entry_state(self):
		assert abs(self.orbiter.h_EI / 1e3 - 1000.0) < 1e-6
		assert abs(round(self.orbiter.longitude_probe_entry_bi * 180 / np.pi, 2) - -10.96) < 1e-2
		assert abs(round(self.orbiter.latitude_probe_entry_bi * 180 / np.pi, 2) - 67.25) < 1e-2
		assert abs(round(self.orbiter.v_mag_probe_entry_atm / 1e3, 4) - 20.4058) < 1e-2
		assert abs(round(self.orbiter.heading_atm_probe_entry * 180 / np.pi, 4) - 87.1628) < 1e-2
		assert abs(round(self.orbiter.gamma_atm_probe_entry * 180 / np.pi, 4) - -14.1463) < 1e-2

	def test_orbiter_deflection_trajectory_periapsis(self):
		assert abs(self.orbiter.h_periapsis_orbiter_defl/1e3 - 4033.662882) < 1e-3







