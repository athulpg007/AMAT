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
date: 31 August 2021
bibliography: paper.bib
---

# Summary
The Aerocapture Mission Analysis Tool (**AMAT**) is a free and open-source Python package for rapid conceptual design of aerocapture and atmospheric Entry, Descent, and Landing (EDL) missions in a Jupyter environment. Compared to conventional propulsive insertion, aerocapture allows interplanetary spacecraft to accomplish a near-propellantless method of orbit insertion at any planetary destination with a significant atmosphere. While aerocapture has been studied for many decades, to our knowledge, there are no publicly available tools for rapid conceptual design of aerocapture missions. AMAT aims to fill this gap by providing scientists and mission planners with an interactive design tool to quickly evaluate aerocapture mission concepts, perform parametric trade space studies, and select baseline mission concepts for higher-fidelity analysis. Atmospheric Entry, Descent, and Landing includes the hypersonic flight regime where the entry vehicle undergoes intense heating and rapid deceleration, followed by supersonic and subsonic flight, terminal descent phase, and final touchdown. AMAT provides capabilites for rapid end-to-end conceptual design of aerocapture and EDL mission concepts at any atmosphere-bearing Solar System destination.

# Statement of Need

Software tools for identification of trajectories and techniques that enhance or enable planetary missions or substantially reduce their cost are of great importance in realizing successful exploration missions [@Squyres2011]. While there have been some aerocapture mission analysis tools developed in the past such as ACAPS [@Leszczynski1998] and HyperPASS [@mcronald2003analysis], these tools are proprietary, outdated, and not publicly available. The NASA Ice Giants Pre-Decadal Mission Study in 2016, which studied mission concepts to Uranus and Neptune in the next decade highlighted the need for a design tool to evaluate aerocapture mission concepts [@Hofstadter2017; @Saikia2021]. A NASA-led study in 2016 to assess the readiness of aerocapture also underlined the need for an integrated aerocapture mission design tool which incorporates both interplanetary trajectory and vehicle design aspects [@Spilker2018]. While several software tools for conceptual design of EDL missions such as PESST [@otero2010planetary], TRAJ [@allen2005trajectory], and SAPE [@samareh2009multidisciplinary] have been developed in the past, these programs are not publicly available. AMAT aims to fill this gap for scientists, engineers, and academic researchers who want to quickly perform aerocapture mission analysis and atmospheric EDL as part of mission concept studies. 


# Rapid Design Capability

AMAT can be used to compute key aerocapture design parameters such as theoretical corridor width (TCW) and stagnation-point heat rate using just a few lines of code. Figure 1 shows an example of undershoot and overshoot trajectories for lift modulation aerocapture at Venus, and the corresponding stagnation-point heat rate computed by using AMAT.

![](https://i.imgur.com/3XPh6JY.png)
**Figure 1.** An example of a Venus aerocapture vehicle trajectory and the stagnation-point heating profile computed by using AMAT. Figure based on [@Craig2005].

AMAT can be used to create **aerocapture feasibility charts**, a graphical method to visualize the mission design trade space considering both interplanetary and vehicle design aspects [@Lu2018Titan]. Aerocapture feasibility charts help the mission designer assess the feasible range of vehicle lift-to-drag ratio ($L/D$) or ballistic-coefficient ratio ($\beta_2/\beta_1$) for lift and drag modulation respectively, as well as the feasible range of interplanetary arrival $V_{\infty}$ considering corridor width, deceleration, peak-heat rate, and total heat load. Figure 2 shows an example feasibility chart for lift modulation aerocapture at Neptune created by using AMAT.

![](https://i.imgur.com/BNINxh4.png)
**Figure 2.** Interplanetary trajectory trade space (left, generated using STOUR code) and aerocapture feasibility chart for Neptune (right, generated using AMAT). Figure based on the mission design presented in [@Saikia2021; @Girija2020b].  

AMAT can also be used to quickly set up and compute single-event jettison drag modulation aerocapture corridor bounds, and propagate guided trajectories. Figure 3 shows an example of trajectories for a drag modulation system at Mars computed by using AMAT.

![](https://i.imgur.com/YlMk6Th.png)
**Figure 3.** Altitude-velocity profiles and deceleration profiles for a drag modulation aerocapture system at Mars. Solid and dashed lines correspond to a 450 km circular and 1-sol target orbit respectively. Figure based on the flight system presented in [@Werner2019].  

AMAT can be used to perform Monte Carlo simulations to assess user-defined guidance schemes and system performance with a vehicle design and interplanetary trajectory considering navigation, atmospheric, and aerodynamic uncertainties as shown in Figure 4.

![](https://i.imgur.com/Jefki5T.png)
**Figure 4.** Examples of Monte Carlo simulation results showing post-aerocapture orbit parameters for a drag modulation system at Venus (left) and a lift modulation system at Neptune (right) computed by using AMAT. Based on [@Girija2020b].

AMAT can be used to generate EDL **carpet plots** which are commonly used to assess the trade space for preliminary entry system and mission design as shown in Figure 5.

![](https://i.imgur.com/uDxfzsS.png)
**Figure 5.** Examples of carpet plots for Venus entry (left), and Titan entry (right) created by using AMAT. Based on [@scott2018preliminary].

# AMAT Modules

The key functionality of the AMAT package is organized into three modules. These modules and their descriptions are shown in Table \ref{modules_table}. 

Table: Modules of AMAT \label{modules_table}

| Module        | Description                                                         |
| ------------- | --------------------------------------------------------------------|
| AMAT.planet   | Stores planetary constants, atmosphere models, entry interface etc. |
| AMAT.vehicle  | Stores vehicle parameters, guidance scheme, propogate trajectory    |
| AMAT.launcher | Stores Earth escape performance for a list of launch vehicles       |

# Documentation and Example Jupyter Notebooks

AMAT documentation along with a number of example Jupyter notebooks are available at https://amat.readthedocs.io. AMAT can be installed from the [Python Package Index](https://pypi.org/project/AMAT/) (`pip install AMAT`).

# Limitations

AMAT is intended to be used as a low-to-mid fidelity preliminary analysis tool to perform trade studies and select a baseline concept, which can be analyzed in further detail using high-fidelity tools such as DSENDS [@balaram2002dsends] or POST [@brauer1977capabilities].

AMAT uses publicly available empirical relations to compute the stagnation-point aerothermal environment. While this is sufficient for preliminary mission analysis, detailed studies require propietary higher-fidelity CFD tools such as LAURA [@mazaheri2013laura], DPLR and NEQAIR. While AMAT computes the stagnation-point total load which can be used to roughly estimate the thermal protection system (TPS) mass fraction [@Laub2004], there is no functionality to provide an accurate TPS mass estimate which is prerequisite when comparing an aerocapture system with propulsive insertion, especially for outer planet missions. Incorporation of improved TPS sizing models and addition of interactive visualization capabilities using Blender is planned for future work. 

# Acknowledgements

AMAT was developed at the Advanced Astrodynamics Concepts (AAC) group at Purdue University. Parts of the source code were originally developed in support of contracts between AAC and the Jet Propulsion Laboratory for various aerocapture mission studies. 

# References


