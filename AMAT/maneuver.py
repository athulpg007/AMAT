# SOURCE FILENAME : manuever.py
# AUTHOR          : Athul Pradeepkumar Girija, apradee@purdue.edu
# DATE MODIFIED   : 04/29/2022, 08:27 MT
# REMARKS         : Compute the deflection maneuver delta-v
#                   following Kyle's dissertation Chapter 2.
# REFERENCE 	  : Hughes, Ph.D. Dissertation, 2016.

import numpy as np
from numpy import linalg as LA

from AMAT.planet import Planet
from AMAT.approach import Approach

class ProbeOrbiterDeflection:
	"""
	Computes the deflection manuever delta-V and time of flight for an orbiter spacecraft
	divert manuever for propulsive orbit insertion after probe release on approach.

	Attributes
	----------
	planetObj : AMAT.planet.Planet object
		arrival planet object for approach trajectory
	probe : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the entry probe
	space : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the orbiter spacecraft
	r_dv_rp : float
		radial distance at which the deflection maneuver is
		performed, in terms of arrival planet radius
		Example: 1000, for maneuver performed at radial distance of
		1000 times the radius of the planet.
	r_dv : float
		radial distance at which the deflection maneuver is
		performed, in meters
	theta_star_dv_probe : float
		true anomaly of the probe at deflection maneuver, rad
	r_vec_dv : numpy.ndarray
		probe position vector at maneuver in body-inertial frame, meters
	r_vec_dv_unit : numpy.ndarray
		probe position unit vector at maneuver in body-inertial frame
	delta_theta_star_probe : float
		true anomaly change for probe (Eq. 2.75, REF), rad
	delta_theta_star_space : float
		true anomaly change for orbiter (Eq. 2.78, REF), rad
	v_vec_dv_probe : numpy.ndarray
		probe velocity vector in body-inertial frame, meters
	v_vec_dv_space : numpy.ndarray
		orbiter velocity vector in body-inertial frame, meters
	v_vec_dv_maneuver : numpy.ndarray
		orbiter deflection maneuver delta-V vector, m/s
	v_vec_dv_maneuver_mag : numpy.ndarray
		orbiter deflection maneuver delta-V magnitude, m/s
	TOF_probe : float
		probe time of flight from deflection maneuver until
		atmospheric entry interface, days
	TOF_space: float
		orbiter time of flight from deflection maneuver until
		periapsis, days

	"""

	def __init__(self, arrivalPlanet, v_inf_vec_icrf_kms,
								  rp_probe, psi_probe,  h_EI_probe,
								  rp_space, psi_space,
								  r_dv_rp):
		"""

		Initializes the ProbeOrbiterDeflection class with the following params

		Parameters
		----------
		arrivalPlanet :  str
			Name of the planetary body, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		v_inf_vec_ICRF_kms : numpy.ndarray
			v_inf vector in ICRF, km/s
		rp_probe : float
			target periapsis radius for entry probe, meters
		psi_probe : float
			target angular position on ring of periapsis radius
			for entry probe, rad
		h_EI_probe : float
			atmospheric entry interface altitude for entry
			probe, meters
		rp_space : float
			target periapsis radius for spacecraft, meters
		psi_space : float
			target angular position on ring of periapsis radius
			for orbiter spacecraft, rad
		r_dv_rp : float
			radial distance at which the deflection manuever is
			performed, in terms of arrival planet radius
			Example: 1000, for manuever performed at radial distance of
			1000 times the radius of the planet.
		"""

		self.planetObj = Planet(arrivalPlanet)
		self.probe = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_probe, psi_probe, is_entrySystem=True, h_EI=h_EI_probe)
		self.space = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_space, psi_space)
		self.r_dv_rp = r_dv_rp
		self.r_dv = self.r_dv_rp * self.planetObj.RP

		self.theta_star_dv_probe = -1*np.arccos(((self.probe.h**2/(self.planetObj.GM * self.r_dv)) - 1)*\
												(1.0/self.probe.e))

		self.r_vec_dv = self.probe.pos_vec_bi(self.theta_star_dv_probe)
		self.r_vec_dv_unit = self.r_vec_dv / LA.linalg.norm(self.r_vec_dv)

		self.delta_theta_star_probe = abs(self.theta_star_dv_probe)
		self.delta_theta_star_space = np.arccos(np.dot(self.space.rp_vec_bi_unit, self.r_vec_dv_unit))

		self.P_probe = self.probe.a*(1 - self.probe.e**2)

		self.f_probe = 1 - (self.probe.rp/self.P_probe)*(1 - np.cos(self.delta_theta_star_probe))
		self.g_probe = ((self.r_dv*self.probe.rp)/(np.sqrt(self.planetObj.GM*self.P_probe)))*np.sin(self.delta_theta_star_probe)

		self.v_vec_dv_probe = (self.probe.rp_vec_bi - self.f_probe*self.r_vec_dv)/self.g_probe

		self.C = np.sqrt(self.space.rp**2 + self.r_dv**2 - 2*self.space.rp*self.r_dv*np.cos(self.delta_theta_star_space))
		self.S = 0.5*(self.space.rp + self.r_dv + self.C)
		self.alpha_prime = 2*np.arcsinh(np.sqrt(self.S/(2*abs(self.space.a))))
		self.beta_prime  = 2*np.arcsinh(np.sqrt((self.S-self.C)/(2*abs(self.space.a))))

		self.P1 = (4*abs(self.space.a)*(self.S - self.space.rp)*(self.S - self.r_dv))/(self.C**2)
		self.P2 = np.sinh(0.5*(self.alpha_prime + self.beta_prime))

		self.P_space = self.P1*self.P2**2

		self.f_space = 1 - (self.space.rp / self.P_space) * (1 - np.cos(self.delta_theta_star_space))
		self.g_space = ((self.r_dv * self.space.rp) / (np.sqrt(self.planetObj.GM * self.P_space))) * np.sin(self.delta_theta_star_space)

		self.v_vec_dv_space = (self.space.rp_vec_bi - self.f_space * self.r_vec_dv) / self.g_space

		self.dv_maneuver_vec = self.v_vec_dv_space - self.v_vec_dv_probe
		self.dv_maneuver_mag = LA.norm(self.dv_maneuver_vec)

		self.H1 = np.sqrt((self.probe.e-1)/(self.probe.e+1))*np.tan(0.5*self.delta_theta_star_probe)
		self.H_dv_probe = 2*np.arctanh(self.H1)

		self.T1 = np.sqrt(abs(self.probe.a)**3/self.planetObj.GM)
		self.T2 = abs(self.probe.e*np.sinh(self.H_dv_probe) - self.H_dv_probe)

		self.TOF_probe = (self.T1*self.T2) / 86400

		self.U1 = np.sqrt(abs(self.space.a)**3/self.planetObj.GM)
		self.U2 = (np.sinh(self.alpha_prime) - self.alpha_prime) - (np.sinh(self.beta_prime) - self.beta_prime)

		self.TOF_space = (self.U1*self.U2) / 86400


