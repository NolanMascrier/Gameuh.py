from data.constants import *

"""Stealth py update for the workflow, this file will be deleted
anyway"""

class Fireball():
    def __init__(self, x, y, angle):
        self._x = x
        self._y = y
        self._speed = 15
        self._angle = angle
        self._length = 75
        self._height = 35
        self._image = pygame.image.load(FIREBALL_IMAGE).convert_alpha()
        if angle == 270 or angle == 90:
            self._rect = pygame.transform.rotate(pygame.transform.scale(self._image, (self._length, self._height)), -angle)
        else:
            self._rect = pygame.transform.rotate(pygame.transform.scale(self._image, (self._length, self._height)), angle)

    def can_be_destroyed(self):
        if self._y < 0 - self._rect.get_rect().bottom:
            return True
        if self._y > SCREEN_HEIGHT + self._rect.get_rect().top:
            return True
        if self._x < 0 - self._rect.get_rect().left:
            return True
        if self._x > SCREEN_WIDTH + self._rect.get_rect().right:
            return True
        return False
    
    def tick(self):
        angle = radians(self._angle)
        self._x = round(self._x + self._speed * cos(angle))
        self._y = round(self._y + self._speed * sin(angle))
        if self.can_be_destroyed():
            PROJECTILE_TRACKER.remove(self)

    def get_pos(self):
        return (self._x, self._y)