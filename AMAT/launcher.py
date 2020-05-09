# Author(s) : Athul Pradeepkumar Girija; apradee@purdue.edu
#
# License : CC-BY-SA-4.0
#
# You are free to:
#
# Share — copy and redistribute the material in any medium or format
# Adapt — remix, transform, and build upon the material for any#
# purpose,  even commercially.

# The licensor cannot revoke these freedoms as long as you follow the 
# license terms

# Attribution — You must give appropriate credit, provide a link to 
# the license, and indicate if changes were made. You may do so in any
# reasonable manner, but not in any way that suggests the licensor 
# endorses you or your use.

# ShareAlike — If you remix, transform, or build upon the material, 
# you must distribute your contributions under the same license as 
# the original.  

# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.

# ===================================================================
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. 

# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ===================================================================

# This script requires that `numpy`, 'scipy', and matplotlib
# be installed within  the Python environment you are running 
# this script in.


import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import os

class Launcher:
	"""
	The Launcher class is used to estimate launch vehicle performance.
	
	Attributes
	----------
	ID : str
		String identifier of planet object
	XY : numpy.ndarray
		contains C3 in column 1, launch mass in column 2
	"""

	def __init__(self, launcherID):
		"""
		Initializes the planet object with the planetary constants.
		
		Parameters
		----------
		launcherID : str
			Name of the launch vehicle, must be one of the following 
			Valid entries are: 
			
			'atlasV401', 
			'atlasV551', 
			'atlasV551-with-kick',
			'deltaIVH',
			'deltaIVH-with-kick', 
			'falconH', 
			'falconH-recovery', 
			'sls-block-1B',
			'sls-block-1B-with-kick'
		"""

		if launcherID == 'atlasV401':
			self.ID     = 'Atlas V401'      
			self.XY     =  np.loadtxt('../launcher-data/atlasV401.csv', delimiter=',')
		

		elif launcherID == 'atlasV551':
			self.ID     = 'Atlas V551'      
			self.XY     =  np.loadtxt('../launcher-data/atlasV551.csv', delimiter=',')

		elif launcherID == 'atlasV551-with-kick':
			self.ID     = 'Atlas V551 with kick'      
			self.XY     =  np.loadtxt('../launcher-data/atlasV551-with-kick.csv', delimiter=',')

		elif launcherID == 'deltaIVH':
			self.ID     = 'Delta IVH'
			self.XY     = np.loadtxt('deltaIVH.csv', delimiter=',')

		elif launcherID == 'deltaIVH-with-kick':
			self.ID     = 'Delta IVH with kick'
			self.XY     = np.loadtxt('../launcher-data/deltaIVH-with-kick.csv', delimiter=',')

		elif launcherID == 'falconH':
			self.ID     = 'Falcon Heavy'
			self.XY     = np.loadtxt('../launcher-data/falconH.csv', delimiter=',')

		elif launcherID == 'falconH-recovery':
			self.ID     = 'Falcon Heavy (Recovery)'
			self.XY     = np.loadtxt('../launcher-data/falconH-recovery.csv', delimiter=',')

		elif launcherID == 'sls-block-1B':
			self.ID     = 'SLS Block 1B'
			self.XY     = np.loadtxt('../launcher-data/sls-block-1B.csv', delimiter=',')

		elif launcherID == 'sls-block-1B-with-kick':
			self.ID     = 'SLS Block 1B with kick'
			self.XY     = np.loadtxt('../launcher-data/sls-block-1B-with-kick.csv', delimiter=',')

		else:
			print(" >>> ERR : Invalid planet identifier provided.")


	def performanceQuery(self, C3):
		"""
		Returns the launch capability of the vehicle for a 
		specified C3.

		Parameters
		----------
		C3 : float
			launch C3, km2/s2

		Returns
		--------
		mass : float
			launch mass capability, kg

		"""

		f = interp1d(self.XY[:,0], self.XY[:,1], kind='cubic', bounds_error=False)

		mass = float(f(C3))

		return mass











		
