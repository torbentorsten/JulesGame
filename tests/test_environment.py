import unittest
import pygame
import os
import sys

# Add the parent directory to the Python path to allow finding game_modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_modules.environment import Environment

class TestEnvironment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # Create a dummy screen - necessary for some Pygame operations
        cls.screen = pygame.display.set_mode((800, 600))

        # Ensure the placeholder background tile exists, or create a dummy one for tests
        cls.tile_path = os.path.join("assets", "images", "background_tile1.png")
        if not os.path.exists(cls.tile_path):
            print(f"TestEnvironment.setUpClass: '{cls.tile_path}' not found. Creating dummy tile for tests.")
            assets_images_dir = os.path.join("assets", "images")
            if not os.path.exists(assets_images_dir):
                os.makedirs(assets_images_dir)
            
            # Create a simple surface and save it
            # Dimensions should match Environment's expectations or be scalable by it
            dummy_surface = pygame.Surface((800, 600)) 
            dummy_surface.fill((100, 149, 237)) # Cornflower Blue (similar to actual tile)
            try:
                pygame.image.save(dummy_surface, cls.tile_path)
                print(f"TestEnvironment.setUpClass: Dummy tile '{cls.tile_path}' created.")
            except pygame.error as e:
                print(f"TestEnvironment.setUpClass: Failed to create dummy tile '{cls.tile_path}': {e}")

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        # Optionally remove the dummy tile if created
        # if "dummy_created_for_test_tile" in cls.tile_path: # Example marker
        #     if os.path.exists(cls.tile_path): os.remove(cls.tile_path)

    def setUp(self):
        """Set up for each test method."""
        self.screen_width = 800
        self.screen_height = 600
        self.environment = Environment(self.screen_width, self.screen_height)

    def test_initial_scroll(self):
        """Test that the environment's scroll is initialized to 0."""
        self.assertEqual(self.environment.scroll, 0, "Initial scroll should be 0.")

    def test_update_scroll(self):
        """Test updating the scroll position."""
        initial_scroll = self.environment.scroll # Should be 0 from setUp

        # Update scroll by a small amount
        scroll_amount1 = 5
        self.environment.update(scroll_amount1)
        self.assertEqual(self.environment.scroll, initial_scroll + scroll_amount1,
                         f"Scroll should be {initial_scroll + scroll_amount1} after first update.")

        # Update scroll by exactly one tile height
        # This should cause the scroll to loop back to (close to) 0.
        # The Environment class's update logic is:
        # if self.scroll >= self.tile_height: self.scroll -= self.tile_height
        # So, if current scroll is 5, and tile_height is, say, 600,
        # environment.update(600) will make scroll = 5 + 600.
        # Then, 605 >= 600, so scroll becomes 605 - 600 = 5.
        # The test asks for scroll to be 0 after updating by tile_height. This implies
        # the update amount itself is tile_height, and the scroll should reset.

        # Reset scroll to 0 for a clean test of tile_height update
        self.environment.scroll = 0
        
        # Check if tile_height is positive to prevent infinite loops or errors in test logic
        self.assertGreater(self.environment.tile_height, 0, "Tile height must be positive for this test.")

        self.environment.update(self.environment.tile_height)
        # Due to `self.scroll -= self.tile_height` for precise reset, it should be exactly 0.
        # If it was `self.scroll = self.scroll % self.tile_height`, then it would also be 0.
        self.assertEqual(self.environment.scroll, 0,
                         f"Scroll should reset to 0 after updating by exactly tile_height. Current: {self.environment.scroll}")

        # Test with a scroll value that is not a multiple of tile_height
        self.environment.scroll = 10 
        scroll_amount2 = self.environment.tile_height - 5 # e.g., 595 if tile_height is 600
        self.environment.update(scroll_amount2) # scroll becomes 10 + 595 = 605
        # Expected: 605 >= 600, so scroll = 605 - 600 = 5
        self.assertEqual(self.environment.scroll, (10 + scroll_amount2) % self.environment.tile_height,
                         "Scroll behavior with non-zero initial and large update incorrect.")


    def test_draw_runs_without_error(self):
        """Test that the draw method runs without raising exceptions."""
        try:
            self.environment.draw(TestEnvironment.screen) # Use the class-level screen
        except Exception as e:
            self.fail(f"environment.draw() raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
