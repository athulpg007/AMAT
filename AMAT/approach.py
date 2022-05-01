# SOURCE FILENAME : approach.py
# AUTHOR          : Athul Pradeepkumar Girija, apradee@purdue.edu
# DAT CREATED     : 04/26/2022, 21:23 MT
# DATE MODIFIED   : 05/01/2022 16:14 MT
# REMARKS         : Compute the probe/spacecraft arrival trajectory
#                   following Kyle's dissertation Chapter 2.
# REFERENCE 	  : Hughes, Ph.D. Dissertation, 2016.

import numpy as np
from numpy import linalg as LA
from AMAT.planet import Planet

class Approach:
	"""
	Compute the probe/spacecraft approach trajectory for a given
	v_inf_vec, periapsis radius, psi.

	REF: Hughes (2016), Ph.D. Dissertation, Purdue University

	Attributes
	----------
	planetObj : AMAT.planet.Planet object
		arrival planet object for approach trajectory
	a : float
		semi-major axis, meters
	e : float
		eccentricity
	beta : float
		true anomaly of the outgoing asymptote, rad
	v_inf_vec_bi_kms : numpy.ndarray
		v_inf vector in body-inertial frame, km/s
	v_inf_vec_bi : numpy.ndarray
		v_inf vector in body-inertial frame, m/s
	v_inf_vec_bi_mag_kms : float
		v_inf magnitude in body-inertial frame, km/s
	phi_1 : float
		rad, as defined in Eq. (2.16) from REF.
	phi_2 : float
		rad, as defined in Eq. (2.17) from REF.
	rp_vec_bi_unit : numpy.ndarray
		periapsis radius unit vector in body-inertial frame
	rp_vec_bi : numpy.ndarray
		periapsis radius vector in body-inertial frame, meters
	e_vec_bi_unit : numpy.ndarray
		eccentricity unit vector in body-inertial frame
	e_vec_bi : numpy.ndarray
		eccentricity vector in body-inertial frame, meters
	h : float
		angular momentum, SI units
	h_vec_bi : numpy.ndarray
		angular momentum vector in body-inertial frame, SI units
	h_vec_bi_unit : numpy.ndarray
		angular momentum unit vector in body-inertial frame, SI units
	i : float
		inclination [0, np.pi], rad
	N_vec_bi : numpy.ndarray
		node vector in body-inertial frame
	N_vec_bi_unit : numpy.ndarray
		node unit vector in body-inertial frame
	OMEGA : float
		right asecension of ascending node, rad
	omega : float
		argument of periapsis, rad
	N_ref_bi : numpy.ndarray
		reference normal vector in body-inertial frame (planet's spin axis)
	S_vec_bi : numpy.ndarray
		S vector in body-inertial frame, meters
	S_vec_bi_unit : numpy.ndarray
		S unit vector in body-inertial frame, meters
	T_vec_bi : numpy.ndarray
		T vector in body-inertial frame, meters
	T_vec_bi_unit : numpy.ndarray
		T unit vector in body-inertial frame, meters
	R_vec_bi : numpy.ndarray
		R vector in body-inertial frame, meters
	R_vec_bi_unit : numpy.ndarray
		R unit vector in body-inertial frame, meters
	B_vec_bi : numpy.ndarray
		B vector in body-inertial frame, meters
	B_vec_bi_unit : numpy.ndarray
		B unit vector in body-inertial frame, meters
	b_mag : float
		aim point vector B magnitude, meters
	b_plane_angle_theta : float
		angle between aim point vector B and T
	r_EI : float
		atmospheric entry interface radius, m
	theta_star_entry : float
		true anomaly at entry interface, rad
	r_vec_entry_bi : numpy.ndarray
		position vector at entry interface in body-inertial frame, meters
	r_vec_entry_bi_unit : numpy.ndarray
		position unit vector at entry interface in body-inertial frame, meters
	r_vec_entry_bi_mag : float
		position vector magnitude at entry interface in body-inertial frame, meters
	v_entry_inertial_mag : float
		inertial velocity magnitude at entry interface in body-inertial frame, m/s
	gamma_entry_inertial : float
		inertial flight path angle at entry interface, rad
	v_vec_entry_bi : numpy.ndarray
		inertial velocity vector at entry interface in body-inertial frame, m/s
	v_vec_entry_bi_unit : numpy.ndarray
		inertial velocity unit vector at entry interface in body-inertial frame, m/s
	gamma_entry_inertial_check : float
		analytic solution for inertial flight path angle at entry interface, rad
	latitude_entry_bi : float
		entry latitude in body-inertial frame, rad
	longitude_entry_bi : float
		entry longitude in body-inertial frame, rad
	v_vec_entry_atm : numpy.ndarray
		atmosphere-relative velocity vector at entry interface in body-inertial frame, m/s
	v_entry_atm_mag : float
		atmosphere-relative velocity magnitude at entry interface in body-inertial frame, m/s
	v_vec_entry_atm_unit : numpy.ndarray
		atmosphere-relative velocity unit vector at entry interface in body-inertial frame, m/s
	gamma_entry_atm: float
		atmosphere-relative flight path angle at entry interface, rad
	v_vec_entry_atm_unit_proj : numpy.ndarray
		projection of atmosphere-relative vector onto local horizontal plane at entry interface
		in body-inertial frame
	local_latitude_parallel_vec_unit : numpy.ndarray
		unit vector direction of local parallel of latitude at entry interface in
		body-inertia frame
	heading_entry_atm : float
		atmosphere-relative heading angle at entry interface, rad
	"""

	def __init__(self, arrivalPlanet, v_inf_vec_icrf_kms, rp, psi,
				       is_entrySystem=False, h_EI=None):
		"""

		Initializes the Approach class with the following params

		Parameters
		----------
		arrivalPlanet : strarrivalPlanet : str
			Name of the planetary body, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		v_inf_vec_ICRF_kms : numpy.ndarray
			v_inf vector in ICRF, km/s
		rp : float
			target periapsis radius, meters
		psi : float
			angular position on ring of periapsis radius, rad
			following Hughes' Ph.D. dissertation (Purdue, 2016)
		is_entrySystem : bool, optional
			must be set to True if approach trajectory is for
			an atmospheric entry system (eg: probe or aerocapture vehicle).
			must be set to False for propulsive insertion orbiter which
			remains outside the atmosphere. False by default
		h_EI : float
			atmospheric entry interface altitude, meters
			must be provided if is_entrySystem is set to True
		"""

		self.planetObj = Planet(arrivalPlanet)
		self.a0 = self.planetObj.a0
		self.d0 = self.planetObj.d0

		self.v_inf_vec_icrf_kms = v_inf_vec_icrf_kms
		self.rp = rp
		self.psi = psi

		self.v_inf_mag_kms = LA.norm(self.v_inf_vec_icrf_kms)
		self.v_inf_mag = self.v_inf_mag_kms*1e3

		# Equations (2.12), (2.13), (2.14)
		self.a = -self.planetObj.GM/(self.v_inf_mag**2)
		self.e = 1 - self.rp/self.a
		self.beta = np.arccos(1.0/self.e)

		# Equation (2.3)
		self.v_inf_vec_bi_kms = self.ICRF_to_BI(self.v_inf_vec_icrf_kms)
		self.v_inf_vec_bi = self.v_inf_vec_bi_kms * 1e3
		self.v_inf_vec_bi_mag_kms = LA.norm(self.v_inf_vec_bi_kms)

		self.v_inf_vec_bi_unit = self.v_inf_vec_bi_kms / LA.norm(self.v_inf_vec_bi_kms)

		# Equation (2.16)
		self.phi_1 = np.arctan(self.v_inf_vec_bi[1] / self.v_inf_vec_bi[0])
		self.v_inf_vec_bi_prime = (np.matmul(self.R3(self.phi_1), self.v_inf_vec_bi.T)).T

		# Equation (2.17)
		self.phi_2 = np.arctan(self.v_inf_vec_bi_prime[0] / self.v_inf_vec_bi_prime[2])
		self.phi_2_analytic = np.arctan((self.v_inf_vec_bi[0] * np.cos(self.phi_1) + \
									     self.v_inf_vec_bi[1] * np.sin(self.phi_1)) / \
								         self.v_inf_vec_bi[2])

		self.rp_vec_bi_x_unit = np.cos(self.phi_1)*(np.sin(self.beta) * np.cos(self.psi) * np.cos(self.phi_2) + np.cos(self.beta) * np.sin(self.phi_2)) - \
								np.sin(self.phi_1) * np.sin(self.beta) * np.sin(self.psi)
		self.rp_vec_bi_y_unit = np.sin(self.phi_1)*(np.sin(self.beta) * np.cos(self.psi) * np.cos(self.phi_2) + np.cos(self.beta) * np.sin(self.phi_2)) + \
								np.cos(self.phi_1) * np.sin(self.beta) * np.sin(self.psi)
		self.rp_vec_bi_z_unit = np.cos(self.beta) * np.cos(self.phi_2) - np.sin(self.beta) * np.cos(self.psi) * np.sin(self.phi_2)

		self.rp_vec_bi_unit = np.array([self.rp_vec_bi_x_unit,
										self.rp_vec_bi_y_unit,
										self.rp_vec_bi_z_unit])

		self.rp_vec_bi = self.rp * self.rp_vec_bi_unit

		self.rp_vec_bi_dprime = self.BI_to_BI_dprime(self.rp_vec_bi)
		self.rp_vec_bi_dprime_analytic = self.rp * np.array([np.sin(self.beta) * np.cos(self.psi),
													np.sin(self.beta) * np.sin(self.psi),
													np.cos(self.beta)])

		self.e_vec_bi = self.e * self.rp_vec_bi_unit
		self.e_vec_bi_unit = self.e_vec_bi / LA.linalg.norm(self.e_vec_bi)

		self.h = np.sqrt(self.a * self.planetObj.GM * (1 - self.e**2))

		self.h_vec_bi = np.cross(self.rp_vec_bi, self.v_inf_vec_bi)
		self.h_vec_bi_unit = self.h_vec_bi / LA.norm(self.h_vec_bi)

		self.i = np.arccos(self.h_vec_bi_unit[2])

		self.N_vec_bi = np.cross(np.array([0, 0, 1]), self.h_vec_bi)
		self.N_vec_bi_unit = self.N_vec_bi / LA.norm(self.N_vec_bi)

		if self.N_vec_bi_unit[1] >= 0:
			self.OMEGA = np.arccos(self.N_vec_bi_unit[0])
		else:
			self.OMEGA = 2*np.pi - np.arccos(self.N_vec_bi_unit[0])

		if self.e_vec_bi_unit[2] >= 0:
			self.omega = np.arccos(np.dot(self.N_vec_bi_unit, self.e_vec_bi_unit))
		else:
			self.omega = 2*np.pi - np.arccos(np.dot(self.N_vec_bi_unit, self.e_vec_bi_unit))

		self.N_ref_bi = np.array([0, 0, 1])
		self.S_vec_bi = self.v_inf_vec_bi
		self.S_vec_bi_unit = self.v_inf_vec_bi_unit

		self.T_vec_bi = np.cross(self.S_vec_bi, self.N_ref_bi)
		self.T_vec_bi_unit = self.T_vec_bi / LA.norm(self.T_vec_bi)
		self.T_vec_bi_unit_dprime = self.BI_to_BI_dprime(self.T_vec_bi_unit)

		self.R_vec_bi = np.cross(self.S_vec_bi, self.T_vec_bi)
		self.R_vec_bi_unit = self.R_vec_bi / LA.norm(self.R_vec_bi)
		self.R_vec_bi_unit_dprime = self.BI_to_BI_dprime(self.R_vec_bi_unit)

		self.b_mag = abs(self.a) * np.sqrt(self.e ** 2 - 1)
		self.b_plane_angle_theta = self.psi + np.pi / 2

		self.B_vec_bi = np.cross(self.S_vec_bi, self.h_vec_bi)
		self.B_vec_bi_unit = self.B_vec_bi / LA.norm(self.B_vec_bi)


		if is_entrySystem == True:
			self.h_EI = h_EI
			self.r_EI = self.planetObj.RP + self.h_EI

			self.theta_star_entry = -1 * np.arccos(((self.h ** 2 / (self.planetObj.GM * self.r_EI)) - 1) * (1.0 / self.e))

			self.r_vec_entry_bi = self.pos_vec_bi(self.theta_star_entry)
			self.r_vec_entry_bi_unit = self.r_vec_entry_bi / LA.linalg.norm(self.r_vec_entry_bi)
			self.r_vec_entry_bi_mag = LA.linalg.norm(self.r_vec_entry_bi)

			self.v_entry_inertial_mag = np.sqrt(self.v_inf_mag**2 + 2 * self.planetObj.GM / self.r_EI)

			self.gamma_entry_inertial = -1 * np.arccos(self.h / (self.r_EI * self.v_entry_inertial_mag))

			self.v_vec_entry_bi = self.vel_vec_bi(self.theta_star_entry)
			self.v_vec_entry_bi_unit = self.v_vec_entry_bi / LA.linalg.norm(self.v_vec_entry_bi)

			self.gamma_entry_inertial_check = np.pi / 2 - \
											  np.arccos(np.dot(self.r_vec_entry_bi_unit, self.v_vec_entry_bi_unit))

			self.latitude_entry_bi = np.arcsin(self.r_vec_entry_bi_unit[2])
			self.longitude_entry_bi = np.arctan(self.r_vec_entry_bi_unit[1] / self.r_vec_entry_bi_unit[0])

			self.xi_1 = np.arctan(self.r_vec_entry_bi_unit[1]/self.r_vec_entry_bi_unit[0])
			self.latitude_entry_bi_analytic = np.arctan(self.r_vec_entry_bi_unit[2]/
														(self.r_vec_entry_bi_unit[0]*np.cos(self.xi_1) + self.r_vec_entry_bi_unit[1]*np.sin(self.xi_1)))

			self.v_vec_entry_atm = self.vel_vec_entry_atm()
			self.v_entry_atm_mag = LA.linalg.norm(self.v_vec_entry_atm)
			self.v_vec_entry_atm_unit = self.v_vec_entry_atm / self.v_entry_atm_mag

			self.gamma_entry_atm = np.pi / 2 - \
								   np.arccos(np.dot(self.r_vec_entry_bi_unit, self.v_vec_entry_atm_unit))

			self.v_vec_entry_atm_unit_proj = self.v_vec_entry_atm_unit - \
										     np.dot(self.v_vec_entry_atm_unit, self.r_vec_entry_bi_unit)*self.r_vec_entry_bi_unit


			self.local_latitude_parallel_vec_unit = np.array([ -np.sin(self.longitude_entry_bi),
															    np.cos(self.longitude_entry_bi),
															    0.0])

			self.heading_entry_atm = np.arccos(np.dot(self.v_vec_entry_atm_unit_proj, self.local_latitude_parallel_vec_unit))

		else:
			self.theta_star_periapsis = 0

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
		R1R3 = np.matmul(self.R1(np.pi/2 - self.d0), self.R3(np.pi / 2 + self.a0))
		return np.matmul(R1R3, X_ICRF.T).T

	def BI_to_BI_dprime(self, X_ICRF):
		"""
		Converts an input vector from body-inertial to body-inertial-double-prime
		frame following Eq. (2.10) of REF.

		Parameters
		----------
		X_ICRF : numpy.ndarray
			row vector in body-inertial frame

		Returns
		-------
		ans : numpy.ndarray
			input vector in body-inertial double-prime frame

		"""
		R2R3 = np.matmul(self.R2(self.phi_2), self.R3(self.phi_1))
		return np.matmul(R2R3, X_ICRF.T).T

	def pos_vec_bi(self, theta_star):
		"""
		Computes the position vector in body-inertial frame
		for a specified true-anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		pos_vec_bi : numpy.ndarray
			position vector in body-inertial frame, meters
		"""

		r = (self.h**2 / self.planetObj.GM) / (1 + self.e*np.cos(theta_star))
		theta = theta_star + self.omega

		rx_unit = np.cos(self.OMEGA)*np.cos(theta) - np.sin(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		ry_unit = np.sin(self.OMEGA)*np.cos(theta) + np.cos(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		rz_unit = np.sin(self.i)*np.sin(theta)

		pos_vec_bi = r*np.array([rx_unit, ry_unit, rz_unit])
		return pos_vec_bi


	def pos_vec_bi_dprime(self, theta_star):

		"""
		Computes the position vector in body-inertial double-prime
		frame for a specified true-anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		pos_vec_bi_dprime : numpy.ndarray
			position vector in body-inertial double-prime frame, meters
		"""

		pos_vec_bi = self.pos_vec_bi(theta_star)

		pos_vec_bi_dprime = (np.matmul(self.R2(self.phi_2),
		        			 np.matmul(self.R3(self.phi_1), pos_vec_bi))).T

		return pos_vec_bi_dprime


	def r_mag_bi(self, theta_star):
		"""
		Computes the position vector magnitude in body-inertial frame at a given true anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		r_mag_bi : float
			position vector magnitude, meters

		"""
		r_mag_bi = (self.h**2 / self.planetObj.GM) / (1 + self.e*np.cos(theta_star))
		return r_mag_bi

	def vel_vec_bi(self, theta_star):
		"""
		Computes the velocity vector magnitude in body-inertial frame at a given true anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		vel_vec_bi : numpy.ndarray
			velocity vector in body-inertial frame, m/s

		"""

		r_mag_bi = self.r_mag_bi(theta_star)
		v_mag_bi = np.sqrt((self.v_inf_mag)**2 + 2*self.planetObj.GM/r_mag_bi)
		gamma = -1*np.arccos(self.h/(r_mag_bi*v_mag_bi))

		vr = v_mag_bi*np.sin(gamma)
		vt = v_mag_bi*np.cos(gamma)
		theta = theta_star + self.omega

		vx = vr*( np.cos(theta)*np.cos(self.OMEGA) - np.sin(theta)*np.cos(self.i)*np.sin(self.OMEGA)) +\
		     vt*(-np.sin(theta)*np.cos(self.OMEGA) - np.cos(theta)*np.cos(self.i)*np.sin(self.OMEGA))

		vy = vr*( np.cos(theta)*np.sin(self.OMEGA) + np.sin(theta)*np.cos(self.i)*np.cos(self.OMEGA)) +\
		     vt*( np.cos(theta)*np.cos(self.i)*np.cos(self.OMEGA) - np.sin(theta)*np.sin(self.OMEGA))

		vz = vr*np.sin(theta)*np.sin(self.i) + vt*np.cos(theta)*np.sin(self.i)

		vel_vec_bi = np.array([vx, vy, vz])
		return vel_vec_bi

	def vel_vec_entry_atm(self):
		"""
		Computes the atmosphere-relative velocity vector magnitude in body-inertial frame
		at atmospheric entry interface.

		Parameters
		----------

		Returns
		-------
		vel_vec_entry_atm : numpy.ndarray
			atmosphere-relative velocity vector in body-inertial frame, at
			atmospheric entry interface, m/s

		"""
		v_entry_atm_x = self.v_vec_entry_bi[0] - \
		          self.r_vec_entry_bi_mag * self.planetObj.OMEGA * \
		          np.cos(self.latitude_entry_bi) * (-np.sin(self.longitude_entry_bi))
		v_entry_atm_y = self.v_vec_entry_bi[1] - \
		          self.r_vec_entry_bi_mag * self.planetObj.OMEGA * \
		          np.cos(self.latitude_entry_bi) * (np.cos(self.longitude_entry_bi))
		v_entry_atm_z = self.v_vec_entry_bi[2]

		vel_vec_entry_atm = np.array([v_entry_atm_x, v_entry_atm_y, v_entry_atm_z])
		return vel_vec_entry_atm
