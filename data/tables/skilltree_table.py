"""Skills for the skill tree."""

from data.constants import SYSTEM, Flags, Classes
from data.numerics.affliction import Affliction
from data.game.tree import Node

STR_NODE_1 = Affliction("tree_str", 5, -1, [Flags.FLAT, Flags.STR, Flags.DESC_FLAT], True)
STR_NODE_2 = Affliction("tree_str", 10, -1, [Flags.FLAT, Flags.STR, Flags.DESC_FLAT], True)
STR_NODE_3 = Affliction("tree_str", 15, -1, [Flags.FLAT, Flags.STR, Flags.DESC_FLAT], True)

FIRE_NODE_1 = Affliction("tree_fir", 0.05, -1, [Flags.BOON, Flags.FIRE_DMG], True)
FIRE_NODE_2 = Affliction("tree_fir", 0.1, -1, [Flags.BOON, Flags.FIRE_DMG], True)
FIRE_NODE_3 = Affliction("tree_fir", 0.15, -1, [Flags.BOON, Flags.FIRE_DMG], True)
FIRE_NODE_4 = Affliction("tree_fir", 0.25, -1, [Flags.BOON, Flags.FIRE_DMG], True)
FIRE_NODE_5 = Affliction("tree_fir", 0.35, -1, [Flags.BOON, Flags.FIRE_DMG], True)
FIRE_NODE_5B = Affliction("tree_firb", 0.05, -1,
                          [Flags.FLAT, Flags.FIRE_PEN], True)

ICE_NODE_1 = Affliction("tree_ice", 0.05, -1, [Flags.BOON, Flags.ICE_DMG], True)
ICE_NODE_2 = Affliction("tree_ice", 0.1, -1, [Flags.BOON, Flags.ICE_DMG], True)
ICE_NODE_3 = Affliction("tree_ice", 0.15, -1, [Flags.BOON, Flags.ICE_DMG], True)
ICE_NODE_4 = Affliction("tree_ice", 0.25, -1, [Flags.BOON, Flags.ICE_DMG], True)
ICE_NODE_5 = Affliction("tree_ice", 0.35, -1, [Flags.BOON, Flags.ICE_DMG], True)
ICE_NODE_5B = Affliction("tree_iceb", 0.05, -1,
                          [Flags.FLAT, Flags.ICE_PEN], True)

LIGHTNING_NODE_1 = Affliction("tree_light", 0.05, -1, [Flags.BOON, Flags.LIGHTNING_DMG], True)
LIGHTNING_NODE_2 = Affliction("tree_light", 0.1, -1, [Flags.BOON, Flags.LIGHTNING_DMG], True)
LIGHTNING_NODE_3 = Affliction("tree_light", 0.15, -1, [Flags.BOON, Flags.LIGHTNING_DMG], True)
LIGHTNING_NODE_4 = Affliction("tree_light", 0.25, -1, [Flags.BOON, Flags.LIGHTNING_DMG], True)
LIGHTNING_NODE_5 = Affliction("tree_light", 0.35, -1, [Flags.BOON, Flags.LIGHTNING_DMG], True)
LIGHTNING_NODE_5B = Affliction("tree_lightb", 0.05, -1,
                          [Flags.FLAT, Flags.LIGHTNING_PEN], True)
