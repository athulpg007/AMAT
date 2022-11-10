class TestImportVisibility:
	def test_import_arrival(self):
		try:
			from AMAT.visibility import TargetElevation
			return True
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import TargetElevation from AMAT.visibility")
			assert False


try:
	from AMAT.visibility import TargetElevation
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import TargetElevation from AMAT.visibility")

class Test_Titan_Earth_Equatorial:
	visibility = TargetElevation(observer_planet="TITAN", target_planet="EARTH", latitude=3.0, date="2034-03-28 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 61.87) < 0.1


class Test_Titan_Earth_High_Latitude_North:
	visibility = TargetElevation(observer_planet="TITAN", target_planet="EARTH", latitude=60.0, date="2034-03-28 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 4.87) < 0.1


class Test_Earth_Mars_40_North:
	visibility = TargetElevation(observer_planet="EARTH", target_planet="MARS", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 74.18) < 0.1


class Test_Earth_Jupiter_40_North:
	visibility = TargetElevation(observer_planet="EARTH", target_planet="JUPITER", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 48.14) < 0.1


class Test_Earth_Saturn_40_North:
	visibility = TargetElevation(observer_planet="EARTH", target_planet="SATURN", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 33.49) < 0.1


class Test_Earth_Uranus_40_North:
	visibility = TargetElevation(observer_planet="EARTH", target_planet="URANUS", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 66.42) < 0.1

class Test_Earth_Neptune_40_North:
	visibility = TargetElevation(observer_planet="EARTH", target_planet="NEPTUNE", latitude=40, date="2022-11-09 00:00:00")

	def test_max_elevation(self):
		assert abs(max(self.visibility.elevation_array) - 45.90) < 0.1
