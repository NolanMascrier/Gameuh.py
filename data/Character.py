from data.constants import *
from data.Fireball import Fireball
from data.physics.hitbox import HitBox

class Character():
    def __init__(self):
        self._x = 50
        self._y = 50
        self._hitbox = (0, 0)
        self._rect = None
        self._sprite = None
        self._image = None
        self._direction = K_DOWN
        self._index = 0
        self._speed = 12
        self._box = HitBox(self._x + 30, self._y + 10, 25, 70)
        self._hitbox = (10, 15)
        self._hitbox_size = (30, 70)
        self._cooldown = 0
        self._max_cooldown = 2
        self._life = 100
        self._mana = 100

    def get_hitbox(self):
        x = self._x + self._hitbox[0]
        y = self._y + self._hitbox[1]
        return (x, y)

    def get_pos(self):
        return (self._x, self._y)

    def get_sprite(self):
        return self._sprite[self._direction][self._index]

    def tick(self):
        self._box.move((self._x + 50, self._y + 30))
        if self._life > 100:
            self._life = 100
        if self._mana > 100:
            self._mana = 100
        if self._cooldown > 0:
            self._cooldown -= 1
        if self.cooldown <= 0 and self._mana < 100:
            self.mana += 0.1

    def shoot_fireball(self):
        orig_x = self.left()
        orig_y = self.top() + self._box.height / 2
        if self._cooldown <= 0 and self._mana >= 10:
            fire = Fireball(orig_x, orig_y, 0, len=32, height=32)
            PROJECTILE_TRACKER.append(fire)
            self._cooldown = 5
            self._max_cooldown = 5
            self._mana -= 2

    def action(self, keys):
        """"""
        if keys[K_LEFT] or keys[K_a]:
            if self.left() >= self._speed:
                self._x -= self._speed
                self._direction = K_LEFT
                self._index = (self._index+1) % 4
        if keys[K_RIGHT] or keys[K_d]:
            if self.right() <= SCREEN_WIDTH - self._speed:
                self._x += self._speed
                self._direction = K_RIGHT
                self._index = (self._index+1) % 4
        if keys[K_UP] or keys[K_w]:
            if self.top() >= self._speed:
                self._y -= self._speed
                self._direction = K_UP
                self._index = (self._index+1) % 4
        if keys[K_DOWN] or keys[K_s]:
            if self.bottom() <= SCREEN_HEIGHT - self._speed:
                self._y += self._speed
                self._direction = K_DOWN
                self._index = (self._index+1) % 4
        if keys[K_q]:
            self.shoot_fireball()

    def top(self):
        return self._box.top

    def bottom(self):
        return self._box.bottom

    def left(self):
        return self._box.left
    
    def right(self):
        return self._box.right

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        self._sprite = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    @property
    def max_cooldown(self):
        return self._max_cooldown

    @max_cooldown.setter
    def max_cooldown(self, value):
        self._max_cooldown = value

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        self._mana = value
    
    @property
    def hitbox_size(self):
        return self._hitbox_size

    @hitbox_size.setter
    def hitbox_size(self, value):
        self._hitbox_size = value
