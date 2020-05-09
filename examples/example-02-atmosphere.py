"""
In this example, you will learn to use add an atmosphere model to planets.

Let us re-use the code from example-01 to create a planet object for Venus.

"""

from AMAT.planet import Planet
planet = Planet("VENUS")

"""
We are now ready to add an atmosphere model to the planet object.

AMAT stores atmospheric data in the form of look up tables located 
in ~root/atmdata. Typically, data is stored in the following format.

#Z(m)	Temp(K)	Pres (Nm2)	rho(kgm3)	a (m/s)
0		735.30	9.209E+06	6.479E+01	428.03
1000	727.70	8.645E+06	6.156E+01	425.46
2000	720.20	8.109E+06	5.845E+01	422.88
3000	712.40	7.601E+06	5.547E+01	420.27
4000	704.60	7.120E+06	5.262E+01	417.63
5000	696.80	6.666E+06	4.987E+01	415.09
.....
.....
"""

# the atmosphere model provided in atmdata/Venus/venus-gram-avg.dat.
# The columns for height, Temp, pressure, density are 0, 1, 2, 3
planet.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)

# Let us now use the checkAtmProfiles function to inspect the atmospheric profiles.
planet.checkAtmProfiles()

# Compute the scale height at the Venusian surface for illustration.
# planet.density_int is the interpolation function created by planet object 
# when atmosphere model is loaded.
planet.scaleHeight(0, planet.density_int)

# Congratulations! 
# Your planet now has an atmosphere model. 
# In the next example, we will compute aerocapture trajectories for a vehicle 
# flying in the Venusian atmosphere.