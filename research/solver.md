---
title: Multiphysics Solvers
layout: default
---

# Multiphysics Modeling and Solver Development

I have developed multiphysics solvers capable of simulating complex cardiovascular behavior. This includes integrating mathematical models of fluid dynamics and vascular solid mechanics into **finite-element** frameworks and designing novel **numerical methods** to improve accuracy and computational efficiency. The resulting solvers have been used for [translational research](/research/translation) and are available as open-source tools for the scientific community.  

### Research Pathway

**Computational fluid dynamics** and **solid mechanics** have provided myriad insights into cardiovasculor behavior. However, most fluid-strucutre solvers focus on solving such equations at an instantaneous time and are not capable of simulating the growth and remodeling of soft-tissue structures in response to experianced forces. As growth and remodeling of cardiovascular structures inevitably changes the hemodynamic forces, this is a tightly coupled problem, perticularly in cases where complex hemodynamic fields or rapid growth and remodeling are expected.

The **constrained mixture theory** of vascular growth and remodeling has become a highly useful framework for modeling cardiovascular evolution as it allows for consideration of individual constituent families that may independently turnover depending on biomechanical stimuli. However, its relative complexity and  computational expensive have previously made it prohibitive to use in a research and clinical context. 

To address these limitations, I developed the first finite-element **fluid-structure-growth solver** that explicitely solves the tightly coupled growth and remodeling equations, the Navier-Stokes equations that govern cardiovascular flow, and the linear momentum balance equations that govern the structural behavior of the vascular wall. This was a major advancement in the field of mechanobiological simulations, and is currently implemented in the open-source solver *SimVascular* as a tool available to the scientific community.

After, I continued my work in multiphysics solvers and numerical methods by assisting with the development of additional frameworks that included electrophysiology coupling as well as more advanced implementations of fluid-structure-growth theory.

### Selected Publications

- **A Fluid–Solid-Growth Solver for Cardiovascular Modeling**  
  **Schwarz, E. L.**, Pfaller, M. R., Szafron, J. M., Latorre, M., Lindsey, S. E., Breuer, C. K., Humphrey, J. D., & Marsden, A. L. (2023)  
  *Computer methods in applied mechanics and engineering*  
  [Link](https://www.sciencedirect.com/science/article/pii/S004578252300436X)

- **Beyond CFD: Emerging Methodologies for Predictive Simulation in Cardiovascular Health and Disease**  
  **Schwarz, E. L.**, Pegolotti, L., Pfaller, M. R., & Marsden, A. L. (2023)  
  [Link](https://pubs.aip.org/aip/bpr/article/4/1/011301/2879057)

- **Multiphysics Simulations of a Bioprinted Pulsatile Fontan Conduit**  
  Hu, Z., Herrmann, J. E., **Schwarz, E. L.**, Gerosa, F. M., Emuna, N., Humphrey, J. D., Feinberg, A. W., Hsia, T., Skylar-Scott, M. A., & Marsden, A. L. (2025)  
  *Journal of Biomechanical Engineering*  
  [Link](https://asmedigitalcollection.asme.org/biomechanical/article-abstract/147/7/071001/1214591)

- **FSGe: A Fast and Strongly-coupled 3D Fluid–Solid-Growth Interaction Method**  
  Pfaller, M. R., Latorre, M., **Schwarz, E. L.**, Gerosa, F. M., Szafron, J. M., Humphrey, J. D., & Marsden, A. L. (2024)  
  *Computer Methods in Applied Mechanics and Engineering*  
  [Link](https://www.sciencedirect.com/science/article/pii/S0045782524005152)



