import pygame
import os

# Ensure Pygame is initialized
pygame.init()

# Define image dimensions and colors
SPRITE_DIM = 30 # Make them small, like 30x30 pixels
FISH_COLOR = (255, 100, 0) # Orange for fish
JELLYFISH_COLOR = (150, 50, 200) # Purple for jellyfish
EYE_COLOR = (0, 0, 0) # Black

# Create assets/images directory if it doesn't exist
assets_images_dir = os.path.join("assets", "images")
if not os.path.exists(assets_images_dir):
    os.makedirs(assets_images_dir)
    print(f"Created directory: {assets_images_dir}")

# --- Create Fish Sprite (fish.png) ---
fish_surface = pygame.Surface((SPRITE_DIM, SPRITE_DIM), pygame.SRCALPHA)
fish_filename = os.path.join(assets_images_dir, "fish.png")

# Body (ellipse)
pygame.draw.ellipse(fish_surface, FISH_COLOR, (0, SPRITE_DIM // 4, SPRITE_DIM, SPRITE_DIM // 2))
# Tail (triangle)
tail_points = [(SPRITE_DIM - (SPRITE_DIM //3) , SPRITE_DIM // 2), (SPRITE_DIM, SPRITE_DIM // 4), (SPRITE_DIM, 3 * SPRITE_DIM // 4)]
pygame.draw.polygon(fish_surface, FISH_COLOR, tail_points)
# Eye
pygame.draw.circle(fish_surface, EYE_COLOR, (SPRITE_DIM // 4, SPRITE_DIM // 2), 2)


try:
    pygame.image.save(fish_surface, fish_filename)
    print(f"Animal sprite '{fish_filename}' created successfully.")
except Exception as e:
    print(f"Error saving animal sprite '{fish_filename}': {e}")

# --- Create Jellyfish Sprite (jellyfish.png) ---
jellyfish_surface = pygame.Surface((SPRITE_DIM, SPRITE_DIM), pygame.SRCALPHA)
jellyfish_filename = os.path.join(assets_images_dir, "jellyfish.png")

# Body (half-circle/ellipse for the bell)
pygame.draw.ellipse(jellyfish_surface, JELLYFISH_COLOR, (SPRITE_DIM // 4, 0, SPRITE_DIM // 2, SPRITE_DIM // 2))
# Tentacles (lines)
for i in range(3):
    start_x = SPRITE_DIM // 2 - 5 + (i * 5)
    pygame.draw.line(jellyfish_surface, JELLYFISH_COLOR, (start_x, SPRITE_DIM // 2), (start_x, SPRITE_DIM), 2)

try:
    pygame.image.save(jellyfish_surface, jellyfish_filename)
    print(f"Animal sprite '{jellyfish_filename}' created successfully.")
except Exception as e:
    print(f"Error saving animal sprite '{jellyfish_filename}': {e}")

# Quit Pygame
pygame.quit()
