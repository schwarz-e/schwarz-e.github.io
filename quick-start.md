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


# Quick Start Guide

## 1. Log On to Bouchet

- Go to: [https://ood-bouchet.ycrc.yale.edu/](https://ood-bouchet.ycrc.yale.edu/) 
*Note: must be on Yale network or Yale VPN*
- On to **TOP BANNER** of the website click on **Bouchet Shell Access**

## 2. Execute the following commands:

```bash
# 2.1 Start interactive computing session
salloc -p devel -t 02:00:00 -n 4
# 2.2 Set environment variables
module load foss
module load CMake
module load SciPy-bundle
source /apps/software/2024a/software/imkl/2024.2.0/setvars.sh

# 2.3 Build solver
git clone https://github.com/febiosoftware/FEBio.git
cd ~/FEBio
mkdir -p build
cd build
cmake .. -DUSE_MKL=ON -DMKLROOT=/apps/software/2024a/software/imkl/2024.2.0/mkl/latest -DMKL_OMP_LIB=/apps/software/2024a/software/imkl/2024.2.0/compiler/2024.2/lib/libiomp5.so
make -j4

# 2.4 Build plugin
cd ~
mkdir -p my_project
cd my_project
git clone https://github.com/yale-humphrey-lab/FEMBE_Plugin.git
cd FEMBE_Plugin
g++ -fPIC -shared FEMbeCmm.cpp dllmain.cpp -o FEMbeCmm.so -std=c++11 -I ~/FEBio/ -L ~/FEBio/build/lib -l febiomech -l fecore

# 2.5 Run simulation
~/FEBio/build/bin/febio4 -i thoracic_aorta_hypertension_mbe.feb -import ./FEMbeCmm.so
```

For more details, see the tutorial pages.