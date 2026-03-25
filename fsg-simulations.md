---
layout: default
title: FSG Simulations
permalink: /fsg-simulations/
---


# Running FSG Simulations

This page explains how to run FSG simulations. There are two necessary components of running FSG simulations:

- **Solver code** (the FEBio-FSG repository)
- **Plugin code** (the FEFSG_Plugin repository)

This is a critical distinction:  
**The plugin must be compiled with this specific fork of the FEBio solver source code.**

---

# 1. Overview

## Prerequisites

**Intel Math Kernel Library (MKL)**

FEBio requires the Intel Math Kernel Library (MKL) in order to utilize the Pardiso linear solver and some of the iterative linear solvers. This library can be downloaded as part of the Intel oneAPI Base Toolkit from [Intel's website](https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit.html). In the absence of MKL, FEBio will default to using the Skyline linear solver. However, the Pardiso solver is significantly faster and more memory-efficient than the Skyline solver, and it is strongly recommended that the Pardiso solver be used.

On Intel's website, follow the specific download instructions for your platform before compiling the FEBio source code.

## Solver Source Code (FEBio-FSG)

The solver source code is the full executable that performs:

- Finite element assembly
- Nonlinear solves
- Time stepping
- Core mechanics infrastructure

It is the engine that actually runs simulations. In this workflow, we use a **custom fork**:

```
yale-humphrey-lab/FEBio-FSG
```

This fork includes modifications that are **not present in the official FEBio release**.  
Your plugin must be built against this exact version to ensure compatibility.

If you compile a plugin against a different FEBio version, it may:
- Fail to load
- Crash at runtime
- Produce incorrect results

---

## Plugin Code (FEFSG_Plugin)

A plugin is a dynamically loaded shared library (`.so`) that extends the solver and is typically used to add new constitutive material models. The plugins do **not** replace solver and does **not** do any actual simulation. It is simply an extra dictionary for the solver to use to look up newly created materials. To reiterate **plugins do not solve any actual code, but need to be used with their solver counterpart**.

---

# 2. Clone the Solver

Move to your home directory:

```bash
cd <my-home>
```

*Note: It is typical to use your home directory to compile source code. Typically, the shortcut for moving to your home directory is `cd ~`.*

Clone the solver repository:

```bash
git clone git@github.com:yale-humphrey-lab/FEBio-FSG.git
```

Alternatively, if SSH is not configured:

```bash
git clone https://github.com/yale-humphrey-lab/FEBio-FSG.git
```

# 3. Build the Solver (CMake-Based Build)

Always build in a clean directory!

```bash
cd <my-home>/FEBio-FSG
mkdir -p build
cd build
```

Configure the project:


```bash
ccmake .. -DCMAKE_C_FLAGS="-fopenmp" -DCMAKE_CXX_FLAGS="-fopenmp" -DUSE_MKL=ON
```

In the ccmake screen, you should see the message **EMPTY CACHE**. Press `c` configure the Makefile. The screen should populate with several flags, beginning with `CMAKE_BUILD_FLAG`, which should be set to `Release`.

You can toggle advanced mode on and off by pressing `t`. You may need to configure other paths manually for additional functionality (e.g., MKL --- ensure that `MKLROOT` is populated with `<my-example-mkl-directory>/opt/intel/oneapi/mkl`).

Press `c` again until it you have the option at the bottom to press `g` to generate the Makefile.

Once configuration is complete, verify that `build` has been populated with new folders (`bin`, `CMakeFiles`, and `lib`) and files (`CMakeCache.txt`, `cmake_install.cmake`, `Makefile`). You can then build the solver using the command:

```bash
make -j
```

*Note: -j enables parallel compilation*

After successful build, the solver executable and libraries will be in:

```bash
<my-home>/FEBio-FSG/build/
```

# 4. Clone the Plugin

Move to your project directory:

```bash
cd <my-project>
git clone https://github.com/yale-humphrey-lab/FEFSG_Plugin.git
cd FEFSG_Plugin
```

# 5. Compile the Plugin

The plugin must link against the exact solver build you compiled earlier.

Example build command:

```bash
g++ -fPIC -shared FEFSG.cpp dllmain.cpp -o FEFSG.so -std=c++11 -I /<my-home>/FEBio-FSG/ -L /<my-home>/FEBio-FSG/build/lib -lfebiomech -lfecore
```

Components explained:

- `g++` - GNU C++ compiler. It translates C++ source code (`.cpp` files) to an executable or shared library.

Flags explained:

- `fPIC` - Position-independent code (required for shared libraries)

- `shared` - Build shared object that can be used by the solver code

- `I` - Include path (solver headers)

- `L` - Library path (solver build libraries)

- `l` - Link against solver libraries

If the include or library paths do not match your solver build, compilation will fail.

# 6. Running Simulations

After the sovler is built and the plugin is compiled, you should be able to run the solver executable and load the plugin.

Typical run command:

```bash
<my-home>/FEBio-FSG/build/bin/febio4 -i input.feb -import ./FEFSG.so
```

**Important: the `-import ./FEFSG.so` flag lets the solver know to import your plugin. If you exclude this flag, it will not be able to run an FSG input file**

If on a cluster, use a scheduling script [TODO: Add tutorial for SLURM scheduling]

# 7. Configuring Simulations

The `<Material>` section of the .feb file specifies that you are using the FSG material, which is implemented through the FEBio-FSG solver (not standard FEBio).

```xml
<Material>
  <material id="1" name="Material1" type="FSG">
    <density>1</density>
    <k>1000.0</k>
    <e_r type="math"> X/sqrt(X^2 + Y^2), Y/sqrt(X^2 + Y^2), 0 </e_r>
    <e_t type="math"> -Y/sqrt(X^2 + Y^2), X/sqrt(X^2 + Y^2), 0 </e_t>
    <e_z type="math"> 0, 0, 1 </e_z>
  </material>
</Material>
```

`type="FSG"` tells FEBio to use the Fluid–Solid–Growth material model implemented in the FEBio-FSG fork of the solver.

This material:

* Reads additional biological parameters from configuration.txt
* Uses internal mixture constituents
* Evolves mass fractions and stresses over time
* Couples mechanical deformation with growth and remodeling

In this input, `e_r`, `e_t`, and `e_z` mathematically define the radial, circumferential, and axial directions, respectively

The configuration.txt is the file that defines the growth and remodeling constituents. While the .feb file defines geometry and coordinate frame, **the vascular properties are defined in configuration.txt**.

The first line defines simulation-level parameters in the following order:

```
timestep_size rho_hat_h bar_tauw_h sigma_inv_h K_delta_tauw K_delta_sigma 
```

Each subsequent line is an individual constituent (up to six total) with properties ordered as follows:

```
m_degradable m_inflammatory m_active m_polymer c1_alpha_h c2_alpha_h eta_alpha_h g_alpha_h g_alpha_r g_alpha_theta g_alpha_z phi_alpha k_alpha_h K_tauw_p_alpha_h K_sigma_p_alpha_h K_tauw_d_alpha_h K_sigma_d_alpha_h
```

# 8. Benchmark Example

The FSG_Plugin repository includes the benchmark file TAA_hypertension.feb, which simulates a murine thoracic aorta subjected to a 1.4-fold increase in pressure. If the solver and plugin are built and linked correctly, this file should produce results where the wall thickens to return the intramural stress toward its homeostatic value over time. This example serves as a basic validation test of the solver build, plugin registration, and proper reading of the configuration.txt file. For instructions on analyzing results and comparing them to benchmark behavior, see the [post-processing page](/post-processing/).

# Appendix A. Making New Branches

If you plan on modifying the source code, create a new branch for development (i.e., if your name was Taylor, you might want to make your version of the code, or "Taylor's Version", so to speak):

```bash
git branch -a
git checkout -b <taylors-version>
```

After editing:

```bash
git add <files>
git commit -m "Short summary of changes"
git push -u origin <taylors-version>
```
