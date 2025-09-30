"""An entity is something that physically exists in the game
world. It has a position, an image and an hitbox."""

import json
import numpy
from data.constants import SYSTEM, SCREEN_HEIGHT, SCREEN_WIDTH
from data.physics.hitbox import HitBox
from data.image.sprite import Sprite

class Entity():
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
    def __init__(self, x, y, imagefile: str, hitbox:HitBox = None,\
                move_speed = 1, hitbox_mod = None):
        self._x = x
        self._y = y
        self._x_def = x
        self._y_def = y
        self._image = imagefile
        if imagefile is None:
            self._real_image = None
        else:
            self._real_image = SYSTEM["images"][self._image].clone()
        if hitbox is not None:
            self._hitbox = hitbox
        elif self._real_image is not None:
            self._hitbox = HitBox(x, y, self._real_image.w, self._real_image.h)
        else:
            self._hitbox = None
        if hitbox_mod is not None:
            self._hitbox.resize(hitbox_mod, self._real_image.scale_factor)
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
        self._animation_state = [0, False]
        self._sprite = isinstance(self._real_image, Sprite)

    def tick(self, character, speed_mod = 1):
        """Ticks down the entity."""
        self._real_image.tick()
        base_speed = character.creature.stats["speed"].c_value * speed_mod
        self._move_speed = base_speed
        if self._dashing:
            if self._dash_time <= 0:
                self._dashing = False
            self._dash_time -= float(0.016)
            self._x += self._dash_dx
            self._y += self._dash_dy
        if self._x < 0 or self._x > SCREEN_WIDTH - SYSTEM["images"][self._image].width or\
            self._y < 0 or self._y > SCREEN_HEIGHT - SYSTEM["images"][self._image].height:
            self._dashing = False
        self._x = max(0, min(self._x, SCREEN_WIDTH - SYSTEM["images"][self._image].width))
        self._y = max(0, min(self._y, SCREEN_HEIGHT - SYSTEM["images"][self._image].height))
        self._hitbox.move_center(self.center)

    def reset(self):
        """Resets the entity."""
        self._x = self._x_def
        self._y = self._y_def
        self._keys = []
        self._flipped = False
        self._hitbox.move_center(self.center)

    def get_image(self):
        """Returns the current image."""
        return self._real_image.get_image()

    def move(self, pos):
        """Moves the entity toward the x;y position."""
        if self._x < pos[0]:
            self._x += self._move_speed * 3
        if self._x > pos[0]:
            self._x -= self._move_speed * 3
        if self._y < pos[1]:
            self._y += self._move_speed
        if self._y > pos[1]:
            self._y -= self._move_speed
        self._hitbox.move_center(self.center)

    def displace(self, pos):
        """Moves the entity toward the x;y position."""
        if self._dashing:
            return
        self.x = pos[0]
        self.y = pos[1]
        self._hitbox.move_center(self.center)

    def dash(self, distance, dash_time = 0.4):
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

    def flip(self):
        """Flips the image."""
        self._flipped = not self._flipped

    def export(self) -> str:
        """Serializes the entity as JSON."""
        data = {
            "type": "entity",
            "image": self._image,
            "hit_box_w": self._hitbox.width,
            "hit_box_h": self._hitbox.height,
            "move_speed": self._move_speed
        }
        return json.dumps(data)

    def play(self, key):
        """Plays an animation."""
        if self._sprite:
            self._real_image.play(key)

    def detach(self, key, center = False):
        """Detach an animation."""
        if self._sprite:
            self._real_image.detach(key, self._x, self._y, center)

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
    def x(self):
        """Returns the entity's x position."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """Returns the entity's y position."""
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def right(self):
        """Returns the entity right side."""
        return self.hitbox.right

    @property
    def max_frame(self):
        """Returns the entity's animation amount of frames."""
        return self._max_frame

    @max_frame.setter
    def max_frame(self, value):
        self._max_frame = value

    @property
    def hitbox(self):
        """Returns the entity's hitbox."""
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        self._hitbox = value

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

    @property
    def center(self):
        """Returns the entity's center."""
        x = self._x + SYSTEM["images"][self._image].width / 2
        y = self._y + SYSTEM["images"][self._image].height / 2
        return (x, y)
