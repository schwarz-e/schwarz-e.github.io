---
layout: default
title: MBE Simulations
permalink: /mbe-simulations/
---

# Running MBE Simulations

This page explains how to run MBE simulations. There are two necessary components:

- **Solver code** (FEBio repository)
- **Plugin code** (FEMBE_Plugin repository)

**The plugin must be compiled with this specific fork of the FEBio solver source code.**

---

# 1. Overview

## Prerequisites

**Intel Math Kernel Library (MKL)**

FEBio requires the Intel Math Kernel Library (MKL) in order to utilize the Pardiso linear solver and some of the iterative linear solvers. This library can be downloaded as part of the Intel oneAPI Base Toolkit from [Intel's website](https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit.html). In the absence of MKL, FEBio will default to using the Skyline linear solver. However, the Pardiso solver is significantly faster and more memory-efficient than the Skyline solver, and it is strongly recommended that the Pardiso solver be used.

On Intel's website, follow the specific download instructions for your platform before compiling the FEBio source code.

## Solver Source Code (FEBio)

The solver source code is the full executable that performs:

- Finite element assembly
- Nonlinear solves
- Time stepping
- Core mechanics infrastructure

It is the engine that actually runs simulations. In this workflow, we use the **official FEBio fork maintained by University of Utah and Columbia University**:

```
git@github.com:febiosoftware/FEBio.git
```

The MBE plugin must be built against this fork.

If you compile a plugin against a different FEBio fork, it may:

- Fail to load
- Crash at runtime
- Produce incorrect results

---

## Plugin Code (FEMBE_Plugin)

A plugin is a dynamically loaded shared library (`.so`) that extends the solver and is typically used to add new constitutive material models. The plugins do **not** replace the solver and do **not** do any actual simulation. They are simply an extra dictionary for the solver to use to look up newly created materials. **Plugins do not solve any actual code but need to be used with their solver counterpart**.

---

# 2. Cloning the Solver

Move to your home directory:

```bash
cd ~
```

*Note: It is typical to use your home directory to compile source code. The shortcut for moving to your home directory is `cd ~`.*

Clone the solver repository:

```bash
git clone git@github.com:febiosoftware/FEBio.git
```

Alternatively, if SSH is not configured:

```bash
git clone https://github.com/febiosoftware/FEBio.git
```

# 3. Building the Solver (CMake-Based Build)

We will compile the FEBio solver from the source code downloaded in the previous step. This is done within the empty directory `build`. If `build` doesn't exist, use the following commands to create and move into the directory:

```bash
cd ~/FEBio
mkdir -p build
cd build
```

*Note: Always build in a clean directory! Ensure that there are no files in `build` using the `ls` command before compiling. If the directory is empty, `ls` should not return anything.*

Once inside the `build` directory, configure the project:

```bash
ccmake .. -DCMAKE_C_FLAGS="-fopenmp" -DCMAKE_CXX_FLAGS="-fopenmp" -DUSE_MKL=ON
```

In the ccmake screen, you should see the message **EMPTY CACHE**. Press `c` configure the Makefile. The screen should populate with several flags, beginning with `CMAKE_BUILD_FLAG`, which should be set to `Release`.

You can toggle advanced mode on and off by pressing `t`. You may need to configure other paths manually for additional functionality (e.g., MKL --- ensure that `MKLROOT` is populated with `<my-example-mkl-directory>/opt/intel/oneapi/mkl`). On the YCRC cluster Bouchet, CMake may not be able to find the `MKL_OMP_LIB`. Populate it manually with the path `/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so`.

Press `c` again until it you have the option at the bottom to press `g` to generate the Makefile.

Once configuration is complete, verify that `build` has been populated with new folders (`bin`, `CMakeFiles`, and `lib`) and files (`CMakeCache.txt`, `cmake_install.cmake`, `Makefile`). You can then build the solver using the command:

```bash
make -j
```

*Note: -j enables parallel compilation*

The terminal window will display the percentage completion of the build. Once completed, it will display **Built target febio4**. After a successful build, the solver executable `febio4` will appear in `bin`, and libraries will be in `lib`.

*Note: If the build is unsuccessful and you need to rebuild, run `make clean` in `build` before trying again.*

# 4. Cloning the Plugin

Now that the solver code is compiled, you can create a new directory specific to your simulations. Create a project directory and move to it, then clone the MBE repository. This will create a new subfolder in your project directory entitled `FEMBE_Plugin`, which you can then move into:

```bash
mkdir -p <my-project>
cd <my-project>
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
cd FEMBE_Plugin
```

# 5. Compiling the Plugin

The plugin must link against the same solver build you compiled earlier. If you alter any build parameters for the FEBio build, you must recompile the plugin as well. **Do not attempt to link it with the FEBio-FSG solver meant to be used with the FSG plugin --- it will not work.**

Example build command:

```bash
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp -o FEMbeCmm.so -std=c++11 -I <my-home>/FEBio/ -L <my-home>/FEBio/build/lib -l febiomech -l fecore
```

You will know the build was successful if no messages are displayed once you regain control of the terminal window.

Components explained:

- `g++` - GNU C++ compiler that translates C++ source code (`.cpp` files) to an executable or shared library

Flags explained:

- `-fPIC` - Position-independent code (required for shared libraries)
- `-shared` - Build shared object that can be used by the solver code
- `-o` - Output name (e.g., name of the compiled plugin)
- `-I` - Include path (solver headers)
- `-L` - Library path (solver build libraries)
- `-l` - Link against solver libraries

*Note: If the include or library paths do not match your solver build, the compilation will fail. Ensure that the paths provided after `-I` and `-L` are the exact paths to where the FEBio source code is located on your system.*

# 6. Running Simulations

After the solver is built and the plugin is compiled, you should be able to run the solver executable (`febio4`) and load the plugin (`FEMbeCmm.so`).

Make sure you are in the project directory containing an FEBio input file (`.feb`). A typical run command may look like:

```bash
<my-home>/FEBio/build/bin/febio4 -i <input>.feb -import ./FEMbeCmm.so
```

Components explained:

- `<my-home>/FEBio/build/bin/febio4` - Path to the FEBio solver build (if the path is different on your system, update this accordingly)
- `-i <input>.feb` - Input file name
- `-import ./FEMbeCmm.so` - Path to the MBE plugin

**Important: The `-import ./FEMbeCmm.so` flag lets the solver know to import your plugin. If you exclude this flag, it will not be able to run an MBE input file.**

MBE simulations are more computationally efficient and can typically be run on a local machine.

# 7. Configuring Simulations

The `<Material>` section of the .feb file specifies that you are using the MBE user material, which is implemented through the FEBio solver.

```xml
<Material>
    <material id="1" name="Material1" type="mbe_cmm">
        <density>1</density>
        <e_r type="math"> X/sqrt(X^2 + Y^2), Y/sqrt(X^2 + Y^2), 0 </e_r>
        <e_t type="math"> -Y/sqrt(X^2 + Y^2), X/sqrt(X^2 + Y^2), 0 </e_t>
        <e_z type="math"> 0, 0, 1 </e_z>
    </material>
</Material>
```

`type="mbe_cmm"` tells FEBio to use the mechanobiologically equilibrated user material.

In this input, `e_r`, `e_t`, and `e_z` mathematically define the radial, circumferential, and axial directions, respectively.

Unlike in the [FSG plugin](/fsg-simulations/), the vascular constituent materials are defined directly in the plugin source code, `FEMbeCmm.cpp`. If you wish to change the material behavior, you must edit the `FEMbeCmm.cpp` directly and the recompile the plugin (Step 5 on this page).

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
