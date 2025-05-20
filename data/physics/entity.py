"""An entity is something that physically exists in the game
world. It has a position, an image and an hitbox."""

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
    def __init__(self, x, y, image, hitbox, frame_rate = 0.25, move_speed = 1):
        self._x = x
        self._y = y
        self._image = image
        if isinstance(image, list):
            self._animated = True
            self._max_frame = len(image)
        else:
            self._animated = False
            self._max_frame = 1
        self._hitbox = hitbox
        self._frame_rate = frame_rate
        self._frame = 0
        self._move_speed = move_speed

    def tick(self, player):
        """Ticks down the entity. Does nothing by default and needs
        to be overriden."""

    def get_image(self):
        """Returns the current image."""
        if self._animated:
            return self._image[int(self._frame) % self._max_frame]
        return self._image

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
        self._hitbox.move((self._x, self._y))

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
    def frame_rate(self):
        """Returns the entity's frame rate."""
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, value):
        self._frame_rate = value
