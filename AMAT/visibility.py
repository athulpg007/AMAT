# SOURCE FILENAME : visibility.py
# AUTHOR          : Athul Pradeepkumar Girija, apradee@purdue.edu
# DATE CREATED    : 11/09/2022, 07:20 MT
# DATE MODIFIED   : 11/09/2022 07:20 MT
# REMARKS         : Compute the visibility of a target planet from an observer planet landing site
# REFERENCE 	  : Hughes, Ph.D. Dissertation, 2016.

from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body_barycentric_posvel
import numpy as np
from astropy.time import Time
from AMAT.planet import Planet

solar_system_ephemeris.set('jpl')


class TargetElevation:
	"""
	Computes the elevation of a target planet from a site on an observer planet over
	one full rotation of the observer planet.

	Attributes
	-----------
	planetObj :  AMAT.planet.Planet
		object for the observer planet
	observer_planet : str
		observer planet
	target_planet : str
		target planet
	a0 : float
		observer planet north pole right ascension wrt ICRF
	d0 : float
		observer planet north pole declination wrt ICRF
	arrival_date : astropy.time.Time object
		datetime object with scale=tdb
	longitude_array : numpy.ndarray
		body inertial longitude array, degrees
	hours_array : numpy.ndarray
		time array, hours
	beta_array : numpy.ndarray
		beta angle array, degrees
	elevation_array : numpy.ndarray
		elevation angle array, degrees
	"""

	def __init__(self, target_planet, observer_planet, latitude, date, num_points=101):
		"""

		Parameters
		----------
		target_planet : str
			Name of the planetary body whose elevation in the sky will be computed.
			Must be all uppercase. Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		observer_planet : str
			Name of the planetary body on which the observer is located.
			Must be all uppercase. Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'.
			Must be different from target_planet
		latitude : float
			latitude of the landing site on observer planet, degrees
		date : str
			Datetime in the format "2036-03-28 00:00:00"
		num_points : int
			number of points to compute over one full rotation, defaults to 101

		"""

		self.planetObj = Planet(observer_planet)
		self.observer_planet = observer_planet
		self.target_planet = target_planet

		self.a0 = self.planetObj.a0
		self.d0 = self.planetObj.d0

		# Compute the Solar System barycentric position of the observer planet
		if observer_planet == 'TITAN':
			self.observer_planet = 'SATURN'
		else:
			self.observer_planet = observer_planet

		self.arrival_date = Time(date, scale="tdb")

		# Compute the ephemeris for the observer and target planet
		self.observer_planet_eph = get_body_barycentric_posvel(self.observer_planet, self.arrival_date)
		self.target_planet_eph = get_body_barycentric_posvel(target_planet, self.arrival_date)

		# Compute observer to target  Solar System barycentric position(s) in ICRF (km)
		self.obs_planet_pos = np.array([self.observer_planet_eph [0].x.value,
										self.observer_planet_eph [0].y.value,
										self.observer_planet_eph [0].z.value])
		self.tar_planet_pos = np.array([self.target_planet_eph[0].x.value,
										self.target_planet_eph[0].y.value,
										self.target_planet_eph[0].z.value])

		# Compute observer to target position vector in ICRF
		self.obs_tar_pos_vec_icrf = self.tar_planet_pos - self.obs_planet_pos
		self.obs_tar_pos_vec_icrf_unit = self.obs_tar_pos_vec_icrf / np.linalg.norm(self.obs_tar_pos_vec_icrf)

		# Convert observer to target unit vector in ICRF to observer BI frame
		self.obs_tar_pos_vec_bi_unit = self.ICRF_to_BI(self.obs_tar_pos_vec_icrf_unit)

		self.longitude_array = np.linspace(0, 360, num_points)  # body inertial longitude array
		self.hours_array = np.linspace(0, 2*np.pi/(self.planetObj.OMEGA*3600), num_points)  # time (hours) array
		self.beta_array = np.array([])  # beta angle array
		self.elevation_array = np.array([])  # elevation angle array

		# Compute the elevation angle of the target for each longitude in longitude_array
		for longitude in self.longitude_array:
			self.lander_pos_x_bi = self.planetObj.RP*np.cos(latitude*np.pi/180)*np.cos(longitude*np.pi/180)
			self.lander_pos_y_bi = self.planetObj.RP*np.cos(latitude*np.pi/180)*np.sin(longitude*np.pi/180)
			self.lander_pos_z_bi = self.planetObj.RP*np.sin(latitude*np.pi/180)

			# Compute the lander zenith direction unit vector in the BI frame
			self.lander_pos_vec_bi = np.array([self.lander_pos_x_bi, self.lander_pos_y_bi, self.lander_pos_z_bi])
			self.lander_pos_vec_bi_unit = self.lander_pos_vec_bi / np.linalg.norm(self.lander_pos_vec_bi)

			# compute angle beta between lander zenith and observer to target unit vector
			self.beta = np.arccos(np.dot(self.lander_pos_vec_bi_unit, self.obs_tar_pos_vec_bi_unit))*180/np.pi
			self.elevation = max(0, 90 - self.beta)  # if negative, target is below the horizon: set to 0

			self.beta_array = np.append(self.beta_array, self.beta)
			self.elevation_array = np.append(self.elevation_array, self.elevation)


	def ICRF_to_BI(self, X_ICRF):
		"""
		Converts an input vector from ICRF to body-inertial frame

		Parameters
		----------
		X_ICRF : numpy.ndarray
			row vector in ICRF frame

		Returns
		-------
		ans : numpy.ndarray
			input vector in body-inertial frame

		"""
		R1R3 = np.matmul(self.R1(np.pi/2 - self.d0), self.R3(np.pi/2 + self.a0))
		return np.matmul(R1R3, X_ICRF.T).T

	def R1(self, theta):
		"""
		Direction cosine matrix for rotation about x-axis.

		Parameters
		----------
		theta : float
			rotation angle about x-axis

		Returns
		-------
		ans : numpy.ndarray
			Direction cosine matrix for rotation about x-axis.

		"""
		return np.array([[1, 0, 0],
						 [0, np.cos(theta), np.sin(theta)],
						 [0, -np.sin(theta), np.cos(theta)]])

	def R2(self, theta):
		"""
		Direction cosine matrix for rotation about y-axis.

		Parameters
		----------
		theta : float
			rotation angle about y-axis

		Returns
		-------
		ans : numpy.ndarray
			Direction cosine matrix for rotation about y-axis.

		"""
		return np.array([[np.cos(theta), 0, -np.sin(theta)],
						 [0, 1, 0],
						 [np.sin(theta), 0, np.cos(theta)]])

	def R3(self, theta):
		"""
		Direction cosine matrix for rotation about z-axis.

		Parameters
		----------
		theta : float
			rotation angle about zaxis

		Returns
		-------
		ans : numpy.ndarray
			Direction cosine matrix for rotation about z-axis.

		"""
		return np.array([[np.cos(theta), np.sin(theta), 0],
						 [-np.sin(theta), np.cos(theta), 0],
						 [0, 0, 1]])
