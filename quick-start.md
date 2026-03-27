---
layout: default
title: Bouchet Quick Start
permalink: /quick-start/
---


# 1. Building the Solver

```bash
git clone https://github.com/febiosoftware/FEBio.git
```

We will compile the FEBio solver from the source code downloaded in the previous step. This is done within the empty directory `build`. If `build` doesn't exist, use the following commands to create and move into the directory:

```bash
cd ~/FEBio
mkdir -p build
cd build
```
*Note: Always build in a clean directory! Ensure that there are no files in `build` using the `ls` command before compiling. If the directory is empty, `ls` should not return anything.*

```bash
cmake .. -DUSE_MKL=ON -DMKLROOT=/apps/software/2024a/software/imkl/2024.2.0/mkl/latest -DMKL_OMP_LIB=/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so
```

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
