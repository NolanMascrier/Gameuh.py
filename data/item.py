"""An item is something that can be held by
characters and used."""

import pygame
from data.constants import Flags, trad, SYSTEM
from data.image.image import Image
from data.image.animation import Animation
from data.image.text import Text

class Item():
    """Creates an item.
    
    Args:
        name (str): name of the item.
        base (str): Name of the base of the item.
        max_held(int, optionnal): Maximum amount of the \
        item that can be held in a single inventory slot. \
        Defaults to 64.
        image (Image|Animation, optionnal): Image of the item.\
        Defaults to None.
        rarity (int, optionnal): Rarity of the item. Defaults to\
        0 (normal). Can be 1 (magic), 2 (rare) or 3 (legendary)
        flags (list, optionnal): List of the items's flags. \
        Defaults to [].
        affixes (list, optionnal): List of the item's affixes,\
        aka its effects. Defaults to [].
    """
    def __init__(self, name, base, price, power, max_held = 64,\
        image:Image|Animation = None, rarity = 0,\
        flags = None, affixes = None):
        self._name = name
        self._base = base
        self._max_held = max_held
        self._price = price
        self._power = power
        self._image = image
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        if affixes is None:
            self._affixes = []
        else:
            self._affixes = affixes
        self._rarity = rarity
        self._popup = self.create_popup()

    def on_use(self, target):
        """Uses the item on the creature."""
        if Flags.GEAR in self._flags:
            return
        if Flags.CONSUMABLE in self._flags:
            if Flags.LIFE in self._flags:
                target.heal(self._power)
            if Flags.MANA in self._flags:
                target.restore_mana(self._power)
        else:
            return

    def describe(self):
        """Returns a text description of the item."""
        text = ""
        for affx in self._affixes:
            text += f"{affx.describe()}\n"
        return text

    def create_popup(self) -> pygame.Surface:
        """Creates the popup surface."""
        affixes = Text(self.describe(), True, force_x=250)
        text = f"{self._name}\n{trad('rarities', self._rarity)}{self._base}"
        title = Text(text, True, force_x=affixes.width)
        sfc = pygame.Surface((affixes.width + 10, affixes.height + title.height + 10),\
                            pygame.SRCALPHA)
        match self._rarity:
            case 1:
                sfc.blit(SYSTEM["images"]["ui_magic"].clone()\
                    .scale(title.height + 10, title.width + 10).image, (0, 0))
            case 2:
                sfc.blit(SYSTEM["images"]["ui_rare"].clone()\
                    .scale(title.height + 10, title.width + 10).image, (0, 0))
            case 3:
                sfc.blit(SYSTEM["images"]["ui_legendary"].clone()\
                    .scale(title.height + 10, title.width + 10).image, (0, 0))
            case _:
                sfc.blit(SYSTEM["images"]["ui_normal"].clone()\
                    .scale(title.height + 10, title.width + 10).image, (0, 0))
        sfc.blit(SYSTEM["images"]["hoverable"].clone().scale(affixes.height,\
                                                            affixes.width + 10).image,\
                                                            (0, title.height + 10))
        sfc.blit(title.surface, (5, 5))
        sfc.blit(affixes.surface, (5, title.height + 20))
        return sfc

    def get_image(self):
        """returns the item's image."""
        if self._image is None:
            return None
        return self._image

    @property
    def name(self):
        """Returns the item's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        """Returns the item's price."""
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def power(self):
        """Return the item's power."""
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def max_held(self) -> int:
        """Returns the item's max holdable value."""
        return self._max_held

    @max_held.setter
    def max_held(self, value):
        self._max_held = value

    @property
    def flags(self):
        """Returns the item's flag list."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def affixes(self):
        """Returns the item's affixes."""
        return self._affixes

    @affixes.setter
    def affixes(self, value):
        self._affixes = value

    @property
    def rarity(self):
        """Return's the item rarity."""
        return self._rarity

    @rarity.setter
    def rarity(self, value):
        self._rarity = value

    @property
    def popup(self) -> pygame.Surface:
        """Returns the popup."""
        return self._popup
