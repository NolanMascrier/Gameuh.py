"""An item is something that can be held by
characters and used."""

import json
import time
import random

from data.api.surface import Surface

from data.constants import Flags, trad, SYSTEM
from data.image.image import Image
from data.image.animation import Animation
from data.image.text import Text
from data.numerics.double_affix import DoubleAffix
from data.numerics.affix import Affix

AFF_RARITY_TABLE = {
    0: 0,
    1: 1,
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
    __slots__ = '_name', '_base', '_max_held', '_price', '_base_price', '_power', '_image', \
                '_flags', '_affixes', '_implicits', '_rarity', '_sealed', '_drop_time', '_popup', \
                '_popup_details', '_level'
    def __init__(self, name:str, base:str, price, power = 0, max_held = 64,\
        image:Image|Animation = None, rarity = 0,\
        flags = None, affixes = None, implicits = None):
        self._name = name
        self._base = base
        self._max_held = max_held
        self._price = price
        self._base_price = price
        self._power = power
        if image is None:
            self._image = None
        else:
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
        self._rarity = int(rarity)
        self._sealed = False
        self._level = 0
        self._drop_time = 0
        self._popup = self.create_popup()
        self._popup_details = self.create_popup(True)

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
            self._flags,
            [affix.copy() for affix in self._affixes] if self._affixes else None,
            [implicit.copy() for implicit in self._implicits] if self._implicits else None
        )

    def describe(self):
        """Returns a text description of the item."""
        text = ""
        if len(self._implicits) > 0:
            for affx in self._implicits:
                text += f"{affx.describe()}\n"
            if len(self._affixes) > 0:
                text += "\n"
        for affx in self._affixes:
            text += f"{affx.describe()}\n"
        return text

    def generate_name(self):
        """Generates a random name."""
        names_data = trad("item_names")
        match self._rarity:
            case 0:
                prefix = random.choice(names_data["0"])
                self._name = f"{prefix} {self._base}"
            case 1:
                affix = self._affixes[0]
                suffix = names_data["1"].get(affix.name, affix.name)
                self._name = f"{self._base} of {suffix}"
            case 2 | 3:
                name_pool = names_data["2"]
                key1 = self._affixes[0].flag_key
                key2 = self._affixes[1].flag_key
                word1 = random.choice(name_pool.get(key1, [key1]))[0]
                word2 = random.choice(name_pool.get(key2, [key2]))[1]
                self._name = f"{word1.capitalize()} {word2.capitalize()}"
            case _:
                return

    def update(self):
        """Updates the name and the price of the item."""
        self._price = self._base_price * (1 + self._rarity * 1.2) * (1 + self._level * 0.1)
        for aff in self._affixes:
            tier, roll = aff.price_factor
            self._price += tier * roll * 100
        self._price = int(round(self._price))
        self.generate_name()
        self._popup = self.create_popup()
        self._popup_details = self.create_popup(True)

    def describe_details(self):
        """Returns a detailed text description of the item."""
        text = f"#c#(200, 200, 200)Item level: {self._level}\n" + \
            f"#c#(200, 200, 200)Price: {self._price}\n"
        if len(self._implicits) > 0:
            for affx in self._implicits:
                text += f"{affx.describe_details()}\n"
            text += "\n"
        for affx in self._affixes:
            text += f"{affx.describe_details()}\n"
        return text

    def create_popup(self, is_details = False):
        """Creates the detailed popup surface."""
        if self._image is None:
            return None
        method = self.describe_details if is_details else self.describe
        affixes = Text(method(), True, font="item_desc")
        if self._rarity == 4:
            text = f"{trad('uniques', self._name)}\n#s#(24)#c#(128, 128, 128)" +\
                f"{trad('rarities', self._rarity)}{self._base}"
            desc = Text(trad('uniques_desc', self._name), True, font="item_desc")
        else:
            text = f"{self._name}\n#s#(24)#c#(128, 128, 128)" +\
                f"{trad('rarities', self._rarity)}{self._base}"
            desc = None
        title = Text(text, size=30, bold=True, font="item_titles")
        width = max(affixes.width, title.width) + 20
        affixes = Text(method(), True, force_x=width, font="item_desc")
        title = Text(text, True, force_x=width, size=30, bold=True, font="item_titles")
        match self._rarity:
            case 1:
                title_card = SYSTEM["images"]["ui_magic"]\
                    .duplicate(width, 48)
            case 2:
                title_card = SYSTEM["images"]["ui_rare"]\
                    .duplicate(width, 48)
            case 3:
                title_card = SYSTEM["images"]["ui_legendary"]\
                    .duplicate(width, 48)
            case 4:
                title_card = SYSTEM["images"]["ui_unique"]\
                    .duplicate(width, 48)
            case _:
                title_card = SYSTEM["images"]["ui_normal"]\
                    .duplicate(width, 48)
        affix_card = SYSTEM["images"]["item_desc"].duplicate(width, affixes.height +\
                ((desc.height + 15) if desc is not None else 0))
        sfc = Surface(width=title_card.get_width(), height=title_card.get_height()\
                + affix_card.get_height() +\
                ((desc.height + 20) if desc is not None else 0))
        title_pos = (title_card.get_width() / 2 - title.width / 2,
                     title_card.get_height() / 2 - title.height / 2)
        affix_pos = (affix_card.get_width() / 2 - affixes.width / 2,
                     affix_card.get_height() / 2 - affixes.height / 2)
        sfc.blit(title_card, (0, 0), True)
        sfc.blit(title.surface, title_pos, True)
        if is_details or self._rarity > 0 or len(self._implicits) > 0:
            affix_card.blit(affixes.surface, affix_pos, True)
            sfc.blit(affix_card, (0, title_card.get_height()), True)
        if desc is not None:
            desc_pos = (title_card.get_width() / 2 - desc.width / 2,
                     affix_pos[1] + title_pos[1] + affixes.height\
                     + title.height + desc.height / 2 + 10)
            sfc.blit(desc.surface, desc_pos, True)
        return sfc

    def __get_gear_flags(self):
        """Returns which gear flag the item uses."""
        for f in self._flags:
            if f in [Flags.BOOTS, Flags.HELM, Flags.HANDS, Flags.ARMOR,\
                Flags.RING, Flags.RELIC, Flags.AMULET, Flags.BELT,\
                Flags.OFFHAND, Flags.WEAPON]:
                return f.value
        return None

    def __get_sealed_affixes(self):
        """Counts how many sealed affixes there are."""
        mods = 0
        for aff in self._affixes:
            if aff.sealed:
                mods += 1
        return mods

    def gray_out(self):
        """Checks whether or not the item should be grayed, ie
        if an incompatible rune is currently activated."""
        if SYSTEM["rune"] == 0 and (self.__get_sealed_affixes() >= len(self._affixes) \
                                or self._rarity == 0):
            return True
        if SYSTEM["rune"] == 1 and self._rarity != 0:
            return True
        if SYSTEM["rune"] == 2 and AFF_RARITY_TABLE[len(self._affixes) + 1] > self._rarity:
            return True
        if SYSTEM["rune"] == 3 and self._rarity == 0:
            return True
        if SYSTEM["rune"] == 4 and (self.__get_sealed_affixes() >= 1 or \
                                    len(self._affixes) == 0):
            return True
        if SYSTEM["rune"] == 5 and self._rarity != 2:
            return True
        if SYSTEM["rune"] == 6 and self._rarity != 2:
            return True
        if SYSTEM["rune"] == 7 and self._rarity != 0:
            return True
        if SYSTEM["rune"] == 8 and self._rarity != 1:
            return True
        if SYSTEM["rune"] == 9 and self._rarity != 1:
            return True
        return False

    def apply_rune(self):
        """Applies the rune contained in the system."""
        if SYSTEM["rune"] == 0:
            if self.scour():
                SYSTEM["player"].runes[0] -= 1
        elif SYSTEM["rune"] == 1 and self._rarity == 0:
            if self.rarify():
                SYSTEM["player"].runes[1] -= 1
        elif SYSTEM["rune"] == 2:
            if self.exalt():
                SYSTEM["player"].runes[2] -= 1
        elif SYSTEM["rune"] == 3:
            if self.reroll_values():
                SYSTEM["player"].runes[3] -= 1
        elif SYSTEM["rune"] == 4:
            if self.lock():
                SYSTEM["player"].runes[4] -= 1
        elif SYSTEM["rune"] == 5 and self._rarity == 2:
            if self.try_upgrade():
                SYSTEM["player"].runes[5] -= 1
        elif SYSTEM["rune"] == 6 and self._rarity == 2:
            if self.chaos():
                SYSTEM["player"].runes[6] -= 1
        elif SYSTEM["rune"] == 7 and self._rarity == 0:
            if self.enchant():
                SYSTEM["player"].runes[7] -= 1
        elif SYSTEM["rune"] == 8 and self._rarity == 1:
            if self.regal():
                SYSTEM["player"].runes[8] -= 1
        elif SYSTEM["rune"] == 9 and self._rarity == 1:
            if self.alteration():
                SYSTEM["player"].runes[9] -= 1
        if not "shift" in SYSTEM["keys"]:
            SYSTEM["rune"] = -1
            SYSTEM["rune_display"] = None
            SYSTEM["cooldown"] = 0.1

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
        self.update()
        return True

    def lock(self):
        """Locks an affix; preventing it from being ever changed.
        
        Returns:
            bool: Whether or not the item was changed."""
        if len(self._affixes) <= 0:
            return False
        sealed = self.__get_sealed_affixes()
        if sealed > 0:
            return False
        while True:
            roll = random.randint(0, len(self._affixes) - 1)
            if not self._affixes[roll].sealed:
                self._affixes[roll].seal(True)
                break
        self.update()
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
        self.update()
        return True

    def rarify(self):
        """Transforms the item into a rare item."""
        self._rarity = 2
        roll = random.randint(3 - len(self._affixes), 6)
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                                            roll, self._level, self._affixes)]
        self._affixes.extend(affixes)
        self.update()
        return True

    def exalt(self):
        """Adds a single modifier to an item."""
        mods = len(self._affixes)
        if AFF_RARITY_TABLE[mods + 1] > self._rarity:
            return False
        affix = SYSTEM["looter"].generate_affixes(self.__get_gear_flags(), 1,\
                                    self._level, self._affixes)[0].roll()
        self._affixes.append(affix)
        self.update()
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
        self.update()
        return True

    def chaos(self):
        """Reroll a rare item."""
        self.scour()
        mods = self.__get_sealed_affixes()
        if mods == 6:
            return False
        roll = random.randint(3 - mods, 6 - mods)
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level)]
        self._rarity = 2
        self._affixes.extend(affixes)
        self.update()
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
        self.update()
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
        self.update()
        return True

    def alteration(self):
        """Rerolls a magic item."""
        self.scour()
        mods = self.__get_sealed_affixes()
        if mods == 2:
            return False
        roll = random.randint(1, 2) - mods
        affixes = [f.roll() for f in SYSTEM["looter"].generate_affixes(self.__get_gear_flags(),\
                        roll, self._level)]
        self._rarity = 1
        self._affixes.extend(affixes)
        self.update()
        return True

    def get_image(self):
        """returns the item's image."""
        if self._image is None:
            return None
        return self._image

    def export(self):
        """Serializes the affix as JSON."""
        data = {
            "type": "item",
            "name": self._name,
            "base": self._base,
            "price": self._price,
            "base_price": self._base_price,
            "implicits": [f.export() for f in self._implicits],
            "affixes": [f.export() for f in self._affixes],
            "flags": self._flags,
            "image": self._image.uri,
            "image_w": self._image.width,
            "image_h": self._image.height,
            "rarity": self._rarity,
            "droptime": self._drop_time,
            "sealed": self._sealed,
            "level": self._level
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a JSON tab and creates an affix from it."""
        affixes = []
        implicits = []
        afx = data["affixes"]
        imp = data["implicits"]
        for a in afx:
            load = json.loads(a)
            if load["type"] == "affix":
                affixes.append(Affix.imports(load))
            elif load["type"] == "double_affix":
                affixes.append(DoubleAffix.imports(load))
        for a in imp:
            load = json.loads(a)
            if load["type"] == "affix":
                implicits.append(Affix.imports(load))
            elif load["type"] == "double_affix":
                implicits.append(DoubleAffix.imports(load))
        item = Item(
            data["name"],
            data["base"],
            float(data["price"]),
            0,
            1,
            Image(data["image"]).scale(int(data["image_h"]), int(data["image_w"])),
            int(data["rarity"]),
            [Flags(f) for f in data["flags"]],
            affixes,
            implicits
        )
        item.name = data["name"]
        return item

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
    def level(self):
        """Return's the item level."""
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def popup(self) -> Surface:
        """Returns the popup."""
        return self._popup

    @property
    def popup_details(self) -> Surface:
        """Returns the detailed popup."""
        return self._popup_details

    @property
    def sealed(self) -> bool:
        """Returns whether or not the item is sealed; ie
        one of its affix is locked."""
        return self._sealed

    @property
    def stamp(self):
        """Stamps the item's drop time"""
        self._drop_time = time.time()
        return self

    @property
    def drop_time(self):
        """returns the items drop time."""
        return self._drop_time

    @drop_time.setter
    def drop_time(self, value):
        self._drop_time = value
