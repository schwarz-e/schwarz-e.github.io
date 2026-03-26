---
layout: default
title: Validation
permalink: /validation/
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


# Validating Benchmark Problems

This page walks through a benchmark validation problem using a **murine thoracic aortic** example vessel. We provide benchmark input files for simulating **hypertension** and **aneurysm** remodeling in both the **MBE** and **FSG** plugins. The goal is to confirm that both implementations produce consistent results and to illustrate the difference between the two solvers. Users should compare the outputs in **ParaView** and verify that the **displacements** and **stresses** match at the final time point for each set of benchmark inputs. This validation is intended to show that:

- the benchmark runs successfully in both the **MBE** and **FSG** workflows,
- both simulations reach the expected final configuration,
- the **deformed geometry** is the same at the last saved time point, and
- key stress fields agree between the two solutions.

---

<details>
<summary>
<span class="summary-title">Hypertension Benchmark Problem</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

The benchmark case is:

- **Input file:** `thoracic_aorta_hypertension_<xxx>.feb`
- **Physical setting:** thickening of thoracic aorta in response to increased pressure over time
- **Comparison:** run appropriate input files with the **MBE plugin** and **FSG plugin**


## 1. Run the Benchmark in the MBE Plugin

Move into the folder containing the MBE version of the benchmark and run:

```bash
<path_to_febio_mbe>/thoracic_aorta_hypertension_mbe.feb
```

After the run finishes, confirm that the sequence of VTK files for each saved time point was created.

## 2. Run the Benchmark in the FSG Plugin

Repeat the same process for the FSG version of the benchmark, run:

```bash
<path_to_febio_fsg>/thoracic_aorta_hypertension_fsg.feb
```
Again, confirm that the run completes successfully and produces the expected VTK output files.


</div>
</details>

---

<details>
<summary>
<span class="summary-title">Aneurysm Benchmark Problem</span><br>
<span class="summary-sub">Click to expand.</span>
</summary>
<div markdown="1">

The benchmark case is:

- **Input file:** `thoracic_aorta_aneurysm_<xxx>.feb`
- **Physical setting:** dilatation of thoracic aorta in response to elastic fiber injury
- **Comparison:** run appropriate input files with the **MBE plugin** and **FSG plugin**


## 1. Run the Benchmark in the MBE Plugin

Move into the folder containing the MBE version of the benchmark and run:

```bash
<path_to_febio_mbe>/thoracic_aorta_aneurysm_mbe.feb
```

After the run finishes, confirm that the sequence of VTK files for each saved time point was created.

## 2. Run the Benchmark in the FSG Plugin

Repeat the same process for the FSG version of the benchmark, run:

```bash
<path_to_febio_fsg>/thoracic_aorta_aneurysm_fsg.feb
```

Again, confirm that the run completes successfully and produces the expected VTK output files.


</div>

</details>

---

After running the desired benchmark problem, complete the following to verify that the expected results were produced.

## 1. Check That Both Simulations Completed Properly

Before comparing results, verify that:

1. Both runs completed without errors
2. Both runs reached the final intended time point

Useful checks include:

- Inspecting the terminal output
- Checking the .log file for convergence
- Confirming that the final VTK file exists in both cases

---

## 2. Open the Results in ParaView

Launch ParaView and load the VTK outputs from both runs.

A convenient workflow is:

1. Open the final VTK file from the MBE run.
2. Open the final VTK file from the FSG run.
3. Rename the two pipeline entries as MBE_final and FSG_final for clarity.
4. **Apply** both datasets.

If the benchmark outputs a time series, you may also load the full time-dependent file sequence for each case.

---

## 3. Compare the Final Deformed Geometry

The first validation step is to confirm that the final deformed configurations match.

### 3.1 Warp by displacement

For each dataset:

- Select the dataset in the **Pipeline Browser**.
- Apply the **Warp By Vector** filter.
- Set the vector field to the displacement field (often named `displacement`).
- Click **Apply**.

Repeat for both the MBE and FSG results.

### 3.2 Overlay the solutions

To compare the shapes:

1. Display both warped datasets together
2. Assign different solid colors or opacities to the MBE and FSG results
3. Rotate and zoom to inspect the geometry

The final deformed shapes should visually overlap.

---

## 4. Compare Stress Fields

The second validation step is to confirm that the stresses match at the final time point.

### 4.1 Color by a stress quantity

For each dataset:

1. Select the dataset.
2. In the coloring menu, choose a stress field of interest.
3. Use the same color limits for both datasets.

To make the comparison fair:

- Manually set the same colormap range for both solutions
- Inspect the same regions of the vessel
- Compare both the distribution pattern and the numerical range

### 4.2 Probe values

If you want a more quantitative check:

1. Use **Probe Location** or **Plot Data Over Line**
2. Sample the same location or path in both datasets
3. Compare the reported stress values directly

---

# 5. Compare the Final Time Point

Although the full output history can be explored for each plugin, the main benchmark validation target is the last saved time point.

At the final state, confirm that:

- The displacement field matches between the MBE and FSG runs
- The stress field matches between the MBE and FSG runs
- Any small differences are at the level of numerical tolerance only

Use the following checklist as you work through the comparison:

- Input files run successfully in the plugins
- Both runs reach the final time point
- Final VTK outputs load correctly in ParaView
- Final warped geometries overlap
- Final stress contours visually match
- Probed displacement values agree
- Probed stress values agree

---

# 6. Saving Comparison Figures

To document the validation:

1. Arrange the MBE and FSG views side by side, or overlay them.
2. Show the same quantity in both panels.
3. Include a shared color scale if possible.
4. Save a screenshot using: **File -> Save Screenshot**

Recommended saved figures include:

- Final warped geometry comparison
- Final stress field comparison
- Plot of stress or displacement over time

---

# 7. Troubleshooting

If the final results do not match, check the following:

- Are the two input files truly identical except for the plugin-specific setup?
- Were the same material parameters and loading conditions used?
- Are you comparing the final saved time point in each simulation?
- Are both datasets being warped using the same displacement field?
- Are the same stress definitions being plotted in ParaView?

If needed, also compare:

- Mesh resolution
- Solver settings
- Time stepping and output frequency
- Boundary conditions and pressure/loading definitions

---

# 8. Explore!

Once this validation is complete, proceed to the [Post-Processing and Visualization](/post-processing/) page to explore the outputs in more detail and extract quantities of interest from the benchmark runs. Have fun!