"""Camera"""

from data.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    """Manages the game camera in world space."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

    def update(self, target_x, target_y, world_width, world_height):
        """Update camera to follow target, constrained to world bounds."""
        self.x = min(max(0, target_x - self.width // 2), world_width - self.width)
        self.y = min(max(0, target_y - self.height // 2), world_height - self.height)

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return (screen_x, screen_y)

    def screen_to_world(self, screen_x, screen_y):
        """Convert screen coordinates to world coordinates."""
        world_x = screen_x + self.x
        world_y = screen_y + self.y
        return (world_x, world_y)