class ProbeProbeDeflection:
	"""
	Computes the deflection maneuver delta-V and time of flight for delivering
	two atmospheric entry systems from an approach trajectory.

	Attributes
	----------
	planetObj : AMAT.planet.Planet object
		arrival planet object for approach trajectory
	probe1 : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the first entry probe
	probe2 : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the second entry probe
	r_dv_rp : float
		radial distance at which the deflection maneuver is
		performed, in terms of arrival planet radius
		Example: 1000, for maneuver performed at radial distance of
		1000 times the radius of the planet.
	r_dv : float
		radial distance at which the deflection maneuver is
		performed, in meters
	theta_star_dv_probe1 : float
		true anomaly of the first probe at deflection maneuver, rad
	theta_star_dv_probe2 : float
		true anomaly of the second probe at deflection maneuver, rad
	delta_theta_star_probe1 : float
		true anomaly change for first probe (Eq. 2.75, REF), rad
	delta_theta_star_probe2 : float
		true anomaly change for second probe (Eq. 2.75, REF), rad
	v_vec_dv_probe1 : numpy.ndarray
		first probe velocity vector in body-inertial frame, meters
	v_vec_dv_probe2 : numpy.ndarray
		second probe velocity vector in body-inertial frame, meters
	v_vec_dv_maneuver : numpy.ndarray
		deflection maneuver delta-V vector, m/s
	v_vec_dv_maneuver_mag : numpy.ndarray
		deflection maneuver delta-V magnitude, m/s
	TOF_probe1 : float
		probe time of flight from deflection maneuver until
		atmospheric entry interface, days
	TOF_probe2: float
		orbiter time of flight from deflection maneuver until
		atmospheric entry interface, days

	"""

	def __init__(self, arrivalPlanet, v_inf_vec_icrf_kms,
					   rp_probe1, psi_probe1,  h_EI_probe1,
					   rp_probe2, psi_probe2,  h_EI_probe2,
					   r_dv_rp):
		"""

		Initializes the ProbeProbeDeflection class with the following params

		Parameters
		----------
		arrivalPlanet : str
			Name of the planetary body, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		v_inf_vec_ICRF_kms : numpy.ndarray
			v_inf vector in ICRF, km/s
		rp_probe1 : float
			target periapsis radius for first entry probe, meters
		psi_probe1 : float
			target angular position on ring of periapsis radius
			for first entry probe, rad
		h_EI_probe1 : float
			atmospheric entry interface altitude for first entry
			probe, meters
		rp_probe2 : float
			target periapsis radius for second entry probe, meters
		psi_probe2 : float
			target angular position on ring of periapsis radius
			for second  entry probe, rad
		h_EI_probe2 : float
			atmospheric entry interface altitude for second entry
			probe, meters
		r_dv_rp : float
			radial distance at which the deflection manuever is
			performed, in terms of arrival planet radius
			Example: 1000, for manuever performed at radial distance of
			1000 times the radius of the planet.
		"""

		self.planetObj = Planet(arrivalPlanet)
		self.probe1 = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_probe1, psi_probe1, is_entrySystem=True, h_EI=h_EI_probe1)
		self.probe2 = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_probe2, psi_probe2, is_entrySystem=True, h_EI=h_EI_probe2)
		self.r_dv_rp = r_dv_rp
		self.r_dv = self.r_dv_rp * self.planetObj.RP

		self.theta_star_dv_probe1 = -1*np.arccos(((self.probe1.h**2/(self.planetObj.GM * self.r_dv)) - 1)*\
												(1.0/self.probe1.e))
		self.theta_star_dv_probe2 = -1 * np.arccos(((self.probe2.h ** 2 / (self.planetObj.GM * self.r_dv)) - 1) * \
												   (1.0 / self.probe2.e))

		self.r_vec_dv = self.probe1.pos_vec_bi(self.theta_star_dv_probe1)
		self.r_vec_dv_unit = self.r_vec_dv / LA.linalg.norm(self.r_vec_dv)

		self.delta_theta_star_probe1 = abs(self.theta_star_dv_probe1)
		self.delta_theta_star_probe2 = abs(self.theta_star_dv_probe2)


		self.P_probe1 = self.probe1.a*(1 - self.probe1.e**2)
		self.f_probe1 = 1 - (self.probe1.rp/self.P_probe1)*(1 - np.cos(self.delta_theta_star_probe1))
		self.g_probe1 = ((self.r_dv*self.probe1.rp)/(np.sqrt(self.planetObj.GM*self.P_probe1)))*np.sin(self.delta_theta_star_probe1)
		self.v_vec_dv_probe1 = (self.probe1.rp_vec_bi - self.f_probe1*self.r_vec_dv)/self.g_probe1

		self.P_probe2 = self.probe2.a*(1 - self.probe2.e**2)
		self.f_probe2 = 1 - (self.probe2.rp / self.P_probe2) * (1 - np.cos(self.delta_theta_star_probe2))
		self.g_probe2 = ((self.r_dv * self.probe2.rp) / (np.sqrt(self.planetObj.GM * self.P_probe2))) * np.sin(self.delta_theta_star_probe2)
		self.v_vec_dv_probe2 = (self.probe2.rp_vec_bi - self.f_probe2 * self.r_vec_dv) / self.g_probe2

		self.dv_maneuver_vec = self.v_vec_dv_probe2 - self.v_vec_dv_probe1
		self.dv_maneuver_mag = LA.norm(self.dv_maneuver_vec)

		self.H1 = np.sqrt((self.probe1.e-1)/(self.probe1.e+1))*np.tan(0.5*self.delta_theta_star_probe1)
		self.H_dv_probe1 = 2*np.arctanh(self.H1)
		self.T1 = np.sqrt(abs(self.probe1.a)**3/self.planetObj.GM)
		self.T2 = abs(self.probe1.e*np.sinh(self.H_dv_probe1) - self.H_dv_probe1)
		self.TOF_probe1 = (self.T1*self.T2) / 86400

		self.H2 = np.sqrt((self.probe2.e - 1) / (self.probe2.e + 1)) * np.tan(0.5 * self.delta_theta_star_probe2)
		self.H_dv_probe2 = 2 * np.arctanh(self.H2)
		self.T3 = np.sqrt(abs(self.probe2.a) ** 3 / self.planetObj.GM)
		self.T4 = abs(self.probe2.e * np.sinh(self.H_dv_probe2) - self.H_dv_probe2)
		self.TOF_probe2 = (self.T3 * self.T4) / 86400

