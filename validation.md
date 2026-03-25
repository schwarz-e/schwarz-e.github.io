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


# 1. Run the Benchmark in the MBE Plugin

Move into the folder containing the MBE version of the benchmark and run:

```bash
<path_to_febio_mbe>/thoracic_aorta_hypertension_mbe.feb
```

After the run finishes, confirm that the sequence of VTK files for each saved time point was created.

# 2. Run the Benchmark in the FSG Plugin

Repeat the same process for the FSG version of the benchmark, run:

```bash
<path_to_febio_fsg>/thoracic_aorta_hypertension_fsg.feb
```
Again, confirm that the run completes successfully and produces the expected VTK output files.

# 3. Check That Both Simulations Completed Properly

Before comparing results, verify that:

- both runs completed without errors
- both runs reached the final intended time point

Useful checks include:

- inspecting the terminal output,
- checking the .log file for convergence,
- confirming that the final VTK file exists in both cases.

# 4. Open the Results in ParaView

Launch ParaView and load the VTK outputs from both runs.

A convenient workflow is:

1. Open the final VTK file from the MBE run.
2. Open the final VTK file from the FSG run.
3. Rename the two pipeline entries as MBE_final and FSG_final for clarity.
4. Apply both datasets.

If the benchmark outputs a time series, you may also load the full time-dependent file sequence for each case.

# 5. Compare the Final Deformed Geometry

The first validation step is to confirm that the final deformed configurations match.

## 5.1 Warp by displacement

For each dataset:

- Select the dataset in the Pipeline Browser.
- Apply the Warp By Vector filter.
- Set the vector field to the displacement field (often named `displacement`).
- Click Apply.

Repeat for both the MBE and FSG results.

## 5.2 Overlay the two solutions

To compare the shapes:

display both warped datasets together,
assign different solid colors or opacities to the MBE and FSG results,
rotate and zoom to inspect the geometry.

The final deformed shapes should visually overlap.

# 6. Compare Stress Fields

The second validation step is to confirm that the stresses match at the final time point.

Useful quantities to inspect include:

Cauchy stress components,
principal stresses,
effective stress or von Mises stress, if available,
constituent or mixture stress fields, depending on the output variables written by the plugins.

## 6.1 Color by a stress quantity

For each dataset:

Select the dataset.
In the coloring menu, choose a stress field of interest.
Use the same color limits for both datasets.

To make the comparison fair:

manually set the same colormap range for both solutions,
inspect the same regions of the vessel,
compare both the distribution pattern and the numerical range.

## 6.2 Probe values if needed

If you want a more quantitative check:

Use Probe Location or Plot Data Over Line.
Sample the same location or path in both datasets.
Compare the reported stress values directly.

# 7. Compare the Final Time Point Only

Although the full time history can be explored, the main benchmark validation target is the last saved time point.

At the final state, confirm that:

the displacement field matches between the MBE and FSG runs,
the stress field matches between the MBE and FSG runs,
any small differences are at the level of numerical tolerance only.

A concise validation statement is:

At the final time point, the MBE and FSG solutions should produce the same deformed configuration and matching stress distributions for the benchmark.

</div>
</details>

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


# 1. Run the Benchmark in the MBE Plugin

Move into the folder containing the MBE version of the benchmark and run:

```bash
<path_to_febio_mbe>/thoracic_aorta_aneurysm_mbe.feb
```

After the run finishes, confirm that the sequence of VTK files for each saved time point was created.

# 2. Run the Benchmark in the FSG Plugin

Repeat the same process for the FSG version of the benchmark, run:

```bash
<path_to_febio_fsg>/thoracic_aorta_aneurysm_fsg.feb
```

Again, confirm that the run completes successfully and produces the expected VTK output files.

# 3. Check That Both Simulations Completed Properly

Before comparing results, verify that:

- both runs completed without errors
- both runs reached the final intended time point

Useful checks include:

