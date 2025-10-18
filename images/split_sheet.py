import numpy as np
import imageio.v3 as iio
import os

# === Configuration ===
input_path = "input.png"      # Path to your 256x256 image
output_folder = "."       # Folder to save the 16 blocks
grid_size = 4                 # 4x4 grid
tile_size = 64                # Each tile will be 64x64 pixels

# === Create output directory if it doesn't exist ===
os.makedirs(output_folder, exist_ok=True)

# === Read the image ===
img = iio.imread(input_path)
h, w = img.shape[:2]

# Sanity check
if (h, w) != (256, 256):
    raise ValueError("Input image must be 256x256 pixels.")

filenames = ['down', 'left', 'right', 'up']

# === Split and save ===
for row in range(grid_size):
    for col in range(grid_size):
        y0, y1 = row * tile_size, (row + 1) * tile_size
        x0, x1 = col * tile_size, (col + 1) * tile_size
        tile = img[y0:y1, x0:x1]
        iio.imwrite(os.path.join(output_folder, f"player_walk_{filenames[row]}_{col}.png"), tile)

        if col == 0:
            iio.imwrite(os.path.join(output_folder, f"player_idle_{filenames[row]}_0.png"), tile)
            iio.imwrite(os.path.join(output_folder, f"player_idle_{filenames[row]}_1.png"), tile)

print("Done! 16 tiles saved in the 'tiles' folder.")
