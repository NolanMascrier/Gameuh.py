"""For the skill trees."""

import json

from data.api.surface import Surface

from data.constants import SYSTEM, trad
from data.numerics.affliction import Affliction
from data.image.hoverable import Hoverable
from data.image.button import Button, Text

GENERATE_SURFACES = True

class Node:
    """
    Defines a tree node.

    Args:
        name (str): Name of the node.
        icon (Image|Animation): Icon of the node.
        effects (list[Affliction]): List of effects from the node.
        previous (Node, optional): Previous node connected to this
        one in the tree.
        skills (list[str], optionnal): List of spells taught by this\
        node. Defaults to []
        rarity (int, optional): Rarity of the node. Same rules as items.\
        Defaults to 0 (common).
    """
    def __init__(self, name, icon: str, x, y,\
        effects:list[Affliction], previous = None,\
        skills:list[str] = None, rarity:int = 0):
        self._name = name
        self._x = x
        self._y = y
        self._icon = icon
        self._effects = effects
        self._previous = previous
        self._connected = []
        self._learned = False
        self._rarity = rarity
        if skills is None:
            skills = []
        self._skills = skills
        self._surface = None
        if GENERATE_SURFACES:
            self.generate_surface()
            if self._previous is not None:
                self._previous.connected.append(self)
            self._button = Button(icon, None, self.action)
            self._hover = Hoverable(x, y, None, None, surface=SYSTEM["images"][self._icon].image,\
                scrollable=SYSTEM["images"]["tree_scroller"], override=self._surface)

    def generate_surface(self):
        """Generates the hoverable surface."""
        surfaces = []
        skill_desc = ""
        h = 0
        w = 0
        for s in self._skills:
            skill = SYSTEM["spells"][s]
            if skill is None:
                continue
            surfaces.append(skill.surface)
            h += skill.surface.get_height()
            skill_desc += f"{trad('meta_words', 'learns')} {trad('spells_name', skill.name)}\n"
            w = max(w, skill.surface.get_width())
        effects_desc = ""
        for e in self._effects:
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
        sfc.blit(title_card, (0, 0))
        sfc.blit(desc_card, (0, title_card.get_height()))
        h_temp = title_card.get_height() + desc_card.get_height()
        for s in surfaces:
            sfc.blit(s, (w / 2 - s.get_width() / 2, h_temp))
            h_temp += s.get_height()
        title_pos = (title_card.get_width() / 2 - title.width / 2,\
            title_card.get_height() / 2 - title.height / 2)
        desc_pos = (desc_card.get_width() / 2 - desc.width / 2,\
            desc_card.get_height() / 2 - desc.height / 2 + title_card.get_height())
        sfc.blit(title.surface, title_pos)
        sfc.blit(desc.surface, desc_pos)
        self._surface = sfc

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
        if self._learned:
            self.unlearn()
        else:
            self.learn()

    def can_be_learned(self) -> bool:
        """Checks whether or not the node can be learnt."""
        if SYSTEM["player"].creature.ap >= 1 and \
            (self._previous is None or self._previous.learned):
            return True
        return False

    def can_be_unlearned(self) -> bool:
        """Checks whether or not the node can be unlearnt."""
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
            self._learned = True
            for f in self._effects:
                SYSTEM["player"].creature.afflict(f)
            for s in self._skills:
                SYSTEM["player"].spellbook.append(s)

    def unlearn(self):
        """Attempt to learn the node."""
        if self.can_be_unlearned():
            SYSTEM["player"].creature.ap += 1
            self._learned = False
            for f in self._effects:
                SYSTEM["player"].creature.remove_affliction(f)
            for s in self._skills:
                SYSTEM["player"].spellbook.remove(s)

    def draw(self, surface: Surface):
        """Draws the tree."""
        pos_origin = (self._x + SYSTEM["images"][self._icon].width / 2,\
            self._y + SYSTEM["images"][self._icon].height / 2)
        if self._previous is not None:
            color = (0, 255, 0) if self._learned else (255, 255, 255) if \
                self._previous.can_be_learned() else (150, 150, 150)
            pos_destin = (self._previous.x + SYSTEM["images"][self._previous.icon].width / 2,\
                self._previous.y + SYSTEM["images"][self._previous.icon].height / 2)
            surface.draw_line(color, pos_origin, pos_destin, 5)
        for f in self._connected:
            f.draw(surface)
        self._button.draw(surface)
        if self._learned:
            surface.blit(SYSTEM["images"]["slot_green"].image, (self._button.x, self._button.y))
        else:
            match self._rarity:
                case 1:
                    surface.blit(SYSTEM["images"]["slot_magic"].image,\
                        (self._button.x, self._button.y))
                case 1:
                    surface.blit(SYSTEM["images"]["slot_rare"].image,\
                        (self._button.x, self._button.y))
                case 1:
                    surface.blit(SYSTEM["images"]["slot_exalted"].image,\
                        (self._button.x, self._button.y))
                case _:
                    surface.blit(SYSTEM["images"]["slot_empty"].image,\
                        (self._button.x, self._button.y))

    def export(self) -> str:
        """Serialize the tree as JSON."""
        effects = []
        connected = []
        for f in self._effects:
            effects.append(f.export())
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
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Recreates the tree from reading JSON."""
        effects = []
        connected = []
        for f in data["effects"]:
            effects.append(Affliction.imports(json.loads(f)))
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
