"""For the skill trees."""

import pygame
from data.constants import SYSTEM, trad
from data.numerics.affliction import Affliction
from data.image.hoverable import Hoverable
from data.image.button import Button

class Node:
    """
    Defines a tree node.

    Args:
        name (str): Name of the node.
        icon (Image|Animation): Icon of the node.
        effects (list[Affliction]): List of effects from the node.
        previous (Node, optional): Previous node connected to this
        one in the tree.
    """
    def __init__(self, name, icon: str, x, y,\
        effects:list[Affliction], previous = None):
        self._name = name
        self._x = x
        self._y = y
        self._icon = icon
        self._effects = effects
        self._previous = previous
        self._connected = []
        self._learned = False
        if self._previous is not None:
            self._previous.connected.append(self)
        self._button = Button(icon, None, self.action)
        hover_desc = f"#s#(35){trad('tree', name)}#s#(20)\n"
        for f in effects:
            hover_desc += f.tree_describe()
        self._hover = Hoverable(x, y, None, hover_desc, surface= SYSTEM["images"][self._icon].image,\
            scrollable=SYSTEM["images"]["tree_scroller"])

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

    def unlearn(self):
        """Attempt to learn the node."""
        if self.can_be_unlearned():
            SYSTEM["player"].creature.ap += 1
            self._learned = False
            for f in self._effects:
                SYSTEM["player"].creature.remove_affliction(f)

    def draw(self, surface: pygame.Surface):
        """Draws the tree."""
        pos_origin = (self._x + SYSTEM["images"][self._icon].width / 2,\
            self._y + SYSTEM["images"][self._icon].height / 2)
        if self._previous is not None:
            color = (0, 255, 0) if self._learned else (255, 255, 255) if \
                self._previous.can_be_learned() else (150, 150, 150)
            pos_destin = (self._previous.x + SYSTEM["images"][self._previous.icon].width / 2,\
                self._previous.y + SYSTEM["images"][self._previous.icon].height / 2)
            pygame.draw.line(surface, color, pos_origin, \
                pos_destin, 5)
        for f in self._connected:
            f.draw(surface)
        self._button.draw(surface)
        #surface.blit(SYSTEM["images"][self._icon].image, (self.x, self.y))

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

