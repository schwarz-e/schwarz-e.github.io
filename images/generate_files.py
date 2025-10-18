import os
import struct
import zlib
import numpy as np

# --- Configuration ---
output_dir = "."
tile_size = (64, 64)  # width, height

# Base types and their placeholder colors (R, G, B, A)
base_types = {
    "tree":  (80, 160, 80, 255),   # green
    "rock":  (120, 120, 130, 255), # gray-blue
    "floor": (200, 180, 140, 255)  # tan
}

# Connection shape names (16 total)
shapes = [
    "isolated",
    "end_up", "end_right", "end_down", "end_left",
    "corner_ur", "corner_rd", "corner_dl", "corner_lu",
    "vertical", "horizontal",
    "t_leftopen", "t_upopen", "t_rightopen", "t_downopen",
    "cross"
]

# --- PNG helper functions ---
def png_chunk(chunk_type, data):
    """Build a PNG chunk."""
    chunk = struct.pack(">I", len(data))
    chunk += chunk_type
    chunk += data
    crc = zlib.crc32(chunk_type + data)
    chunk += struct.pack(">I", crc & 0xFFFFFFFF)
    return chunk

def array_to_png_bytes(arr):
    """Convert RGBA NumPy array to PNG bytes."""
    h, w, _ = arr.shape
    png = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)  # 8-bit RGBA
    png += png_chunk(b"IHDR", ihdr)

    # prepend filter byte (0) to each scanline
    raw_data = b"".join(b"\x00" + arr[y].tobytes() for y in range(h))
    compressed = zlib.compress(raw_data, 9)
    png += png_chunk(b"IDAT", compressed)
    png += png_chunk(b"IEND", b"")
    return png

# --- Pattern generation helpers ---
def pattern_for_shape(shape, color, size):
    """Return a (H, W, 4) NumPy RGBA array with a simple overlay pattern."""
    w, h = size
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0] = color[0]
    arr[..., 1] = color[1]
    arr[..., 2] = color[2]
    arr[..., 3] = color[3]

    # simple repeating pattern logic
    y, x = np.indices((h, w))
    mod = (x + y) % 8  # basic diagonal stripes
    overlay = np.zeros_like(arr[..., 0])

    # --- pattern logic ---
    if shape == "cross":
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((abs(x - cx) < half) | (abs(y - cy) < half))
        overlay[mask] = 40
    elif "end_up" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = (((abs(x - cx) < half) & (y < cy) ) | (abs(y - cy) < half))
        overlay[mask] = 40
    elif "end_down" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = (((abs(x - cx) < half) & (y > cy) ) | (abs(y - cy) < half))
        overlay[mask] = 40
    elif "end_left" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((abs(x - cx) < half) | ((abs(y - cy) < half) & (x < cx)))
        overlay[mask] = 40
    elif "end_right" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((abs(x - cx) < half) | ((abs(y - cy) < half) & (x > cx)))
        overlay[mask] = 40
    elif "corner_ur" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((((abs(x - cx) < half) & (y > cy) ) | ((abs(y - cy) < half) & (x < cx))) | ((abs(x - cx) < half) & (abs(y - cy) < half)))
        overlay[mask] = 40
    elif "corner_lu" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((((abs(x - cx) < half) & (y > cy) ) | ((abs(y - cy) < half) & (x > cx))) | ((abs(x - cx) < half) & (abs(y - cy) < half)))
        overlay[mask] = 40
    elif "corner_rd" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((((abs(x - cx) < half) & (y < cy) ) | ((abs(y - cy) < half) & (x < cx))) | ((abs(x - cx) < half) & (abs(y - cy) < half)))
        overlay[mask] = 40
    elif "corner_dl" in shape:
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = ((((abs(x - cx) < half) & (y < cy) ) | ((abs(y - cy) < half) & (x > cx))) | ((abs(x - cx) < half) & (abs(y - cy) < half)))
        overlay[mask] = 40
    elif shape == "vertical":
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = (abs(x - cx) < half) 
        overlay[mask] = 40
    elif shape == "horizontal":
        # Large centered cross: 48-pixel wide vertical + horizontal bars
        overlay[(x * y) % 11 < 6] = 20
        cx, cy = w // 2, h // 2
        half = 36 // 2
        mask = (abs(y - cy) < half)
        overlay[mask] = 40
    elif "t_" in shape:
        overlay[(x ^ y) % 10 < 5] = 80
    else:  # isolated or other
        overlay[(x * y) % 11 < 6] = 30

    # Apply overlay (lighten color)
    arr[..., :3] = np.clip(arr[..., :3] + overlay[..., None], 0, 255)
    return arr

# --- Main generation ---
os.makedirs(output_dir, exist_ok=True)

for base, color in base_types.items():
    for shape in shapes:
        filename = f"{base}_{shape}.png"
        filepath = os.path.join(output_dir, filename)

        arr = pattern_for_shape(shape, color, tile_size)
        png_bytes = array_to_png_bytes(arr)

        with open(filepath, "wb") as f:
            f.write(png_bytes)
        print(f"Created {filepath}")

print("\nAll patterned PNGs created successfully!")
