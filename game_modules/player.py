import pygame
import os

class Player:
    def __init__(self, x, y):
        # Initialize Pygame, primarily for image loading and rect manipulation
        # It's generally good practice to initialize pygame once in the main game loop,
        # but for modularity, if a module uses pygame features like image loading,
        # it might initialize parts of it or ensure it's initialized.
        # For this class, we'll assume pygame is initialized before a Player object is created.
        # However, loading images might require pygame.display to be set up if not done,
        # which is a common source of "video system not initialized" errors.
        # For robustness, we'll ensure the display module is initialized if not already.
        if not pygame.display.get_init():
            pygame.display.init() # Initialize display module if not already initialized
            # Note: This might not be ideal if a display mode hasn't been set yet.
            # A better approach is to ensure pygame.init() is called once in main.py.

        self.image_path = os.path.join("assets", "images", "diver.png")
        try:
            self.image = pygame.image.load(self.image_path)
            # Convert alpha for better rendering performance
            self.image = self.image.convert_alpha()
        except pygame.error as e:
            print(f"Error loading player sprite '{self.image_path}': {e}")
            # Create a placeholder surface if image loading fails
            self.image = pygame.Surface((50, 100), pygame.SRCALPHA) # Same dimensions as placeholder script
            pygame.draw.rect(self.image, (0, 0, 255), (0, 20, 50, 80)) # Blue body
            pygame.draw.circle(self.image, (173, 216, 230), (25, 20), 15) # Light blue helmet
            print("Created a fallback placeholder surface for the player.")

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity_y = 0
        self.dive_speed = 0.5  # Downward acceleration when dive key is pressed
        self.max_fall_speed = 10 # Maximum downward speed

    def update(self, events):
        # Assume gravity or constant downward pull for now, adjusted by player input
        # For this iteration, descent is player-controlled only.
        
        # Process events for diving
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    # Apply dive acceleration directly on KEYDOWN event
                    self.velocity_y += self.dive_speed
                    if self.velocity_y > self.max_fall_speed:
                        self.velocity_y = self.max_fall_speed
            #keyup event could be used to stop acceleration or apply deceleration if needed.
            # For now, velocity persists until player hits boundaries or other forces act.

        # Optional: Implement slight upward drift or constant gravity if no key is pressed
        # (This part is not driven by direct key events, but by absence of them or other conditions)
        # For example, if you want player to slow down if K_DOWN is not actively being pressed:
        # (This would require a more complex state, e.g. self.diving_active)
        # if not any(event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN for event in events):
        #     pass # Potentially decelerate here if that was the desired mechanic

        # Update position based on current velocity
        self.rect.y += int(self.velocity_y) # Use int to avoid subpixel issues with rect if not handled

        # Keep player within screen bounds (assuming screen height is known, e.g., 600)
        # This part might be better handled in the main game loop or a game state manager
        # For now, let's add a basic boundary.
        # if self.rect.bottom > 600: # Assuming screen_height = 600
        #     self.rect.bottom = 600
        #     self.velocity_y = 0
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0


    def draw(self, screen):
        screen.blit(self.image, self.rect)

if __name__ == '__main__':
    # This is for basic testing of the Player class if run directly.
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Player Class Test")

    # Create a player instance
    player = Player(screen_width // 2 - 25, screen_height // 2 - 50)

    # Simple game loop for testing
    running = True
    clock = pygame.time.Clock()

    # Create .gitkeep files if they don't exist, to ensure directories are tracked
    # This is a bit unusual to do in a module, but for the sake of the task structure:
    if not os.path.exists("assets/images/.gitkeep"):
        with open("assets/images/.gitkeep", "w") as f: f.write("")
    if not os.path.exists("assets/sounds/.gitkeep"): # Though sounds is not used yet
        with open("assets/sounds/.gitkeep", "w") as f: f.write("")
    if not os.path.exists("game_modules/.gitkeep"):
        with open("game_modules/.gitkeep", "w") as f: f.write("")


    print(f"Player image loaded: {hasattr(player, 'image')}")
    print(f"Player rect: {player.rect}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Checking for player image at: {os.path.abspath(player.image_path)}")
    if not os.path.exists(player.image_path):
        print(f"Error: Player image not found at {player.image_path} from {os.getcwd()}")
        # Attempt to create the placeholder again if it's missing during test
        # This indicates a potential issue with where the script is run from vs. where assets are.
        # The create_placeholder_sprite.py should have placed it in /app/assets/images/diver.png
        if not os.path.exists("assets/images"):
            os.makedirs("assets/images")
            print("Created assets/images directory during test.")
        
        # Create a simple surface if pygame is available
        temp_surface = pygame.Surface((50, 100))
        temp_surface.fill((0,0,255)) # Blue
        try:
            pygame.image.save(temp_surface, player.image_path)
            print(f"Re-created a placeholder at {player.image_path} for testing.")
            # Reload the image
            player.image = pygame.image.load(player.image_path).convert_alpha()
            player.rect = player.image.get_rect(topleft=(player.rect.x, player.rect.y))
        except Exception as e:
            print(f"Could not create placeholder during test: {e}")


    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # The Player class's update method now takes all events,
            # but it only processes key presses internally.
            # If direct event passing is needed for other inputs, it's ready.

        player.update(events) # Pass all events to player update

        # Drawing
        screen.fill((135, 206, 235))  # Sky blue background
        player.draw(screen)
        pygame.display.flip()

        clock.tick(60) # 60 FPS

    pygame.quit()
    print("Player class test finished.")
