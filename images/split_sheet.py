import numpy as np
import imageio.v3 as iio
import os

# === Configuration ===
input_path = "sprite_me.png"      # Path to your 256x256 image
output_folder = "."       # Folder to save the 16 blocks
grid_row_size = 5                 # 4x4 grid
grid_column_size = 4                 # 4x4 grid
tile_size = 64                # Each tile will be 64x64 pixels

# === Create output directory if it doesn't exist ===
os.makedirs(output_folder, exist_ok=True)

# === Read the image ===
img = iio.imread(input_path)
h, w = img.shape[:2]

# Sanity check
if (h, w) != (tile_size*grid_row_size, tile_size*grid_column_size):
    raise ValueError("Input image must be correct size.")

filenames = ['walk_down', 'walk_left', 'walk_right', 'walk_up', 'idle']

# === Split and save ===
for row in range(grid_row_size):
    for col in range(grid_column_size):
        y0, y1 = row * tile_size, (row + 1) * tile_size
        x0, x1 = col * tile_size, (col + 1) * tile_size
        tile = img[y0:y1, x0:x1]
        iio.imwrite(os.path.join(output_folder, f"player_{filenames[row]}_{col}.png"), tile)

print("Done! Tiles saved.")
