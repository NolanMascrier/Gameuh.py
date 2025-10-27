"""Handles image post treatment."""

import numpy

from data.api.surface import Surface, flip

from data.constants import SYSTEM, SCREEN_WIDTH, ANIMATION_TICK_TRACKER, SCREEN_HEIGHT, BLACK_TRANSP

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
        self._flash_surface = Surface(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._scaled_cache = None
        self._cached_resolution = None

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

    def stop_shaking(self):
        """force Stops the shaking."""
        self._shaking = False
        self._simple_shaking = False
        self._shake_x = 0
        self._shake_y = 0
        self._max_x = 0
        self._max_y = 0

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
        for f in ANIMATION_TICK_TRACKER:
            f.tick()
        if self._pause > 0:
            self._pause -= 1
        if self._shaking and self._simple_shaking:
            if self._max_x > 0:
                self._shake_x = numpy.random.randint(-self._max_x, self._max_x)
            if self._max_y > 0:
                self._shake_y = numpy.random.randint(-self._max_y, self._max_y)
            self._timer -= 1
            if self._timer <= 0:
                self.stop_shaking()
        SYSTEM["clock"].tick(SYSTEM["options"]["fps"])
        SYSTEM["text_generator"].generate_fps()
        current_res = SYSTEM["options"]["screen_resolution"]
        if current_res != (SCREEN_WIDTH, SCREEN_HEIGHT):
            if self._cached_resolution != current_res or self._scaled_cache is None:
                self._cached_resolution = current_res
                if self._scaled_cache is None:
                    self._scaled_cache = Surface(current_res[0], current_res[1])
            scaled = SYSTEM["windows"].scale(current_res)
            SYSTEM["real_windows"].blit(scaled, (0, 0))
        else:
            SYSTEM["real_windows"].blit(SYSTEM["windows"], (0, 0), True)
        if self._flash_timer > 0:
            self._flash_timer -= 1
            self._flash_opacity = int(self._flash_timer / self._flash_max * 255)
            self._flash_surface.set_alpha(self._flash_opacity)
        flip()

    @property
    def pause(self):
        """Returns the processor's pause status."""
        return self._pause > 0

    @property
    def shake_factor(self):
        """Returns the shake factor."""
        return self._shake_x, self._shake_y

    @property
    def flash_surface(self):
        """FLASHDANCE"""
        return self._flash_surface

    @flash_surface.setter
    def flash_surface(self, value):
        self._flash_surface = value

    @property
    def flash_timer(self):
        """Returns the flash's timer."""
        return self._flash_timer

    @flash_timer.setter
    def flash_timer(self, value):
        self._flash_timer = value
