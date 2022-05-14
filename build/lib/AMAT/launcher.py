import numpy as np
from scipy.interpolate import interp1d

class Launcher:
	"""
	The Launcher class is used to estimate launch vehicle performance.
	
	Attributes
	----------
	launcherID : str
		String identifier for launch vehicle
	datafile : CSV file
		CSV file containing C3,launch mass (kg)
	kind : str
			type of interpolation to use. Defaults to 'linear'
	f : scipy.interpolate.interp1d
		interpolation function for launch mass at a specified C3
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
		self.f = interp1d(self.XY[:, 0], self.XY[:, 1], kind=kind, fill_value=0, bounds_error=False)

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











		
