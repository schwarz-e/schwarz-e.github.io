---
layout: default
title: Bouchet Quick Start
permalink: /quick-start/
---
<style>
summary {
  font-weight: 700;
  font-size: 1.75em;        /* ≈ ## heading size */
  cursor: pointer;
  line-height: 1.2;
  color: #267CB9;
  margin-bottom: 0.5em;
}
summary:hover {
  color: #069;
}
.summary-sub {
  display: block;
  font-size: 0.8em;               /* same as normal body text */
  font-weight: normal;
  margin-bottom: 0.5em;
}

</style>


# Overview

From starting a computing session to running a simulation, execute the following commands:

```bash
# 1. Log on to cluster

# Start interactive computing session
salloc -p devel -t 02:00:00 -n 4
# Set environment variables
module load foss
module load CMake
module load SciPy-bundle
source /apps/software/2024a/software/imkl/2024.2.0/setvars.sh

# 2. Build solver
git clone https://github.com/febiosoftware/FEBio.git
cd ~/FEBio
mkdir -p build
cd build
cmake .. -DUSE_MKL=ON -DMKLROOT=/apps/software/2024a/software/imkl/2024.2.0/mkl/latest -DMKL_OMP_LIB=/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so
make -j4

# 3. Build plugin
cd ~
mkdir -p my_project
cd my_project
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
cd FEMBE_Plugin
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp -o FEMbeCmm.so -std=c++11 -I ~/FEBio/ -L ~/FEBio/build/lib -l febiomech -l fecore

# 4. Run simulation
~/FEBio/build/bin/febio4 -i thoracic_aorta_hypertension_mbe.feb -import ./FEMbeCmm.so
```

Details are summarized below and more details can be found on each tutorial page.

---


<details>
<summary>
<span class="summary-title">1. Log On to Bouchet Cluster</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

[Todo]

</div>
</details>

---

<details>
<summary>
<span class="summary-title">2. Build Solver</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

## 2.1 Start an Interactive Compute Session

```bash
salloc -p devel -t 02:00:00 -n 4
```

- `salloc`: Request an interactive job on the cluster  
- `-p devel`: Use the development partition (short jobs for testing)  
- `-t 02:00:00`: Request 2 hours of runtime  
- `-n 4`: Request 4 CPU cores 

---

## 2.2 Load Required Software Modules

```bash
module load foss
```
- Loads compiler toolchain (GCC, MPI, etc.)

```bash
module load CMake
```
- Loads CMake (build system generator)

```bash
module load SciPy-bundle
```
- Loads Python scientific libraries

---

## 2.3 Load MKL Environment

```bash
source /apps/software/2024a/software/imkl/2024.2.0/setvars.sh
```

- Sets environment variables for Intel MKL
- Enables optimized math libraries for FEBio

---

## 2.4 Download FEBio Source Code

```bash
git clone https://github.com/febiosoftware/FEBio.git
```

- Downloads FEBio source code from GitHub

```bash
cd ~/FEBio
```

- Move into the FEBio directory

---

## 2.5 Create a Build Directory

```bash
mkdir -p build
cd build
```

- Keeps compiled files separate from source code
- Best practice for CMake projects

---

## 2.6 Configure the Build with CMake

```bash
cmake .. -DUSE_MKL=ON -DMKLROOT=/apps/software/2024a/software/imkl/2024.2.0/mkl/latest -DMKL_OMP_LIB=/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so
```

- `..`: Specifies that the project to be configured is in the directory above the build directory  
- `-DUSE_MKL=ON`: Enable MKL support  
- `-DMKLROOT=...`: Path to MKL installation  
- `-DMKL_OMP_LIB=...`: Path to OpenMP runtime library  

This step generates a Makefile for compilation.

---

## 2.7 Compile FEBio

```bash
make -j4
```

- Builds the code using the Makefile
- `-j4`: Use 4 cores in parallel (the number specified when the interactive node was launched)

</div>
</details>

---

<details>
<summary>
<span class="summary-title">3. Build Plugin</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

## 3.1 Set Up a Working Directory

```bash
cd ~
```
- Move to your home directory

```bash
mkdir -p my_project
```
- Create a project folder

```bash
cd my_project
```
- Enter your project directory

---

## 3.2 Download the Plugin Source Code

```bash
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
```
- Downloads the FEMBE plugin repository from GitHub

```bash
cd FEMBE_Plugin
```
- Move into the plugin source directory

---

## 3.3 Compile the Plugin

```bash
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp -o FEMbeCmm.so -std=c++11 -I ~/FEBio/ -L ~/FEBio/build/lib -l febiomech -l fecore
```

### Flags:

- `g++`: GNU C++ compiler  
- `-fPIC`: Generate shared libraries (.so files)
- `-shared`: Create a shared library instead of an executable  
- `FEMbeCmm.cpp dllmain.cpp`: Source files to compile  
- `-o FEMbeCmm.so`: Output file name (shared library)  
- `-std=c++11`: Use the C++11 standard  

### Linking to FEBio Solver:

- `-I ~/FEBio/`: Path to FEBio header files (include directory)
- `-L ~/FEBio/build/lib`: Path to FEBio compiled libraries  
- `-l febiomech`: Link against FEBio mechanics library  
- `-l fecore`: Link against FEBio core library  

---

## 3.3 Check Plugin is Created

After successful compilation, you should see:

```bash
FEMbeCmm.so
```

This is the plugin file that can be loaded into FEBio.

</div>
</details>

---


<details>
<summary>
<span class="summary-title">4. Run Simulation</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

```bash
~/FEBio/build/bin/febio4 -i thoracic_aorta_hypertension_mbe.feb -import ./FEMbeCmm.so
```

## Command Breakdown

- `~/FEBio/build/bin/febio4`: Path to the FEBio executable  
- `-i <...>.feb`: Specifies the input file (in this case, `thoracic_aorta_hypertension_mbe.feb`)  
- `-import ./FEMbeCmm.so`: Loads the custom plugin at runtime. `./` means the plugin is in the current directory  
</div>
</details>

---