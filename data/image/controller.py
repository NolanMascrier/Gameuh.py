"""Blabla"""

from data.image.sprite import Sprite

class AnimationController:
    """Lightweight wrapper that references shared animation data but maintains
    independent playback state."""

    __slots__ = ('_shared_animation', '_current_frame', '_finished',
                 '_frame_accumulator', '_current_key', '_flipped', '_flip_anim')

    def __init__(self, shared_animation):
        """
        Args:
            shared_animation: Reference to the shared Animation/Sprite object
        """
        self._shared_animation = shared_animation
        self._current_frame = 0.0
        self._finished = False
        self._frame_accumulator = 0.0
        self._current_key = None
        self._flipped = False
        if isinstance(shared_animation, Sprite):
            self._current_key = shared_animation._keys[0]

    def tick(self, frame_modifier=1):
        """Advance this instance's animation state."""
        if isinstance(self._shared_animation, Sprite):
            self._tick_sprite(frame_modifier)
        else:
            self._tick_animation(frame_modifier)

    def _tick_animation(self, frame_modifier):
        """Tick for simple Animation."""
        anim = self._shared_animation
        if not anim.animated:
            return

        start_frame = anim.frame_loop[0] if anim.frame_loop else 0
        end_frame = anim.frame_loop[1] if anim.frame_loop else anim.frame_max

        self._current_frame += anim.frame_rate * frame_modifier

        if self._current_frame > end_frame:
            if anim.loops:
                self._current_frame = start_frame
            else:
                self._finished = True
                self._current_frame = end_frame

    def _tick_sprite(self, frame_modifier):
        """Tick for Sprite."""
        sprite = self._shared_animation
        if self._current_key not in sprite.animations:
            return

        anim = sprite.animations[self._current_key]

        start_frame = anim.frame_loop[0] if anim.frame_loop else 0
        end_frame = anim.frame_loop[1] if anim.frame_loop else anim.frame_max

        self._current_frame += anim.frame_rate * frame_modifier

        if self._current_frame > end_frame:
            if anim.loops:
                self._current_frame = start_frame
            elif sprite.loop_times[self._current_key] < 0:
                self.play(sprite.keys[0])
            elif sprite.loop_times[self._current_key] > 0:
                self._current_frame = start_frame
                sprite.loop_times[self._current_key] -= 1
            else:
                self._finished = True
                self._current_frame = end_frame

    def play(self, key):
        """Play a specific animation (for sprites)."""
        if isinstance(self._shared_animation, Sprite):
            if key in self._shared_animation.animations:
                self._current_key = key
                self._current_frame = 0.0
                self._finished = False

    def reset(self):
        """Reset animation to start."""
        self._current_frame = 0.0
        self._finished = False

    def get_image(self):
        """Get current frame image."""
        if isinstance(self._shared_animation, Sprite):
            anim = self._shared_animation.animations[self._current_key]
            return anim.get_image([self._current_frame])
        return self._shared_animation.get_image([self._current_frame])

    def detach(self, key, x, y, center=False):
        """Detach an animation (for sprites)."""
        if isinstance(self._shared_animation, Sprite):
            self._shared_animation.detach(key, x, y, center)

    def flip(self, flipped):
        """Track flip state (don't modify shared data)."""
        self._flipped = flipped

    @property
    def w(self):
        """Returns the w"""
        return self._shared_animation.w

    @property
    def h(self):
        """Returns the w"""
        return self._shared_animation.h

    @property
    def finished(self):
        """Returns the w"""
        return self._finished

    @property
    def frame(self):
        """Returns the w"""
        return self._current_frame
