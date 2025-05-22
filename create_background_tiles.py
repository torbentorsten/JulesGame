import pygame
import os

# Ensure Pygame is initialized
pygame.init()

# Define image dimensions and colors
TILE_WIDTH = 800  # Assuming a common screen width
TILE_HEIGHT = 600 # Assuming a common screen height, can be adjusted

# Create assets/images directory if it doesn't exist
assets_images_dir = os.path.join("assets", "images")
if not os.path.exists(assets_images_dir):
    os.makedirs(assets_images_dir)
    print(f"Created directory: {assets_images_dir}")

# --- Create Tile 1 (Lighter Blue Gradient) ---
tile1_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
tile1_filename = os.path.join(assets_images_dir, "background_tile1.png")

# Simple vertical gradient from a lighter blue to a slightly darker blue
color_top = (100, 149, 237)  # Cornflower Blue
color_bottom = (70, 130, 180) # Steel Blue

for y in range(TILE_HEIGHT):
    # Calculate the interpolation factor (0 at top, 1 at bottom)
    interp = y / TILE_HEIGHT
    # Interpolate each color component
    r = int(color_top[0] * (1 - interp) + color_bottom[0] * interp)
    g = int(color_top[1] * (1 - interp) + color_bottom[1] * interp)
    b = int(color_top[2] * (1 - interp) + color_bottom[2] * interp)
    pygame.draw.line(tile1_surface, (r, g, b), (0, y), (TILE_WIDTH -1, y))

try:
    pygame.image.save(tile1_surface, tile1_filename)
    print(f"Background tile '{tile1_filename}' created successfully.")
except Exception as e:
    print(f"Error saving background tile '{tile1_filename}': {e}")


# --- Create Tile 2 (Darker Blue Gradient) - Optional ---
# This tile will be darker to simulate depth.
# For seamless tiling, the bottom of tile1 should ideally match the top of tile2 if they are meant to transition.
# For simple repeating tiles, this is less critical as one tile will just repeat.
# For this example, tile2 will be a darker gradient overall.

tile2_surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
tile2_filename = os.path.join(assets_images_dir, "background_tile2.png")

color_top_dark = (70, 130, 180)   # Steel Blue (same as bottom of tile1 for potential transition)
color_bottom_dark = (25, 25, 112) # Midnight Blue

for y in range(TILE_HEIGHT):
    interp = y / TILE_HEIGHT
    r = int(color_top_dark[0] * (1 - interp) + color_bottom_dark[0] * interp)
    g = int(color_top_dark[1] * (1 - interp) + color_bottom_dark[1] * interp)
    b = int(color_top_dark[2] * (1 - interp) + color_bottom_dark[2] * interp)
    pygame.draw.line(tile2_surface, (r, g, b), (0, y), (TILE_WIDTH-1, y))

try:
    pygame.image.save(tile2_surface, tile2_filename)
    print(f"Background tile '{tile2_filename}' created successfully.")
except Exception as e:
    print(f"Error saving background tile '{tile2_filename}': {e}")


# Quit Pygame
pygame.quit()
