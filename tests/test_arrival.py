"""
test_arrival.py

Tests for Arrival class

"""

import numpy as np
from astropy.time import Time


class TestImportArrival():
	def test_import_arrival(self):
		try:
			from AMAT.arrival import Arrival
			return True
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import Arrival from AMAT.arrival")
			assert False

try:
	from AMAT.arrival import Arrival
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Arrival from AMAT.arrival")


class Test_Arrival_specified_vinf_vec:

	arrival = Arrival()
	arrival.set_vinf_vec_manually("NEPTUNE", np.array([17.78952518,  8.62038536,  3.15801163]))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 20.01877337298844) < 1e-6

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (abs(declination) - 8.755478798) < 1e-6


class Test_Arrival_Neptune_2039:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('JUPITER',
	                                  'NEPTUNE',
	                                  Time("2032-06-29 00:00:00", scale='tdb'),
	                                  Time("2039-01-03 00:00:00", scale='tdb'))

	def test_compute_v_inf_vector(self):
		v_inf_vector = self.arrival.compute_v_inf_vector()
		assert abs(v_inf_vector[0] - 17.78952518) < 1e-6
		assert abs(v_inf_vector[1] - 8.62038536) < 1e-6
		assert abs(v_inf_vector[2] - 3.15801163) < 1e-6

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 20.01877337298844) < 1e-6

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (abs(declination) - 8.755478798) < 1e-6


class Test_Arrival_Uranus_2043:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('JUPITER',
	                                  'URANUS',
	                                  Time("2036-03-28 00:00:00", scale='tdb'),
	                                  Time("2043-05-17 00:00:00", scale='tdb'))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 8.41) < 1e-2

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (abs(declination) - 48) < 1.0


class Test_Arrival_Neptune_2043:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('JUPITER',
	                                  'NEPTUNE',
	                                  Time("2033-08-22 00:00:00", scale='tdb'),
	                                  Time("2043-04-28 00:00:00", scale='tdb'))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 11.4) < 1e-1

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (abs(declination) - 9.1) < 0.5


class Test_Arrival_Saturn_2034:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('EARTH',
	                                  'SATURN',
	                                  Time("2031-09-03 00:00:00", scale='tdb'),
	                                  Time("2034-12-30 00:00:00", scale='tdb'))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		pass


class Test_Arrival_Uranus_2045:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('JUPITER',
	                                  'URANUS',
	                                  Time("2036-04-29 00:00:00", scale='tdb'),
	                                  Time("2045-05-03 00:00:00", scale='tdb'))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 5.96) < 1e-1

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (declination + 49.69) < 0.5


class Test_Arrival_Uranus_2039:

	arrival = Arrival()
	arrival.set_vinf_vec_from_lambert_arc('JUPITER',
	                                  'URANUS',
	                                  Time("2035-09-04 00:00:00", scale='tdb'),
	                                  Time("2039-05-18 00:00:00", scale='tdb'))

	def test_compute_v_inf_mag(self):
		v_inf_mag = self.arrival.compute_v_inf_mag()
		assert abs(v_inf_mag - 20.518) < 1e-2

	def test_compute_declination(self):
		declination = self.arrival.compute_declination()
		assert (declination + 48.89) < 0.5
