"""An item is something that can be held by
characters and used."""

import random
import pygame
from data.constants import Flags, trad, SYSTEM
from data.image.image import Image
from data.image.animation import Animation
from data.image.text import Text

AFF_RARITY_TABLE = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
    4: 2,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 4
}

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
    def __init__(self, name:str, base:str, price, power, max_held = 64,\
        image:Image|Animation = None, rarity = 0,\
        flags = None, affixes = None, implicits = None):
        self._name = name
        self._base = base
        self._max_held = max_held
        self._price = price
        self._power = power
        self._image = image.clone()
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        if affixes is None:
            self._affixes = []
        else:
            self._affixes = affixes
        if implicits is None:
            self._implicits = []
        else:
            self._implicits = implicits
        self._rarity = rarity
        self._popup = None
        self._popup_details = None
        self.create_popup()
        self.create_popup_details()
        self._sealed = False
        self._level = 0

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

    def copy(self):
        """Returns a copy of the item."""
        return Item(
            self._name,
            self._base,
            self._price,
            self._power,
            self._max_held,
            self._image,
            self._rarity,
            self._flags.copy(),
            self._affixes.copy(),
            self._implicits.copy()
        )

    def describe(self):
        """Returns a text description of the item."""
        text = ""
        if len(self._implicits) > 0:
            for affx in self._implicits:
                text += f"{affx.describe()}\n"
            text += "_______________\n"
        for affx in self._affixes:
            text += f"{affx.describe()}\n"
        return text

    def describe_details(self):
        """Returns a detailed text description of the item."""
        text = ""
        if len(self._implicits) > 0:
            for affx in self._implicits:
                text += f"{affx.describe_details()}\n"
            text += "_______________\n"
        for affx in self._affixes:
            text += f"{affx.describe_details()}\n"
        return text

    def create_popup(self):
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
        self._popup = sfc

    def create_popup_details(self):
        """Creates the detailed popup surface."""
        affixes = Text(self.describe_details(), True, force_x=250)
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
        self._popup_details = sfc

    def __get_gear_flags(self):
        """Returns which gear flag the item uses."""
        for f in self._flags:
            if f in [Flags.BOOTS, Flags.HELM, Flags.HANDS, Flags.ARMOR,\
                Flags.RING, Flags.RELIC, Flags.AMULET, Flags.BELT,\
                Flags.OFFHAND, Flags.WEAPON]:
                return f.value

    def apply_rune(self):
        """Applies the rune contained in the system."""
        if SYSTEM["rune"] == 0:
            if self.scour():
                pass
                #SYSTEM["player"].runes[0] -= 1
        elif SYSTEM["rune"] == 1 and self._rarity == 0:
            self.rarify()
        elif SYSTEM["rune"] == 2:
            self.exalt()
        elif SYSTEM["rune"] == 3:
            self.reroll_values()
        elif SYSTEM["rune"] == 4:
            self.lock()
        elif SYSTEM["rune"] == 5 and self._rarity == 2:
            self.try_upgrade()
        elif SYSTEM["rune"] == 6 and self._rarity == 2:
            self.chaos()
        elif SYSTEM["rune"] == 7 and self._rarity == 0:
            self.enchant()
        elif SYSTEM["rune"] == 8 and self._rarity == 1:
            self.regal()
        elif SYSTEM["rune"] == 9 and self._rarity == 1:
            self.alteration()

    def reroll_values(self):
        """Reroll the numerical values of the affixes.
        ie Divine Orb
        
        Returns:
            bool: Whether or not the item was changed."""
        sealed = 0
        for aff in self._affixes:
            if aff.sealed:
                sealed += 1
        if sealed == len(self._affixes):
            return False
        for aff in self._affixes:
            aff.reroll()
        self.create_popup()
        self.create_popup_details()
        return True

    def lock(self):
        """Locks an affix; preventing it from being ever changed.
        
        Returns:
            bool: Whether or not the item was changed."""
        sealed = 0
        for aff in self._affixes:
            if aff.sealed:
                sealed += 1
        if sealed > 0:
            return False
        while True:
            roll = random.randint(0, len(self._affixes) - 1)
            if not self._affixes[roll].sealed:
                self._affixes[roll].seal(True)
                break
        self.create_popup()
        self.create_popup_details()
        return True

    def scour(self):
        """Removes all non sealed affixes from the item.
                
        Returns:
            bool: Whether or not the item was changed."""
        size = len(self._affixes)
        for aff in self._affixes.copy():
            if not aff.sealed:
                self._affixes.remove(aff)
        if len(self._affixes) == size:
            return False
        self._rarity = AFF_RARITY_TABLE[len(self._affixes)]
        self.create_popup()
        self.create_popup_details()
        return True

    def rarify(self):
        """Transforms the item into a rare item."""
        self._rarity = 2
        roll = random.randint(3 - len(self._affixes), 6)
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                                            roll, self._level, self._affixes)]
        self._affixes.extend(affixes)
        self.create_popup()
        self.create_popup_details()
        return True

    def exalt(self):
        """Adds a single modifier to an item."""
        mods = len(self._affixes)
        if AFF_RARITY_TABLE[mods + 1] > self._rarity:
            return False
        affix = SYSTEM["looter"].generate_affixes(self.__get_gear_flags(), 1,\
                                    self._level, self._affixes)[0].roll()
        self._affixes.append(affix)
        self.create_popup()
        self.create_popup_details()
        return True

    def try_upgrade(self):
        """Attemps to make a rare item into an exalted item.
        Scours the item if it fails."""
        roll = random.randint(0, 1)
        if roll == 0:
            return self.scour()
        mods = len(self._affixes)
        roll = random.randint(7, 8)
        roll -= mods
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level, self._affixes)]
        self._affixes.extend(affixes)
        self._rarity = 3
        self.create_popup()
        self.create_popup_details()
        return True

    def chaos(self):
        """Reroll a rare item."""
        roll = random.randint(3, 6)
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level)]
        self._affixes = affixes
        self.create_popup()
        self.create_popup_details()
        return True

    def enchant(self):
        """Makes a blank item magic."""
        mods = len(self._affixes)
        roll = random.randint(1, 2)
        roll -= mods
        if roll <= 0:
            return False #should never happen anyway
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level, self._affixes)]
        self._rarity = 1
        self._affixes.extend(affixes)
        self.create_popup()
        self.create_popup_details()
        return True

    def regal(self):
        """Makes a magic item rare."""
        mods = len(self._affixes)
        roll = 3 - mods
        if roll <= 0:
            return False #should never happen anyway
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level, self._affixes)]
        self._rarity = 2
        self._affixes.extend(affixes)
        self.create_popup()
        self.create_popup_details()
        return True

    def alteration(self):
        """Rerolls a magic item."""
        roll = random.randint(1, 2)
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level)]
        self._affixes = affixes
        self.create_popup()
        self.create_popup_details()

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
    def base(self):
        """Returns the item's base."""
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

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
    def implicits(self):
        """Returns the item's implicits."""
        return self._implicits

    @implicits.setter
    def implicits(self, value):
        self._implicits = value

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

    @property
    def popup_details(self) -> pygame.Surface:
        """Returns the detailed popup."""
        return self._popup_details

    @property
    def sealed(self) -> bool:
        """Returns whether or not the item is sealed; ie
        one of its affix is locked."""
        return self._sealed
