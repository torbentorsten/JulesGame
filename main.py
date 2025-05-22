import pygame
import sys
import random # Though not directly used here, good to have if modules need seeding from main

# Game Modules
from game_modules.player import Player
from game_modules.environment import Environment
import game_modules.animals as animals_module # Using an alias for clarity
from game_modules.ui import UI

def main():
    # --- Pygame and Game Variables Initialization ---
    pygame.init()
    # pygame.font.init() # UI module handles its own font init

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Underwater Adventure")
    clock = pygame.time.Clock()

    # Initial scroll speed - this will be adjusted based on player movement
    # For now, it represents a potential speed, actual scroll is determined dynamically
    base_scroll_speed = 0 # Environment scrolls based on player's movement relative to screen edges

    # --- Game Object Instances ---
    player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 50) # Player sprite is 50x100
    environment = Environment(SCREEN_WIDTH, SCREEN_HEIGHT) # Uses default background_tile1.png
    ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)

    # Sprite groups
    # all_sprites = pygame.sprite.Group() # Not strictly necessary if drawing individually
    animals_group = pygame.sprite.Group()
    # all_sprites.add(player)

    total_depth_scrolled = 0 # Tracks the total depth the player has reached

    # Ensure animal types are available for spawning
    if not animals_module.AVAILABLE_ANIMAL_CLASSES:
        print("Warning: No animal types available for spawning in animals_module.")

    # --- Main Game Loop ---
    running = True
    while running:
        # --- Event Handling ---
        events = pygame.event.get() # Get all events once per frame
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # --- Updates ---
        # Player update needs the list of events for its own processing if it uses event-based input.
        # The current player.update uses pygame.key.get_pressed(), so events list isn't strictly needed there,
        # but it's good practice to pass it if some inputs might be event-based.
        player.update(events) # Pass events list

        # Scroll Logic: Environment scrolls when player approaches edges while moving
        actual_scroll = 0
        # Player moving down, near bottom third of the screen
        if player.rect.bottom > SCREEN_HEIGHT * 0.7 and player.velocity_y > 0:
            actual_scroll = player.velocity_y
            player.rect.y -= player.velocity_y # Counteract player's own movement to keep them "in place" while world scrolls
        # Player moving up, near top third of the screen (less common in this game's design, but for completeness)
        elif player.rect.top < SCREEN_HEIGHT * 0.3 and player.velocity_y < 0:
            actual_scroll = player.velocity_y # velocity_y is negative, so scroll is negative (upwards)
            player.rect.y -= player.velocity_y # Counteract player's own movement

        environment.update(actual_scroll)
        total_depth_scrolled += actual_scroll

        # Adjust Y positions of existing animals based on scrolling
        # This makes them appear fixed in the world, not fixed to the screen
        for animal_sprite in animals_group:
            animal_sprite.rect.y -= actual_scroll
            # If an animal scrolls off the top of the screen due to upward scrolling, kill it
            if actual_scroll < 0 and animal_sprite.rect.bottom < 0:
                animal_sprite.kill()
            # If an animal scrolls off the bottom of the screen due to downward scrolling, kill it
            # (More relevant if animals could also spawn above the screen and scroll into view)
            elif actual_scroll > 0 and animal_sprite.rect.top > SCREEN_HEIGHT:
                 animal_sprite.kill()


        # Animal Management (Spawning and Updating positions)
        # Note: update_and_manage_animals calls animal.update(SCREEN_WIDTH) internally for horizontal movement.
        # The y-positions of animals are relative to the world, so they need to be adjusted by actual_scroll
        animals_module.update_and_manage_animals(
            animals_group, 
            SCREEN_WIDTH, 
            SCREEN_HEIGHT, # Used for initial spawn Y-positioning
            total_depth_scrolled, 
            spawn_chance=0.02 # Example spawn chance
        )

        # --- Collision Detection ---
        # pygame.sprite.collide_rect_ratio is a good choice for forgiving collisions.
        # The ratio (0.8) means the collision rectangle is 80% of the sprite's actual size.
        collided_animals = pygame.sprite.spritecollide(player, animals_group, False, pygame.sprite.collide_rect_ratio(0.8))
        
        if collided_animals:
            for animal in collided_animals:
                # Ensure the animal has a 'type' attribute
                if hasattr(animal, 'type'):
                    if animal.type not in animals_module.discovered_animals_set:
                        animals_module.discovered_animals_set.add(animal.type)
                        print(f"Discovered: {animal.type}") # For debugging
                else:
                    print("Warning: Collided with an animal that has no 'type' attribute.")
        
        # --- Drawing (Render) ---
        screen.fill((0, 0, 25)) # Deep blue as a fallback if environment doesn't cover all

        environment.draw(screen)
        player.draw(screen)       # or all_sprites.draw(screen)
        animals_group.draw(screen)

        # Update and draw UI
        # For now, discovered_animals_set is not updated by collisions yet,
        # so it will likely remain empty. This will be part of collision detection task.
        ui.update_logbook(animals_module.discovered_animals_set)
        ui.draw(screen)

        pygame.display.flip()

        # --- Clock Tick ---
        clock.tick(FPS)

    # --- Quit Pygame ---
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
