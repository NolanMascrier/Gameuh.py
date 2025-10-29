"""An entity is something that physically exists in the game
world. It has a position, an image and an hitbox."""

import json
import numpy
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH
from data.physics.hitbox import HitBox
from data.image.sprite import Sprite
from data.image.controller import AnimationController

class Entity(HitBox):
    """Defines an entity.
    
    Args:
        x (float): x position of the entity.
        y (float): y position of the entity.
        image (Surface|list) : Image surface or spriteset of \
        the entity. Autmatically detects if it's a spriteset.
        hitbox (HitBox): Hitbox of the entity.
        frame_rate (float, optionnal): delay between each update\
        of the animation. Delays to 0.25.
        move_speed (float, optionnal): speed at which the entity\
        moves. Defaults to 1.
    """
    __slots__ = '_image', '_real_image', "_x_def", "_y_def", "_move_speed", "_keys", "_flipped", \
                "_angle", "_dash_speed", "_dashing", "_x_dest", "_y_dest", "_dash_dx", "_dash_dy", \
                "_dash_time", "_sprite", "_animation_controller"
    def __init__(self, x, y, imagefile: str, hitbox:HitBox = None,\
                move_speed = 1, hitbox_mod = None):
        self._image = imagefile
        if imagefile is None:
            self._real_image = None
            w = 0
            h = 0
        else:
            self._real_image = SYSTEM["images"][imagefile]
            flipped_key = f"{imagefile}_flipped"
            flipped_image = SYSTEM["images"].get(flipped_key, None)
            self._animation_controller = AnimationController(self._real_image, flipped_image)
            w = self._real_image.w
            h = self._real_image.h
        if hitbox is not None:
            super().__init__(hitbox.x, hitbox.y, hitbox.width, hitbox.height)
        else:
            super().__init__(x, y, w, h)
        self._x_def = x
        self._y_def = y
        if hitbox_mod is not None:
            self.resize(hitbox_mod, self._real_image.scale_factor)
        self._move_speed = move_speed
        self._keys = []
        self._flipped = False
        self._angle = 0
        self._dash_speed = 1.35
        self._dashing = False
        self._x_dest = None
        self._y_dest = None
        self._dash_dx = 0
        self._dash_dy = 0
        self._dash_time = 0
        self._sprite = isinstance(self._real_image, Sprite)

    def tick(self, character, speed_mod = 1):
        """Ticks down the entity."""
        self._animation_controller.tick()
        base_speed = character.creature.stats["speed"].c_value * speed_mod
        self._move_speed = base_speed
        if self._dashing:
            if self._dash_time <= 0:
                self._dashing = False
            self._dash_time -= float(0.016)
            self.x += self._dash_dx
            self.y += self._dash_dy
        if self.x < 0 or self.x > SCREEN_WIDTH - SYSTEM["images"][self._image].width or\
            self.y < 0 or self.y > SCREEN_HEIGHT - SYSTEM["images"][self._image].height:
            self._dashing = False
        self.x = max(0, min(self.x, SCREEN_WIDTH - SYSTEM["images"][self._image].width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - SYSTEM["images"][self._image].height))
        self.move_center(self.center)

    def reset(self):
        """Resets the entity."""
        self.x = self._x_def
        self.y = self._y_def
        self._keys = []
        self._flipped = False
        self.move_center(self.center)

    def get_image(self):
        """Returns the current image."""
        return self._animation_controller.get_image()

    def move(self, pos):
        """Moves the entity toward the x;y position."""
        if self.x < pos[0]:
            self.x += self._move_speed * 3
        if self.x > pos[0]:
            self.x -= self._move_speed * 3
        if self.y < pos[1]:
            self.y += self._move_speed
        if self.y > pos[1]:
            self.y -= self._move_speed
        self.move_center(self.center)

    def displace(self, pos):
        """Moves the entity toward the x;y position."""
        if self._dashing:
            return
        self.x = pos[0]
        self.y = pos[1]

    def dash(self, distance, dash_time = 0.2):
        """dash a certain distance depending on the last input angle."""
        self._dash_dx = numpy.cos(self._angle)
        self._dash_dy = numpy.sin(self._angle)
        length = (self._dash_dx ** 2 + self._dash_dy ** 2) ** 0.5
        if length != 0:
            self._dash_dx /= length
            self._dash_dy /= length
        velocity = distance / dash_time
        self._dash_dx *= velocity
        self._dash_dy *= velocity
        self._dash_time = dash_time
        self._dashing = True

    def flip(self, flips = None):
        """Flips the image."""
        if self._animation_controller:
            if flips is None:
                self._flipped = not self._flipped
                self._animation_controller.flip(self._flipped)
            else:
                self._flipped = flips
                self._animation_controller.flip(self._flipped)
        else:
            if flips is None:
                self._flipped = not self._flipped
                self._real_image.flip(False, self._flipped)
            else:
                self._flipped = flips
                self._real_image.flip(False, self._flipped)

    def export(self) -> str:
        """Serializes the entity as JSON."""
        data = {
            "type": "entity",
            "image": self._image,
            "hit_box_w": self.width,
            "hit_box_h": self.height,
            "move_speed": self._move_speed
        }
        return json.dumps(data)

    def play(self, key):
        """Plays an animation."""
        self._animation_controller.play(key)

    def detach(self, key, center = False):
        """Detach an animation."""
        self._animation_controller.detach(key, self.center_x, self.center_y, center)

    @staticmethod
    def imports(data):
        """Creates a entity from a json data array."""
        return Entity(
            0, 0,
            data["image"],
            HitBox(10, SCREEN_HEIGHT/2, int(data["hit_box_w"]), int(data["hit_box_h"])),
            float(data["move_speed"])
        )

    @property
    def hitbox(self):
        """Returns the entity's hitbox."""
        return self

    @property
    def move_speed(self):
        """Returns the entity's move speed."""
        return self._move_speed

    @move_speed.setter
    def move_speed(self, value):
        self._move_speed = value

    @property
    def real_image(self):
        """Returns the entity's image instance."""
        return self._real_image

    @real_image.setter
    def real_image(self, value):
        self._real_image = value

    @property
    def flipped(self):
        """Returns whether or not the image has been flipped."""
        return self._flipped

    @flipped.setter
    def flipped(self, value):
        self._flipped = value

    @property
    def angle(self):
        """Returns the entity's angle. Useful only for players."""
        return self._angle

    @angle.setter
    def angle(self, value):
        if not self._dashing:
            self._angle = value
