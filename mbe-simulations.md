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

## Solver Source Code (FEBio)

The solver source code is the full executable that performs:

- Finite element assembly
- Nonlinear solves
- Time stepping
- Core mechanics infrastructure

It is the engine that actually runs simulations. In this workflow, we use the **official FEBio fork maintained by University of Utah and Columbia University.**:

```
febiosoftware/FEBio
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

# 2. Clone the Solver

Move to your home directory:

```bash
cd ~
```

*Note: It is typical to use your home directory to compile source code. Typically, the shortcut for moving to your home directory is `cd ~`.*

Clone the solver repository:

```bash
git clone git@github.com:febiosoftware/FEBio.git
```

Alternatively, if SSH is not configured:

```bash
git clone https://github.com/febiosoftware/FEBio.git
```

# 3. Build the Solver (CMake-Based Build)

We will compile the FEBio solver from the source code downloaded in the previous step. This is done within the empty directory `build`. If `build` doesn't exist, use the following commands to create and move into the directory:

```bash
cd <my-home>/FEBio
mkdir -p build
cd build
```

*Note: Always build in a clean directory! Ensure that there are no files in `build` using the `ls` command before compiling.*

Once inside the `build` directory, configure the project:

```bash
ccmake -DCMAKE_BUILD_TYPE=Release ..
```

In the ccmake screen, you should see the message **EMPTY CACHE**. Press `c` configure the Makefile. The screen should populate with several flags, beginning with `CMAKE_BUILD_FLAG`, which should be set to `Release`.

You can toggle advanced mode by pressing `t`. Ensure `CMAKE_CXX_FLAGS` is set to `-fopenmp`. You may need to configure paths manually for additional functionality (e.g., MKL).

Press `c` again until it you have the option at the bottom to press `g` to generate the Makefile.



Once configuration is complete:

```bash
make -j
```

*Note: -j enables parallel compilation*

After a successful build, the solver executable ` and libraries will be in:

```bash
<my-home>/FEBio/build/
```

# 4. Clone the Plugin

Move to your project directory:

```bash
cd <my-project>
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
cd FEMBE_Plugin
```

# 5. Compile the Plugin

The plugin must link against the same solver build you compiled earlier. **Do not attempt to link it with the FEBio-FSG solver meant to be used with the FSG plugin, it will not work and it will be confusing to all involved.**

Example build command:

```bash
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp \
    -o FEMbeCmm.so \
    -std=c++11 \
    -I/<my-home>/FEBio/ \
    -L/<my-home>/FEBio/build/lib \
    -lfebiomech -lfecore
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
<my-home>/FEBio/build/bin/febio4 -i <input>.feb -import ./FEMbeCmm.so
```

**Important: the `-import ./FEMbeCmm.so` flag lets the solver know to import your plugin. If you exclude this flag, it will not be able to run an MBE input file**

MBE simultions can typically be run on a local machine.

# 7. Configuring Simulations

The `<Material>` section of the .feb file specifies that you are using the MBE material, which is implemented through the FEBio solver.

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

`type="mbe_cmm"` tells FEBio to use the mechanobiologically equilibrated material model.

In this input, `e_r`, `e_t`, and `e_z` mathematically define the radial, circumferential, and axial directions, respectively.

Unlike in the FSG plugin, the vascular constituent materials are defined directly in the plugin code, `FEMbeCmm.cpp`. If you wish to change the material behavior, you must edit the `FEMbeCmm.cpp` directly and the recompile the plugin (Step 5 on this page).

# 8. Benchmark Example

[TODO: Add benchmark example to repository] The FEMBE_Plugin repository includes the benchmark file TAA_hypertension.feb, which simulates a murine thoracic aorta.  If the solver and plugin are built and linked correctly, at each timestep the solver will find the homeostatic configuration of the vessel as it ramps from its original pressure (1.0-fold) to a hypertensive pressure (1.4-fold). This example serves as a basic validation test of the solver build and plugin registration. For instructions on analyzing results and comparing them to benchmark behavior, see the [post-processing page](/post-processing/).

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
