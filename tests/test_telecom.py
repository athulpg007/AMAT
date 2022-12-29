from AMAT.telecom import Link, Schedule
from AMAT.approach import Approach
from AMAT.orbiter import PropulsiveOrbiter
from AMAT.visibility import LanderToPlanet, LanderToOrbiter, OrbiterToPlanet
import numpy as np


class Test_Cassini_Earth_Downlink:
	link = Link(freq=8.425, Pt=20, Gt_dBi=47.20, Gr_dBi=68.24, Ts=40.5,
				range_km=1.5E9, L_other_dB=0.55, rate_kbps=14.00, Eb_N0_req=0.31)

	def test_Eb_N0(self):
		assert round(self.link.EB_N0, 2) == 1.94


class Test_Huygens_Cassini_Relay:
	link = Link(freq=2.040, Pt=11.7, Gt_dBi=1.05, Gr_dBi=34.7, Ts=230,
				range_km=80E3, La_dB=0.05, L_other_dB=3.3, rate_kbps=8.00, Eb_N0_req=2.55)

	def test_Eb_N0(self):
		assert round(self.link.EB_N0, 2) == 10.14


class Test_OCEANUS_Uranus_Earth_Downlink:
	link = Link(freq=32, Pt=40, Gt_dBi=60.33, Gr_dBi=80.0, Ts=46.97,
				range_km=3.05E9, L_other_dB=0.60, rate_kbps=34, Eb_N0_req=0.31)

	def test_Eb_N0(self):
		assert round(self.link.EB_N0, 2) == 7.54


class Test_OCEANUS_Saturn_Probe_Relay:
	link = Link(freq=0.405, Pt=10.7, Gt_dBi=5.10, Gr_dBi=22.3, Ts=183.0,
				range_km=1.62E6, La_dB=2.0,  L_other_dB=2.75, rate_kbps=0.2, L_DSN_dB=0, Eb_N0_req=5.00)

	def test_Eb_N0(self):
		assert round(self.link.EB_N0, 2) == 5.93


class Test_OCEANUS_Uranus_Probe_Relay:
	link = Link(freq=0.405, Pt=10.7, Gt_dBi=5.89, Gr_dBi=22.3, Ts=104.0,
				range_km=1.55E5, L_other_dB=1.34, rate_kbps=0.2, Eb_N0_req=5.00)

	def test_Eb_N0(self):
		assert round(self.link.EB_N0, 2) == 31.62


class Test_Dragonfly_Downlink:
	link = Link(freq=8.425, Pt=30, Gt_dBi=30, Gr_dBi=80.0, Ts=40.5,
				range_km=1.5E9, L_other_dB=0.54, rate_kbps=2.00, Eb_N0_req=0.31)

	def test_link_budget(self):
		pass


class Test_Titan_Lander_To_Relay_Orbiter_X_Uplink:
	link = Link(freq=8.425, Pt=30, Gt_dBi=30, Gr_dBi=32.0, Ts=230,
				range_km=15E3, La_dB=0.05, L_other_dB=3.3, rate_kbps=7500.00, Eb_N0_req=2.55)

	def test_Eb_N0(self):
		self.link.print_link_budget()

class Test_Relay_Orbiter_Earth_Ka_Downlink:
	link = Link(freq=32.00, Pt=40, Dt=4.0, eta_t=0.60, Gr_dBi=79.83, Ts=48.0,
				range_km=1.5E9, L_other_dB=0.50, rate_kbps=500, Eb_N0_req=0.31)

	def test_Eb_N0(self):
		self.link.print_link_budget()

class Test_WorldView_4_Earth_Downlink:
	link = Link(freq=8.185, Pt=7.5, Gt_dBi=29.1, Gr_dBi=48.0, Ts=273.0,
				range_km=2718.0, L_other_dB=2.00, rate_kbps=400E3, Eb_N0_req=11.9)

	def test_Eb_N0(self):
		self.link.print_link_budget()


class Test_Schedule:
	schedule = Schedule(86400*16, 2001, [np.array([0, 86400]), np.array([86400*2, 86400*3])])

	def test_dummy(self):
		pass


class Test_Data_Volume_DTE:
	visibility1 = LanderToPlanet(observer_planet="TITAN", target_planet="EARTH",
								 latitude=3.0, date="2034-03-28 00:00:00")
	link = Link(freq=8.425, Pt=30, Gt_dBi=30, Gr_dBi=80.0, Ts=40.5,
				range_km=1.5E9, L_other_dB=0.54, rate_kbps=2.00, Eb_N0_req=0.31)
	schedule1 = Schedule(86400*16, 101, [np.array([4*86400, 5*86400]),
										  np.array([6*86400, 7*86400]),
										  np.array([8*86400, 9*86400]),
										  np.array([10*86400, 11*86400])])
	link.compute_data_volume(visibility1, schedule1)

	def test_data_volume(self):
		pass


class Test_Data_Volume_To_Relay:
	approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]),
						rp=(2575+1500) * 1e3, psi=3*np.pi/2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
	visibility1 = LanderToOrbiter(planet="TITAN", latitude=3.00, orbiter=orbiter, t_seconds=86400*16, num_points=2001)


	link = Link(freq=8.425, Pt=30, Gt_dBi=30, Gr_dBi=32.0, Ts=230, range_km=15E3,
				La_dB=0.05, L_other_dB=3.3, rate_kbps=7500.00, Eb_N0_req=2.55)
	schedule1 = Schedule(86400*16, 2001, [np.array([0.04*86400, 0.66*86400]),
										  np.array([0.92*86400, 1.30*86400])])
	link.compute_data_volume(visibility1, schedule1)

	def test_data_volume(self):
		pass


class Test_Relay_to_Earth_Downlink:
	approach = Approach("TITAN", v_inf_vec_icrf_kms=np.array([-0.910, 5.081, 4.710]),
						rp=(2575 + 1500) * 1e3, psi=3 * np.pi / 2)
	orbiter = PropulsiveOrbiter(approach=approach, apoapsis_alt_km=15000)
	visibility1 = OrbiterToPlanet(target_planet="EARTH", observer_planet="TITAN",
								  orbiter=orbiter, date="2034-03-28 00:00:00", t_seconds=86400*2, num_points=2001)

	link = Link(freq=32.00, Pt=40, Dt=4.0, eta_t=0.60, Gr_dBi=79.83, Ts=48.0,
				range_km=1.5E9, L_other_dB=0.50, rate_kbps=500, Eb_N0_req=0.31)
	schedule1 = Schedule(86400*2, 2001, [np.array([1.30*86400, 86400*16])])
	link.compute_data_volume(visibility1, schedule1)

	def test_data_volume(self):
		pass



