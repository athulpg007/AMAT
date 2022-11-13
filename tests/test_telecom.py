from AMAT.telecom import Link


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
