import unittest
import pygame
import os
import sys

# Add the parent directory to the Python path to allow finding game_modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game_modules.ui import UI

class TestUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # UI class itself handles pygame.font.init() with a check.
        # So, explicitly calling it here is okay but not strictly necessary if UI does it robustly.
        if not pygame.font.get_init(): # Optional: ensure it's init'd if tests rely on font before UI instance
            pygame.font.init()
            print("TestUI.setUpClass: Pygame font module initialized by test.")
            
        cls.screen = pygame.display.set_mode((800, 600))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        """Set up for each test method."""
        self.screen_width = 800
        self.screen_height = 600
        self.ui = UI(self.screen_width, self.screen_height)

    def test_initial_logbook_empty(self):
        """Test that the logbook is initially empty or shows 'None'."""
        # The UI.__init__ calls self.update_logbook(set())
        # which sets discovered_animals_cache to "Discovered: None"
        self.assertIn("Discovered: None", self.ui.discovered_animals_cache,
                      f"Initial logbook message incorrect: '{self.ui.discovered_animals_cache}'")

    def test_update_logbook_single_animal(self):
        """Test updating the logbook with a single discovered animal."""
        self.ui.update_logbook({"fish"})
        self.assertIn("fish", self.ui.discovered_animals_cache, "Logbook should contain 'fish'.")
        self.assertNotIn("None", self.ui.discovered_animals_cache, "Logbook should not contain 'None' after update.")
        self.assertIn("Discovered: fish", self.ui.discovered_animals_cache, "Logbook format incorrect for single animal.")

    def test_update_logbook_multiple_animals(self):
        """Test updating the logbook with multiple discovered animals."""
        animal_set = {"fish", "jellyfish"}
        # The UI sorts the set before display, so check for both orders or the sorted version.
        # Current UI implementation sorts them: "Discovered: fish, jellyfish"
        expected_text_sorted = "Discovered: fish, jellyfish" 
        
        self.ui.update_logbook(animal_set)
        
        self.assertIn("fish", self.ui.discovered_animals_cache, "Logbook should contain 'fish'.")
        self.assertIn("jellyfish", self.ui.discovered_animals_cache, "Logbook should contain 'jellyfish'.")
        # Check for the exact formatted string based on UI's sorting behavior
        self.assertEqual(self.ui.discovered_animals_cache, expected_text_sorted,
                         f"Logbook format incorrect for multiple animals. Expected sorted. Got: '{self.ui.discovered_animals_cache}'")

    def test_update_logbook_no_change_no_update(self):
        """Test that cache prevents re-render if animal set is identical."""
        initial_set = {"crab"}
        self.ui.update_logbook(initial_set)
        initial_cache = self.ui.discovered_animals_cache
        
        # Get a reference to the surface before the second update
        # This is a bit tricky, as the surface object might be the same but its contents changed.
        # A better way would be to mock font.render if we want to check it wasn't called.
        # For now, we rely on the cache string not changing as an proxy.
        
        self.ui.update_logbook(initial_set) # Call with same set
        self.assertEqual(self.ui.discovered_animals_cache, initial_cache, 
                         "Cache string should remain identical if the set hasn't changed.")
        # This test implicitly checks that font.render was not called again unnecessarily,
        # assuming discovered_animals_cache is only updated when a re-render happens.

    def test_draw_runs_without_error(self):
        """Test that the draw method runs without raising exceptions."""
        try:
            # Ensure logbook is updated first so surface is properly initialized
            self.ui.update_logbook({"test_animal"}) 
            self.ui.draw(TestUI.screen) # Use the class-level screen
        except Exception as e:
            self.fail(f"ui.draw() raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
