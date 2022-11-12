# SOURCE FILENAME : orbiter.py
# AUTHOR          : Athul Pradeepkumar Girija, apradee@purdue.edu
# DATE CREATED    : 06/01/2022 07:51 AM
# DATE MODIFIED   : 06/01/2022 07:51 MT
# REMARKS         : Compute the coast trajectory from atmospheric exit until
#					apoapsis, the periapsis raise manuever dv, and the
#   				first full orbit post aerocapture. Also computes the
#					probe trajectory following a probe-targeting maneuver,
#					probe atmospheric entry conditions, and the orbiter trajectory
#					following an orbiter deflection manuever.


import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from AMAT.planet import Planet
from AMAT.vehicle import Vehicle

from AMAT.approach import Approach

class Orbiter:
	"""
	Compute the coast trajectory from atmospheric exit until
	apoapsis, the periapsis raise manuever dv, and the
	first full orbit post aerocapture. Also computes the
	probe trajectory following a probe-targeting maneuver,
	probe atmospheric entry conditions, and the orbiter trajectory
	following an orbiter deflection manuever.

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
		initial capture orbit semi-major axis, m
	e : float
		initial capture orbit eccentricity
	i : float
		initial capture inclination, rad
	h : float
		initial capture specific angular momentum, SI units
	OMEGA : float
		initial capture RAAN, rad
	omega : float
		initial capture AoP, rad
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
	theta_star_probe_targeting : float
		true anomaly of the probe targeting manuever, from the initial capture orbit
		[0, 2*pi], rad
	a_probe_orbit : float
		probe approach orbit semi-major axis, m
	e_probe_orbit : float
		probe approach eccentricity
	i_probe_orbit : float
		probe approach inclination, rad
	h_probe_orbit : float
		probe approach  specific angular momentum, SI units
	OMEGA_probe_orbit  : float
		probe approach  RAAN, rad
	omega_probe_orbit : float
		probe approach  AoP, rad
	r_periapsis_probe : float
		periapsis radius of probe approach trajectory, m
	r_apoapsis_probe : float
		apoapsis radius of probe approach trajectory, m
	h_periapsis_probe : float
		periapsis altitude of probe approach trajectory, m
	h_EI : float
		probe atmospheric interface altitude, m
	r_EI : float
		probe atmospheric interface radius, m
	theta_star_probe_entry : float
		true anomaly at probe atmospheric entry, rad
	r_vec_bi_probe_entry : numpy.ndarray
		position vector at probe atmospheric entry, m
	r_vec_bi_probe_entry_unit : numpy.ndarray
		unit position vector at probe atmospheric entry
	r_vec_bi_probe_entry_mag : float
		position vector magnitude at probe atmospheric entry, m
	v_bi_vec_probe_entry : numpy.ndarray
		inertial velocity vector at probe atmospheric entry, m/s
	v_bi_mag_probe_entry : float
	 	inertial velocity magnitude at probe atmospheric entry, m/s
	v_bi_vec_probe_entry_unit : numpy.ndarray
		unit inertial velocity vector at probe atmospheric entry, m/s
	gamma_inertial_probe_entry : float
		inertial flight-path angle at probe atmospheric entry, rad
	latitude_probe_entry_bi : float
		inertial latitude at probe atmospheric entry, rad
	longitude_probe_entry_bi : float
		inertial longitude at probe atmospheric entry, rad
	v_vec_probe_entry_atm : numpy.ndarray
		atmosphere-relative velocity vector at probe atmospheric entry, m/s
	v_mag_probe_entry_atm : float
		atmosphere-relative velocity magnitude at probe atmospheric entry, m/s
	v_vec_probe_entry_atm_unit : numpy.ndarray
		atmosphere-relative velocity unit vector at probe atmospheric entry, m/s
	gamma_atm_probe_entry : float
		atmosphere-relative flight-path angle at probe atmospheric entry, rad
	v_atm_probe_entry_unit_proj : numpy.ndarray
		atmosphere-relative velocity unit vector projection on local horizontal plane
	atm_probe_entry_local_latitude_parallel_vec_unit : numpy.ndarray
		local parallel of latitude unit vector at probe atmospheric entry interface
	heading_atm_probe_entry : float
		atmosphere-relative heading angle at probe atmospheric entry, rad
	x_probe_arr : numpy.ndarray
		body-inertial x-coordinate positions of probe approach trajectory from
		probe targeting manuever until atmospheric entry
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	y_probe_arr : numpy.ndarray
		body-inertial y-coordinate positions of probe approach trajectory from
		probe targeting manuever until atmospheric entry
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	z_probe_arr : numpy.ndarray
		body-inertial z-coordinate positions of probe approach trajectory from
		probe targeting manuever until atmospheric entry
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	dV_mag_probe_targeting : float
		probe targeting maneuver delta-V magnitude, m/s
	dV_vec_probe_targeting : float
		probe targeting maneuver delta-V vector, m/s
	theta_star_orbiter_defl : float
		true anomaly of the orbiter deflection maneuever, from the probe targeting orbit
		[0, 2*pi], rad
	a_orbiter_defl : float
		orbiter deflection orbit semi-major axis, m
	e_orbiter_defl : float
		orbiter deflection orbit eccentricity
	i_orbiter_defl : float
		orbiter deflection orbit inclination, rad
	h_orbiter_defl : float
		orbiter deflection orbit  specific angular momentum, SI units
	OMEGA_orbiter_defl  : float
		orbiter deflection orbit  approach  RAAN, rad
	omega_orbiter_defl : float
		orbiter deflection  AoP, rad
	r_periapsis_orbiter_defl : float
		periapsis radius of orbiter deflection orbit trajectory, m
	r_apoapsis_orbiter_defl : float
		apoapsis radius of orbiter deflection orbit trajectory, m
	h_periapsis_orbiter_defl : float
		periapsis altitude of orbiter deflection orbit, m
	x_orbiter_defl_arr : numpy.ndarray
		body-inertial x-coordinate positions of orbiter deflection trajectory
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	y_orbiter_defl_arr : numpy.ndarray
		body-inertial y-coordinate positions of orbiter deflection trajectory
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	z_orbiter_defl_arr : numpy.ndarray
		body-inertial z-coordinate positions of orbiter deflection trajectory
		in non-dimensional units in terms of planet radius (vehicle.planetObj.RP)
	dV_mag_orbiter_defl : float
		orbiter deflection maneuver delta-V magnitude, m/s
	dV_vec_orbiter_defl : float
		orbiter deflection maneuver delta-V vector, m/s
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
		self.compute_post_PRM_orbital_elements()
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

	def pos_vec_bi_probe(self, theta_star):
		"""
		Computes the position vector in body-inertial frame
		of the probe trajectory for a specified true-anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		pos_vec_bi : numpy.ndarray
			position vector in body-inertial frame, meters
		"""

		r = (self.h_probe_orbit**2 / self.vehicle.planetObj.GM) / (1 + self.e_probe_orbit*np.cos(theta_star))
		theta = theta_star + self.omega

		rx_unit = np.cos(self.OMEGA_probe_orbit)*np.cos(theta) - np.sin(self.OMEGA_probe_orbit)*np.cos(self.i)*np.sin(theta)
		ry_unit = np.sin(self.OMEGA_probe_orbit)*np.cos(theta) + np.cos(self.OMEGA_probe_orbit)*np.cos(self.i)*np.sin(theta)
		rz_unit = np.sin(self.i_probe_orbit)*np.sin(theta)

		pos_vec_bi = r*np.array([rx_unit, ry_unit, rz_unit])
		return pos_vec_bi

	def pos_vec_bi_orbiter_defl(self, theta_star):
		"""
		Computes the position vector in body-inertial frame
		of the orbiter deflection trajectory for a specified true-anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		pos_vec_bi : numpy.ndarray
			position vector in body-inertial frame, meters
		"""

		r = (self.h_orbiter_defl**2 / self.vehicle.planetObj.GM) / (1 + self.e_orbiter_defl*np.cos(theta_star))
		theta = theta_star + self.omega

		rx_unit = np.cos(self.OMEGA_orbiter_defl)*np.cos(theta) - np.sin(self.OMEGA_orbiter_defl)*np.cos(self.i_orbiter_defl)*np.sin(theta)
		ry_unit = np.sin(self.OMEGA_orbiter_defl)*np.cos(theta) + np.cos(self.OMEGA_orbiter_defl)*np.cos(self.i_orbiter_defl)*np.sin(theta)
		rz_unit = np.sin(self.i_orbiter_defl)*np.sin(theta)

		pos_vec_bi = r*np.array([rx_unit, ry_unit, rz_unit])
		return pos_vec_bi

	def vel_vec_bi(self, theta_star):
		"""
		Computes the velocity vector in body-inertial frame at a given true anomaly.

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


	def vel_vec_bi_probe(self, theta_star):
		"""
		Computes the velocity vector  in body-inertial frame for the probe trajectory
		at a given true anomaly.

		Parameters
		----------
		theta_star : float
			true anomaly, rad

		Returns
		-------
		vel_vec_bi : numpy.ndarray
			velocity vector in body-inertial frame, m/s

		"""

		r_mag_bi = np.linalg.norm(self.pos_vec_bi_probe(theta_star))
		v_mag_bi = np.sqrt(self.vehicle.planetObj.GM*(2/r_mag_bi - 1/self.a_probe_orbit))

		gamma = -1*np.arccos(self.h_probe_orbit/(r_mag_bi*v_mag_bi*1.0000001))

		vr = v_mag_bi*np.sin(gamma)
		vt = v_mag_bi*np.cos(gamma)
		theta = theta_star + self.omega_probe_orbit

		vx = vr*( np.cos(theta)*np.cos(self.OMEGA_probe_orbit) - np.sin(theta)*np.cos(self.i_probe_orbit)*np.sin(self.OMEGA_probe_orbit)) +\
		     vt*(-np.sin(theta)*np.cos(self.OMEGA_probe_orbit) - np.cos(theta)*np.cos(self.i_probe_orbit)*np.sin(self.OMEGA_probe_orbit))

		vy = vr*( np.cos(theta)*np.sin(self.OMEGA_probe_orbit) + np.sin(theta)*np.cos(self.i_probe_orbit)*np.cos(self.OMEGA_probe_orbit)) +\
		     vt*( np.cos(theta)*np.cos(self.i_probe_orbit)*np.cos(self.OMEGA_probe_orbit) - np.sin(theta)*np.sin(self.OMEGA_probe_orbit))

		vz = vr*np.sin(theta)*np.sin(self.i_probe_orbit) + vt*np.cos(theta)*np.sin(self.i_probe_orbit)

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

	def compute_post_PRM_orbital_elements(self):
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
		Computes the coordinates of initial capture orbit after periapsis raise manuever

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

	def vel_vec_probe_entry_atm(self):
		"""
		Computes the atmosphere-relative velocity vector magnitude in body-inertial frame
		of the probe at atmospheric entry interface.

		Parameters
		----------

		Returns
		-------
		vel_vec_entry_atm : numpy.ndarray
			atmosphere-relative velocity vector in body-inertial frame, at
			atmospheric entry interface, m/s

		"""
		v_entry_atm_x = self.v_bi_vec_probe_entry[0] - \
		          self.r_vec_bi_probe_entry_mag * self.vehicle.planetObj.OMEGA * \
		          np.cos(self.latitude_probe_entry_bi) * (-np.sin(self.longitude_probe_entry_bi))
		v_entry_atm_y = self.v_bi_vec_probe_entry[1] - \
		          self.r_vec_bi_probe_entry_mag * self.vehicle.planetObj.OMEGA * \
		          np.cos(self.latitude_probe_entry_bi) * (np.cos(self.longitude_probe_entry_bi))
		v_entry_atm_z = self.v_bi_vec_probe_entry[2]

		vel_vec_entry_atm = np.array([v_entry_atm_x, v_entry_atm_y, v_entry_atm_z])
		return vel_vec_entry_atm


	def compute_probe_targeting_trajectory(self, theta_star, dV, num_points=301):
		"""
		Computes the coordinates of probe approach trajectory following a probe targeting manuever
		at theta_star of the initial capture orbit.

		Parameters
		----------
		theta_star : float
			true anomaly of the initial capture orbit at which the probe targeting maneuever
			is performed [0,2pi], rad
		dV : float
			delta-V magnitude of the probe targeting maneuver, along the direction
			of orbital velocity, can be positive or negative. Must be negative to
			deliver probe into the atmosphere from the initial capture orbit. m/s
		num_points : int
			number of grid points for the probe approach trajectory
		"""

		self.theta_star_probe_targeting = theta_star
		self.dV_mag_probe_targeting = dV

		# Compute state vector (r1,v1) at theta_star before manuever
		r_vec_1 = self.pos_vec_bi(theta_star)
		v_vec_1 = self.vel_vec_bi(theta_star)

		# Compute state vector (r2, v2) after applying dV
		r_vec_2 = r_vec_1
		v_vec_2 = v_vec_1 + dV*v_vec_1/(np.linalg.norm(v_vec_1))

		self.dV_vec_probe_targeting =  dV*v_vec_1/(np.linalg.norm(v_vec_1))

		r2 = np.linalg.norm(r_vec_2)
		v2 = np.linalg.norm(v_vec_2)

		r_vec_2_unit = r_vec_2 / np.linalg.norm(r_vec_2)
		v_vec_2_unit = v_vec_2 / np.linalg.norm(v_vec_2)

		ie_fpa_2_deg     = 90.0 - (180 / np.pi) * \
								   np.arccos(np.dot(r_vec_2_unit, v_vec_2_unit))
		ie_fpa_2_rad     = ie_fpa_2_deg*np.pi/180

		# Compute orbit energy and angular momentum post manueuver
		self.E_post_maneuver = self.vehicle.computeEnergyScalar(r2, v2)
		self.h_post_maneuver = self.vehicle.computeAngMomScalar(r2, v2, ie_fpa_2_rad)

		# Compute semi-major axis and eccentricity of the probe orbit
		self.a_probe_orbit = self.vehicle.computeSemiMajorAxisScalar(self.E_post_maneuver)
		self.e_probe_orbit = self.vehicle.computeEccScalar(self.h_post_maneuver, self.E_post_maneuver)
		self.h_probe_orbit = np.sqrt(self.a_probe_orbit * self.vehicle.planetObj.GM * (1 - self.e_probe_orbit ** 2))

		self.h_vec_bi_probe_orbit = np.cross(r_vec_2, v_vec_2)
		self.h_vec_bi_unit_probe_orbit = self.h_vec_bi_probe_orbit / np.linalg.norm(self.h_vec_bi_probe_orbit)

		self.i_probe_orbit = np.arccos(self.h_vec_bi_unit_probe_orbit[2])

		self.N_vec_bi_probe_orbit = np.cross(np.array([0, 0, 1]), self.h_vec_bi_probe_orbit)
		self.N_vec_bi_unit_probe_orbit = self.N_vec_bi_probe_orbit / np.linalg.norm(self.N_vec_bi_probe_orbit)

		if self.N_vec_bi_unit_probe_orbit[1] >= 0:
			self.OMEGA_probe_orbit = np.arccos(self.N_vec_bi_unit_probe_orbit[0])
		else:
			self.OMEGA_probe_orbit = 2 * np.pi - np.arccos(self.N_vec_bi_unit_probe_orbit[0])

		self.e_vec_bi_probe_orbit = ((v2 ** 2 - self.vehicle.planetObj.GM / r2) * r_vec_2 - \
						 			np.dot(r_vec_2, v_vec_2) * v_vec_2) / self.vehicle.planetObj.GM

		self.e_vec_bi_unit_probe_orbit = self.e_vec_bi_probe_orbit / np.linalg.norm(self.e_vec_bi_probe_orbit)

		if self.e_vec_bi_unit_probe_orbit[2] >= 0:
			self.omega_probe_orbit = np.arccos(np.dot(self.N_vec_bi_unit_probe_orbit, self.e_vec_bi_unit_probe_orbit))
		else:
			self.omega_probe_orbit = 2 * np.pi - np.arccos(np.dot(self.N_vec_bi_unit_probe_orbit, self.e_vec_bi_unit_probe_orbit))

		self.r_periapsis_probe = self.a_probe_orbit * (1 - self.e_probe_orbit)
		self.r_apoapsis_probe = self.a_probe_orbit * (1 + self.e_probe_orbit)
		self.h_periapsis_probe = self.r_periapsis_probe - self.vehicle.planetObj.RP

		if self.h_periapsis_probe < self.vehicle.planetObj.h_skip:
			self.h_EI = self.vehicle.planetObj.h_skip
			self.r_EI = self.vehicle.planetObj.RP + self.h_EI
			self.theta_star_probe_entry = 2*np.pi - np.arccos(((self.h_probe_orbit ** 2 / (self.vehicle.planetObj.GM * self.r_EI)) - 1) * (1.0 / self.e_probe_orbit))

			self.r_vec_bi_probe_entry = self.pos_vec_bi_probe(self.theta_star_probe_entry)
			self.r_vec_bi_probe_entry_unit = self.r_vec_bi_probe_entry / np.linalg.norm(self.r_vec_bi_probe_entry)
			self.r_vec_bi_probe_entry_mag = np.linalg.norm(self.r_vec_bi_probe_entry)

			self.v_bi_vec_probe_entry = self.vel_vec_bi_probe(self.theta_star_probe_entry)
			self.v_bi_mag_probe_entry = np.linalg.norm(self.v_bi_vec_probe_entry)
			self.v_bi_vec_probe_entry_unit = self.v_bi_vec_probe_entry / self.v_bi_mag_probe_entry

			self.gamma_inertial_probe_entry = -1 * np.arccos(self.h_probe_orbit / (self.r_EI * self.v_bi_mag_probe_entry))

			self.latitude_probe_entry_bi = np.arcsin(self.r_vec_bi_probe_entry_unit[2])
			self.longitude_probe_entry_bi = np.arctan(self.r_vec_bi_probe_entry_unit[1] / self.r_vec_bi_probe_entry_unit[0])

			self.v_vec_probe_entry_atm = self.vel_vec_probe_entry_atm()
			self.v_mag_probe_entry_atm = np.linalg.norm(self.v_vec_probe_entry_atm)
			self.v_vec_probe_entry_atm_unit = self.v_vec_probe_entry_atm / self.v_mag_probe_entry_atm

			self.gamma_atm_probe_entry = np.pi / 2 - np.arccos(np.dot(self.r_vec_bi_probe_entry_unit, self.v_bi_vec_probe_entry_unit))

			self.v_atm_probe_entry_unit_proj = self.v_vec_probe_entry_atm_unit  - \
											 np.dot(self.v_vec_probe_entry_atm_unit ,
													self.r_vec_bi_probe_entry_unit) * self.r_vec_bi_probe_entry_unit

			self.atm_probe_entry_local_latitude_parallel_vec_unit = np.array([-np.sin(self.longitude_probe_entry_bi),
															  				   np.cos(self.longitude_probe_entry_bi),
															  				   0.0])

			self.heading_atm_probe_entry = np.arccos(np.dot(self.v_atm_probe_entry_unit_proj,
													  self.atm_probe_entry_local_latitude_parallel_vec_unit))

		else:
			print("Probe orbit periapsis outside atmospheric skip altitude.")

		theta_star_arr = np.linspace(theta_star, self.theta_star_probe_entry, num_points)
		pos_vec_bi_arr = self.pos_vec_bi_probe(theta_star_arr) / self.vehicle.planetObj.RP

		self.x_probe_orbit_arr = pos_vec_bi_arr[0][:]
		self.y_probe_orbit_arr = pos_vec_bi_arr[1][:]
		self.z_probe_orbit_arr = pos_vec_bi_arr[2][:]

	def compute_orbiter_deflection_trajectory(self, theta_star, dV, num_points=601):
		"""
		Computes the coordinates of orbiter deflection trajectory following an orbiter deflection manuever
		at theta_star of the probe approach trajectory orbit.

		Parameters
		----------
		theta_star : float
			true anomaly of the probe approach trajectory orbit at which the orbiter deflection manuever
			is performed [0,2pi], rad
		dV : float
			delta-V magnitude of the orbiter deflection manuever, along the direction
			of orbital velocity, can be positive or negative. Must be positive to
			raise the periapsis outside the atmosphere. m/s
		num_points : int
			number of grid points for the orbiter deflection trajectory
		"""

		self.theta_star_orbiter_defl = theta_star
		self.dV_mag_orbiter_deflection = dV


		# Compute state vector (r1,v1) at theta_star before manuever
		r_vec_1 = self.pos_vec_bi_probe(theta_star)
		v_vec_1 = self.vel_vec_bi_probe(theta_star)

		# Compute state vector (r2, v2) after applying dV
		r_vec_2 = r_vec_1
		v_vec_2 = v_vec_1 + dV * v_vec_1 / (np.linalg.norm(v_vec_1))

		self.dV_vec_orbiter_deflection =  dV * v_vec_1 / (np.linalg.norm(v_vec_1))

		r2 = np.linalg.norm(r_vec_2)
		v2 = np.linalg.norm(v_vec_2)

		r_vec_2_unit = r_vec_2 / np.linalg.norm(r_vec_2)
		v_vec_2_unit = v_vec_2 / np.linalg.norm(v_vec_2)

		ie_fpa_2_deg = 90.0 - (180 / np.pi) * \
					   np.arccos(np.dot(r_vec_2_unit, v_vec_2_unit))
		ie_fpa_2_rad = ie_fpa_2_deg * np.pi / 180

		# Compute orbit energy and angular momentum for orbiter deflection trajectory
		self.E_orbiter_defl = self.vehicle.computeEnergyScalar(r2, v2)
		self.h_orbiter_defl = self.vehicle.computeAngMomScalar(r2, v2, ie_fpa_2_rad)

		# Compute semi-major axis and eccentricity of the probe orbit
		self.a_orbiter_defl = self.vehicle.computeSemiMajorAxisScalar(self.E_orbiter_defl)
		self.e_orbiter_defl = self.vehicle.computeEccScalar(self.h_orbiter_defl, self.E_orbiter_defl)
		self.h_orbiter_defl = np.sqrt(self.a_orbiter_defl * self.vehicle.planetObj.GM * (1 - self.e_orbiter_defl ** 2))

		self.h_vec_bi_orbiter_defl  = np.cross(r_vec_2, v_vec_2)
		self.h_vec_bi_unit_orbiter_defl  = self.h_vec_bi_orbiter_defl  / np.linalg.norm(self.h_vec_bi_orbiter_defl)

		self.i_orbiter_defl = np.arccos(self.h_vec_bi_unit_orbiter_defl[2])

		self.N_vec_bi_orbiter_defl = np.cross(np.array([0, 0, 1]), self.h_vec_bi_orbiter_defl)
		self.N_vec_bi_unit_orbiter_defl = self.N_vec_bi_orbiter_defl / np.linalg.norm(self.N_vec_bi_orbiter_defl)

		if self.N_vec_bi_unit_orbiter_defl[1] >= 0:
			self.OMEGA_orbiter_defl = np.arccos(self.N_vec_bi_unit_orbiter_defl[0])
		else:
			self.OMEGA_orbiter_defl = 2 * np.pi - np.arccos(self.N_vec_bi_unit_orbiter_defl[0])

		self.e_vec_bi_orbiter_defl = ((v2 ** 2 - self.vehicle.planetObj.GM / r2) * r_vec_2 -
									 np.dot(r_vec_2, v_vec_2) * v_vec_2) / self.vehicle.planetObj.GM

		self.e_vec_bi_unit_orbiter_defl =  self.e_vec_bi_orbiter_defl  / np.linalg.norm(self.e_vec_bi_orbiter_defl)

		if self.e_vec_bi_unit_orbiter_defl[2] >= 0:
			self.omega_orbiter_defl = np.arccos(np.dot(self.N_vec_bi_unit_orbiter_defl, self.e_vec_bi_unit_orbiter_defl))
		else:
			self.omega_orbiter_defl = 2 * np.pi - np.arccos(np.dot(self.N_vec_bi_unit_orbiter_defl, self.e_vec_bi_unit_orbiter_defl))

		self.r_periapsis_orbiter_defl = self.a_orbiter_defl * (1 - self.e_orbiter_defl)
		self.r_apoapsis_orbiter_defl = self.a_orbiter_defl* (1 + self.e_orbiter_defl)
		self.h_periapsis_orbiter_defl = self.r_periapsis_orbiter_defl - self.vehicle.planetObj.RP

		theta_star_arr = np.linspace(0, 2*np.pi, num_points)
		pos_vec_bi_arr = self.pos_vec_bi_orbiter_defl(theta_star_arr) / self.vehicle.planetObj.RP

		self.x_orbiter_defl_arr = pos_vec_bi_arr[0][:]
		self.y_orbiter_defl_arr = pos_vec_bi_arr[1][:]
		self.z_orbiter_defl_arr = pos_vec_bi_arr[2][:]

		if self.h_periapsis_orbiter_defl < self.vehicle.planetObj.h_skip:
			print("Periapsis inside atmospheric skip altitude.")


