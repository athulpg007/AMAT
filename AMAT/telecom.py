# SOURCE FILENAME : telecom.py
# AUTHOR          : Athul Pradeepkumar Girija, athulpg007@gmail.com
# DATE CREATED    : 11/12/2022, 08:42 MT
# DATE MODIFIED   : 11/12/2022 08:42 MT
# REMARKS         : Compute the link margin and data rate for a telecom link.

import numpy as np
from scipy.integrate import cumtrapz


class Link:
	"""
	Computes the link budget for a telecom link.

	Attributes
	-----------
	freq : float
		Frequency, Hz
	wavelength : float
		Wavelength, m
	Pt : float
		Transmitter power, W
	Pt_dB : float
		Transmitter power, dBW
	Lt_dB : float
		Transmitter antenna loss, dB
	L_sc_dB : float
		Spacecraft circuit loss, dB
	Dt : float
		Transmitter antenna diameter, m
	At : float
		Transmitter antenna area, m2
	eta_t : float
		Transmitter antenna efficiency
	Gt_dBi : float
		Transmitter antenna gain, dBi
		Computed using Dt and eta_t if provided, or from Gt_dBi
	Dr : float
		Receiver antenna diameter, m
	Ar : float
		Receiver antenna area, m2
	eta_r : float
		Receiver antenna efficiency
	Gr_dBi: float
		Receiver gain, dBi
		Computed using Dr and eta_r if provided, or from Gr_dBi
	Ts : float
		System Noise Temperature, K
	Ts_dBK : float
		System Noise Temperature, dBK
	range : float
		Link distance, m
	Ls_dB : float
		Free space loss, dB
	La_dB : float
		Atmospheric attenuation, dB
	L_other_dB : float
		Other losses, dB
	L_DSN_dB : float
		DSN System Loss, dB
	Ka_dB : float
		Boltzmann's constant term
	R : float
		Data rate, bps
	R_dBHz : float
		Data rate, dBHz
	EB_N0_req : float
		Required Eb/N0
	EB_N0 : float
		Required Eb/N0
	EB_N0_margin : float
		Eb/N0 margin
	"""

	def __init__(self, freq, Pt, Ts, range_km, L_other_dB, rate_kbps, Eb_N0_req,
				 Dt=None, eta_t=None, Gt_dBi=None, Dr=None, eta_r=None, Gr_dBi=None,
				 Lt_dB=1.0, L_sc_dB=0.2, La_dB=0.35, L_DSN_dB=1.0):
		"""

		Parameters
		----------
		freq : float
			Frequency, GHz
		Pt : float
			Transmitter power, W
		Ts : float
			System Noise Temperature, K
		range_km : float
			link distance, km
		L_other_dB : float
			other losses, dB
		rate_kbps : float
			data rate, kbps
		Eb_N0_req : float
			required Eb/No
		Dt : float
			Transmitter antenna diameter, m
		eta_t : float
			Transmitter antenna efficiency
		Gt_dBi : float, optional
			Transmitter antenna gain, dBi
			Must be provided if Dt and eta_t are not provided.
		Dr : float
			Receiver antenna diameter, m
		eta_r : float
			Receiver antenna efficiency
		Gr_dBi: float
			Receiver gain, dBi
			Must be provided if Dr and eta_r are not provided.
		Lt_dB : float, optional
			Transmitter antenna loss, dB; defaults to 1.0 dB
		L_sc_dB : float, optional
			Spacecraft circuit loss, dB; defaults to 0.2 dB
		La_dB : float, optional
			atmospheric attenuation loss, dB; defaults to 0.35 dB
		L_DSN_dB : float, optional
			DSN system losses, dBl defaults to 1.0 dB

		"""

		self.freq = freq*1E9
		self.wavelength = 3E8/self.freq
		self.Pt = Pt
		self.Pt_dB = self.compute_dB(self.Pt)
		self.Lt_dB = Lt_dB
		self.L_sc_dB = L_sc_dB

		# if Dt and eta_t are provided, compute transmitter gain using these values,
		# else if Gt_dBi is provided, use this value directly for transmitter gain
		if Dt and eta_t:
			self.Dt = Dt
			self.At = 0.25*np.pi*self.Dt*self.Dt
			self.eta_t = eta_t
			self.Gt = self.compute_antenna_gain(self.eta_t, self.Dt, self.wavelength)
			self.Gt_dBi = self.compute_dB(self.Gt)
		elif Gt_dBi:
			self.Dt = None
			self.At = None
			self.eta_t = None
			self.Gt_dBi = Gt_dBi

		# if Dr and eta_r are provided, compute receiver gain using these values,
		# else if Gr_dBi is provided, use this value directly for receiver gain
		if Dr and eta_r:
			self.Dr = Dt
			self.Ar = 0.25 * np.pi * self.Dr * self.Dr
			self.eta_r = eta_r
			self.Gr = self.compute_antenna_gain(self.eta_r, self.Dr, self.wavelength)
			self.Gr_dBi = self.compute_dB(self.Gr)
		elif Gr_dBi:
			self.Dr = None
			self.Ar = None
			self.eta_r = None
			self.Gr_dBi = Gr_dBi

		self.Ts = Ts
		self.Ts_dBK = self.compute_dB(self.Ts)
		self.range = range_km*1E3
		self.Ls_dB = self.compute_free_space_loss_dB(self.range, self.wavelength)
		self.La_dB = La_dB
		self.L_other_dB = L_other_dB
		self.L_DSN_dB = L_DSN_dB
		self.Ka = 1.38E-23
		self.Ka_dB = self.compute_dB(self.Ka)
		self.R = rate_kbps*1E3
		self.R_dBHz = self.compute_dB(self.R)
		self.EB_N0_req = Eb_N0_req

		self.EB_N0 = self.Pt_dB + self.Gt_dBi - self.Lt_dB - self.L_sc_dB + self.Gr_dBi - self.Ts_dBK -\
					 self.Ls_dB - self.La_dB - self.L_other_dB - self.L_DSN_dB - self.R_dBHz - self.Ka_dB
		self.EB_N0_margin = self.EB_N0 - self.EB_N0_req

	def compute_dB(self, X):
		"""

		Parameters
		----------
		X : float
			any parameter to be converted to dB

		Returns
		-------
		ans : float
			Power in dBW

		"""
		return 10*np.log10(X)

	def compute_antenna_gain(self, eta, D, wavelength):
		"""

		Parameters
		----------
		eta : float
			antenna efficiency
		D : float
			antenna diameter, m
		wavelength : float
			wavelength, m

		Returns
		-------
		ans : float
			antenna gain, before converting to dBi
		"""
		return eta*((np.pi*D)/wavelength)**2

	def compute_free_space_loss_dB(self, range, wavelength):
		"""

		Parameters
		----------
		range : float
			link distance, m
		wavelength : float
			wavelength, m

		Returns
		-------
		ans : float
			free space loss, dB
		"""
		return 20*np.log10(4*np.pi*range/wavelength)

	def print_link_budget(self):
		print("\n")
		print("-------------------------------------------")
		print(f"Frequency, GHz:          {self.freq/1E9}")
		print(f"Transmitter Power, W:    {self.Pt}")
		print(f"Transmitter Power, dB:   {round(self.Pt_dB,2)}")
		print(f"Transmitter Loss, dB:   -{round(self.Lt_dB, 2)}")
		print(f"S/C Circuit Loss, dB:   -{round(self.L_sc_dB, 2)}")
		print(f"Transmit antenna D., m:  {self.Dt}")
		print(f"Transmit antenna eff:    {self.eta_t}")
		print(f"Transmitter Gain, dBi:   {round(self.Gt_dBi,2)}")
		print(f"Receive antenna D., m:   {self.Dr}")
		print(f"Receive antenna eff:     {self.eta_r}")
		print(f"Receiver Gain, dBi:      {round(self.Gr_dBi,2)}")
		print(f"System Noise Temp, K:    {self.Ts}")
		print(f"System Noise Temp, dBK: -{round(self.Ts_dBK,2)}")
		print(f"Link Distance, km:       {self.range/1E3}")
		print(f"Free Space Loss, dB:    -{round(self.Ls_dB,2)}")
		print(f"Atmospheric Loss, dB:   -{self.La_dB}")
		print(f"Other Losses, dB:       -{self.L_other_dB}")
		print(f"Boltzmann's const, dB:  +{round(-self.Ka_dB,2)}")
		print(f"Data rate, kbps:         {self.R/1E3}")
		print(f"Data rate, dBhz:        -{round(self.R_dBHz,2)}")
		print("-------------------------------------------")
		print(f"Available Eb/N0:         {round(self.EB_N0,2)}")
		print(f"Required Eb/N0:          {self.EB_N0_req}")
		print(f"Eb/N0 Margin:            {round(self.EB_N0_margin,2)}")
		print("-------------------------------------------")

	def compute_data_volume(self, visibility, schedule):
		"""

		Parameters
		----------
		visibility : one of AMAT.visibility.LanderToPlanet, AMAT.visibility.LanderToOrbiter,
					 AMAT.visibility.OrbiterToPlanet objects
		schedule : AMAT.telecom.Schedule
			Transmit schedule

		Returns
		-------
		"""

		self.visibility = visibility
		self.schedule = schedule
		self.t_array = self.visibility.t_array
		self.data_volume_array = cumtrapz((self.R/1e3)*self.visibility.visible_array*self.schedule.transmit_array,
										  self.t_array, initial=0)


class Schedule:
	def __init__(self, t_seconds, num_points, t_transmit_times_list):
		"""

		Parameters
		----------
		t_seconds : float
			time for schedule in seconds
		num_points : int
			number of points to compute for the schedule
		t_transmit_times_list : list of numpy.ndarray
			Specify the times the data link is transmitting
			eg: [np.array([0, 86400]), np.array([123000, 125000])]
		"""
		self.t_array = np.linspace(0, t_seconds, num_points)
		self.transmit_array = np.zeros(num_points, dtype=bool)

		for i, t in enumerate(self.t_array):
			for window in t_transmit_times_list:
				if window[0] <= t <= window[1]:
					self.transmit_array[i] = True
					break
				else:
					self.transmit_array[i] = False
