---
title: "AMAT: A Python package for rapid conceptual design of aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a Jupyter environment"
tags:
    - Python
    - aerocapture
    - atmospheric entry
    - mission design
    - planetary probe
authors:
    - name: Athul P. Girija
      orcid: 0000-0002-9326-3293
      affiliation: "1"
    - name: Sarag J. Saikia
      affiliation: "1"
    - name: James M. Longuski
      affiliation: "1"
    - name: James A. Cutts
      affiliation: "2"
affiliations:
    - name: School of Aeronautics and Astronautics, Purdue University, West Lafayette, IN 47907, United States
      index: 1
    - name: Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA 91109, United States
      index: 2
date: 01 August 2021
bibliography: paper.bib
---

# Summary
The Aerocapture Mission Analysis Tool (**AMAT**) is a free and open-source Python package for rapid conceptual design of aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a Jupyter environment. Compared to conventional propulsive insertion, aerocapture allows interplanetary spacecraft to accomplish a near-propellantless method of orbit insertion at any planetary destination with a signficant atmosphere. While aerocapture has been studied for many decades, to our knowledge, there are no publicly available tools for rapid conceptual design of aerocapture missions. AMAT aims to fill this gap by providing scientists and mission planners an interactive design tool to quickly evaluate aerocapture mission concepts, perform parametric trade space studies, and select a baseline mission concept for higher-fidelity analysis. Atmospheric Entry, Descent, and Landing (EDL) includes the hypersonic flight regime where the entry vehicle undergoes intense heating and rapid deceleration, followed by supersonic and subsonic flight, terminal descent phase, and final touchdown. AMAT comes with a suite of tools for rapid end-to-end conceptual design of aerocapture and EDL mission concepts at any atmosphere-bearing Solar System destination.

# Statement of Need

Software tools for identification of trajectories and techniqes that enhance or enable planetary missions or substantially reduce their cost is of great importance in realizing succesful exploration missions [@Squyres2011]. While there have been some aerocapture mission analysis tools developed in the past such as ACAPS [@Leszczynski1998] and HyperPASS [@mcronald2003analysis], these tools are propreitary, and not accessible to the general public. The NASA Ice Giants Pre-Decadal Mission Study in 2016, which studied mission concepts to Uranus and Neptune in the next decade highlighted the need for a design tool to evaluate aerocapture mission concepts [@Hofstadter2017]. A NASA-led study in 2016 to assess the readiness of aerocapture also underlined the need for an integrated aerocapture mission design tool which incorporated both interplanetary trajectory and vehicle design aspects [@Spilker2018]. While several software tools for conceptual design of EDL missions such as PESST [@otero2010planetary], TRAJ [@allen2005trajectory], and SAPE [@samareh2009multidisciplinary] have been developed in the past, these programs are not publicly available.  AMAT aims to fill this gap for scientists, engineers, and academic researchers who want to quickly perform aerocapture mission analysis and atmospheric EDL as part of mission concept studies. 


# Rapid Design Capability

AMAT can be used to compute aerocapture trajectories as well as key design parameters such as theoretical corridor width (TCW) and stagnation-point heat rate using just a few lines of code. Figure 1 shows the undershoot and overshoot trajectories for lift modulation aerocapture at Venus, and the stagnation-point heat rates computed using AMAT.

![](https://i.imgur.com/3XPh6JY.png)
**Figure 1.** Venus aerocapture vehicle trajectory and stagnation-point heat rate computed using AMAT. Figure based on the parameters listed in [@Craig2005].

AMAT can be used to create **aerocapture feasibility charts**, which is a graphical method to visualize the mission design trade space considering both interplanetary and vehicle design aspects [@Lu2018Titan; @Girija2020Venus; @Girija2020Neptune]. Aerocapture feasibility charts help the mission designer assess the feasible range of vehicle lift-to-drag ratio ($L/D$) or ballistic-coefficient ratio ($\beta_2/\beta_1$) for lift and drag modulation respectively, as well as the feasible range of interplanetary arrival $V_{\infty}$ considering corridor width, decleration, peak-heat rate, and total heat load. Figure 2 shows an example feasibility chart for lift modulation aerocapture at Neptune created using AMAT.

![](https://i.imgur.com/BNINxh4.png)
**Figure 2.** Lift modulation aerocapture feasibility charts for Neptune. Figure based on the mission design presented in [@Girija2020Neptune].  

AMAT can also be used to quickly set up and compute single-event jettison drag modulation aerocapture corridor bounds, and propogate guided trajectories. Figure 3 shows example trajectories for a drag modulation system at Mars computed using AMAT.

![](https://i.imgur.com/YlMk6Th.png)
**Figure 3.** Altitude-velocity profiles and deceleration profiles for a drag modulation aerocapture system at Mars. Solid and dashed lines correspond to a 450 km circular and 1-sol target orbit respectively. Figure based on the flight system presented in [@Werner2019].  

AMAT can be used to perform Monte Carlo simulations to assess guidance scheme and flight system performance with a baseline vehicle design and interplanetary trajectory considering navigation, atmospheric, and aerodynamic uncertainties.

![](https://i.imgur.com/Jefki5T.png)
**Figure 4.** Monte Carlo simulation results showing post-aerocapture orbit dispersion (before the periapsis-raise maneuever) for a drag modulation system at Venus (left) and a lift modulation system at Neptune (right). Based on  [@Girija2020Neptune].

AMAT can be used to generate EDL **carpet plots** which are commonly used to assess the trade space for entry system design considering the limits from deceleration load, peak heat rate, peak stagnation pressure, and total heat load as shown in Figure 5.

![](https://i.imgur.com/uDxfzsS.png)
**Figure 5.** EDL carpet plots for Venus (left), and Titan entry. Based on [@scott2018preliminary].

# AMAT Modules

The key functionality of the AMAT package is organized into three modules.

| Module        | Description                                                         |
| ------------- | --------------------------------------------------------------------|
| AMAT.planet   | Stores planetary constants, atmosphere models, entry interface etc. |
| AMAT.vehicle  | Stores vehicle parameters, guidance scheme, propogate trajectory    |
| AMAT.launcher | Utility to query launch vehicle performance                         |

# Documentation and Example Jupyter Notebooks

AMAT documentation along with a number of example Jupyter notebooks are available at https://amat.readthedocs.io. AMAT is available from the [Python Package Index](https://pypi.org/project/AMAT/).

# Limitations

AMAT is intended to be used as a low-to-mid fidelity preliminary analysis tool to perform trade studies and select a baseline concept, which can be analyzed in further detail using high-fidelity tools such as DSENDS [@balaram2002dsends] or POST [@brauer1977capabilities].

AMAT uses publicly available empirical relations to compute the stagnation-point aerothermal environment. While this is sufficient for preliminary mission analysis, detailed studies require propreitary higher-fidelity CFD tools such as LAURA [@mazaheri2013laura], DPLR and NEQAIR [@hash2007fire]. While AMAT computes the stagnation-point total load which can be used to roughly estimate the TPS mass fraction [@Laub2004], there is no functionality to provide an accurate TPS mass estimate which is important to compare an aerocapture system with propulsive insertion, especially for outer planet missions.

# Acknowledgements

AMAT was developed at the Advanced Astodynamics Concepts (AAC) group at Purdue University. Parts of the source code were originally developed in support of contracts between AAC and the Jet Propulsion Laboratory for various aerocapture mission studies. 

# References


