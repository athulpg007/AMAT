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

# This script requires that `numpy`, 'scipy', and ''matplotlib
# be installed within  the Python environment you are running 
# this script in.

import numpy as np
from scipy.interpolate import interp1d
from matplotlib import rcParams
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz


class Planet:
	"""
	The Planet class is used to store planetary constants, 
	load atmospheric data from look-up tables, and define
	non-dimensional parameters used in the simulations.
	
	Attributes
	----------
	ID : str
		String identifier of planet object
	RP : float
		Mean equatorial radius of the target planet in meters
	OMEGA : float
		Mean angular velocity of rotation of the planet about 
		its axis of rotation in rad/s
	GM : float
		Standard gravitational parameter of the planet in m3/s2
	rho0 : float
		Reference atmospheric density at the surface of the target 
		planet in kg/m3
	CPCV : float
		Specific heat ratio CP/CV at the surface of the planet
	J2 : float
		zonal harmonic coefficient J2
	J3 : float
		zonal harmonic coefficient J3
	h_thres : float
		Atmospheric model cutoff altitude in meters, 
		density is set to 0, if altitude exceeds h_thres
	h_skip : float
		If vehicle altitude exceeds this value, trajectory is cut off
		and vehicle is assumed to skip off the atmosphere
	h_trap : float
		If vehicle altitude falls below this value, trajectory is cut off
		and vehicle is assumed to hit the surface
	h_low : float
		If terminal altitude is below this value vehicle is assumed to
		be trapped in the atmosphere. 
	Vref : float
		Reference velocity for non-dimensionalization of entry equations
	tau : float
		Reference timescale used to non-dimensionalize time, angular rates
	OMEGAbar : float
		Reference non-dimensional angular rate of planet's rotation
	EARTHG : float
		Reference value of acceleration due to Earth's gravity
	ATM : numpy.ndarray
		Array containing the data loaded from atmospheric lookup file
	ATM_height : numpy.ndarray
		Array containing height values from atm. look up dat file
	ATM_temp : numpy.ndarray
		Array containing temperature values from atm. look up dat file
	ATM_pressure : numpy.ndarray
		Array containing pressure values from atm. look up dat file
	ATM_density : numpy.ndarray
		Array containing density values from atm. look up dat file
	ATM_sonic : numpy.ndarray
		Array containing computed sonic speed values
	temp_int : scipy.interpolate.interpolate.interp1d
		Function which interpolates temperature as function of height
	pressure_int : scipy.interpolate.interpolate.interp1d
		Function which interpolates pressure as function of height
	density_int : scipy.interpolate.interpolate.interp1d
		Function which interpolates density as function of height
	sonic_int : scipy.interpolate.interpolate.interp1d
		Function which interpolates sonic speed as function of height
	"""


	def __init__(self, planetID):
		"""
		Initializes the planet object with the planetary constants.
		
		Parameters
		----------
		planetID : str
			Name of the planetary body, must be all uppercase; 
			Valid entries are: 'VENUS', 'EARTH', 'MARS',
			'JUPITER', 'SATURN', 'TITAN', 'URANUS', 'NEPTUNE'

		"""

		if planetID == 'VENUS':

			self.ID     = 'VENUS'      
			self.RP     = 6051.8000E3  
			self.OMEGA  = -2.99237E-7  
			self.GM     = 3.248599E14  
			self.rho0   = 64.790       
			self.CPCV   = 1.289        
			self.J2     = 4.458E-6     
			self.J3     = 0.000000    
			self.h_thres= 180000.0     
			self.h_skip = 180000.0     
			self.h_trap = 10000.0
			self.h_low  = 60.0E3      

		elif planetID == 'EARTH':

			self.ID     = 'EARTH'      
			self.RP     = 6371.0000E3  
			self.OMEGA  = 7.272205E-5  
			self.GM     = 3.986004E14   
			self.rho0   = 1.2250       
			self.CPCV   = 1.4          
			self.J2     = 1082.6E-6    
			self.J3     = -2.532E-6    
			self.h_thres= 120.0E3      
			self.h_skip = 120.0E3      
			self.h_trap = 10.0E3
			self.h_low  = 50.0E3       

		elif planetID == 'MARS':

			self.ID     = 'MARS'       
			self.RP     = 3389.5000E3  
			self.OMEGA  = 7.088253E-5  
			self.GM     = 4.282837E13   
			self.rho0   = 0.0200       
			self.CPCV   = 1.289        
			self.J2     = 1960.45E-6   
			self.J3     = 31.5E-6      
			self.h_thres= 120.0E3      
			self.h_skip = 120.0E3      
			self.h_trap = 10.0E3 
			self.h_low  = 50.0E3

		elif planetID == 'JUPITER':

			self.ID     = 'JUPITER'      
			self.RP     = 69911.0E3      
			self.OMEGA  = 1.758518E-04   
			self.GM     = 1.26686534E17   
			self.rho0   = 0.16288        
			self.CPCV   = 1.4348         
			self.J2     = 14736E-6      
			self.J3     = 0.0            
			self.h_thres= 1000.0E3     
			self.h_skip = 1000.0E3     
			self.h_trap = 50.0E3 

		elif planetID == 'SATURN':
			self.ID     = 'SATURN'      
			self.RP     = 58232.0E3     
			self.OMEGA  = 1.6379E-04   
			self.GM     = 3.7931187E16  
			self.rho0   = 0.19847      
			self.CPCV   = 1.4348       
			self.J2     = 16298E-6     
			self.J3     = 0.0          
			self.h_thres= 1000.0E3     
			self.h_skip = 1000.0E3     
			self.h_trap = 50.0E3      

		elif planetID == 'TITAN':

			self.ID     = 'TITAN'       
			self.RP     = 2575.0000E3   
			self.OMEGA  = 4.5451280E-6  
			self.GM     = 8.9780000E12  
			self.rho0   = 5.43500       
			self.CPCV   = 1.400         
			self.J2     = 31.808E-6     
			self.J3     = -1.880E-6     
			self.h_thres= 1000.0E3      
			self.h_skip = 1000.0E3      
			self.h_trap = 30.0E3
			self.h_low  = 300.0E3


		elif planetID == 'URANUS':

			self.ID     = 'URANUS'      
			self.RP     = 25559.0E3     
			self.OMEGA  = -1.01237E-4   
			self.GM     = 5.793939E15   
			self.rho0   = 0.3788        
			self.CPCV   = 1.450         
			self.J2     = 3343.3E-6     
			self.J3     = 0.000000      
			self.h_thres= 1500.0E3      
			self.h_skip = 1500.0E3      
			self.h_trap = 50.0E3
			self.h_low  = 100.0E3        

		elif planetID == 'NEPTUNE':

			self.ID     = 'NEPTUNE'     
			self.RP     = 24622.000E3   
			self.OMEGA  = 1.083385E-4   
			self.GM     = 6.8365299E15   
			self.rho0   = 0.44021       
			self.CPCV   = 1.450         
			self.J2     = 3411.0E-6     
			self.J3     = 0.000000      
			self.h_thres= 1000.0E3      
			self.h_skip = 1000.0E3      
			self.h_trap = 10.0E3
			self.h_low  = 100.0E3        

		else:
			print(" >>> ERR : Invalid planet identifier provided.")
			print("Valid entries are: VENUS, EARTH, MARS, \
			JUPITER, SATURN, TITAN, URANUS, NEPTUNE")

		# compute reference values
		self.Vref      = np.sqrt(self.GM/self.RP)     
		self.tau       = self.RP / self.Vref          
		self.OMEGAbar  = self.OMEGA*self.tau          
		self.EARTHG    = 9.80665                      

	def loadAtmosphereModel(self, datfile, heightCol, tempCol, presCol, \
		densCol, intType='cubic', heightInKmFlag=False):
		"""
		Load atmospheric model from a look up table with 
		height, temperature, pressure, and density
		
		Parameters
		----------
		datfile : str
			file containing atmospheric lookup table
		heightCol : int
			column number of height values, assumes unit = meters 
			(first column = 0, second column = 1, etc.)
		presCol : int
			column number of pressure values, assumes unit = Pascals 
			(first column = 0, second column = 1, etc.)
		densCol : int
			column number of density values, assumes unit = kg/m3 
			(first column = 0, second column = 1, etc.)
		intType : str, optional
			interpolation type: 'linear', 'quadratic' or 'cubic'
			defaults to 'cubic'
		heightInKmFlag : bool, optional
			optional, set this to True if heightCol has units of km, 
			False by default
		"""
	
		self.ATM          = np.loadtxt(datfile) 

		if heightInKmFlag == True:
			# convert heightCol from km to meters
			self.ATM_height   = self.ATM[:,heightCol]*1E3    
		else:
			self.ATM_height   = self.ATM[:,heightCol]  

		self.ATM_temp     = self.ATM[:,tempCol]          
		self.ATM_pressure = self.ATM[:,presCol]          
		self.ATM_density  = self.ATM[:,densCol]          

		# derive speed of sound profile from pressure, density 
		# and specific heat ratio
		self.ATM_sonic    = np.sqrt(self.CPCV*self.ATM_pressure/self.ATM_density)
		
		# create interpolating functions using scipy.interpolate.interp1d

		
		# fill_value is the value returned by the interpolating function if 
		# input arguments fall outside available data range.
		# fill_value = 0.0 for temp_int, pressure_int, density_int

		# bounds_error=False indicates the function will not return an error 
		# if input arguments fall outside available data range.

		# The fill_value and bounds_error arguments are used due to the fact that 
		# while propogating trajectories, the vehicle
		# might go above the altitude for which atmospheric data is available, or 
		# go below the surface where at atmpospheric data is available.

		self.temp_int      = interp1d(self.ATM_height, self.ATM_temp    ,\
		                     kind=intType, fill_value=0.0, bounds_error=False)
		self.pressure_int  = interp1d(self.ATM_height, self.ATM_pressure, \
			                 kind=intType, fill_value=0.0, bounds_error=False)
		self.density_int   = interp1d(self.ATM_height, self.ATM_density , \
			                 kind=intType, fill_value=0.0, bounds_error=False)
		self.sonic_int     = interp1d(self.ATM_height, self.ATM_sonic   ,\
		                     kind=intType, fill_value=1E20, bounds_error=False)


	def density(self, h):
		"""
		Returns atmospheric density, scalar value, 
		at altitude h (in meters)

		
		Parameters
		----------
		h : float
			altitude in meters

		Returns
		----------
		ans : float
			atmospheric density at height h
		"""


		if h>=0 and h<=self.h_thres:
		# if altitude is within available data range, return 
		# density data from interpolating function density_int()
			return np.float(self.density_int(h))

		elif h>self.h_thres:
			# if altitude is above atmospheric 
			# cut off altitude, return density=0
			return 0

		elif h<0:
			# if altitude is below 0, return the reference 
			# density at the surface the trajectory will be cut off at
			# the surface / trap in altitude during post-processing 
			# rho0 is provided so that the solver has some numerical 
			# density value to work with even if the
			# trajectory goes below the surface during propogation
			return self.rho0


	def tempvectorized(self, h):
		"""
		Returns atmospheric temperature, vector
		at altitudes array h[:] in meters

		
		Parameters
		----------
		h : numpy.ndarray
			altitude h[:] at which atmospheric temperature is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric temperature at altitudes h[:], K
		"""		
		ans    = np.zeros(len(h))
		ans[:] = self.temp_int(h[:])
		
		return ans

	def presvectorized(self, h):
		"""
		Returns atmospheric pressure, vector
		at altitudes array h[:] in meters

		Parameters
		----------
		h : numpy.ndarray
			altitude h[:] at which atmospheric pressure is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric pressure at altitudes h[:], K
		"""		
		ans    = np.zeros(len(h))
		ans[:] = self.pressure_int(h[:])
		
		return ans

	def densityvectorized(self, h):
		"""
		Returns atmospheric density, vector
		at altitudes array h[:] in meters

		Parameters
		----------
		h : numpy.ndarray
			altitude h[:] at which atmospheric density is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric density at altitudes h[:], K
		"""		

		ans    = np.zeros(len(h))
		ans[:] = self.density_int(h[:])
		
		return ans

	def avectorized(self, h):
		"""
		Returns atmospheric sonic speed, vector
		at altitudes array h[:] in meters

		Parameters
		----------
		h : numpy.ndarray
			altitude h[:] at which sonic speed is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the sonic speed at altitudes h[:], K
		"""		

		ans    = np.zeros(len(h))
		ans[:] = self.sonic_int(h[:])
		
		return ans

	def rho(self, r, theta, phi):
		"""
		Returns atmospheric density rho, scalar, as a function
		of radial distance from the target planet center r
		as well as longitude theta and latitude phi
		
		
		Parameters
		----------
		r : float
			radial distance r measured from the planet center
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		
		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric density at (r,theta,phi)
		"""		
		h = r - self.RP       # compute altitude from radial distance
		ans = self.density(h) # compute density
		
		return ans

	def rhovectorized(self, r):
		"""
		Returns atmospheric density, vector
		at radial distance array r[:] in meters

		Parameters
		----------
		r : numpy.ndarray
			radial distance r[:] at which density is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric density at radial distance r[:]
		"""		
		h      = np.zeros(len(r))
		ans    = np.zeros(len(r))
		RP_vec = np.ones(len(r))*self.RP
		h[:]   = r[:] - RP_vec[:]
		ans[:] = self.density_int(h[:])

		return ans


	def pressurevectorized(self, r):
		"""
		Returns atmospheric pressure, vector
		at radial distance array r[:] in meters

		Parameters
		----------
		r : numpy.ndarray
			radial distance r[:] at which pressure is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric pressure at radial distance r[:]
		"""		
		h      = np.zeros(len(r))
		ans    = np.zeros(len(r))
		RP_vec = np.ones(len(r))*self.RP
		h[:]   = r[:] - RP_vec[:]
		ans[:] = self.pressure_int(h[:])
		return ans



	def temperaturevectorized(self, r):
		"""
		Returns atmospheric temperature, vector
		at radial distance array r[:] in meters

		Parameters
		----------
		r : numpy.ndarray
			radial distance r[:] at which temperature is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric temperature at radial distance r[:]
		"""		
		h      = np.zeros(len(r))
		ans    = np.zeros(len(r))
		RP_vec = np.ones(len(r))*self.RP
		h[:]   = r[:] - RP_vec[:]
		ans[:] = self.temp_int(h[:])
		return ans


	def sonicvectorized(self, r):
		"""
		Returns atmospheric sonic speed, vector
		at radial distance array r[:] in meters

		Parameters
		----------
		r : numpy.ndarray
			radial distance r[:] at which sonic speed is desired

		Returns
		----------
		ans : numpy.ndarray
			returns the atmospheric speed at radial distance r[:]
		"""
		h      = np.zeros(len(r))
		ans    = np.zeros(len(r))
		RP_vec = np.ones(len(r))*self.RP
		h[:]   = r[:] - RP_vec[:]
		ans[:] = self.sonic_int(h[:])
		return ans

	def rbar(self, r):
		"""
		Returns non-dimensional rbar=r/RP
		
		Parameters
		----------
		r : float
			radial distance in meters

		Returns
		----------
		ans : float
			non-dimensional rbar
		"""
		ans = r/self.RP
		return ans

	def rho2(self, rbar, theta, phi):
		"""
		Returns atmospheric density rho, scalar, as a function
		of non-dimensional radial distance rbar, longitude theta, 
		and latitude phi
		
		Parameters
		----------
		rbar : float
			nondimensional radial distance rbar
			measured from the planet center
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		
		Returns
		----------
		ans : float
			returns the atmospheric density at (rbar,theta,phi)
		"""		
		r = rbar*self.RP
		ans = self.rho(r,theta,phi)
		return ans


	def rhobar(self, rbar, theta, phi):
		"""
		Returns non-dimensional density rhobar = rho / rho0
		as a function of non-dimensional radial distance rbar, 
		longitude theta, and latitude phi
		
		Parameters
		----------
		rbar : float
			nondimensional radial distance rbar
			measured from the planet center
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		
		Returns
		----------
		ans : float
			non-dimensional density at (rbar,theta,phi)
		"""		
		ans = self.rho2(rbar,theta,phi)/self.rho0
		return ans

	def checkAtmProfiles(self, h0 = 0.0, dh = 1000.0):
		"""
		Function to check the loaded atmospheric profile data.
		Plots temperature, pressure, density and sonic speed
		as function of altitude.

		Parameters
		----------
		h0 : float, optional
			lower limit of altitude, defaults to 0.0
		dh : float, optional
			height interval
		
		Returns
		----------
		A plot showing the atmospheric profiles loaded
		from the lookup tables
		"""
		h_array = np.linspace(h0,self.h_thres,int(self.h_thres/dh))

		# compute profiles of T, P, rho, a using interpolated functions
		# vectorized functions are more efficient for this kind of computation.
		
		T_array = self.tempvectorized(h_array)
		P_array = self.presvectorized(h_array)
		r_array = self.densityvectorized(h_array)
		a_array = self.avectorized(h_array)

		
		fig = plt.figure()
		fig.set_size_inches([6.5, 6.5])
		rcParams['font.family'] = 'sans-serif'
		rcParams['font.sans-serif'] = ['DejaVu Sans']
	
	

		plt.subplot(2,2,1)
		plt.plot(T_array,h_array*1E-3,'r-',linewidth=2.0)
		plt.xlabel("Temperature, K",fontsize=12)
		plt.ylabel("Altitude, km",fontsize=12)
		plt.xticks(fontsize=12)
		plt.yticks(fontsize=12)
		plt.grid('on',linestyle='-', linewidth=0.2)
		
		plt.subplot(2,2,2)
		plt.plot(P_array*1E-3,h_array*1E-3,'r-',linewidth=2.0)
		plt.xlabel("Pressure, kPa",fontsize=12)
		plt.ylabel("Altitude, km",fontsize=12)
		plt.xscale('log')
		plt.xticks(fontsize=12)
		plt.yticks(fontsize=12)
		plt.grid('on',linestyle='-', linewidth=0.2)

		plt.subplot(2,2,3)
		plt.plot(r_array,h_array*1E-3,'r-',linewidth=2.0)
		plt.xlabel("Density, kg/m3",fontsize=12)
		plt.ylabel("Altitude, km",fontsize=12)
		plt.xscale('log')
		plt.xticks(fontsize=12)
		plt.yticks(fontsize=12)
		plt.grid('on',linestyle='-', linewidth=0.2)

		plt.subplot(2,2,4)
		plt.plot(a_array,h_array*1E-3,'r-',linewidth=2.0)
		plt.xlabel("Speed of Sound, m/s",fontsize=12)
		plt.ylabel("Altitude, km",fontsize=12)
		plt.xticks(fontsize=12)
		plt.yticks(fontsize=12)
		plt.grid('on',linestyle='-', linewidth=0.2)

		ax = plt.gca()
		ax.tick_params(direction='in')
		ax.yaxis.set_ticks_position('both')
		ax.xaxis.set_ticks_position('both')

		plt.tight_layout()

		plt.show()

		
	def computeR(self, h):
		"""
		Returns radial distance r, as 
		a function of altitude h, METERS

		Parameters
		----------
		h : float
			altitude in meters

		Returns
		----------
		r : float
			radial distance r=RP+h
		"""
		r = self.RP + h
		return r

	def computeH(self,r):
		"""
		Returns altitude h, as 
		a function of radial distance r, METERS

		Parameters
		----------
		r : float
			radial distance in meters

		Returns
		----------
		h : float
			h = r - RP
		"""
		h = r - self.RP
		return h

	def nonDimState(self,r,theta,phi,v,psi,gamma,drange):
		"""
		Computes non-dimensional trajectory state variables from 
		dimensional trajectory state variables

		Parameters
		----------
		r : float
			radial distance in meters
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		v : float
			planet-relative speed, m/s
		psi : float
			heading angle, radians
		gamma : float
			planet-relative flight-path angle, radians
		drange : float
			downrange distance measured from entry-interface

		Returns
		----------
		rbar : float
			non-dimensional radial distance in meters
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		vbar : float
			non-dimensional planet-relative speed, m/s
		psi : float
			heading angle, radians
		gamma : float
			planet-relative flight-path angle, radians
		drangebar : float
			non-dimensional downrange distance measured from 
			entry-interface
		"""
		rbar       = r / self.RP           # Non-dimensional entry radius
		vbar       = v / self.Vref         # Non-dimensional entry velocity
		drangebar  = drange / self.RP      # Non-dimensional entry downrange

		return rbar,theta,phi,vbar,psi,gamma,drangebar

	def dimensionalize(self,tbar,rbar,theta,phi,vbar,psi,gamma,drangebar):
		"""
		Computes dimensional trajectory state variables from 
		non-dimensional trajectory state variables

		Parameters
		----------
		rbar : float
			non-dimensional radial distance in meters
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		vbar : float
			non-dimensional planet-relative speed, m/s
		psi : float
			heading angle, radians
		gamma : float
			planet-relative flight-path angle, radians
		drangebar : float
			non-dimensional downrange distance measured from 
			entry-interface

		Returns
		----------
		r : float
			radial distance in meters
		theta : float
			longitude theta(RADIANS), theta in [-PI,PI]	
		phi : float	
			latitude phi (RADIANS), phi in (-PI/2, PI/2)
		v : float
			planet-relative speed, m/s
		psi : float
			heading angle, radians
		gamma : float
			planet-relative flight-path angle, radians
		drange : float
			downrange distance measured from entry-interface

		"""
		
		t      = self.tau*tbar
		r      = rbar*self.RP
		v      = vbar*self.Vref 
		drange = drangebar*self.RP

		return t,r,theta,phi,v,psi,gamma,drange

	def scaleHeight(self, h, density_int):
		"""
		Returns the scale height as a function of altitude 
		for given density profile 
		
		Parameters
		----------
		h : float
			altitude at which scale height is desired
		density_int  : scipy.interpolate.interpolate.interp1d
			density interpolation function
		--
		Returns
		--
		ans : float
			scale height, meters
		"""

		# create and store an array of heights from 0 to h_skip at 
		# every 1 km
		h_array  = np.linspace(0,self.h_skip,int(self.h_skip/1000.0))
		# compute the density at these altitudes using the
		# vectorized density function
		d_array  = self.densityvectorized(h_array)

		# Compute the density scale height using the formula in Hamel 2006
		# AIAA. DOI = 10.2514/1.20126
		integ = cumtrapz(d_array[int(h/1000.0):] ,\
				h_array[int(h/1000.0):], initial=0)[-1]
		
		ans   = integ / (self.density(h) - self.density(self.h_skip))

		return ans

	def loadMonteCarloDensityFile2(self, atmfile, heightCol, densLowCol, \
								   densAvgCol, densHighCol, densTotalCol, \
								   heightInKmFlag=False):
		"""
		Loads a Monte Carlo density look up table from GRAM-Model output

		Parameters
		----------
		atmfile : str
			filename, contains mean density profile data
		heightCol : int
			column number of height values, assumes unit = meters 
			(first column = 0, second column = 1, etc.)
		densLowCol : int
			column number of the low mean density 
		densAvgCol : int
			column number of the average mean density
		densHigCol : int
			column number of the high mean desnity
		densTotalCol : int
			column number of the total (=mean + perturb.) density
		heightinKmFlag : bool, optional
			optional, set this to True if heightCol has units of km, 
			False by default

		Returns
		----------
		ATM_height : numpy.ndarray
			height array, m
		ATM_density_low : numpy.ndarray
			low density array, kg/m3
		ATM_density_avg : numpy.ndarray
			avg. density array, kg/m3
		ATM_density_high : numpy.ndarray
			high density array, kg/m3
		ATM_density_pert : numpy.ndarray
			1 sigma mean deviation from avg

		""" 
		
		# load data from textfile using np.loadtxt()
		ATM          = np.loadtxt(atmfile) 
		
		if heightInKmFlag == True:
			# convert heightCol from km to meters
			ATM_height   = ATM[:,heightCol]*1E3    
		else:
			ATM_height   = ATM[:,heightCol]

		# extract data for low, avg, and mean density from file
		ATM_density_low  = ATM[:,densLowCol]  
		ATM_density_avg  = ATM[:,densAvgCol]  
		ATM_density_high = ATM[:,densHighCol] 

		ATM_density_pert = ATM[:,densTotalCol] - \
						   ATM[:,densAvgCol]
		# perturb = (avg + perturb) - avg

		return ATM_height, ATM_density_low, ATM_density_avg,\
			   ATM_density_high, ATM_density_pert

	def pSigmaFunc(self,x):
		"""
		Utility function. Returns 1 if x>=0, 0.0 otherwise
		
		Parameters
		----------
		x : float
			input x

		Returns
		----------
		ans : float
			1 if x>=0, 0.0 otherwise 

		"""
		if x>=0:
			return 1.0

		else:
			return 0.0

	def nSigmaFunc(self,x):
		"""
		Utility function. Returns 1 if x<0, 0.0 otherwise
		
		Parameters
		----------
		x : float
			input x

		Returns
		----------
		ans : float
			1 if x<0, 0.0 otherwise 

		"""
		if x<0:
			return 1.0

		else:
			return 0.0


	def loadAtmosphereModel5(self, ATM_height, ATM_density_low, \
							 ATM_density_avg, ATM_density_high,  \
							 ATM_density_pert, sigmaValue, NPOS, i):
		"""
		Read and create density_int for a single entry from a list 
		of perturbed monte carlo density profiles.
		
		Parameters
		----------
		ATM_height : numpy.ndarray
			height array, m
		ATM_density_low : numpy.ndarray
			low density array, kg/m3
		ATM_density_avg : numpy.ndarray
			avg. density array, kg/m3
		ATM_density_high : numpy.ndarray
			high density array, kg/m3
		ATM_density_pert : numpy.ndarray
			1 sigma mean deviation from avg
		sigmaValue : float
			mean desnity profile sigma deviation value
			(intended as input from a normal distribution
			with mean=0, sigma=1)
		NPOS : int
			NPOS value from GRAM model
			equals the number of positions (altitude) for which
			density value is available in look up table.

		Returns
		----------
		density_int : scipy.interpolate.interpolate.interp1d
			density interpolation function

		"""
		nSigma = ATM_density_avg[int((i-1)*NPOS):int(i*NPOS)]  - \
				 ATM_density_low[int((i-1)*NPOS):int(i*NPOS)]
		pSigma = ATM_density_high[int((i-1)*NPOS):int(i*NPOS)] - \
				 ATM_density_avg[int((i-1)*NPOS):int(i*NPOS)]

		h_array = ATM_height[int((i-1)*NPOS):int(i*NPOS)]

		d_array = ATM_density_avg[int((i-1)*NPOS):int(i*NPOS)] + \
				  pSigma*self.pSigmaFunc(sigmaValue)*sigmaValue + \
				  nSigma*self.nSigmaFunc(sigmaValue)*sigmaValue + \
				  ATM_density_pert[int((i-1)*NPOS):int(i*NPOS)]

		density_int   = interp1d(h_array, d_array  , kind='linear',\
						fill_value=0.0, bounds_error=False)

		return density_int
