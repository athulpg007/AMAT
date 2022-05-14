"""
test_approach.py

Tests for Approach class

"""

import numpy as np
from numpy import linalg as LA


class TestImportApproach():
	def test_import_arrival(self):
		try:
			from AMAT.approach import Approach
			return True
		except ModuleNotFoundError:
			raise ModuleNotFoundError("Cannot import Approach from AMAT.approach")
			assert False

try:
	from AMAT.approach import Approach
except ModuleNotFoundError:
	raise ModuleNotFoundError("Cannot import Approach from AMAT.approach")


class Test_Approach_Entry:

	approach = Approach("NEPTUNE",
						v_inf_vec_icrf_kms=np.array([17.78952518, 8.62038536, 3.15801163]),
						rp=(24622+400)*1e3, psi=3*np.pi/2,
						is_entrySystem=True, h_EI=1000e3)

	def test_R1_0(self):

		assert (self.approach.R1(0) == np.array([[1,0,0],
		                                       [0, np.cos(0), np.sin(0)],
		                                       [0, -np.sin(0), np.cos(0)]])).all()

	def test_R1_90(self):

		assert (self.approach.R1(np.pi/2) == np.array([[1, 0, 0],
		                                         [0, np.cos(np.pi/2), np.sin(np.pi/2)],
		                                         [0, -np.sin(np.pi/2), np.cos(np.pi/2)]])).all()

	def test_R2_90(self):
		assert (self.approach.R2(np.pi/2) == np.array([[np.cos(np.pi/2), 0,  -np.sin(np.pi/2)],
		                                                 [0, 1, 0],
		                                                 [np.sin(np.pi/2), 0,  np.cos(np.pi/2)]])).all()

	def test_R3_0(self):

		assert (self.approach.R3(0) == np.array([[np.cos(0), np.sin(0), 0],
		                                        [-np.sin(0), np.cos(0), 0],
		                                        [0, 0, 1]])).all()

	def test_R3_90(self):
		assert (self.approach.R3(np.pi/2) == np.array([[np.cos(np.pi/2), np.sin(np.pi/2), 0],
		                                                [-np.sin(np.pi/2), np.cos(np.pi/2), 0],
		                                                [0, 0, 1]])).all()

	def test_ICRF_to_BI_unit_vec(self):

		delta =  abs(np.linalg.norm(self.approach.ICRF_to_BI(np.array([1, 0, 0])))) - 1
		assert delta < 1e-8

	def test_ICRF_to_BI_123(self):

		delta = abs(np.linalg.norm(self.approach.ICRF_to_BI(np.array([1, 2, 3])))) - np.sqrt(14)
		assert delta < 1e-8


	def test_v_inf_mag(self):
		assert abs(self.approach.v_inf_mag_kms - 20.018) < 1e-3
		assert abs(self.approach.v_inf_mag - 20018) < 1

	def test_a(self):
		assert ((abs(self.approach.a) - abs(-17059283.6903)) / abs(-17059283.6903)) < 1e-6

	def test_e(self):
		assert (abs(self.approach.e - 2.466767) / 2.466767) < 1e-4

	def test_beta(self):
		assert (abs(self.approach.beta - 1.153392) / 1.153392) < 1e-4

	def test_v_inf_bi(self):
		assert abs(self.approach.v_inf_vec_bi_mag_kms - 20.018) < 1e-3
		assert abs(np.arcsin(self.approach.v_inf_vec_bi_unit[2])*180/np.pi - 8.7554787) < 1e-4

	def test_phi(self):
		assert abs(self.approach.phi_1 - 0.07416) < 1e-3
		assert abs(self.approach.phi_2 - self.approach.phi_2_analytic) < 1e-8

	def test_rp_vec(self):
		assert (self.approach.rp_vec_bi_dprime[0] - self.approach.rp_vec_bi_dprime_analytic[0]) < 1e-6
		assert (self.approach.rp_vec_bi_dprime[1] - self.approach.rp_vec_bi_dprime_analytic[1]) < 1e-6
		assert (self.approach.rp_vec_bi_dprime[2] - self.approach.rp_vec_bi_dprime_analytic[2]) < 1e-6

	def test_e_vec_bi_unit(self):
		assert (self.approach.e_vec_bi_unit[0] - self.approach.rp_vec_bi_unit[0]) < 1e-6
		assert (self.approach.e_vec_bi_unit[1] - self.approach.rp_vec_bi_unit[1]) < 1e-6
		assert (self.approach.e_vec_bi_unit[2] - self.approach.rp_vec_bi_unit[2]) < 1e-6

	def test_h_vec_bi_unit(self):
		assert abs(np.arccos(self.approach.h_vec_bi_unit[2])*180/np.pi - 8.7554787) < 1e-4

	def test_N_vec_bi_unit(self):
		assert abs(self.approach.N_vec_bi_unit[0] - 0.07409418) < 1e-6
		assert abs(self.approach.N_vec_bi_unit[1] - -0.99725125) < 1e-6
		assert abs(self.approach.N_vec_bi_unit[2] - 0.) < 1e-6

	def test_i(self):
		assert abs(self.approach.i*180/np.pi - 8.75547878) < 1e-4

	def test_OMEGA(self):
		assert abs(self.approach.OMEGA - 4.78655112) < 1e-6

	def test_omega(self):
		assert abs(self.approach.omega - 0.41740417) < 1e-6

	def test_B_plane(self):
		assert abs(LA.norm(self.approach.R_vec_bi_unit) - 1) < 1e-8
		assert abs(LA.norm(self.approach.S_vec_bi_unit) - 1) < 1e-8
		assert abs(LA.norm(self.approach.T_vec_bi_unit) - 1) < 1e-8
		assert abs(self.approach.T_vec_bi_unit_dprime[1] + 1)  < 1e-8
		assert abs(self.approach.R_vec_bi_unit_dprime[0] - 1)  < 1e-8
		assert np.dot(self.approach.R_vec_bi_unit, self.approach.S_vec_bi_unit) < 1e-8
		assert np.dot(self.approach.R_vec_bi_unit, self.approach.T_vec_bi_unit) < 1e-8
		assert np.dot(self.approach.S_vec_bi_unit, self.approach.T_vec_bi_unit) < 1e-8
		assert np.dot(self.approach.S_vec_bi_unit, self.approach.B_vec_bi_unit) < 1e-8

	def test_theta_star_entry(self):
		assert abs(self.approach.theta_star_entry - -0.25726498) < 1e-6

	def test_r_vec_entry_bi(self):
		delta =  abs(LA.norm(self.approach.r_vec_entry_bi) - self.approach.r_EI)
		assert delta < 1e-4

	def test_v_entry_mag(self):
		assert abs(self.approach.v_entry_inertial_mag - 30567.901209444415) < 1e-6

	def test_gamma_entry_inertial(self):
		assert abs(self.approach.gamma_entry_inertial + 0.18330372) < 1e-6

	def test_v_vec_entry_bi(self):
		assert abs(LA.linalg.norm(self.approach.v_vec_entry_bi) - 30567.901209444415) < 1e-6

	def test_latitude_entry(self):
		ans1 = self.approach.latitude_entry_bi
		ans2 = self.approach.latitude_entry_bi_analytic
		assert abs(ans1 - ans2) < 1e-8

	def test_longitude_entry(self):
		assert abs(self.approach.longitude_entry_bi + 1.33832990) < 1e-6

	def test_v_vec_entry_atm(self):
		assert abs(self.approach.v_vec_entry_atm[0] - 24906.113142) < 1e-3
		assert abs(self.approach.v_vec_entry_atm[1] - 11733.340980) < 1e-3
		assert abs(self.approach.v_vec_entry_atm[2] - 4381.2517221) < 1e-3

	def test_v_entry_atm_mag(self):
		assert abs(self.approach.v_entry_atm_mag - 27877.9685250) < 1e-4

	def test_gamma_entry_inertial_check(self):
		ans1 = self.approach.gamma_entry_inertial
		ans2 = self.approach.gamma_entry_inertial_check
		assert abs(ans1-ans2) < 1e-6

	def test_gamma_entry_atm(self):
		assert abs(self.approach.gamma_entry_atm + 0.2012221) < 1e-4

	def test_heading_entry(self):
		assert abs(self.approach.heading_entry_atm*180/np.pi - 14.910607) < 1e-4


class Test_Approach_Orbiter:

	approach = Approach("NEPTUNE",
						v_inf_vec_icrf_kms=np.array([17.78952518, 8.62038536, 3.15801163]),
						rp=(24622+4000)*1e3, psi=3*np.pi/2)

	def test_theta_star_periapsis(self):
		ans1 = self.approach.theta_star_periapsis
		ans2 = self.approach.pos_vec_bi(self.approach.theta_star_periapsis)





class Test_Approach_Entry_Uranus:

	approach = Approach("URANUS",
						v_inf_vec_icrf_kms=np.array([-9.62521831, 16.51192666,  7.46493598]),
						rp=(25559+400)*1e3, psi=3*np.pi/2,
						is_entrySystem=True, h_EI=1000e3)

	def test_gamma_entry_atm(self):
		pass
