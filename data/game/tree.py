"""For the skill trees."""

import json

from data.api.surface import Surface

from data.constants import SYSTEM, trad
from data.numerics.affliction import Affliction
from data.image.hoverable import Hoverable
from data.image.button import Button, Text

from data.interface.skilltree import UPDATED

GENERATE_SURFACES = True

class Node:
    """
    Defines a tree node. A node can have multiple levels.

    IMPORTANT - Getting from lvl x to lvl x + 1 removes the buffs learnt from x and replaces them\
    with those from x + 1 !!!

    This is not the case for spells.

    Args:
        name (str): Name of the node.
        icon (Image|Animation): Icon of the node.
        effects (list[list[Affliction]]): List of effects from the node.
        previous (Node, optional): Previous node connected to this\
        one in the tree.
        skills (list[list[str]], optionnal): List of spells taught by this\
        node. Defaults to []
        rarity (int, optional): Rarity of the node. Same rules as items.\
        Defaults to 0 (common).
        points_to_unlock (int, optional): How many points must be invested into\
        the previous node to unlock this one. Defaults to 1.
    """
    def __init__(self, name, icon: str, x, y,\
        effects:list[list[Affliction]], previous = None,\
        skills:list[list[str]] = None, rarity:int = 0, points_to_unlock = 1):
        self._name = name
        self._x = x
        self._y = y
        self._icon = icon
        self._effects = effects
        self._previous = previous
        self._connected = []
        self._learned = False
        self._rarity = rarity
        self._points_to_unlock = points_to_unlock
        self._invested = -1
        self._levels = len(effects)
        if skills is None:
            skills = []
        self._skills = skills
        self._surface = None
        self._text = None
        if GENERATE_SURFACES:
            self.generate_hoverable(True)

    def generate_hoverable(self, generate_button = False):
        """Generates the Hoverable."""
        self.generate_surface()
        if self._previous is not None:
            self._previous.connected.append(self)
        if generate_button:
            self._button = Button(self._icon, None, self.action, alt_action=self.action_alt)
        self._hover = Hoverable(self._x, self._y, None, None,
                                surface=SYSTEM["images"][self._icon].image,\
                                scrollable=SYSTEM["images"]["tree_scroller"],
                                override=self._surface)

    def generate_surface(self):
        """Generates the hoverable surface."""
        surfaces = []
        skill_desc = ""
        h = 0
        w = 0
        l = 0
        for lvl in self._skills:
            l += 1
            for s in lvl:
                skill = SYSTEM["spells"][s]
                if skill is None:
                    continue
                surfaces.append(skill.surface)
                h += skill.surface.get_height()
                skill_desc += f"{l}: {trad('meta_words', 'learns')}" + \
                              f" {trad('spells_name', skill.name)}\n"
                w = max(w, skill.surface.get_width())
        effects_desc = ""
        print(f"For node {self._name}, invested is {self._invested}")
        if self._invested < 0:
            effects_desc += "#s#(15)Learns\n"
            for e in self._effects[0]:
                effects_desc += e.tree_describe()
        elif self._invested + 1 >= self._levels:
            effects_desc += "#s#(15)Maximum level reached\n"
            for e in self._effects[self._invested]:
                effects_desc += e.tree_describe()
        else:
            effects_desc += "#c#(201, 201, 201)#s#(15)Current\n"
            for e in self._effects[self._invested]:
                effects_desc += "#c#(201, 201, 201)#s#(18)" + e.tree_describe()
            effects_desc += "#s#(17)Next\n"
            for e in self._effects[self._invested + 1]:
                effects_desc += e.tree_describe()
        effects_desc += skill_desc
        desc = Text(effects_desc,  size=20, font="item_desc", centered=True)
        title = Text(f"{trad('tree', self._name)}", size=42, font="item_titles")
        w = max(w, desc.width, title.width)
        match self._rarity:
            case 1:
                title_card = SYSTEM["images"]["ui_magic"]\
                    .duplicate(w, title.height + 32)
            case 2:
                title_card = SYSTEM["images"]["ui_rare"]\
                    .duplicate(w, title.height + 32)
            case 3:
                title_card = SYSTEM["images"]["ui_legendary"]\
                    .duplicate(w, title.height + 32)
            case 4:
                title_card = SYSTEM["images"]["ui_unique"]\
                    .duplicate(w, title.height + 32)
            case _:
                title_card = SYSTEM["images"]["ui_normal"]\
                    .duplicate(w, title.height + 32)
        desc_card = SYSTEM["images"]["item_desc"].duplicate(w, desc.height)
        h = title_card.get_height() + desc_card.get_height() + h + 10
        w = max(title_card.get_width(), desc_card.get_width())
        sfc = Surface(w, h)
        sfc.blit(title_card, (0, 0), True)
        sfc.blit(desc_card, (0, title_card.get_height()), True)
        h_temp = title_card.get_height() + desc_card.get_height()
        for s in surfaces:
            sfc.blit(s, (w / 2 - s.get_width() / 2, h_temp))
            h_temp += s.get_height()
        title_pos = (title_card.get_width() / 2 - title.width / 2,\
            title_card.get_height() / 2 - title.height / 2)
        desc_pos = (desc_card.get_width() / 2 - desc.width / 2,\
            desc_card.get_height() / 2 - desc.height / 2 + title_card.get_height())
        sfc.blit(title.surface, title_pos, True)
        sfc.blit(desc.surface, desc_pos, True)
        self._surface = sfc
        self._text = Text(f"{self._invested + 1}/{self._levels}", font="item_desc", size=26)

    def tick(self):
        """Ticks down the node."""
        rect = SYSTEM["images"]["tree_scroller"].coordinates_rectangle(self._x, self._y,\
            SYSTEM["images"][self._icon].width, SYSTEM["images"][self._icon].height)
        if rect is not None:
            x, y, _, _ = rect
            self._hover.set(x, y).tick()
        self._button.set(self._x, self._y, SYSTEM["images"]["tree_scroller"]).tick()
        for t in self._connected:
            t.tick()

    def action(self):
        """Actions the node."""
        UPDATED[0] = True
        self.learn()
        self.generate_hoverable()

    def action_alt(self):
        """Unleashes the unlearning"""
        UPDATED[0] = True
        self.unlearn()
        self.generate_hoverable()

    def can_be_learned(self) -> bool:
        """Checks whether or not the node can be learnt."""
        if self._learned:
            return False
        if SYSTEM["player"].creature.ap >= 1 and \
            (self._previous is None or self._previous.learned or
                                       self._previous.invested + 1 >= self._points_to_unlock):
            return True
        return False

    def can_be_unlearned(self) -> bool:
        """Checks whether or not the node can be unlearnt."""
        if self._invested < 0:
            return False
        if len(self._connected) == 0:
            return True
        for f in self._connected:
            if f.learned:
                return False
        return True

    def learn(self):
        """Attempt to learn the node."""
        if self.can_be_learned():
            SYSTEM["player"].creature.ap -= 1
            #Unlearn new versions
            if self._invested >= 0:
                for f in self._effects[self._invested]:
                    SYSTEM["player"].creature.remove_affliction(f)
            self._invested += 1
            #Learn new versions
            for f in self._effects[self._invested]:
                SYSTEM["player"].creature.afflict(f)
            #Spells
            if self._skills and self._skills[self._invested] is not None:
                for s in self._skills[self._invested]:
                    SYSTEM["player"].spellbook.append(s)
            if self._invested + 1 >= self._levels:
                self._learned = True

    def unlearn(self):
        """Attempt to learn the node."""
        if self.can_be_unlearned():
            SYSTEM["player"].creature.ap += 1
            #Buffs
            for f in self._effects[self._invested]:
                SYSTEM["player"].creature.remove_affliction(f)
            #Spells
            if self._skills and self._skills[self._invested] is not None:
                for s in self._skills[self._invested]:
                    if s in SYSTEM["player"].spellbook:
                        SYSTEM["player"].spellbook.remove(s)
            self._invested -= 1
            #Gives the previous level buffs
            if self._invested >= 0:
                for f in self._effects[self._invested]:
                    SYSTEM["player"].creature.afflict(f)
            self._learned = False

    def draw(self, surface: Surface):
        """Draws the tree."""
        pos_origin = (self._x + SYSTEM["images"][self._icon].width / 2,\
            self._y + SYSTEM["images"][self._icon].height / 2)
        if self._previous is not None:
            if self._learned:
                color = (0, 255, 0)
            elif self.can_be_learned():
                color = (255, 255, 255)
            else:
                color = (150, 150, 150)
            pos_previous = (self._previous.x + SYSTEM["images"][self._previous.icon].width / 2,\
                self._previous.y + SYSTEM["images"][self._previous.icon].height / 2)
            surface.draw_line(color, pos_origin, pos_previous, 5)
        for f in self._connected:
            f.draw(surface)
        self._button.draw(surface)
        if self._learned:
            surface.blit(SYSTEM["images"]["slot_green"].image,
                         (self._button.x, self._button.y), True)
        else:
            match self._rarity:
                case 1:
                    surface.blit(SYSTEM["images"]["slot_magic"].image,\
                        (self._button.x, self._button.y), True)
                case 1:
                    surface.blit(SYSTEM["images"]["slot_rare"].image,\
                        (self._button.x, self._button.y), True)
                case 1:
                    surface.blit(SYSTEM["images"]["slot_exalted"].image,\
                        (self._button.x, self._button.y), True)
                case _:
                    surface.blit(SYSTEM["images"]["slot_empty"].image,\
                        (self._button.x, self._button.y), True)
        if self._levels <= 1:
            return
        pos_text = (self._button.x + self._button.width // 2 - self._text.width // 2,
            self._button.y + self._button.height // 2 + self._text.height)
        surface.blit(self._text.image, pos_text)

    def export(self) -> str:
        """Serialize the tree as JSON."""
        effects = []
        connected = []
        for lvl in self._effects:
            add = []
            for f in lvl:
                add.append(f.export())
            effects.append(add)
        for c in self._connected:
            connected.append(c.export())
        data = {
            "type": "tree",
            "name": self._name,
            "icon": self._icon,
            "x": self._x,
            "y": self._y,
            "learned": self._learned,
            "effects": effects,
            "skills": self._skills,
            "rarity": self._rarity,
            "connected": connected,
            "invested": self._invested
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Recreates the tree from reading JSON."""
        effects = []
        connected = []
        for lvl in data["effects"]:
            add = []
            for f in lvl:
                add.append(Affliction.imports(json.loads(f)))
            effects.append(add)
        node = Node(
            data["name"],
            data["icon"],
            int(data["x"]),
            int(data["y"]),
            effects,
            None,
            data["skills"]
        )
        for c in data["connected"]:
            connex = Node.imports(json.loads(c))
            connex.previous = node
            connected.append(connex)
        node.connected = connected
        node.invested = int(data["invested"])
        node.learned = bool(data["learned"])
        return node

    @property
    def name(self):
        """Return the node's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def effects(self):
        """Return the node's effects."""
        return self._effects

    @effects.setter
    def effects(self, value):
        self._effects = value

    @property
    def previous(self):
        """Return the node's previous node."""
        return self._previous

    @previous.setter
    def previous(self, value):
        self._previous = value

    @property
    def learned(self):
        """Returns whether or not the node is learned."""
        return self._learned

    @learned.setter
    def learned(self, value):
        self._learned = value

    @property
    def x(self):
        """Returns the node's x position."""
        return self._x

    @property
    def y(self):
        """Returns the node's y position."""
        return self._y

    @property
    def icon(self):
        """Returns the node's icon."""
        return self._icon

    @property
    def connected(self):
        """Returns the node's connected nodes."""
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    @property
    def invested(self):
        """Returns the number of points invested in the node."""
        return self._invested

    @invested.setter
    def invested(self, value):
        self._invested = value
