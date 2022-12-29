import numpy as np
from AMAT.approach import Approach
from AMAT.orbiter import PropulsiveOrbiter

try:
	from AMAT.visibility import LanderToPlanet, LanderToOrbiter, OrbiterToPlanet
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import LanderToPlanet, LanderToOrbiter, OrbiterToPlanet from AMAT.visibility")


class Test_Titan_Earth_Equatorial:
	visibility = LanderToPlanet(observer_planet="TITAN", target_planet="EARTH", latitude=3.0, date="2034-03-28 00:00:00")

	def test_range(self):
		assert abs(self.visibility.range/1.5e11 - 8.836) < 0.01

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 61.87) < 0.1


class Test_Titan_Earth_High_Latitude_North:
	visibility = LanderToPlanet(observer_planet="TITAN", target_planet="EARTH", latitude=60.0, date="2034-03-28 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 4.87) < 0.1


class Test_Earth_Mars_40_North:
	visibility = LanderToPlanet(observer_planet="EARTH", target_planet="MARS", latitude=40, date="2022-11-09 00:00:00")

	def test_range(self):
		assert abs(self.visibility.range/1.4959e11 - 0.587) < 0.01

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 74.18) < 0.1


class Test_Earth_Jupiter_40_North:
	visibility = LanderToPlanet(observer_planet="EARTH", target_planet="JUPITER", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 48.14) < 0.1


class Test_Earth_Saturn_40_North:
	visibility = LanderToPlanet(observer_planet="EARTH", target_planet="SATURN", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 33.49) < 0.1


class Test_Earth_Uranus_40_North:
	visibility = LanderToPlanet(observer_planet="EARTH", target_planet="URANUS", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 66.42) < 0.1

class Test_Earth_Neptune_40_North:
	visibility = LanderToPlanet(observer_planet="EARTH", target_planet="NEPTUNE", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 45.90) < 0.1


class Test_OrbiterElevationRange_Titan:
	approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]), rp=(2575+1500)*1e3, psi=3*np.pi/2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
	visibility = LanderToOrbiter(planet="TITAN", latitude=3.00, orbiter=orbiter, t_seconds=86400 * 16, num_points=2001)

	def test_elevation_and_range(self):
		assert abs(min(self.visibility.range_array) / 1e3 - 1520.05) < 0.1
		assert abs(max(self.visibility.elevation_array) - 86.69) < 0.1


class Test_OrbiterElevationRange_EQUATORIAL_ORBIT_EARTH:
	approach = Approach("EARTH", v_inf_vec_icrf_kms=np.array([1, 1, 0]), rp=(6371 + 250) * 1e3, psi=3*np.pi/2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=250)
	visibility = LanderToOrbiter(planet="EARTH", latitude=0.00, orbiter=orbiter, t_seconds=1200, num_points=1001)

	def test_elevation_and_range(self):
		assert abs(min(self.visibility.range_array)/1e3 - 250) < 0.1
		assert abs(max(self.visibility.elevation_array) - 90) < 1.0


class Test_OrbiterToPlanet:
	approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]), rp=(2575+1500)*1e3, psi=3*np.pi/2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
	visibility = OrbiterToPlanet(target_planet="EARTH", observer_planet="TITAN",
								 orbiter=orbiter, date="2034-03-28 00:00:00", t_seconds=86400, num_points=1600)

	def test_visibility(self):
		assert True in self.visibility.visible_array
		assert False in self.visibility.visible_array