def generate_tree():
    """Creates the tree."""

    #SORCERESS

    #FIRE
    sorceress_start = Node("start", "sorceress_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                      None, rarity=1)
    _fire_mastery = Node("fire_mastery", "fire_mastery", 500, 350, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], sorceress_start)
    _firebolter = Node("fireball", "explosion", 500, 250, 20, _fire_mastery,
                       rarity=2) #Mets rarity=2 pour dire un skill, c'est purement visuel
    _firestorm = Node("firestorm", "firestorm", 600, 250, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _firebolter, rarity=2)
    _meteor = Node("meteor", "meteor", 700, 250, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _firestorm, ["meteor"], rarity=2)
    _pyrotechnics = Node("pyrotechnics", "pyrotechnics", 700, 350, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _fire_mastery)
    _cone_of_flames = Node("cone_of_flames", "cone_of_flames", 500, 450, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _fire_mastery,["cone_of_flames"], rarity=2)
    _inferno = Node("inferno", "inferno", 600, 450, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _cone_of_flames, rarity=2)
    _ring_of_fire = Node("ring_of_fire", "ring_of_fire", 800, 350, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _pyrotechnics, rarity=2)
    tree_b = Node("skil_a", "tree_b", 500, 500, [[]], None)
    #ICE
    _ice_mastery = Node("ice_mastery", "ice_mastery", 500, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], sorceress_start)
    _congelation = Node("congelation", "congelation", 600, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_mastery)
    _icebolt = Node("icebolt", "icebolt", 600, 800, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_mastery, rarity=2)
    _nova = Node("nova", "nova", 700, 800, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _icebolt)
    _ring_of_frost = Node("ring_of_frost", "ring_of_frost", 700, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _congelation, ["ring_of_frost"], rarity=2)
    _blizzard = Node("blizzard", "blizzard", 800, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _nova, rarity=2)
    _ice_orb = Node("ice_orb", "ice_orb", 600, 600, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_mastery, ["ice_orb"], rarity=2)
    _ice_spear = Node("ice_spear", "ice_spear", 700, 600, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_orb,["ice_spear"], rarity=2)
    _ice_wall = Node("ice_wall", "ice_wall", 800, 600, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3], 
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_spear,["ice_wall"], rarity=2)
    tree_c = Node("skil_b", "tree_b", 650, 500, [[]], tree_b)
    #LIGHTNING
    _lightning_mastery = Node("lightning_mastery", "lightning_mastery", 500, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], sorceress_start)
    _shock = Node("shock", "shock", 600, 1200, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery, ["shock"], rarity=2)
    _lightning_bolt = Node("lightning_bolt", "lightning_bolt", 600, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery, ["lightning_bolt"], rarity=2)
    _conduction = Node("conduction", "conduction", 600, 1000, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery)
    _lightning_sphere = Node("lightning_sphere", "tree_a", 700, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_bolt, rarity=2)
    _call_lightning = Node("call_lightning", "call_lightning", 700, 1200, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _shock, rarity=2)
    _rising_tempest = Node("rising_tempest", "rising_tempest", 800, 1200, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _call_lightning)
    _ride_the_storm = Node("ride_the_storm", "ride_the_storm", 800, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_sphere)
    _lightning_fork = Node("lightning_fork", "lightning_fork", 900, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _ride_the_storm)
    
    #WARRIOR
    #MELEE
    warrior_start = Node("start", "warrior_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                        None, rarity=1)
    _warrior_node_1 = Node("warrior_node_1", "tree_a", 500, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], warrior_start, rarity=2)
    _warrior_node_2 = Node("warrior_node_2", "tree_a", 600, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_1, rarity=2)
    _warrior_node_3 = Node("warrior_node_3", "tree_a", 700, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_2, rarity=2)
    _warrior_node_4 = Node("warrior_node_4", "tree_a", 800, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_3, rarity=2)
    _warrior_node_5 = Node("warrior_node_5", "tree_a", 900, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_4, rarity=2)
    _warrior_node_5B = Node("warrior_node_5B", "tree_a", 900, 450, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_4, rarity=2)
    _warrior_node_6 = Node("warrior_node_6", "tree_a", 1000, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_5, rarity=2)
    _warrior_node_6B = Node("warrior_node_6B", "tree_a", 1000, 450, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_5B, rarity=2)
    _warrior_node_7 = Node("warrior_node_7", "tree_a", 1100, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_6, rarity=2)
    _warrior_node_7B = Node("warrior_node_7B", "tree_a", 1100, 450, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_6B, rarity=2)
    _warrior_node_8 = Node("warrior_node_8", "tree_a", 1200, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_7, rarity=2)
    _warrior_node_8B = Node("warrior_node_8B", "tree_a", 1200, 450, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_7B, rarity=2)
    _warrior_node_9 = Node("warrior_node_9", "tree_a", 1300, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_8, rarity=2)
    _warrior_node_9B = Node("warrior_node_9B", "tree_a", 1300, 450, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_8B, rarity=2)
    _warrior_node_10 = Node("warrior_node_10", "tree_a", 1400, 350, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], _warrior_node_9, rarity=2)
    #RANGED
    _warrior_node_11 = Node("warrior_node_11", "tree_a", 500, 700, [[STR_NODE_1], [STR_NODE_2], \
        [STR_NODE_3]], warrior_start, rarity=2)
    _warrior_node_12 = Node("warrior_node_12", "tree_a", 600, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_11, rarity=2)
    _warrior_node_13 = Node("warrior_node_13", "tree_a", 700, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_12, rarity=2)
    _warrior_node_14 = Node("warrior_node_14", "tree_a", 800, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_13, rarity=2)
    _warrior_node_15 = Node("warrior_node_15", "tree_a", 900, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_14, rarity=2)
    _warrior_node_16 = Node("warrior_node_16", "tree_a", 1000, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_15, rarity=2)
    _warrior_node_17 = Node("warrior_node_17", "tree_a", 1100, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_16, rarity=2)
    _warrior_node_18 = Node("warrior_node_18", "tree_a", 1200, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_17, rarity=2)
    _warrior_node_19 = Node("warrior_node_19", "tree_a", 1300, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_18, rarity=2)
    _warrior_node_20 = Node("warrior_node_20", "tree_a", 1400, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_19, rarity=2)
    #DEFENSE
    _warrior_node_21 = Node("warrior_node_21", "tree_a", 500, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], warrior_start, rarity=2)
    _warrior_node_22 = Node("warrior_node_22", "tree_a", 600, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_21, rarity=2)
    _warrior_node_23 = Node("warrior_node_23", "tree_a", 700, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_22, rarity=2)
    _warrior_node_24 = Node("warrior_node_24", "tree_a", 800, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_23, rarity=2)
    _warrior_node_25 = Node("warrior_node_25", "tree_a", 900, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_24, rarity=2)
    _warrior_node_26 = Node("warrior_node_26", "tree_a", 1000, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_25, rarity=2)
    _warrior_node_27 = Node("warrior_node_27", "tree_a", 1100, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_26, rarity=2)
    _warrior_node_28 = Node("warrior_node_28", "tree_a", 1200, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_27, rarity=2)
    _warrior_node_29 = Node("warrior_node_29", "tree_a", 1300, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_28, rarity=2)
    _warrior_node_30 = Node("warrior_node_30", "tree_a", 1400, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _warrior_node_29, rarity=2)

    #ESSENTIALIST 
    essentialist_start = Node("start", "essentialist_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                      None, rarity=1)
    #LIGHT
    _essentialist_node_1 = Node("essentialist_node_1", "tree_a", 500, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], essentialist_start, rarity=2)
    _essentialist_node_2 = Node("essentialist_node_2", "tree_a", 600, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_1, rarity=2)
    _essentialist_node_3 = Node("essentialist_node_3", "tree_a", 700, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_2, rarity=2)
    _essentialist_node_4 = Node("essentialist_node_4", "tree_a", 800, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_3, rarity=2)
    _essentialist_node_5 = Node("essentialist_node_5", "tree_a", 900, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_4, rarity=2)
    _essentialist_node_5B = Node("essentialist_node_5B", "tree_a", 900, 450, [[STR_NODE_1], [STR_NODE_2   ], [STR_NODE_3]], _essentialist_node_4, rarity=2)
    _essentialist_node_6 = Node("essentialist_node_6", "tree_a", 1000, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_5, rarity=2)
    _essentialist_node_6B = Node("essentialist_node_6B", "tree_a", 1000, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_5B, rarity=2)
    _essentialist_node_7 = Node("essentialist_node_7", "tree_a", 1100, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_6, rarity=2)
    _essentialist_node_7B = Node("essentialist_node_7B", "tree_a", 1100, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_6B, rarity=2)
    _essentialist_node_8 = Node("essentialist_node_8", "tree_a", 1200, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_7, rarity=2)
    _essentialist_node_8B = Node("essentialist_node_8B", "tree_a", 1200, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_7B, rarity=2)
    _essentialist_node_9 = Node("essentialist_node_9", "tree_a", 1300, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_8, rarity=2)
    _essentialist_node_9B = Node("essentialist_node_9B", "tree_a", 1300, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_8B, rarity=2)
    _essentialist_node_10 = Node("essentialist_node_10", "tree_a", 1400, 350, [[ STR_NODE_1 ],[ STR_NODE_2 ],[ STR_NODE_3 ]],
                                   _essentialist_node_9, rarity=2)
    #BALANCE
    _essentialist_node_11 = Node("essentialist_node_11", "tree_a", 500, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], warrior_start, rarity=2)
    _essentialist_node_12 = Node("essentialist_node_12", "tree_a", 600, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_11, rarity=2)
    _essentialist_node_13 = Node("essentialist_node_13", "tree_a", 700, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_12, rarity=2)
    _essentialist_node_14 = Node("essentialist_node_14", "tree_a", 800, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_13, rarity=2)
    _essentialist_node_15 = Node("essentialist_node_15", "tree_a", 900, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_14, rarity=2)
    _essentialist_node_16 = Node("essentialist_node_16", "tree_a", 1000, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_15, rarity=2)
    _essentialist_node_17 = Node("essentialist_node_17", "tree_a", 1100, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_16, rarity=2)
    _essentialist_node_18 = Node("essentialist_node_18", "tree_a", 1200, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_17, rarity=2)
    _essentialist_node_19 = Node("essentialist_node_19", "tree_a", 1300, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_18, rarity=2)
    _essentialist_node_20 = Node("essentialist_node_20", "tree_a", 1400, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_19, rarity=2)
    #SHADOW
    _essentialist_node_21 = Node("essentialist_node_21", "tree_a", 500, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], warrior_start, rarity=2)
    _essentialist_node_22 = Node("essentialist_node_22", "tree_a", 600, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_21, rarity=2)
    _essentialist_node_23 = Node("essentialist_node_23", "tree_a", 700, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_22, rarity=2)
    _essentialist_node_24 = Node("essentialist_node_24", "tree_a", 800, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_23, rarity=2)
    _essentialist_node_25 = Node(" essentialist node__ ", "tree_a", 900, 1000, [[ STR_NODE_1 ],[ STR_NODE_2 ],[ STR_NODE_3 ]],
                                   _essentialist_node_21 , rarity=4)
    _essentialist_node_26 = Node("essentialist_node_26", "tree_a", 1000, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_25, rarity=2)
    _essentialist_node_27 = Node("essentialist_node_27", "tree_a", 1100, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_26, rarity=3)
    _essentialist_node_28 = Node("essentialist_node_28", "tree_a", 1200, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_27, rarity=2)
    _essentialist_node_29 = Node("essentialist_node_29", "tree_a", 1300, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_28, rarity=2)
    _essentialist_node_30 = Node("essentialist_node_30", "tree_a", 1400, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _essentialist_node_29, rarity=2)
    

    #ARCANIST

    arcanist_start = Node("start", "arcanist_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                      None, rarity=1)
    
    #INVENTIVE

    _arcanist_node_1 = Node("arcanist_node_1", "tree_a", 500, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], arcanist_start, rarity=2)
    _arcanist_node_2 = Node("arcanist_node_2", "tree_a", 600, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_1, rarity=2)
    _arcanist_node_3 = Node("arcanist_node_3", "tree_a", 700, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_2, rarity=2)
    _arcanist_node_4 = Node("arcanist_node_4", "tree_a", 800, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_3, rarity=2)
    _arcanist_node_5 = Node("arcanist_node_5", "tree_a", 900, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_4, rarity=2)
    _arcanist_node_5B = Node("arcanist_node_5B", "tree_a", 900, 450, [[STR_NODE_1], [STR_NODE_2   ], [STR_NODE_3]], _arcanist_node_4, rarity=2)
    _arcanist_node_6 = Node("arcanist_node_6", "tree_a", 1000, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_5, rarity=2)
    _arcanist_node_6B = Node("arcanist_node_6B", "tree_a", 1000, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_5B, rarity=2)
    _arcanist_node_7 = Node("arcanist_node_7", "tree_a", 1100, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_6, rarity=2)
    _arcanist_node_7B = Node("arcanist_node_7B", "tree_a", 1100, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_6B, rarity=2)
    _arcanist_node_8 = Node("arcanist_node_8", "tree_a", 1200, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_7, rarity=2)
    _arcanist_node_8B = Node("arcanist_node_8B", "tree_a", 1200, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_7B , rarity=2)
    _arcanist_node_9 = Node("arcanist_node_9", "tree_a", 1300, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_8, rarity=2)

    #MENTALISM

    _arcanist_node_11 = Node("arcanist_node_11", "tree_a", 500, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], arcanist_start, rarity=2)
    _arcanist_node_12 = Node("arcanist_node_12", "tree_a", 600, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_11, rarity=2)
    _arcanist_node_13 = Node("arcanist_node_13", "tree_a", 700, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_12, rarity=2)
    _arcanist_node_14 = Node("arcanist_node_14", "tree_a", 800, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_13, rarity=2)
    _arcanist_node_15 = Node("arcanist_node_15", "tree_a", 900, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_14, rarity=2)
    _arcanist_node_16 = Node("arcanist_node_16", "tree_a", 1000, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_15, rarity=2)
    _arcanist_node_17 = Node("arcanist_node_17", "tree_a", 1100, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_16, rarity=2)
    _arcanist_node_18 = Node("arcanist_node_18", "tree_a", 1200, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_17, rarity=2)
    _arcanist_node_19 = Node("arcanist_node_19", "tree_a", 1300, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_18, rarity=2)
    _arcanist_node_20 = Node("arcanist_node_20", "tree_a", 1400, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_19, rarity=2)

    #VARIATION

    _arcanist_node_21 = Node("arcanist_node_21", "tree_a", 500, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], arcanist_start, rarity=2)
    _arcanist_node_22 = Node("arcanist_node_22", "tree_a", 600, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_21, rarity=2)
    _arcanist_node_23 = Node("arcanist_node_23", "tree_a", 700, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_22, rarity=2)
    _arcanist_node_24 = Node("arcanist_node_24", "tree_a", 800, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_23, rarity=2)
    _arcanist_node_25 = Node("arcanist_node_25", "tree_a", 900, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_24, rarity=2)
    _arcanist_node_26 = Node("arcanist_node_26", "tree_a", 1000, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_25, rarity=2)
    _arcanist_node_27 = Node("arcanist_node_27", "tree_a", 1100, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_26, rarity=2)
    _arcanist_node_28 = Node("arcanist_node_28", "tree_a", 1200, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_27, rarity=2)
    _arcanist_node_29 = Node("arcanist_node_29", "tree_a", 1300, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_28, rarity=2)
    _arcanist_node_30 = Node("arcanist_node_30", "tree_a", 1400, 1000, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _arcanist_node_29, rarity=2)

    #SUMMONER
    
    summoner_start = Node("start", "summoner_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                      None, rarity=1)
    
    #CELESTIAL SUMMONING

    summoner_node_1 = Node("summoner_node_1", "tree_a", 500, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_start, rarity=2)
    summoner_node_2 = Node("summoner_node_2", "tree_a", 600, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_1, rarity=2)
    summoner_node_3 = Node("summoner_node_3", "tree_a", 700, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_2, rarity=2)
    summoner_node_4 = Node("summoner_node_4", "tree_a", 800, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_3, rarity=2)
    summoner_node_5 = Node("summoner_node_5", "tree_a", 900, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_4, rarity=2)
    summoner_node_5B = Node("summoner_node_5B", "tree_a", 900, 450, [[STR_NODE_1], [STR_NODE_2   ], [STR_NODE_3]], summoner_node_4, rarity=2)
    summoner_node_6 = Node("summoner_node_6", "tree_a", 1000, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_5, rarity=2)
    summoner_node_6B = Node("summoner_node_6B", "tree_a", 1000, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_5B, rarity=2)
    summoner_node_7 = Node("summoner_node_7", "tree_a", 1100, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_6, rarity=2)
    summoner_node_7B = Node("summoner_node_7B", "tree_a", 1100, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_6B, rarity=2)
    summoner_node_8 = Node("summoner_node_8", "tree_a", 1200, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_7, rarity=2)
    summoner_node_8B = Node("summoner_node_8B", "tree_a", 1200, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_7B, rarity=2)
    summoner_node_9 = Node("summoner_node_9", "tree_a", 1300, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_8, rarity=2)
    summoner_node_9B = Node("summoner_node_9B", "tree_a", 1300, 450, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_8B, rarity=2)
    summoner_node_10 = Node("summoner_node_10", "tree_a", 1400, 350, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_9, rarity=2)

    #DEMON_SUMMONING

    summoner_node_11 = Node("summoner_node_11", "tree_b", 500, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_start, rarity=2)
    summoner_node_12 = Node("summoner_node_12", "tree_b", 600, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_11, rarity=2)
    summoner_node_13 = Node("summoner_node_13", "tree_b", 700, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_12, rarity=2)
    summoner_node_14 = Node("summoner_node_14", "tree_b", 800, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_13, rarity=2)
    summoner_node_15 = Node("summoner_node_15", "tree_b", 900, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_14, rarity=2)
    summoner_node_16 = Node("summoner_node_16", "tree_b", 1000, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_15, rarity=2)
    summoner_node_17 = Node("summoner_node_17", "tree_b", 1100, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_16, rarity=2)
    summoner_node_18 = Node("summoner_node_18", "tree_b", 1200, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_17, rarity=2)
    summoner_node_19 = Node("summoner_node_19", "tree_b", 1300, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_18, rarity=2)
    summoner_node_20 = Node("summoner_node_20", "tree_b", 1400, 500, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_node_19, rarity=2)
    
    #UNDEAD_SUMMONING

    _summoner_node_21 = Node("summoner_node_21", "tree_b", 500, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], summoner_start, rarity=2)
    _summoner_node_22 = Node("summoner_node_22", "tree_b", 600, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_21, rarity=2)
    _summoner_node_23 = Node("summoner_node_23", "tree_b", 700, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_22, rarity=2)
    _summoner_node_24 = Node("summoner_node_24", "tree_b", 800, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_23, rarity=2)
    _summoner_node_25 = Node("summoner_node_25", "tree_b", 900, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_24, rarity=2)
    _summoner_node_26 = Node("summoner_node_26", "tree_b", 1000, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_25, rarity=2)
    _summoner_node_27 = Node("summoner_node_27", "tree_b", 1100, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_26, rarity=2)
    _summoner_node_28 = Node("summoner_node_28", "tree_b", 1200, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_27, rarity=2)
    _summoner_node_29 = Node("summoner_node_29", "tree_b", 1300, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_28, rarity=2)
    _summoner_node_30 = Node("summoner_node_30", "tree_b", 1400, 650, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]], _summoner_node_29, rarity=2)
    tree_d = Node("skil_d", "tree_b", 825, 500, [[]], tree_c)
    tree_e = Node("skil_e", "tree_b", 825, 650, [[]], tree_d)
    _ = Node("skil_d", "tree_b", 825, 500, [[]], tree_c)
    _ = Node("skil_c", "tree_b", 825, 350, [[]], tree_c)
    _ = Node("skil_e", "tree_b", 825, 650, [[]], tree_c)
    _ = Node("skil_f", "tree_b", 825, 800, [[]], tree_c)
    #ENSUITE, AJOUTE UNE ENTREE DANS LE FICHIER DE LOCALISATION (./ressources/locales/EN_US.json)
    #CORRESPONDANT AU name DE LA NODE DANS tree

    #CHANGE LA CLASSE DANS character.py POUR VOIR L'ARBRE DES AUTRES CLASSES
    #FOCUS SUR UNE CLASSE ET QUE LES MECHANIQUES
    #POUR LE DECOR ON VERA APRES

    #ICI, AJOUTE LA PREMIERE NODE DE L'ARBRE POUR CHAQUE CLASSE
    SYSTEM["tree"] = {
        Classes.SORCERESS: sorceress_start,
        Classes.WARRIOR: warrior_start,
        Classes.ESSENTIALIST: essentialist_start,
        Classes.ARCANIST: arcanist_start,
        Classes.SUMMONER: summoner_start
    }