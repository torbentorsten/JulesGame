import pygame

class UI:
    def __init__(self, screen_width, screen_height):
        # Initialize Pygame and pygame.font
        # It's good practice to initialize pygame.font once.
        # Pygame itself should be initialized in the main game file.
        if not pygame.get_init():
            pygame.init() # Ensure Pygame itself is initialized
            print("Pygame initialized by UI class (should ideally be done in main.py).")
        
        if not pygame.font.get_init():
            pygame.font.init()
            print("Pygame font module initialized by UI class.")

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Font settings
        try:
            self.font = pygame.font.Font(None, 24) # Use default system font, size 24
        except Exception as e:
            print(f"Error loading default font: {e}. Falling back to pygame.font.SysFont.")
            # Fallback to a known system font if default `None` fails (rare)
            self.font = pygame.font.SysFont("sans-serif", 24) 


        # Logbook surface settings
        self.logbook_surface_height = 50  # Enough for one line of text
        self.logbook_surface = pygame.Surface((self.screen_width, self.logbook_surface_height))
        self.logbook_surface.set_alpha(180)  # Semi-transparent (0-255 range)
        
        self.logbook_color = (20, 20, 20)  # Dark grey
        self.text_color = (230, 230, 230)  # Light grey

        self.discovered_animals_cache = "" # To avoid re-rendering text if no change
        
        # Initial rendering of the logbook surface (e.g., empty or with a default message)
        # This ensures it's drawn correctly on the first frame even if update_logbook isn't called immediately.
        self.update_logbook(set()) # Initialize with an empty set

    def update_logbook(self, discovered_animals_set):
        """
        Updates the logbook display with the set of discovered animals.
        discovered_animals_set: A set of strings, e.g., {"fish", "jellyfish"}
        """
        if not discovered_animals_set:
            display_text = "Discovered: None"
        else:
            display_text = "Discovered: " + ", ".join(sorted(list(discovered_animals_set)))

        if display_text != self.discovered_animals_cache:
            self.discovered_animals_cache = display_text
            
            self.logbook_surface.fill(self.logbook_color) # Fill with background color
            
            try:
                text_surf = self.font.render(display_text, True, self.text_color)
            except Exception as e: # Catch potential errors during font rendering
                print(f"Error rendering text for logbook: {e}")
                # Fallback: render a simple error message or use a known safe string
                error_message = "Error rendering text"
                text_surf = self.font.render(error_message, True, (255,0,0)) # Red color for error

            text_rect = text_surf.get_rect(center=(self.screen_width // 2, self.logbook_surface_height // 2))
            self.logbook_surface.blit(text_surf, text_rect)

    def draw(self, screen):
        """
        Blits the logbook_surface onto the main screen at (0,0) (top of the screen).
        """
        screen.blit(self.logbook_surface, (0, 0))


if __name__ == '__main__':
    # This is for basic testing of the UI class if run directly.
    pygame.init() # Main pygame init
    pygame.font.init() # Font init

    screen_width_test = 800
    screen_height_test = 600
    screen_test = pygame.display.set_mode((screen_width_test, screen_height_test))
    pygame.display.set_caption("UI Class Test")

    # Create a UI instance
    ui_test = UI(screen_width_test, screen_height_test)

    # Test data
    discovered_test_set1 = {"fish"}
    discovered_test_set2 = {"fish", "jellyfish"}
    discovered_test_set3 = {"fish", "jellyfish", "shark"} # shark not yet an animal type

    # Simulate game loop for testing UI updates
    running_test = True
    clock_test = pygame.time.Clock()
    test_phase = 0
    frames_per_phase = 120 # Change displayed text every 2 seconds (at 60fps)

    print("UI Test Started. Display will cycle through different discovered animal sets.")

    while running_test:
        for event_test in pygame.event.get():
            if event_test.type == pygame.QUIT:
                running_test = False

        # Simulate updating the discovered animals set periodically
        if frames_per_phase % 120 == 0: # Change every 2 seconds
            test_phase = (test_phase + 1) % 4
            if test_phase == 0:
                current_set = set()
                print("UI Test: Displaying empty set.")
            elif test_phase == 1:
                current_set = discovered_test_set1
                print(f"UI Test: Displaying {current_set}")
            elif test_phase == 2:
                current_set = discovered_test_set2
                print(f"UI Test: Displaying {current_set}")
            else: # test_phase == 3
                current_set = discovered_test_set3
                print(f"UI Test: Displaying {current_set}")
            
            ui_test.update_logbook(current_set)
        
        frames_per_phase +=1

        # Drawing
        screen_test.fill((100, 149, 237))  # Background color (light blue, similar to game)
        ui_test.draw(screen_test)          # Draw the UI on top
        pygame.display.flip()

        clock_test.tick(60) # 60 FPS

    pygame.quit()
    print("UI class test finished.")
