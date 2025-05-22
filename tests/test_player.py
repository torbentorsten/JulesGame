import unittest
import pygame
import os

# Add the parent directory to the Python path to allow finding game_modules
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_modules.player import Player

class TestPlayer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Pygame modules once for the entire test class
        pygame.init()
        # Create a dummy screen - necessary for some Pygame operations like image loading/conversion
        # and drawing, even if not visually displayed during tests.
        cls.screen = pygame.display.set_mode((800, 600)) # Screen is required for Player.draw

        # Ensure the placeholder sprite exists, or create a dummy one for tests
        # This is crucial because Player.__init__ tries to load it.
        cls.sprite_path = os.path.join("assets", "images", "diver.png")
        if not os.path.exists(cls.sprite_path):
            print(f"TestPlayer.setUpClass: '{cls.sprite_path}' not found. Creating dummy sprite for tests.")
            assets_images_dir = os.path.join("assets", "images")
            if not os.path.exists(assets_images_dir):
                os.makedirs(assets_images_dir)
            
            dummy_surface = pygame.Surface((50, 100)) # Dimensions of original placeholder
            dummy_surface.fill((0,0,255)) # Blue
            try:
                pygame.image.save(dummy_surface, cls.sprite_path)
                print(f"TestPlayer.setUpClass: Dummy sprite '{cls.sprite_path}' created.")
            except pygame.error as e:
                print(f"TestPlayer.setUpClass: Failed to create dummy sprite '{cls.sprite_path}': {e}")
                # Consider raising an error here if sprite is critical and cannot be created
                # For now, tests might fail at Player instantiation if this path fails.

    def setUp(self):
        """Set up for each test method."""
        # Instantiate a player for each test
        self.player = Player(x=100, y=100)

    # --- Test initial attributes ---
    def test_initial_position(self):
        self.assertEqual(self.player.rect.topleft, (100, 100), "Player initial position is incorrect.")

    def test_initial_velocity(self):
        self.assertEqual(self.player.velocity_y, 0, "Player initial Y velocity should be 0.")

    def test_dive_speed_and_max_fall(self):
        self.assertGreater(self.player.dive_speed, 0, "Player dive_speed should be positive.")
        self.assertGreater(self.player.max_fall_speed, 0, "Player max_fall_speed should be positive.")
        # It's also good practice that dive_speed is less than or equal to max_fall_speed,
        # though not strictly required by the current problem description.
        self.assertLessEqual(self.player.dive_speed, self.player.max_fall_speed, 
                             "dive_speed should typically be <= max_fall_speed.")


    # --- Test player movement (diving) ---
    def test_diving_increases_velocity(self):
        initial_velocity = self.player.velocity_y
        # Simulate a KEYDOWN event for the down arrow key
        keydown_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        
        self.player.update([keydown_event]) # Pass the event in a list
        
        self.assertGreater(self.player.velocity_y, initial_velocity, 
                         "Diving with K_DOWN event should increase Y velocity.")
        self.assertEqual(self.player.velocity_y, initial_velocity + self.player.dive_speed,
                         "Y velocity did not increase by dive_speed.")

    def test_diving_updates_position(self):
        initial_y = self.player.rect.y
        initial_velocity = self.player.velocity_y # Should be 0
        
        # Simulate a KEYDOWN event for the down arrow key
        keydown_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        
        # Call update twice because dive_speed is 0.5, so velocity becomes 1.0 after two events,
        # which is then enough to change integer rect.y by 1.
        self.player.update([keydown_event]) # velocity_y = 0.5, rect.y still initial_y (100)
        self.player.update([keydown_event]) # velocity_y = 1.0, rect.y should be initial_y + int(1.0) = 101
        
        expected_final_velocity = initial_velocity + (self.player.dive_speed * 2) # 0 + 0.5 * 2 = 1.0
        # After first update: rect.y += int(0.5) -> no change
        # After second update: velocity is 1.0. rect.y += int(1.0) -> change by 1
        # This assumes velocity from previous step is used for movement in current step.
        # Player.update first updates velocity, then updates position with new velocity.
        # Frame 1: vel=0.5, pos_change=int(0.5)=0.  pos=100.
        # Frame 2: vel=0.5+0.5=1.0, pos_change=int(1.0)=1. pos=100+1=101.
        expected_final_y = initial_y + int(expected_final_velocity)
        
        self.assertEqual(self.player.velocity_y, expected_final_velocity,
                         "Velocity not correctly updated after two dive events.")
        self.assertEqual(self.player.rect.y, expected_final_y,
                         "Player's Y position did not update correctly after two dive events.")
        self.assertGreater(self.player.rect.y, initial_y, 
                         "Diving should change player's Y position downwards after sufficient updates.")


    def test_max_fall_speed_limit(self):
        # Simulate holding down arrow for many frames by sending multiple KEYDOWN events
        keydown_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        
        # Calculate how many steps to reach max_fall_speed
        # (max_fall_speed / dive_speed) steps, plus a few more to ensure it caps.
        # Add a margin for floating point inaccuracies if dive_speed is float.
        steps_to_reach_max = int(self.player.max_fall_speed / self.player.dive_speed) + 5 
        
        for _ in range(steps_to_reach_max):
            self.player.update([keydown_event])
            # Optional: check velocity at each step if debugging, but not required for this test.
            # print(f"Velocity after step: {self.player.velocity_y}")


        # Assert that velocity does not exceed max_fall_speed
        # It could be slightly greater due to float arithmetic before capping, so check <=
        self.assertLessEqual(self.player.velocity_y, self.player.max_fall_speed, 
                             "Player Y velocity should not exceed max_fall_speed.")
        
        # Also check that it's close to max_fall_speed (i.e., it actually accelerated)
        # This assumes dive_speed is positive and significant enough.
        # If max_fall_speed is a multiple of dive_speed, it should be equal.
        # Otherwise, it will be slightly less than max_fall_speed + dive_speed, then capped.
        # So, being equal to max_fall_speed is the expected state if it's capped.
        if self.player.dive_speed > 0: # Avoid issues if dive_speed is zero for some reason
             self.assertEqual(self.player.velocity_y, self.player.max_fall_speed,
                             f"Player Y velocity should be equal to max_fall_speed when capped. Got {self.player.velocity_y}")


    # --- Test drawing (basic check) ---
    def test_draw_runs_without_error(self):
        try:
            self.player.draw(TestPlayer.screen) # Use the class-level screen
        except Exception as e:
            self.fail(f"player.draw() raised an exception: {e}")

    def tearDown(self):
        """Clean up after each test method."""
        # self.player = None # Python's garbage collector will handle it.
        # Pygame is quit in tearDownClass, not after each test.
        pass

    @classmethod
    def tearDownClass(cls):
        # Quit Pygame once after all tests in the class have run
        pygame.quit()
        # Optionally remove the dummy sprite if it was created for testing
        # This part is commented out as it might be risky if the path is misconfigured
        # or if the original sprite was actually missing and this dummy is now used.
        # if hasattr(cls, 'sprite_path_created_for_test') and cls.sprite_path_created_for_test:
        #     if os.path.exists(cls.sprite_path):
        #         print(f"TestPlayer.tearDownClass: Removing dummy sprite '{cls.sprite_path}'.")
        #         os.remove(cls.sprite_path)

if __name__ == '__main__':
    # This allows running the tests directly from this file
    # Useful for debugging specific test files.
    unittest.main()
