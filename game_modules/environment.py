import pygame
import os

class Environment:
    def __init__(self, screen_width, screen_height, tile_image_name="background_tile1.png"):
        # Initialize Pygame (or ensure it's initialized)
        if not pygame.get_init():
            pygame.init()
            print("Pygame initialized by Environment class.")
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scroll = 0

        self.image_path = os.path.join("assets", "images", tile_image_name)
        try:
            self.bg_image = pygame.image.load(self.image_path).convert()
            # Scale the image to fit the screen width if it's not already matching
            # This is a common requirement for background tiles.
            # The height will be scaled proportionally.
            current_width = self.bg_image.get_width()
            current_height = self.bg_image.get_height()
            if current_width != self.screen_width:
                new_height = int(current_height * (self.screen_width / current_width))
                self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, new_height))
                print(f"Background tile scaled to width: {self.screen_width}, new height: {new_height}")

        except pygame.error as e:
            print(f"Error loading background tile '{self.image_path}': {e}")
            # Create a fallback surface if image loading fails
            # Use screen_width and a default height (e.g., screen_height)
            self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
            # Simple gradient for fallback
            for y in range(self.screen_height):
                interp = y / self.screen_height
                color = (int(100 * (1 - interp) + 70 * interp), \
                         int(149 * (1 - interp) + 130 * interp), \
                         int(237 * (1 - interp) + 180 * interp))
                pygame.draw.line(self.bg_image, color, (0, y), (self.screen_width -1, y))
            print("Created a fallback placeholder surface for the environment background.")

        self.tile_height = self.bg_image.get_height()
        
        if self.tile_height == 0: # Avoid division by zero if image loading failed catastrophically
            print("Error: Background tile height is zero. Defaulting to screen height.")
            self.tile_height = self.screen_height # Fallback to prevent crash
            if self.tile_height == 0: # If screen_height is also 0, this is a problem
                 self.tile_height = 600 # Absolute fallback

        # Calculate number of tiles needed to cover the screen plus one for smooth scrolling
        self.num_tiles = (self.screen_height // self.tile_height) + 2
        if self.tile_height > 0 and self.screen_height % self.tile_height == 0:
             self.num_tiles = (self.screen_height // self.tile_height) + 1 # if it fits perfectly, +1 is enough
        
        print(f"Environment initialized: Screen({screen_width}x{screen_height}), Tile({self.bg_image.get_width()}x{self.tile_height}), NumTiles({self.num_tiles})")


    def update(self, scroll_speed):
        """
        Updates the scroll position of the background.
        scroll_speed: The number of pixels to scroll the background.
                      Positive for downward movement of the world (player appears to go down).
        """
        self.scroll += scroll_speed
        
        # If scroll exceeds one tile height, reset or adjust to keep it within 0 to tile_height range
        # This ensures the seamless tiling effect.
        if self.scroll >= self.tile_height:
            self.scroll -= self.tile_height # More precise than self.scroll = 0 for variable scroll_speed
            # self.scroll = self.scroll % self.tile_height # Alternative using modulo

    def draw(self, screen):
        """
        Draws the scrolling background tiles onto the screen.
        """
        if not self.bg_image or self.tile_height == 0: # Safety check
            return

        for i in range(self.num_tiles):
            # Calculate the y-position for each tile.
            # The tiles are placed one after another, and the self.scroll value creates the illusion of movement.
            y_position = (i * self.tile_height) - self.scroll
            
            # Draw the tile
            screen.blit(self.bg_image, (0, y_position))
            
            # For debugging tile positions:
            # print(f"Drawing tile {i} at (0, {y_position})")
            # pygame.draw.rect(screen, (255,0,0), (0, y_position, self.bg_image.get_width(), self.bg_image.get_height()), 1)


if __name__ == '__main__':
    # This is for basic testing of the Environment class if run directly.
    pygame.init()
    screen_width_test = 800
    screen_height_test = 600
    screen_test = pygame.display.set_mode((screen_width_test, screen_height_test))
    pygame.display.set_caption("Environment Class Test")

    # Ensure background images exist (run create_background_tiles.py if not)
    if not os.path.exists("assets/images/background_tile1.png"):
        print("Test: background_tile1.png not found. Please run create_background_tiles.py first.")
        # Create a dummy file for testing if it's missing, just so it doesn't crash here
        # In a real scenario, you'd handle this better
        temp_surf = pygame.Surface((screen_width_test, screen_height_test))
        temp_surf.fill((100,149,237))
        if not os.path.exists("assets/images"): os.makedirs("assets/images")
        pygame.image.save(temp_surf, "assets/images/background_tile1.png")
        print("Test: Created a dummy background_tile1.png")


    # Create an environment instance
    environment = Environment(screen_width_test, screen_height_test)
    
    # Simple game loop for testing
    running_test = True
    clock_test = pygame.time.Clock()
    test_scroll_speed = 2 # Pixels per frame

    while running_test:
        for event_test in pygame.event.get():
            if event_test.type == pygame.QUIT:
                running_test = False

        # Update environment
        environment.update(test_scroll_speed)

        # Drawing
        screen_test.fill((0, 0, 0))  # Fill with black before drawing environment (or let environment be first draw)
        environment.draw(screen_test)
        pygame.display.flip()

        clock_test.tick(60) # 60 FPS

    pygame.quit()
    print("Environment class test finished.")
