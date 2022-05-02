# SOURCE FILENAME : arrival.py
# AUTHOR          : Athul Pradeepkumar Girija, athulpg007@gmail.com
# DATE CREATED    : 04/19/2022, 07:54 MT
# DATE MODIFIED   : 04/30/2022, 07:54 MT
# REMARKS         : Compute the arrival conditions: v_inf_vector, v_inf_mag,
#					arrival declination.


from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric_posvel
import numpy as np

from poliastro.bodies import Sun
from poliastro import iod
from astropy import units as u
from numpy import linalg as LA

from AMAT.planet import Planet

solar_system_ephemeris.set('jpl')

class Arrival:
	"""
	Compute the arrival declination from either a user-supplied v_inf vector in ICRF,
	or a v_inf_vector computed from a Lambert arc (last planetary encounter prior to
	arrival anf arrival date)

	Attributes
	----------
	v_inf_vec : numpy.ndarray
		v_inf vector, km/s
	v_inf_mag : float
		v_inf magnitude, km/s
	v_inf_vec_unit : numpy.ndarray
		v_inf unit vector
	north_pole : numpy.ndarray
		north pole direction in ICRF unit vector
	angle : float
		angle between v_inf_vec and planet north pole, rad
	declination : float
		arrival declination, angle between v_inf_vec and
		planetary equator
	"""

	def init__(self):
		self.v_inf_vec = None
		self.v_inf_mag = None
		self.v_inf_vec_unit = None
		self.north_pole = None
		self.angle = None
		self.declination = None

	def set_vinf_vec_manually(self, arrivalPlanet, v_inf_vec_ICRF_kms):
		"""
		Set arrival v_inf_vec manually if available

		Parameters
		----------
		arrivalPlanet : str
			Name of the planetary body, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		v_inf_vec_ICRF_kms : numpy.ndarray
			v_inf vector in ICRF, km/s
		"""

		self.v_inf_vec = v_inf_vec_ICRF_kms
		self.v_inf_mag = LA.norm(self.v_inf_vec)

		# compute arrival vinf unit vector
		self.v_inf_vec_unit = self.v_inf_vec / self.v_inf_mag

		# compute arrival planet north pole vector
		planetObj = Planet(arrivalPlanet)
		a0 = planetObj.a0
		d0 = planetObj.d0
		self.north_pole = np.array([np.cos(d0) * np.cos(a0), np.cos(d0) * np.sin(a0), np.sin(d0)])

		# compute angle between vinf vector and north pole vector
		self.angle = np.arccos(np.dot(self.north_pole, self.v_inf_vec_unit)) * 180 / np.pi

		# compute declination
		self.declination = 90 - self.angle

	def set_vinf_vec_from_lambert_arc(self, lastFlybyPlanet, arrivalPlanet, lastFlybyDate, arrivalDate,
									  M=0, numiter=100, rtol=1e-6):
		"""
		Compute the v_inf_vec from a lambert arc solution
		if the last flyby date and the arrival date is known

		Parameters
		----------
		lastFlybyPlanet : str
			Name of the last flyby planet, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		arrivalPlanet : str
			Name of the arrival planet, must be all uppercase;
				Valid entries are: 'VENUS', 'EARTH', 'MARS',
				'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		lastFlybyDate : astropy.time.Time object
			last planetary flyby date-time before arrival,
			scale = tdb (Barycentric Dynamical Time)
			example: Time("2036-03-28 00:00:00", scale='tdb')
		arrivalDate : astropy.time.Time object
			planetary arrival date-time at destination,
			scale = tdb (Barycentric Dynamical Time)
			example: Time("2036-03-28 00:00:00", scale='tdb')
		M : int, optional
			number of full revolutions for Lambert solution
			defaults to 0
		numiter :  int, optional
			maximum number of iterations
			defaults to 100
		rtol: float, optional
			relative tolerance for lambert solver
			defaults to 1e-6
		"""

		self.lastFlybyPlanet_eph = get_body_barycentric_posvel(lastFlybyPlanet, lastFlybyDate)
		self.arrivalPlanet_eph = get_body_barycentric_posvel(arrivalPlanet, arrivalDate)

		self.TOF = arrivalDate - lastFlybyDate

		self.lastFlybyPlanet_pos = np.array([self.lastFlybyPlanet_eph[0].x.value,
											 self.lastFlybyPlanet_eph[0].y.value,
											 self.lastFlybyPlanet_eph[0].z.value])

		self.lastFlybyPlanet_vel = np.array([self.lastFlybyPlanet_eph[1].x.value / 86400,
											 self.lastFlybyPlanet_eph[1].y.value / 86400,
											 self.lastFlybyPlanet_eph[1].z.value / 86400])

		self.arrivalPlanet_pos = np.array([self.arrivalPlanet_eph[0].x.value,
										   self.arrivalPlanet_eph[0].y.value,
										   self.arrivalPlanet_eph[0].z.value])

		self.arrivalPlanet_vel = np.array([self.arrivalPlanet_eph[1].x.value / 86400,
										   self.arrivalPlanet_eph[1].y.value / 86400,
										   self.arrivalPlanet_eph[1].z.value / 86400])

		(self.v_dep, self.v_arr), = iod.izzo.lambert(Sun.k, self.lastFlybyPlanet_pos * u.km,
													 self.arrivalPlanet_pos * u.km,
													 self.TOF,
													 M=M, numiter=numiter, rtol=rtol)

		self.v_inf_vec = self.v_arr.value - self.arrivalPlanet_vel
		self.v_inf_mag = LA.norm(self.v_inf_vec)

		# compute arrival vinf unit vector
		self.v_inf_vec_unit = self.v_inf_vec / self.v_inf_mag

		# compute arrival planet north pole vector
		planetObj = Planet(arrivalPlanet)
		a0 = planetObj.a0
		d0 = planetObj.d0
		self.north_pole = np.array([np.cos(d0) * np.cos(a0), np.cos(d0) * np.sin(a0), np.sin(d0)])

		# compute angle between vinf vector and north pole vector
		self.angle = np.arccos(np.dot(self.north_pole, self.v_inf_vec_unit)) * 180 / np.pi

		# compute declination
		self.declination = 90 - self.angle


	def compute_v_inf_vector(self):
		"""

		Returns
		-------
		self.v_inf_vec : numpy.ndarray
			returns the manually set / computed v_inf_vec in ICRF, km/s
		"""

		return self.v_inf_vec

	def compute_v_inf_mag(self):
		"""

		Returns
		-------
		self.v_inf_mag : float
			returns the computed v_inf magnitude in ICRF, km/s
		"""

		return self.v_inf_mag

	def compute_declination(self):
		"""

		Returns
		-------
		self.declination : float
			returns the computed arrival declination, rad
		"""

		return self.declination