class PropulsiveOrbiter:
	"""
	Compute the orbit of a propulsive insertion orbiter after OI burn.
	"""

	def __init__(self, approach, apoapsis_alt_km):
		"""

		Parameters
		----------
		approach : AMAT.approach.Approach
			Approach object which has been propagated until periapsis
		apoapsis_alt_km : float
			orbit apoapsis altitude, km
		"""

		self.approach = approach
		self.apoapsis_alt_km = apoapsis_alt_km

		self.approach_terminal_r = self.approach.r_vec_rp_bi
		self.approach_terminal_v = self.approach.v_vec_rp_bi

		self.rp = self.approach.rp
		self.ra = self.approach.planetObj.RP + self.apoapsis_alt_km*1e3

		self.a = (self.rp + self.ra)/2
		self.e = (self.ra - self.rp) / (self.ra + self.rp)
		self.h = np.sqrt(self.a * self.approach.planetObj.GM * (1 - self.e ** 2))

		self.i = self.approach.i
		self.OMEGA = self.approach.OMEGA
		self.omega = self.approach.omega

		self.vp_vec = self.vel_vec_bi(theta_star=0)
		self.vp = np.linalg.norm(self.vp_vec)

		self.DV_OI_vec = self.approach_terminal_v - self.vp_vec
		self.DV_OI_mag = np.linalg.norm(self.DV_OI_vec)

		self.vp_check = np.sqrt(self.approach.planetObj.GM * (2 / self.rp - 1 / self.a))
		self.DV_OI_mag_check = np.linalg.norm(self.approach.v_vec_rp_bi) - self.vp_check

		self.compute_orbit_trajectory()


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
		r_mag_bi = (self.h**2 / self.approach.planetObj.GM) / (1 + self.e*np.cos(theta_star))
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

		r = (self.h**2 / self.approach.planetObj.GM) / (1 + self.e*np.cos(theta_star))
		theta = theta_star + self.omega

		rx_unit = np.cos(self.OMEGA)*np.cos(theta) - np.sin(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		ry_unit = np.sin(self.OMEGA)*np.cos(theta) + np.cos(self.OMEGA)*np.cos(self.i)*np.sin(theta)
		rz_unit = np.sin(self.i)*np.sin(theta)

		pos_vec_bi = r*np.array([rx_unit, ry_unit, rz_unit])
		return pos_vec_bi

	def vel_vec_bi(self, theta_star):
		"""
		Computes the velocity vector in body-inertial frame at a given true anomaly.

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
		v_mag_bi = np.sqrt(self.approach.planetObj.GM*(2/r_mag_bi - 1/self.a))

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

	def compute_orbit_trajectory(self, num_points=601):
		"""
		Computes the coordinates of initial capture orbit of the propulsive orbiter

		Parameters
		----------
		num_points : int
			grid points for full final orbit trajectory


		"""
		theta_star_arr = np.linspace(0, 2*np.pi, num_points)
		pos_vec_bi_arr = self.pos_vec_bi(theta_star_arr) / self.approach.planetObj.RP

		self.x_orbit_arr = pos_vec_bi_arr[0][:]
		self.y_orbit_arr = pos_vec_bi_arr[1][:]
		self.z_orbit_arr = pos_vec_bi_arr[2][:]

	def compute_timed_orbit_trajectory(self, t_seconds, num_points=101):
		"""
		Computes the coordinates of initial capture orbit of the propulsive orbiter
		as a function of time.

		Parameters
		----------
		t_seconds : float
			time to compute the orbit trajectory from periapsis, seconds
		num_points : int
			number of grid points in the time interval
		"""

		self.P = 2 * np.pi * np.sqrt(self.a ** 3 / self.approach.planetObj.GM)

		self.t_array = np.linspace(0, t_seconds, num_points)
		self.M_array = (2*np.pi*self.t_array)/self.P

		self.E_array = np.array([])
		self.theta_star_array = np.array([])

		for M in self.M_array:
			E = self.compute_E(M)
			theta_star = self.compute_theta_star(E)

			self.E_array = np.append(self.E_array, E)
			self.theta_star_array = np.append(self.theta_star_array, theta_star)

		pos_vec_bi_arr = self.pos_vec_bi(self.theta_star_array) / self.approach.planetObj.RP

		self.x_timed_orbit_arr = pos_vec_bi_arr[0][:]
		self.y_timed_orbit_arr = pos_vec_bi_arr[1][:]
		self.z_timed_orbit_arr = pos_vec_bi_arr[2][:]


	def compute_E(self, M, rtol=1e-6):
		root = optimize.newton(lambda E: E - self.e*np.sin(E) - M, x0=M)
		return root

	def compute_theta_star(self, E):
		return 2*np.arctan(np.sqrt((1 + self.e) / (1 - self.e)) * np.tan(E/2))


class Test_compute_timed_orbit:
	approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]), rp=(2575 + 1500) * 1e3,
						psi=3 * np.pi / 2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
	orbiter.compute_timed_orbit_trajectory(t_seconds=75000, num_points=101)

	def test_timed_orbit(self):
		assert max(self.orbiter.t_array) == 75000




