import numpy as np
from scipy.interpolate import interp1d

class Launcher:
	"""
	The Launcher class is used to estimate launch vehicle performance.
	
	Attributes
	----------
	ID : str
		String identifier for launch vehicle
	XY : numpy.ndarray
		contains C3 in column 1, launch mass in column 2
	"""

	def __init__(self, launcherID, datafile, kind='linear'):
		"""
		Initializes the launcher class.
		
		Parameters
		----------
		launcherID : str
			identifier for the launch vehicle
		datafile : file
			CSV file containing the C3,launch mass data
		kind : str
			type of interpolation to use. Defaults to 'linear'.

		"""

		self.ID = launcherID
		self.XY = np.loadtxt(datafile, delimiter=',')
		self.f = interp1d(self.XY[:, 0], self.XY[:, 1], kind=kind, bounds_error=True)

	def launchMass(self, C3):
		"""
		Returns the launch capability of the vehicle for a 
		specified C3 array.

		Parameters
		----------
		C3 : float
			launch C3, km2/s2

		Returns
		--------
		mass : float
			launch mass capability, kg

		"""
		mass = self.f(C3)
		return mass











		
