---
layout: default
title: MBE Simulations
permalink: /mbe-simulations/
---

# Running Simulations on Expanse

This page explains how to run MBE simulations. There are two necessary components of running FSG simulations:

- **Solver code** (the FEBio repository)
- **Plugin code** (the FEMBE repository)

This is a critical distinction:  
**The plugin must be compiled with this specific fork of the FEBio solver source code.**

---

# 1. Overview

## Solver Source Code (FEBio)

The solver source code is the full executable that performs:

- Finite element assembly
- Nonlinear solves
- Time stepping
- Fluid–solid–growth coupling
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

## Plugin Code (FEMBE)

A plugin is a dynamically loaded shared library (`.so`) that extends the solver and is typically used to add new constitutive material models. The plugins do **not** replace solver and do **not** do any actual simulation. It is simply an extra dictionary for the solver to use to look up newly created materials. To reiterate **plugins do not solve any actual code, but need to be used with their solver counterpart**.

---

# 2. Clone the Solver

Move to your home directory:

```bash
cd <my-home>
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

# 4. Build the Solver (CMake-Based Build)

Always build in a clean directory!

```bash
cd <my-home>/FEBio
mkdir -p build
cd build
```

Configure the project:


```bash
ccmake -DCMAKE_BUILD_TYPE=Release ..
```

In the ccmake screen, press `c` to configure the Makefile until it gives you the option to press `g` to generate the Makefile. You may need to configure paths manually for additional functionality (e.g., MKL).

Once configuration is complete:

```bash
make -j
```

*Note: -j enables parallel compilation*

After successful build, the solver executable and libraries will be in:

```bash
<my-home>/FEBio/build/
```

# 4. Clone the Plugin

Move to your project directory:

```bash
cd <my-project>
git clone https://github.com/yale-humphrey-lab/FEMBE.git
cd FEFSG
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
<my-home>/FEBio/build/bin/febio4 -i input.feb -import FEMbeCmm.o
```

**Important: the `-import FEMbeCmm.o` flag lets the solver know to import your plugin. If you exclude this flag, it will not be able to run an MBE input file**

MBE simultions can typically be run on a local machine.

# 7. Making New Branches

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