class OrbiterOrbiterDeflection:
	"""
	Computes the deflection maneuver delta-V and time of flight for delivering
	two orbiter spacecraft from an approach trajectory.

	Attributes
	----------
	planetObj : AMAT.planet.Planet object
		arrival planet object for approach trajectory
	space1 : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the first orbiter spacecraft
	space2 : AMAT.approach.Approach object
		Approach object with approach trajectory parameters for the second orbiter spacecraft
	r_dv_rp : float
		radial distance at which the deflection maneuver is
		performed, in terms of arrival planet radius
		Example: 1000, for maneuver performed at radial distance of
		1000 times the radius of the planet.
	r_dv : float
		radial distance at which the deflection maneuver is
		performed, in meters
	theta_star_dv_space1 : float
		true anomaly of the first orbiter spacecraft at deflection maneuver, rad
	r_vec_dv : numpy.ndarray
		position vector at deflection maneuver in body-inertial frame, meters
	r_vec_dv_unit : numpy.ndarray
		position unit vector at deflection maneuver in body-inertial frame
	delta_theta_star_space1 : float
		true anomaly change for first orbiter spacecraft (Eq. 2.78, REF), rad
	delta_theta_star_space2 : float
		true anomaly change for second orbiter spacecraft (Eq. 2.78, REF), rad
	v_vec_dv_space1 : numpy.ndarray
		first orbiter spacecraft velocity vector in body-inertial frame, meters
	v_vec_dv_space2 : numpy.ndarray
		second orbiter spacecraft velocity vector in body-inertial frame, meters
	v_vec_dv_maneuver : numpy.ndarray
		deflection maneuver delta-V vector, m/s
	v_vec_dv_maneuver_mag : numpy.ndarray
		deflection maneuver delta-V magnitude, m/s
	TOF_space1 : float
		first spacecraft orbiter time of flight from deflection maneuver until
		periapsis, days
	TOF_space2 : float
		second spacecraft orbiter time of flight from deflection maneuver until
		periapsis, days

	"""

	def __init__(self, arrivalPlanet, v_inf_vec_icrf_kms,
								  rp_space1, psi_space1,
								  rp_space2, psi_space2,
								  r_dv_rp):
		"""

		Initializes the OrbiterOrbiterDeflection class with the following params

		Parameters
		----------
		arrivalPlanet :  str
			Name of the planetary body, must be all uppercase
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'
		v_inf_vec_ICRF_kms : numpy.ndarray
			v_inf vector in ICRF, km/s
		rp_space1 : float
			target periapsis radius for first orbiter spacecraft, meters
		psi_space1 : float
			target angular position on ring of periapsis radius
			for first orbiter spacecraft, rad
		rp_space2 : float
			target periapsis radius for first orbiter spacecraft, meters
		psi_space2 : float
			target angular position on ring of periapsis radius
			for first orbiter spacecraft, rad
		r_dv_rp : float
			radial distance at which the deflection manuever is
			performed, in terms of arrival planet radius
			Example: 1000, for maneuver performed at radial distance of
			1000 times the radius of the planet.

		"""

		self.planetObj = Planet(arrivalPlanet)
		self.space1 = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_space1, psi_space1)
		self.space2 = Approach(arrivalPlanet, v_inf_vec_icrf_kms, rp_space2, psi_space2)
		self.r_dv_rp = r_dv_rp
		self.r_dv = self.r_dv_rp * self.planetObj.RP

		self.theta_star_dv_space1 = -1*np.arccos(((self.space1.h**2/(self.planetObj.GM * self.r_dv)) - 1)*\
												(1.0/self.space1.e))

		self.r_vec_dv = self.space1.pos_vec_bi(self.theta_star_dv_space1)
		self.r_vec_dv_unit = self.r_vec_dv / LA.linalg.norm(self.r_vec_dv)

		self.delta_theta_star_space1 = np.arccos(np.dot(self.space1.rp_vec_bi_unit, self.r_vec_dv_unit))
		self.delta_theta_star_space2 = np.arccos(np.dot(self.space2.rp_vec_bi_unit, self.r_vec_dv_unit))


		self.C1 = np.sqrt(self.space1.rp**2 + self.r_dv**2 - 2*self.space1.rp*self.r_dv*np.cos(self.delta_theta_star_space1))
		self.S1 = 0.5*(self.space1.rp + self.r_dv + self.C1)
		self.alpha_prime1 = 2*np.arcsinh(np.sqrt(self.S1/(2*abs(self.space1.a))))
		self.beta_prime1  = 2*np.arcsinh(np.sqrt((self.S1-self.C1)/(2*abs(self.space1.a))))
		self.P1 = (4*abs(self.space1.a)*(self.S1 - self.space1.rp)*(self.S1 - self.r_dv))/(self.C1**2)
		self.P2 = np.sinh(0.5*(self.alpha_prime1 + self.beta_prime1))
		self.P_space1 = self.P1*self.P2**2
		self.f_space1 = 1 - (self.space1.rp / self.P_space1) * (1 - np.cos(self.delta_theta_star_space1))
		self.g_space1 = ((self.r_dv * self.space1.rp) / (np.sqrt(self.planetObj.GM * self.P_space1))) * np.sin(self.delta_theta_star_space1)
		self.v_vec_dv_space1 = (self.space1.rp_vec_bi - self.f_space1 * self.r_vec_dv) / self.g_space1

		self.C2 = np.sqrt(self.space2.rp ** 2 + self.r_dv ** 2 - 2 * self.space2.rp * self.r_dv * np.cos(self.delta_theta_star_space2))
		self.S2 = 0.5 * (self.space2.rp + self.r_dv + self.C2)
		self.alpha_prime2 = 2 * np.arcsinh(np.sqrt(self.S2 / (2 * abs(self.space2.a))))
		self.beta_prime2 = 2 * np.arcsinh(np.sqrt((self.S2 - self.C2) / (2 * abs(self.space2.a))))
		self.P3 = (4 * abs(self.space2.a) * (self.S2 - self.space2.rp) * (self.S2 - self.r_dv)) / (self.C2 ** 2)
		self.P4 = np.sinh(0.5 * (self.alpha_prime2 + self.beta_prime2))
		self.P_space2 = self.P3 * self.P4 ** 2
		self.f_space2 = 1 - (self.space2.rp / self.P_space2) * (1 - np.cos(self.delta_theta_star_space2))
		self.g_space2 = ((self.r_dv * self.space2.rp) / (np.sqrt(self.planetObj.GM * self.P_space2))) * np.sin(self.delta_theta_star_space2)
		self.v_vec_dv_space2 = (self.space2.rp_vec_bi - self.f_space2 * self.r_vec_dv) / self.g_space2

		self.dv_maneuver_vec = self.v_vec_dv_space2 - self.v_vec_dv_space1
		self.dv_maneuver_mag = LA.norm(self.dv_maneuver_vec)

		self.U1 = np.sqrt(abs(self.space1.a)**3/self.planetObj.GM)
		self.U2 = (np.sinh(self.alpha_prime1) - self.alpha_prime1) - (np.sinh(self.beta_prime1) - self.beta_prime1)
		self.TOF_space1 = (self.U1*self.U2)/86400

		self.U3 = np.sqrt(abs(self.space2.a) ** 3 / self.planetObj.GM)
		self.U4 = (np.sinh(self.alpha_prime2) - self.alpha_prime2) - (np.sinh(self.beta_prime2) - self.beta_prime2)
		self.TOF_space2 = (self.U3 * self.U4)/86400
