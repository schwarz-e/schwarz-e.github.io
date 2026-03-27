---
layout: default
title: Bouchet Quick Start
permalink: /quick-start/
---


# 1. Building the Solver

```bash
salloc -p devel -t 03:00:00 -n 4
module load foss
module load CMake
module load SciPy-bundle
source /apps/software/2024a/software/imkl/2024.2.0/setvars.sh
git clone https://github.com/febiosoftware/FEBio.git
cd ~/FEBio
mkdir -p build
cd build
cmake .. -DUSE_MKL=ON -DMKLROOT=/apps/software/2024a/software/imkl/2024.2.0/mkl/latest -DMKL_OMP_LIB=/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so
make -j4
```

# 2. Building the Plugin
```bash
cd ~
mkdir -p my_project
cd my_project
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
cd FEMBE_Plugin
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp -o FEMbeCmm.so -std=c++11 -I /home/<netID>/FEBio/ -L /home/<netID>/FEBio/build/lib -l febiomech -l fecore
```

# 3. Running a Simulation
```bash
/home/<netID>/FEBio/build/bin/febio4 -i <input>.feb -import ./FEMbeCmm.so
```
