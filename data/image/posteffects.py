"""Handles image post treatment."""

import pygame
import numpy
from data.constants import SYSTEM, SCREEN_WIDTH

BLACK = (0,0,0)

class PostEffects():
    """Handle whole screen effects."""
    def __init__(self):
        self._timer = 0
        self._shake_x = 0
        self._shake_y = 0
        self._max_x = 0
        self._max_y = 0
        self._direction_x = 1
        self._direction_y = 1
        self._intensity = 0
        self._pause = 0
        self._shaking = False
        self._simple_shaking = False
        self._flash_max = 0
        self._flash_timer = 0
        self._flash_opacity = 0
        self._flash_surface = pygame.Surface((SYSTEM["options"]["screen_resolution"][0],\
            SYSTEM["options"]["screen_resolution"][1]), pygame.SRCALPHA)

    def hitstop(self, timer):
        """Sets a hitstop for timer frames."""
        self._pause = int(timer)

    def shake(self, x, y, duration: int = 120):
        """Sets a simple shake of x;y intensity."""
        duration *= SYSTEM["options"]["fps"] / 60
        self._max_x = x
        self._max_y = y
        self._shaking = True
        self._simple_shaking = True
        self._timer = duration

    def flash(self, color, duration: int = 120):
        """Flashs the screen for a duration."""
        duration *= SYSTEM["options"]["fps"] / 60
        self._flash_timer = duration
        self._flash_max = duration
        self._flash_opacity = 150
        self._flash_surface.fill(color)
        self._flash_surface.set_alpha(self._flash_opacity)

    def tick(self):
        """Applies the effects."""
        if self._pause > 0:
            self._pause -= 1
        if self._shaking and self._simple_shaking:
            if self._max_x > 0:
                self._shake_x = numpy.random.randint(-self._max_x, self._max_x)
            if self._max_y > 0:
                self._shake_y = numpy.random.randint(-self._max_y, self._max_y)
            self._timer -= 1
            if self._timer <= 0:
                self._shaking = False
                self._simple_shaking = False
                self._shake_x = 0
                self._shake_y = 0
                self._max_x = 0
                self._max_y = 0
        SYSTEM["clock"].tick(SYSTEM["options"]["fps"])
        SYSTEM["text_generator"].generate_fps()
        if SYSTEM["fps_counter"] is not None and SYSTEM["options"]["show_fps"]:
            SYSTEM["windows"].blit(SYSTEM["fps_counter"].surface,\
                                (SCREEN_WIDTH - SYSTEM["fps_counter"].width, 0))
        window = pygame.transform.scale(SYSTEM["windows"],\
                (SYSTEM["options"]["screen_resolution"][0],\
                 SYSTEM["options"]["screen_resolution"][1]))
        SYSTEM["real_windows"].fill(BLACK)
        SYSTEM["real_windows"].blit(window, (self._shake_x, self._shake_y))
        if self._flash_timer > 0:
            self._flash_timer -= 1
            self._flash_opacity = int(self._flash_timer / self._flash_max * 255)
            self._flash_surface.set_alpha(self._flash_opacity)
            SYSTEM["real_windows"].blit(self._flash_surface, (0, 0))
        pygame.display.flip()

    @property
    def pause(self):
        """Returns the processor's pause status."""
        return self._pause > 0