- inspecting the terminal output,
- checking the .log file for convergence,
- confirming that the final VTK file exists in both cases.

# 4. Open the Results in ParaView

Launch ParaView and load the VTK outputs from both runs.

A convenient workflow is:

1. Open the final VTK file from the MBE run.
2. Open the final VTK file from the FSG run.
3. Rename the two pipeline entries as MBE_final and FSG_final for clarity.
4. Apply both datasets.

If the benchmark outputs a time series, you may also load the full time-dependent file sequence for each case.

# 5. Compare the Final Deformed Geometry

The first validation step is to confirm that the final deformed configurations match.

## 5.1 Warp by displacement

For each dataset:

- Select the dataset in the Pipeline Browser.
- Apply the Warp By Vector filter.
- Set the vector field to the displacement field (often named `displacement`).
- Click Apply.

Repeat for both the MBE and FSG results.

## 5.2 Overlay the two solutions

To compare the shapes:

display both warped datasets together,
assign different solid colors or opacities to the MBE and FSG results,
rotate and zoom to inspect the geometry.

The final deformed shapes should visually overlap.

# 6. Compare Stress Fields

The second validation step is to confirm that the stresses match at the final time point.

Useful quantities to inspect include:

Cauchy stress components,
principal stresses,
effective stress or von Mises stress, if available,
constituent or mixture stress fields, depending on the output variables written by the plugins.

## 6.1 Color by a stress quantity

For each dataset:

Select the dataset.
In the coloring menu, choose a stress field of interest.
Use the same color limits for both datasets.

To make the comparison fair:

manually set the same colormap range for both solutions,
inspect the same regions of the vessel,
compare both the distribution pattern and the numerical range.

## 6.2 Probe values if needed

If you want a more quantitative check:

Use Probe Location or Plot Data Over Line.
Sample the same location or path in both datasets.
Compare the reported stress values directly.

# 7. Compare the Final Time Point Only

Although the full time history can be explored, the main benchmark validation target is the last saved time point.

At the final state, confirm that:

the displacement field matches between the MBE and FSG runs,
the stress field matches between the MBE and FSG runs,
any small differences are at the level of numerical tolerance only.

A concise validation statement is:

At the final time point, the MBE and FSG solutions should produce the same deformed configuration and matching stress distributions for the benchmark.

</div>

</details>


# Suggested Validation Checklist

Use the following checklist as you work through the comparison:

 TAA_hypertension.feb runs successfully in the MBE plugin
 TAA_hypertension.feb runs successfully in the FSG plugin
 Both runs reach the final time point
 Final VTK outputs load correctly in ParaView
 Final warped geometries overlap
 Final stress contours visually match
 Probed displacement values agree
 Probed stress values agree

# Saving Comparison Figures

To document the validation:

Arrange the MBE and FSG views side by side, or overlay them.
Show the same quantity in both panels.
Include a shared color scale if possible.
Save a screenshot using:

File -> Save Screenshot

Recommended saved figures include:

final warped geometry comparison,
final stress contour comparison,
optional line plot of stress or displacement along a selected path.


# Expected Outcome

This benchmark is considered validated when the MBE and FSG versions of TAA_hypertension.feb produce matching results at the final time point.

In particular, users should observe that:

the final deformation is the same,
the final stress state is the same,
both implementations reproduce the same benchmark solution.

# Troubleshooting

If the final results do not match, check the following:

Are the two input files truly identical except for the plugin-specific setup?
Were the same material parameters and loading conditions used?
Are you comparing the same saved time point in each simulation?
Are both datasets being warped using the same displacement field?
Are the same stress definitions being plotted in ParaView?

If needed, also compare:

mesh resolution,
solver settings,
time stepping and output frequency,
boundary conditions and pressure/loading definitions.

# Next Steps: Explore!

Once this validation is complete, proceed to the Post-Processing and Visualization page to explore the outputs in more detail and extract quantities of interest from the benchmark runs.