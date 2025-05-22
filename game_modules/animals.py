import pygame
import os
import random

# Initialize Pygame (or ensure it's initialized)
if not pygame.get_init():
    pygame.init()
    print("Pygame initialized by animals.py.")

# Set for discovered animal types
discovered_animals_set = set()

class Animal(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, speed_x):
        super().__init__()
        
        self.image_path = image_path
        try:
            self.image = pygame.image.load(self.image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading animal sprite '{self.image_path}': {e}")
            # Create a placeholder surface if image loading fails
            # Make it a generic color, e.g. red, to indicate an error
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.image.fill((255, 0, 0)) # Red color for error
            print(f"Created a fallback placeholder surface for {self.image_path}.")

        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = speed_x
        
        # Extract animal type from image path (e.g., "fish")
        # Assuming path like "assets/images/fish.png"
        try:
            self.type = os.path.basename(self.image_path).split('.')[0]
        except Exception: # Generic exception if path splitting fails
            self.type = "unknown_animal" 

    def update(self, screen_width): # screen_width needed for boundary checks
        self.rect.x += self.speed_x

        # Basic boundary check: kill if off-screen
        if self.speed_x > 0 and self.rect.left > screen_width: # Moving right, off right edge
            self.kill()
        elif self.speed_x < 0 and self.rect.right < 0: # Moving left, off left edge
            self.kill()
        # Animals that go off top/bottom due to scrolling are handled by main game logic (not moving vertically themselves yet)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Fish(Animal):
    def __init__(self, x, y, speed_x=None):
        image_file = "fish.png"
        image_full_path = os.path.join("assets", "images", image_file)
        if speed_x is None:
            speed_x = random.choice([-2, -1, 1, 2]) # Default random speed if not provided
        super().__init__(image_full_path, x, y, speed_x)
        # Fish-specific attributes or behaviors can be added here

class Jellyfish(Animal):
    def __init__(self, x, y, speed_x=None):
        image_file = "jellyfish.png"
        image_full_path = os.path.join("assets", "images", image_file)
        if speed_x is None:
            speed_x = random.choice([-1, 1]) # Default random speed if not provided
        super().__init__(image_full_path, x, y, speed_x)
        # Jellyfish specific attributes
        self.bob_speed = random.choice([-0.5, 0.5]) # Slow vertical bobbing
        self.bob_range = random.randint(5, 15) # How far it bobs
        self.original_y = y
        self.current_bob_offset = 0

    def update(self, screen_width): # screen_width needed for boundary checks
        super().update(screen_width) # Horizontal movement and boundary checks
        
        # Vertical bobbing for Jellyfish
        if not self.alive(): # Check if the sprite is still alive after super().update()
            return

        self.current_bob_offset += self.bob_speed
        if abs(self.current_bob_offset) > self.bob_range:
            self.bob_speed *= -1 # Reverse bob direction
            self.current_bob_offset = self.bob_range * (-1 if self.bob_speed < 0 else 1) # Clamp to range

        self.rect.y = self.original_y + int(self.current_bob_offset)


# --- Animal Spawning Logic ---

# List of available animal classes for spawning
AVAILABLE_ANIMAL_CLASSES = [Fish, Jellyfish] 
# We could use weights or conditions for depth later

def spawn_animal(screen_width, screen_height, current_depth): # screen_height for y-positioning
    """
    Randomly chooses an animal type, determines its starting position, speed,
    and returns a new animal instance.
    current_depth is not used yet but planned for future depth-based spawning.
    """
    if not AVAILABLE_ANIMAL_CLASSES:
        return None

    animal_class = random.choice(AVAILABLE_ANIMAL_CLASSES)

    # Randomly determine starting x position (just off screen left or right)
    # And initial y position (within screen height for now)
    
    # Determine speed magnitude based on animal type (example)
    base_speed_magnitude = 1
    if animal_class == Fish:
        base_speed_magnitude = random.choice([1, 2])
    elif animal_class == Jellyfish:
        base_speed_magnitude = 1
        
    speed_x_sign = random.choice([-1, 1])
    final_speed_x = base_speed_magnitude * speed_x_sign

    if speed_x_sign > 0: # Moving right (positive speed)
        x_pos = -50      # Start off-screen to the left
    else: # Moving left (negative speed)
        x_pos = screen_width + 50 # Start off-screen to the right
    
    # y_pos should be within the visible screen.
    y_pos = random.randint(0, screen_height - 50) # -50 to ensure animal is mostly visible if y was edge

    # Pass the determined speed to the constructor
    new_animal_instance = animal_class(x_pos, y_pos, speed_x=final_speed_x)
    
    # Add to discovered set (optional, if not already handled by adding to sprite group and checking type)
    # discovered_animals_set.add(new_animal_instance.type) 
    # This is better handled when an animal is "collected" or observed by player.

    return new_animal_instance


def update_and_manage_animals(animal_group, screen_width, screen_height, current_depth, spawn_chance=0.01):
    """
    Updates all animals in animal_group.
    Handles spawning new animals based on spawn_chance.
    Removes animals that have been killed (e.g., went off-screen).
    """
    # Update existing animals
    for animal in animal_group:
        animal.update(screen_width) # Pass screen_width for boundary checks

    # Spawn new animals
    if random.random() < spawn_chance: # e.g., 1% chance per frame to spawn
        new_animal = spawn_animal(screen_width, screen_height, current_depth)
        if new_animal:
            animal_group.add(new_animal)
            # print(f"Spawned a new {new_animal.type} at ({new_animal.rect.x}, {new_animal.rect.y}) with speed {new_animal.speed_x}")

    return animal_group # Return the (potentially modified) group


if __name__ == '__main__':
    # This is for basic testing of the Animal classes and spawning logic.
    pygame.init()
    screen_width_test = 800
    screen_height_test = 600
    screen_test = pygame.display.set_mode((screen_width_test, screen_height_test))
    pygame.display.set_caption("Animal Classes & Spawning Test")

    # Ensure animal images exist (run create_animal_sprites.py if not)
    # For test, create dummy files if missing.
    for img_name in ["fish.png", "jellyfish.png"]:
        path = os.path.join("assets", "images", img_name)
        if not os.path.exists(path):
            print(f"Test: {img_name} not found. Creating dummy.")
            temp_surf = pygame.Surface((30, 30))
            temp_surf.fill((random.randint(50,200), random.randint(50,200), random.randint(50,200)))
            if not os.path.exists("assets/images"): os.makedirs("assets/images")
            pygame.image.save(temp_surf, path)

    all_animals = pygame.sprite.Group()

    # Spawn a few initial animals for testing
    for _ in range(5):
        animal = spawn_animal(screen_width_test, screen_height_test, 0)
        if animal:
            all_animals.add(animal)

    running_test = True
    clock_test = pygame.time.Clock()

    print(f"Starting test with {len(all_animals)} animals.")

    while running_test:
        for event_test in pygame.event.get():
            if event_test.type == pygame.QUIT:
                running_test = False

        # Update and manage animals (includes spawning)
        all_animals = update_and_manage_animals(all_animals, screen_width_test, screen_height_test, 0, spawn_chance=0.02)
        
        # Drawing
        screen_test.fill((100, 149, 237))  # Light blue background
        all_animals.draw(screen_test) # Use group's draw method
        
        pygame.display.flip()
        clock_test.tick(30) # Lower FPS for easier observation during test

    pygame.quit()
    print(f"Animal classes & spawning test finished. Discovered: {discovered_animals_set}")
