---
layout: default
title: Linux Environment Setup
permalink: /linux-setup/
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

# Linux Environment Setup

Simulations are most reliably executed in a Linux environment. Many of the required tools (compilers, MPI libraries, FEBio builds, scripting workflows) are designed with Linux-based systems in mind.

This page outlines three common approaches to set up a Linux environment:

- Installing Linux as your primary operating system  
- Running Linux inside a virtual machine  
- Using a remote high-performance computing (HPC) cluster  

Choose the option that best matches your experience level, hardware access, and computational needs.

---

<details>
<summary>
<span class="summary-title">Option 1 — Native Linux Operating System</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>

<div markdown="1">

## Overview

Installing Linux directly on your machine provides the most stable and highest-performance environment. This is recommended for users who plan to run simulations regularly or compile custom plugins.

## Recommended Distributions

- **Ubuntu** (most common and well-supported)

## Installation Approaches

1. **Full Installation**  
   Replace your current OS with Linux.

2. **Dual Boot**  
   Install Linux alongside Windows or macOS.

3. **Separate Workstation**  
   Use a dedicated Linux machine for simulations.

## Advantages

- Best performance
- Full control over compilers and dependencies
- Simplest path for building FEBio from source
- Most consistent with HPC cluster environments

</div>

</details>

<details>
<summary>
<span class="summary-title">Option 2 — Linux Virtual Machine</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

## Overview

A virtual machine (VM) allows you to run Linux inside your existing operating system. This is a good option if you cannot replace your OS but want a stable Linux environment.

## VM Software Options

- VirtualBox (free)
- VMware Workstation / Fusion
- UTM (macOS Apple Silicon)

Install a Linux ISO (Ubuntu) inside the VM.

## Recommended VM Configuration

- At least 8 GB RAM allocated (if available)
- 2–4 CPU cores (allows testing parallelization)
- 40+ GB storage

## Advantages

- No need to modify your primary OS
- Safe sandbox environment for learning workflows, testing small changes to code, and developing scripts
- Can run most MBE simulations

## Limitations

- Slower than native Linux
- Limited memory and CPU availability
- Not ideal for large-scale simulations (e.g., for large FSG simulations, an HPC cluster is preferred)

</div>

</details>

<details>

<summary>
<span class="summary-title">Option 3 — High-Performance Computing Cluster</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>

<div markdown="1">

## Overview

Clusters provide scalable computational power for large simulations, parameteric sweeps, and optimization studies. Most research institutions provide access to an HPC system. Commonly used clusters:

- **Yale Grace Cluster**  
  Documentation: [https://docs.ycrc.yale.edu/clusters/grace/  ](https://docs.ycrc.yale.edu/clusters/grace/)<br>
  To request access, follow the instructions under **“Access the Cluster.”**

- **Expanse (SDSC)**  
  Access and documentation: *[link to be added]*  
  *(Instructions to be added.)*


## Typical Workflow

1. Connect via SSH:

```bash
ssh username@cluster.address.edu
```

2. Load required modules:

```bash
module load gcc
module load cmake
module load mpi
```

3. Compile or run simulations (specifics under simulation tutorials), first on debug node and then submitted through scheduler (e.g., SLURM):

```bash
sbatch run_simulation.sh
```

## Advantages

* Massive parallelization
* Large memory nodes
* Ideal for long running simulations or large meshes

## Limitations

* Requires learning job schedulers and file management via command line
* Often no graphical interface

**Suggestion:** Use a local machine to develop code and workflow, then use clusters for scaling to final study.

</div>

</details>

---

# Typical Software Stack

After establishing your Linux environment, you will typically install:

```bash
sudo apt update
sudo apt install build-essential cmake git python3 python3-pip
```
Additional tools may include:

* GCC (modern version)
* OpenMPI
* MKL (if required)
* Paraview
* PyVista / NumPy / SciPy

This setup provides a reproducible computational environment.

---

# Linux Terminal/Command Line Cheat Sheet
- `pwd` — Print the current working directory.
- `ls` — List files.
- `cd <dir>` — Change directory.  
- `cd ..` — Move up one level.
- `mkdir` — Create a directory.
- `cp <src> <dst>` — Copy files.
- `mv <src> <dst>` — Move or rename files and directories.
- `rm <file>` — Delete a file.
- `cat file.txt` — View file contents.  
- `head -n 20 file.txt` — View the first 20 lines of a file.  
- `tail -n 20 file.txt` — View the last 20 lines of a file.
- `less file.txt` — View large text files (press `q` to quit).
- `vim file.txt` — Edit a file in Vim.
- `emacs file.txt` — Edit a file in Emacs.
