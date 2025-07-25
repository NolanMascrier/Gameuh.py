"""Skills for the skill tree."""

from data.numerics.affliction import Affliction
from data.game.tree import Node

TREE_START = Node("start", "tree_start", 250, 250, [], None)
TREE_A = Node("start", "tree_a", 500, 250, [], TREE_START)
TREE_B = Node("start", "tree_b", 500, 500, [], TREE_START)