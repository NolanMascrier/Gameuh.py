"""For the skill trees."""

from data.constants import SYSTEM
from data.numerics.affliction import Affliction

class Node:
    """
    Defines a tree node.

    Args:
        name (str): Name of the node.
        effects (list[Affliction]): List of effects from the node.
        previous (Node, optional): Previous node connected to this
        one in the tree.
    """
    def __init__(self, name, effects:list[Affliction], previous = None):
        self._name = name
        self._effects = effects
        self._previous = previous
        self._learned = False

    def learn(self):
        """Attempt to learn the node."""
        if SYSTEM["player"].creature.ap >= 1 and \
            (self._previous is None or self._previous.learned):
            pass

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
