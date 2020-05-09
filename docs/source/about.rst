About AMAT
===========

Overview
--------

**AMAT** is an open source collection of Python subroutines for mission design and analysis
of aerocapture mission concepts.

AMAT comes with a suite of tools to allow end-to-end conceptual design of aerocapture missions: launch vehicle performance calculator, extensive database of interplanetary trajectories, sample atmosphere models, guidance schemes, and aeroheating models. AMAT supports analysis for Venus, Earth, Mars, Titan, Uranus, and Neptune for both lift and drag modulation techniques.

AMAT has been extensively used in various mission studies at the Advanced Astrodynamics Concepts (AAC) research group at Purdue University in collaboration with the NASA Jet Propulsion Laboratory (JPL). 

History
-------

The lack of a rapid mission design tool for aerocapture mission concepts was identified in 2016 by the NASA Ice Giants Pre-Decadal (IGPD) Study led by JPL. This meant there was no quick way of designing aerocapture mission concepts without resorting to resource-intensive, time-consuming exercises involving various NASA centers with expertise in specific disciplines.  

Graduate researchers at Purdue University were closely involved in the aerocapture studies for the IGPD, and have since then been extending the methods and tools for other atmosphere-bearing Solar System destinations. The focus was on developing an integrated systems engineering framework to allow mission designers to quickly evaluate the feasibility and performance of aerocapture mission concepts. Doctoral students Ye Lu and Athul P. Girija collaborated from 2016--2019 to develop the **aerocapture feasibility charts**, now a commonly used graphical method for aerocapture mission design.

Athul P. Girija further developed the systems framework for rapid conceptual design of aerocapture missions for his doctoral thesis. He conceptualized the developement of a rapid mission design tool which implements the framework to address the gap identified by the IGPD in 2016. AMAT was first publicly released in November 2019, and has since then been maintained by the author. In the spirit of open-code for open-science, AMAT is free and open-source to foster universal access to the knowledge, and allow reproducibility of results by other researchers. Sugestions for improvement and potential contributions are greatly welcome.

Related software
----------------

These are other software tools which offer mission analysis capabilities for aerocapture missions. These offer much higher fidelity, but are also significantly more complex to set up and run  and generally are used for mission concepts in a more advanced stage. Normally, these are usually available only to U.S. government affiliated institutions and contractors.

* `POST2`_: According to NASA Langley Research Center, "The Program to Optimize Simulated Trajectories II (POST2) is a generalized point mass, discrete parameter targeting and optimization program. POST2 provides the capability to target and optimize point mass trajectories for multiple powered or un-powered vehicles near an arbitrary rotating, oblate planet. POST2 has been used successfully to solve a wide variety of atmospheric ascent and entry problems, as well as exo-atmospheric orbital transfer problems."

* `DSENDS`_: According to NASA Jet Propulsion Laboratory, "DSENDS is a high-fidelity spacecraft simulator for Entry, Descent and Landing (EDL) on planetary and small-bodies. DSENDS (Dynamics Simulator for Entry, Descent and Surface landing) is an EDL-specific extension of a JPL multi-mission simulation toolkit Darts/Dshell which is capable of modeling spacecraft dynamics, devices, and subsystems, and is in use by interplanetary and science-craft missions such as Cassini, Galileo, SIM, and Starlight. DSENDS is currently in use by the JPL Mars Science Laboratory project to provide a high-fidelity testbed for the test of precision landing and hazard avoidance functions for future Mars missions. "


.. _POST2: https://post2.larc.nasa.gov/
.. _DSENDS: https://dartslab.jpl.nasa.gov/DSENDS/index.php


Future ideas
------------

Some things I would like to implement in the future:

* Pairing AMAT with Blender and NASA 3D models of planets and spacecraft to produce high resolution renders of aerocapture vehicle trajectories.

* Improved guidance schemes for lift and drag modulation aerocapture.

* Improved support for EDL mission concepts in the areas of precision landing, parachute dynamics, terminal descent and landing phases.


Note from the original author
---------------------------

I am Athul P. Girija, an aerospace engineer with a passion for robotic exploration of our Solar System. When I started working towards my Ph.D. in 2016, I had not heard of the concept of aerocapture. Throughout the course of my Ph.D, I gained a significant amount of knowledge and expertise in the design of aerocapture mission concepts by studying nearly 400+ journal articles, conference papers, and technical reports. This tool is dedicated to all the researchers who worked on aerocapture over nearly six decades, standing on whose shoulders I could see far.