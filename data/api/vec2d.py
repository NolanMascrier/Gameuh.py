"""2D Vector class to replace pygame's."""

import pygame

class Vec2(pygame.Vector2):
    """Replace a pygame 2D vector."""
    def normalize(self):
        """Return the normalized vector."""
        norm = self.length()
        return self if norm == 0 else super().normalize()

    def to_tuple(self):
        """Returns the vector's as a tuple."""
        return (self.x, self.y)
