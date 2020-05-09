# In this example, we will demonstrate the application of aerocapture for SmallSat missions to Venus.

# We analyze the design proposed by "Austin et al. SmallSat Aerocapture to Enable a New Paradigm of Planetary Missions, IEEE Aerospace Conference, 2019, Big Sky, MT. DOI: 10.1109/AERO.2019.8742220

# Shown below is the aerocapture vehicle design for Venus SmallSat proposed by Austin et al. The design consists of a drag skirt (shown in green), which is jettisoned. The vehicle parameters are 𝑚=68.1
# kg, 𝛽1=38.1 kg/m2, 𝛽2/𝛽1=7.5. The objective is to insert the small satellite (shown in brown) into a 2,000 km x 200 km orbit around Venus. We will use AMAT to perform Monte Carlo analysis to assess aerocapture performance.


from planet import Planet
from vehicle import Vehicle

# Set up the planet and atmosphere model.
planet=Planet("VENUS")    
planet.loadAtmosphereModel('../atmdata/Venus/venus-gram-avg.dat', 0 , 1 ,2, 3)
planet.h_skip = 150000.0 

# Set up the drag modulation vehicle.
vehicle=Vehicle('DMVehicle', 68.2, 38.1, 0.0, 3.1416, 0.0, 0.10, planet)
vehicle.setInitialState(150.0,0.0,0.0,11.0,0.0,-5.50,0.0,0.0)
vehicle.setSolverParams(1E-6)
vehicle.setDragModulationVehicleParams(38.1,7.5)

# Set up the drag modulation entry phase guidance parameters.
vehicle.setDragEntryPhaseParams(6.0, 80.0, 101, -300.0)

# Set the target orbit parameters.
vehicle.setTargetOrbitParams(200.0, 2000.0, 50.0)

# Define the path to atmospheric files to be used for the Monte Carlo simulations.
atmfiles = ['../atmdata/Venus/LAT80S.txt', 
            '../atmdata/Venus/LAT60S.txt',
            '../atmdata/Venus/LAT40S.txt',  
            '../atmdata/Venus/LAT20S.txt',
            '../atmdata/Venus/LAT10S.txt',
            '../atmdata/Venus/LAT80N.txt',  
            '../atmdata/Venus/LAT60N.txt',
            '../atmdata/Venus/LAT40N.txt',
            '../atmdata/Venus/LAT20N.txt',
            '../atmdata/Venus/LAT10N.txt', 
]

# Set up the Monte Carlo simulation for drag modulation.
# NPOS = 151, NMONTE = 200
# Target EFPA = -5.40 deg
# EFPA 1-sigma error = +/- 0.033 deg
# Nominal beta_1 = 38.1 kg/m2
# beta_1 1-sigma = 0.0
# guidance time step for entry = 0.1s (Freq. = 10 Hz)
# guidance time step after jettison = 1.0 s
# max. solver time step = 0.1 s
# max. time used by solver = 1200 s

vehicle.setupMonteCarloSimulationD(151, 200, atmfiles,0, 1, 2, 3, 4, True,
                                   -5.40,  0.033, 38.1, 0.0,
                                    0.1, 1.0, 0.1, 1200.0)

vehicle.runMonteCarloD(10, '../data/austin2019/MCB1')		