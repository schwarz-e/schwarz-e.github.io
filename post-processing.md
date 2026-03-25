---
layout: default
title: Post-Processing and Visualization
permalink: /post-processing/
---

# Post-Processing and Visualization

This page explains how to post-process and visualize outputs from MBE and FSG simulations. **ParaView** is used for visualization of the simulation geometry and computed metrics.

---

# 1. Install ParaView

Download ParaView from the official site:

- https://www.paraview.org/download/

---

# 2. Load Time-Series VTK Data

1. Open **ParaView**
2. Go to **File → Open**
3. Select your `.vtk` or `.vtu` file(s). If you have a time series, select all files in the sequence
4. Click **Apply** in the Properties panel
5. Use the **time controls** (top toolbar) to scroll through time

---

# 3. Warp Geometry by Displacement

To visualize deformation:

1. Select your dataset in the **Pipeline Browser**
2. Go to **Filters → Alphabetical → Warp By Vector**
3. In the Properties panel:
   - Set **Vectors** = `displacement` (or equivalent field)
4. Click **Apply**

Notes:
- Use **Scale Factor = 1** for true deformation, adjust **Scale Factor** if needed
---

# 4. Inspect Quantities of Interest

## 4.1 Color by Field

1. In the toolbar, change **Coloring** to desired field:
   - `stress`
   - `relative_volume` (volume ratio)
   - `etc`

2. Adjust color map:
   - Click **Color Map Editor**
   - Use **Rescale to Data Range** or **Custom Range**

---

## 4.2 Probe Values

To inspect values at a point select **Hover Points/Cells On**

---

## 4.3 Plot Over Time

1. Select dataset using **Interactive Select Points/Cells On**
2. Go to **Filters → Data Analysis → Plot Data Over Time**
3. Click **Apply**

Useful for:
- Tracking stress/strain at a point
- Monitoring global quantities

---

# 5. Animate Time Series

1. Use the **Play** button in the time toolbar
2. Adjust playback speed in **Animation View**
3. Optionally:
   - Add camera motion
   - Add annotations (time, scale)

---

# 6. Save Screenshots

1. Go to **File → Save Screenshot**
2. Choose:
   - Resolution (e.g., 300 dpi for publications)
   - Transparent background (optional)
3. Save as `.png` or `.tiff`

Tips:
- Use **View → Full Screen** for clean exports
- Lock colorbar range before exporting multiple frames

---

# 7. Export Data

## 7.1 Extract Point/Cell Data

- Use **Plot Selection Over Time** for tracked points
- Use **Spreadsheet View** to inspect raw values

---

# 8. Tips for MBE / FSG Simulations

- Check consistency of:
  - Reference vs deformed configuration
  - Units (stress, length, pressure)
- For growth/remodeling:
  - Track `relative_volume` (volume change)
- Use consistent color limits across time for comparisons

---

# 10. Common Issues

- **No time controls visible**  
  → Ensure files are loaded as a time series

- **Warp looks incorrect**  
  → Check displacement field name and scale factor

- **Color map misleading**  
  → Fix range manually instead of auto-rescaling

---