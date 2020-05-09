"""
In this 'hello world' program, you will learn to use AMAT 
to create a planet object.
"""

# First let us import the Planet class from AMAT
from AMAT.planet import Planet

# Now let us create a planet object which represents Venus.
planet = Planet("VENUS")

# Let us look at the an attribute of the created object. 
# For example let us, print the radius of the planet. 
# A full list of attributes and functions can be obtained using help(planet).
print(planet.RP)

# Congratulations! 
# You have now created a planet object using AMAT. 
# In the next example, we will add an atmosphere model to this planet object.