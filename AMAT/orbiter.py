# SOURCE FILENAME : orbiter.py
# AUTHOR          : Athul Pradeepkumar Girija, apradee@purdue.edu
# DATE CREATED    : 06/01/2022 07:51 AM
# DATE MODIFIED   : 06/01/2022 07:51 MT
# REMARKS         : Compute the coast trajectory from atmospheric exit until
#					apoapsis, the periapsis raise manuever dv, and the
#   				first full orbit post aerocapture.



import numpy as np

class Orbiter:
	"""
	Compute the coast trajectory from atmospheric exit until
	apoapsis, the periapsis raise manuever dv, and the
	first full orbit trajectory post aerocapture.

	Attributes
	----------
	vehicle : AMAT.vehicle.Vehicle
		Vehicle object which has been propagated until atmospheric exit
	peri_alt_km : float
		target orbit periapsis altitude, km
	r_periapsis_mag : float
		target orbit periapsis radial distance, m
	terminal_r : float
		planet-relative atmospheric exit state terminal radial distance, m
	terminal_theta : float
		planet-relative atmospheric exit state terminal longitude, rad
	terminal_phi : float
		planet-relative atmospheric exit state terminal latitude, rad
	terminal_v : float
		planet-relative atmospheric exit state terminal speed, m/s
	terminal_g : float
		planet-relative atmospheric exit state terminal flight-path angle, rad
	terminal_psi : float
		planet-relative atmospheric exit state terminal heading angle, rad
	terminal_r_vec : numpy.ndarray
		planet-relative atmospheric exit state radius vector, m
	terminal_r_hat_vec : numpy.ndarray
		planet-relative atmospheric exit state radius unit vector
	terminal_v_vec : numpy.ndarray
		planet-relative atmospheric exit state velocity vector, m/s
	terminal_r_hat_vec : numpy.ndarray
		planet-relative atmospheric exit state velocity unit vector
	terminal_v_ie_vec : numpy.ndarray
		inertial atmospheric exit state velocity vector, m/s
	terminal_v_ie_hat_vec : numpy.ndarray
		inertial atmospheric exit state velocity unit vector
	terminal_fpa_ie_deg : float
		inertial atmospheric exit state flight-path angle, deg
	terminal_fpa_ie_rad : float
		inertial atmospheric exit state flight-path angle, rad
	terminal_r_bi : float
		body-inertial atmospheric exit state terminal radial distance, m
	terminal_theta_bi : float
		body-inertial atmospheric exit state terminal longitude, rad
	terminal_phi_bi : float
		body-inertial atmospheric exit state terminal latitude, rad
	terminal_v_bi : float
		body-inertial atmospheric exit state terminal speed, m/s
	terminal_g_bi : float
		body-inertial atmospheric exit state terminal flight-path angle, rad
	terminal_psi_bi : float
		body-inertial atmospheric exit state terminal heading angle, rad
	terminal_E : float
		orbit total specific energy at atmospheric exit
	terminal_h : float
		orbit specific angular momentum scalar at atmospheric exit
	a : float
		final orbit semi-major axis, m
	e : float
		final orbit eccentricity
	i : float
		final orbit inclination, rad
	h : float
		final orbit specific angular momentum, SI units
	OMEGA : float
		final orbit RAAN, rad
	omega : float
		final orbit AoP, rad
	theta_star_exit : float
		true anomaly at atmospheric exit, rad
	x_coast_arr : numpy.ndarray
		body-inertial x-coordinate positions of coast trajectory from atmospheric exit until apoapsis,
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	y_coast_arr : numpy.ndarray
		body-inertial y-coordinate positions of coast trajectory from atmospheric exit until apoapsis,
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	z_coast_arr : numpy.ndarray
		body-inertial z-coordinate positions of coast trajectory from atmospheric exit until apoapsis,
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	r_apoapsis_vec : numpy.ndarray
		body-inertial radial vector of apoapsis, in terms of planet radius (vehicle.planetObj.RP)
	r_apoapsis_mag : float
		body-inertial radial apoapsis distance, m
	v_apoapsis_vec_coast : float
		body-inertial velocity vector at apoapsis for coast orbit, m/s
	v_apoapsis_mag_coast : float
		body-inertial velocity vector magnitude at apoapsis for coast orbit, m/s
	v_apoapsis_vec_orbit : numpy.ndarray
		body-inertial velocity vector at apoapsis for final orbit, m/s
	v_apoapsis_mag_orbit : float
		body-inertial velocity vector magnitude at apoapsis for final orbit, m/s
	PRM_dv_vec : numpy.ndarray
		periapsis raise manuever delta-V vector, m/s
	PRM_dv_mag : float
		periapsis raise manuever delta-V magnitude, m/s
	x_orbit_arr : numpy.ndarray
		body-inertial x-coordinate positions of one full final orbit after PRM
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	y_orbit_arr : numpy.ndarray
		body-inertial y-coordinate positions of one full final orbit after PRM
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	z_orbit_arr : numpy.ndarray
		body-inertial z-coordinate positions of one full final orbit after PRM
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)

	"""

	def __init__(self, vehicle, peri_alt_km):
		"""

		Parameters
		----------
		vehicle : AMAT.vehicle.Vehicle
			Vehicle object which has been propagated until atmospheric exit
		peri_alt_km : float
			orbit periapsis altitude, km
		"""

		self.vehicle = vehicle
		self.peri_alt_km = peri_alt_km
		self.r_periapsis_mag = self.peri_alt_km*1e3 + self.vehicle.planetObj.RP

		self.compute_exit_state_atm_relative()
		self.compute_exit_state_inertial()
		self.compute_coast_orbital_elements()
		self.compute_theta_star_exit()
		self.compute_coast_trajectory()
		self.post_PRM_orbital_elements()
		self.compute_PRM_dv()
		self.compute_orbit_trajectory()

	def compute_exit_state_atm_relative(self):
		"""
		Extracts the exit state vector in atmosphere relative coordinates
		from the propagated vehicle exit state.
		"""

		self.terminal_r = self.vehicle.rc[self.vehicle.index - 1]
		self.terminal_theta = self.vehicle.thetac[self.vehicle.index - 1]
		self.terminal_phi = self.vehicle.phic[self.vehicle.index - 1]
		self.terminal_v = self.vehicle.vc[self.vehicle.index - 1]
		self.terminal_g = self.vehicle.gammac[self.vehicle.index - 1]
		self.terminal_psi = self.vehicle.psic[self.vehicle.index - 1]

	def compute_exit_state_inertial(self):
		"""
		Computes the exit state vector in body inertial frame.
		"""

		# Compute terminal radial vector
		self.terminal_r_vec = self.terminal_r * np.array([np.cos(self.terminal_phi) * np.cos(self.terminal_theta), \
												np.cos(self.terminal_phi) * np.sin(self.terminal_theta), np.sin(self.terminal_phi)])

		# Compute terminal radial unit vector
		self.terminal_r_hat_vec = self.terminal_r_vec / np.linalg.norm(self.terminal_r_vec)

		# Compute planet relative speed in Cartesian XYZ coordinates
		self.v_pr_x = self.terminal_v * np.sin(self.terminal_g) * np.cos(self.terminal_phi) * np.cos(self.terminal_theta) \
				 + self.terminal_v * np.cos(self.terminal_g) * np.cos(self.terminal_psi) * (-1 * np.sin(self.terminal_theta)) \
				 + self.terminal_v * np.cos(self.terminal_g) * np.sin(self.terminal_psi) * (-1 * np.sin(self.terminal_phi) * \
																			 np.cos(self.terminal_theta))

		self.v_pr_y = self.terminal_v * np.sin(self.terminal_g) * np.cos(self.terminal_phi) * np.sin(self.terminal_theta) + \
				 self.terminal_v * np.cos(self.terminal_g) * np.cos(self.terminal_psi) * np.cos(self.terminal_theta) + \
				 self.terminal_v * np.cos(self.terminal_g) * np.sin(self.terminal_psi) * (-1 * np.sin(self.terminal_phi) * \
																		   np.sin(self.terminal_theta))

		self.v_pr_z = self.terminal_v * np.sin(self.terminal_g) * np.sin(self.terminal_phi) + \
				 self.terminal_v * np.cos(self.terminal_g) * np.sin(self.terminal_psi) * np.cos(self.terminal_phi)

		self.terminal_v_vec = np.array([self.v_pr_x, self.v_pr_y, self.v_pr_z])
		self.terminal_v_hat_vec = self.terminal_v_vec / np.linalg.norm(self.terminal_v_vec)

		# Compute inertial speed in Cartesian XYZ coordinates
		self.v_ie_x = self.v_pr_x + self.terminal_r * self.vehicle.planetObj.OMEGA * np.cos(self.terminal_phi) * \
				 np.sin(self.terminal_theta) * (-1.0)

		self.v_ie_y = self.v_pr_y + self.terminal_r * self.vehicle.planetObj.OMEGA * np.cos(self.terminal_phi) * \
				 np.cos(self.terminal_theta)

		self.v_ie_z = self.v_pr_z

		# Compute inertial velocity magnitude
		self.v_ie_mag = np.sqrt(self.v_ie_x ** 2 + self.v_ie_y ** 2 + self.v_ie_z ** 2)

		# Compute inertial velocity vector
		self.terminal_v_ie_vec = np.array([self.v_ie_x, self.v_ie_y, self.v_ie_z])

		# Compute inertial velocity unit vector
		self.terminal_v_ie_hat_vec = self.terminal_v_ie_vec / np.linalg.norm(self.terminal_v_ie_vec)

		# Compute inertial flight path angle at exit using
		# terminal inertial radial and velocity vectors
		self.terminal_fpa_ie_deg = 90.0 - (180 / np.pi) * \
							  np.arccos(np.dot(self.terminal_r_hat_vec, self.terminal_v_ie_hat_vec))

		self.terminal_fpa_ie_rad = self.terminal_fpa_ie_deg * np.pi / 180.0

		self.terminal_r_bi = self.terminal_r
		self.terminal_theta_bi = self.terminal_theta
		self.terminal_phi_bi = self.terminal_phi
		self.terminal_v_bi = self.v_ie_mag
		self.terminal_g_bi = self.terminal_fpa_ie_rad
		self.terminal_psi_bi = self.terminal_psi

	def compute_coast_orbital_elements(self):

		"""
		Computes the orbital elements of the coast phase
		"""

		# Compute orbit energy using inertial speed
		self.terminal_E = self.vehicle.computeEnergyScalar(self.terminal_r, self.v_ie_mag)
		self.terminal_h = self.vehicle.computeAngMomScalar(self.terminal_r, self.v_ie_mag, self.terminal_fpa_ie_rad)

		# Compute semi-major axis and eccentricity of the post atmospheric exit orbit
		self.a = self.vehicle.computeSemiMajorAxisScalar(self.terminal_E)
		self.e = self.vehicle.computeEccScalar(self.terminal_h, self.terminal_E)
		self.h = np.sqrt(self.a * self.vehicle.planetObj.GM * (1 - self.e ** 2))

		self.h_vec_bi = np.cross(self.terminal_r_vec, self.terminal_v_ie_vec)
		self.h_vec_bi_unit = self.h_vec_bi / np.linalg.norm(self.h_vec_bi)

		self.i = np.arccos(self.h_vec_bi_unit[2])

		self.N_vec_bi = np.cross(np.array([0, 0, 1]), self.h_vec_bi)
		self.N_vec_bi_unit = self.N_vec_bi / np.linalg.norm(self.N_vec_bi)

		if self.N_vec_bi_unit[1] >= 0:
			self.OMEGA = np.arccos(self.N_vec_bi_unit[0])
		else:
			self.OMEGA = 2 * np.pi - np.arccos(self.N_vec_bi_unit[0])

		self.e_vec_bi = ((self.v_ie_mag**2 - self.vehicle.planetObj.GM/self.terminal_r)*self.terminal_r_vec - \
						 np.dot(self.terminal_r_vec, self.terminal_v_ie_vec)*self.terminal_v_ie_vec)/self.vehicle.planetObj.GM

		self.e_vec_bi_unit = self.e_vec_bi / np.linalg.norm(self.e_vec_bi)

		if self.e_vec_bi_unit[2] >= 0:
			self.omega = np.arccos(np.dot(self.N_vec_bi_unit, self.e_vec_bi_unit))
		else:
			self.omega = 2*np.pi - np.arccos(np.dot(self.N_vec_bi_unit, self.e_vec_bi_unit))


	def compute_theta_star_exit(self):
		self.theta_star_exit = np.arccos(((self.h ** 2 / (self.vehicle.planetObj.GM * self.terminal_r)) - 1) * (1.0 / self.e))

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
		r_mag_bi = (self.h**2 / self.vehicle.planetObj.GM) / (1 + self.e*np.cos(theta_star))
		return r_mag_bi

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

		r = (self.h**2 / self.vehicle.planetObj.GM) / (1 + self.e*np.cos(theta_star))
		theta = theta_star + self.omega

		rx_unit = np.cos(self.OMEGA)*np.cos(theta) - np.sin(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		ry_unit = np.sin(self.OMEGA)*np.cos(theta) + np.cos(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		rz_unit = np.sin(self.i)*np.sin(theta)

		pos_vec_bi = r*np.array([rx_unit, ry_unit, rz_unit])
		return pos_vec_bi

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
		v_mag_bi = np.sqrt(self.vehicle.planetObj.GM*(2/r_mag_bi - 1/self.a))

		gamma = 1*np.arccos(self.h/(r_mag_bi*v_mag_bi*1.0000001))

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


	def compute_coast_trajectory(self, num_points=301):
		"""
		Computes the coast trajectory from atmospheric exit until first apoapsis

		Parameters
		----------
		num_points : int
			number of grid points

		Returns
		-------

		"""

		theta_star_arr = np.linspace(self.theta_star_exit, np.pi, num_points)
		pos_vec_bi_arr = self.pos_vec_bi(theta_star_arr) / self.vehicle.planetObj.RP

		self.x_coast_arr = pos_vec_bi_arr[0][:]
		self.y_coast_arr = pos_vec_bi_arr[1][:]
		self.z_coast_arr = pos_vec_bi_arr[2][:]

		self.r_apoapsis_vec =  np.array([self.x_coast_arr[-1],
										self.y_coast_arr[-1],
										self.z_coast_arr[-1]])

		self.r_apoapsis_mag = np.linalg.norm(self.r_apoapsis_vec)*self.vehicle.planetObj.RP

		self.v_apoapsis_vec_coast = self.vel_vec_bi(np.pi)
		self.v_apoapsis_mag_coast = np.linalg.norm(self.v_apoapsis_vec_coast)

	def post_PRM_orbital_elements(self):
		"""
		Computes the orbit elements for orbit with periapsis raised
		"""

		self.e = (self.r_apoapsis_mag - self.r_periapsis_mag) / (self.r_apoapsis_mag + self.r_periapsis_mag)
		self.a = self.r_apoapsis_mag / (1 + self.e)
		self.h = np.sqrt(self.a * self.vehicle.planetObj.GM * (1 - self.e ** 2))

	def compute_PRM_dv(self):
		"""
		Computes the periapsis raise manuever delta-V vector and magnitude
		"""

		self.v_apoapsis_vec_orbit = self.vel_vec_bi(np.pi)
		self.v_apoapsis_mag_orbit = np.linalg.norm(self.v_apoapsis_vec_orbit)

		self.PRM_dv_vec = self.v_apoapsis_vec_orbit - self.v_apoapsis_vec_coast
		self.PRM_dv_mag = np.linalg.norm(self.PRM_dv_vec)

	def compute_orbit_trajectory(self, num_points=601):
		"""
		Computes the coordinates of one full orbit after periapsis raise manuever

		Parameters
		----------
		num_points : int
			grid points for full final orbit trajectory


		"""
		theta_star_arr = np.linspace(np.pi, 3*np.pi, num_points)
		pos_vec_bi_arr = self.pos_vec_bi(theta_star_arr) / self.vehicle.planetObj.RP

		self.x_orbit_arr = pos_vec_bi_arr[0][:]
		self.y_orbit_arr = pos_vec_bi_arr[1][:]
		self.z_orbit_arr = pos_vec_bi_arr[2][:]
