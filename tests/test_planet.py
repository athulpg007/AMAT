"""
test_planet.py

Tests to check if Planet objects can be created and loaded with
atmospheric profiles.

"""

import unittest

try:
    from AMAT.planet import Planet
except ModuleNotFoundError:
    raise ModuleNotFoundError("Cannot import Planet from AMAT.planet")

class TestPlanet(unittest.TestCase):

	def test_create_planet(self):
		"""
		Test that if a Planet object instances can be created for
		various Solar System destinations
		"""
		planet1 = Planet("VENUS")
		message = "Could not create Planet instance for Venus"
		self.assertIsInstance(planet1, Planet, message)

		planet2 = Planet("EARTH")
		message = "Could not create Planet instance for Earth"
		self.assertIsInstance(planet2, Planet, message)

		planet3 = Planet("MARS")
		message = "Could not create Planet instance for Mars"
		self.assertIsInstance(planet3, Planet, message)

		planet4 = Planet("JUPITER")
		message = "Could not create Planet instance for Jupiter"
		self.assertIsInstance(planet4, Planet, message)

		planet5 = Planet("SATURN")
		message = "Could not create Planet instance for Saturn"
		self.assertIsInstance(planet5, Planet, message)

		planet6 = Planet("TITAN")
		message = "Could not create Planet instance for Saturn"
		self.assertIsInstance(planet6, Planet, message)

		planet7 = Planet("URANUS")
		message = "Could not create Planet instance for URANUS"
		self.assertIsInstance(planet7, Planet, message)
		
		planet8 = Planet("NEPTUNE")
		message = "Could not create Planet instance for Saturn"
		self.assertIsInstance(planet8, Planet, message)

		"""
		check GM values for all planet objects
		"""

		self.assertEqual(planet1.GM, 3.248599E14, msg="Check Venus GM")
		self.assertEqual(planet2.GM, 3.986004E14, msg="Check Earth GM")
		self.assertEqual(planet3.GM, 4.282837E13, msg="Check Mars GM")
		self.assertEqual(planet4.GM, 1.26686534E17, msg="Check Jupiter GM")
		self.assertEqual(planet5.GM, 3.7931187E16, msg="Check Saturn GM")
		self.assertEqual(planet6.GM, 8.9780000E12, msg="Check Titan GM")
		self.assertEqual(planet7.GM, 5.793939E15, msg="Check Uranus GM")
		self.assertEqual(planet8.GM, 6.8365299E15, msg="Check Neptune GM")

		"""
		check h_thres is set to a sufficiently high value for all planets
		"""
		self.assertGreaterEqual(planet1.h_thres, 100.0E3, msg="Venus atm. cut off height likely too low.")
		self.assertGreaterEqual(planet2.h_thres, 100.0E3, msg="Earth atm. cut off height likely too low.")
		self.assertGreaterEqual(planet3.h_thres, 100.0E3, msg="Mars atm. cut off height likely too low.")
		self.assertGreaterEqual(planet4.h_thres, 800.0E3, msg="Jupiter atm. cut off height likely too low.")
		self.assertGreaterEqual(planet5.h_thres, 800.0E3, msg="Saturn atm. cut off height likely too low.")
		self.assertGreaterEqual(planet6.h_thres, 600.0E3, msg="Titan atm. cut off height likely too low.")
		self.assertGreaterEqual(planet7.h_thres, 800.0E3, msg="Uranus atm. cut off height likely too low.")
		self.assertGreaterEqual(planet8.h_thres, 800.0E3, msg="Neptune atm. cut off height likely too low.")

		"""
		check h_thres (atm. cut off) and h_skip agree to within 10 km.
		"""
		self.assertAlmostEqual(planet1.h_thres, planet1.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Venus")
		self.assertAlmostEqual(planet2.h_thres, planet2.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Earth")
		self.assertAlmostEqual(planet3.h_thres, planet3.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Mars")
		self.assertAlmostEqual(planet4.h_thres, planet4.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Jupiter")
		self.assertAlmostEqual(planet5.h_thres, planet5.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Saturn")
		self.assertAlmostEqual(planet6.h_thres, planet6.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Titan")
		self.assertAlmostEqual(planet7.h_thres, planet7.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Uranus")
		self.assertAlmostEqual(planet8.h_thres, planet8.h_skip, delta=10e3, msg="h_thres, h_skip disagree for Neptune")


		"""
		check h_trap (traj. cut-off low-altitude) is set to a sufficiently low value
		"""
		self.assertLessEqual(planet1.h_trap, 40.0E3, msg="Venus trap alt. likely too high.")
		self.assertLessEqual(planet2.h_trap, 40.0E3, msg="Earth trap alt. likely too high.")
		self.assertLessEqual(planet3.h_trap, 60.0E3, msg="Mars trap alt. likely too high.")
		self.assertLessEqual(planet4.h_trap, 100.0E3, msg="Jupiter trap alt. likely too high.")
		self.assertLessEqual(planet5.h_trap, 100.0E3, msg="Saturn trap alt. likely too high.")
		self.assertLessEqual(planet6.h_trap, 100.0E3, msg="Titan trap alt. likely too high.")
		self.assertLessEqual(planet7.h_trap, 100.0E3, msg="Uranus trap alt. likely too high.")
		self.assertLessEqual(planet8.h_trap, 100.0E3, msg="Neptune trap alt. likely too high.")

	def test_load_atm_models(self):
		"""
		Test atmosphere models can be loaded for various planetary bodies.
		"""

		# create planet objects
		planet1 = Planet("VENUS")
		planet2 = Planet("EARTH")
		planet3 = Planet("MARS")
		planet4 = Planet("JUPITER")
		planet5 = Planet("SATURN")
		planet6 = Planet("TITAN")
		planet7 = Planet("URANUS")
		planet8 = Planet("NEPTUNE")

		# load atmosphere models
		try:
			planet1.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet2.loadAtmosphereModel('../atmdata/Earth/earth-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet3.loadAtmosphereModel('../atmdata/Mars/mars-gram-avg.dat', 0 , 1 ,2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet4.loadAtmosphereModel('../atmdata/Jupiter/jupiter-galileo-asi.dat', 0 , 1 , 2, 3, heightInKmFlag=True)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet5.loadAtmosphereModel('../atmdata/Saturn/saturn-nominal.dat', 0 , 1 , 2, 3, heightInKmFlag=True)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet6.loadAtmosphereModel('../atmdata/Titan/titan-gram-avg.dat', 0 , 1 , 2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet7.loadAtmosphereModel('../atmdata/Uranus/uranus-ames.dat', 0 , 1 , 2, 3)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")

		try:
			planet8.loadAtmosphereModel('../atmdata/Neptune/neptune-gram-avg.dat', 0 , 7 ,6, 5 , heightInKmFlag=True)
		except OSError:
			raise OSError("File not found. Check file path/name, and make sure file is present.")


		# check loaded atmosphere data has equal number of rows for 
		# height, temperature, pressure and density
		self.assertEqual(len(planet1.ATM_height),len(planet1.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet1.ATM_height),len(planet1.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet1.ATM_height),len(planet1.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet2.ATM_height),len(planet2.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet2.ATM_height),len(planet2.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet2.ATM_height),len(planet2.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet3.ATM_height),len(planet3.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet3.ATM_height),len(planet3.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet3.ATM_height),len(planet3.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet4.ATM_height),len(planet4.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet4.ATM_height),len(planet4.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet4.ATM_height),len(planet4.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet5.ATM_height),len(planet5.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet5.ATM_height),len(planet5.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet5.ATM_height),len(planet5.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet6.ATM_height),len(planet6.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet6.ATM_height),len(planet6.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet6.ATM_height),len(planet6.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet7.ATM_height),len(planet7.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet7.ATM_height),len(planet7.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet7.ATM_height),len(planet7.ATM_density), msg="Number of rows disagree in atm. data file" )

		self.assertEqual(len(planet8.ATM_height),len(planet8.ATM_temp), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet8.ATM_height),len(planet8.ATM_pressure), msg="Number of rows disagree in atm. data file" )
		self.assertEqual(len(planet8.ATM_height),len(planet8.ATM_density), msg="Number of rows disagree in atm. data file" )

		# check h_thres is set to a lower value (<=) than the maximum height for 
		# which data is available

		self.assertLessEqual(planet1.h_thres, max(planet1.ATM_height), msg="h_thres > max. height from atmospheric table for Venus.")
		self.assertLessEqual(planet2.h_thres, max(planet2.ATM_height), msg="h_thres > max. height from atmospheric table for Earth.")
		self.assertLessEqual(planet3.h_thres, max(planet3.ATM_height), msg="h_thres > max. height from atmospheric table for Mars.")
		self.assertLessEqual(planet4.h_thres, max(planet4.ATM_height), msg="h_thres > max. height from atmospheric table for Jupiter.")
		self.assertLessEqual(planet5.h_thres, max(planet5.ATM_height), msg="h_thres > max. height from atmospheric table for Saturn.")
		self.assertLessEqual(planet6.h_thres, max(planet6.ATM_height), msg="h_thres > max. height from atmospheric table for Titan.")
		self.assertLessEqual(planet7.h_thres, max(planet7.ATM_height), msg="h_thres > max. height from atmospheric table for Uranus.")
		self.assertLessEqual(planet8.h_thres, max(planet8.ATM_height), msg="h_thres > max. height from atmospheric table for Neptune.")

		# check some atmospheric data values are correct.

		self.assertAlmostEqual(planet1.density(h=0.0), 64.79, places=1)
		self.assertAlmostEqual(planet2.density(h=0.0), 1.221, places=1)
		self.assertAlmostEqual(planet3.density(h=0.0), 0.01319, places=3)
		self.assertAlmostEqual(planet4.density(h=0.0), 0.16288, places=3)
		self.assertAlmostEqual(planet5.density(h=0.0), 0.18658, places=3)
		self.assertAlmostEqual(planet6.density(h=0.0), 5.43503, places=2)
		self.assertAlmostEqual(planet7.density(h=0.0), 0.37879, places=2)
		self.assertAlmostEqual(planet8.density(h=0.0), 0.44021, places=2)

	
		# 
if __name__ == '__main__':
	unittest.main()
