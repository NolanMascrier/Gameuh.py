"""Skills for the skill tree."""

from data.constants import SYSTEM, Flags
from data.numerics.affliction import Affliction
from data.game.tree import Node


STR_NODE = Affliction("tree_str", 5, -1, [Flags.FLAT, Flags.STR], True)

def generate_tree():
    """Creates the tree."""
    tree_start = Node("start", "tree_start", 250, 250, [STR_NODE], None)
    tree_a = Node("buffa", "tree_a", 500, 250, [], tree_start, ["firebolt2"])
    tree_b = Node("skilla", "tree_b", 500, 500, [], tree_start)
    tree_c = Node("skil_b", "tree_b", 750, 500, [], tree_b)
    SYSTEM["tree"] = tree_start