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

    #ICI, AJOUTE CHAQUE NODE UNE PAR UNE
    #SI UNE NODE EST UNE FEUILLE, ELLE N'AS PAS BESOIN D'AVOIR DE NOM
    sorceress_start = Node("start", "tree_start", 250, 700, [[STR_NODE_1], [STR_NODE_2], [STR_NODE_3]],
                      None, rarity=1)
    _fire_mastery = Node("fire_mastery", "fire_mastery", 500, 350, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], sorceress_start)
    _firebolter = Node("fireball", "explosion", 500, 250, 20, _fire_mastery,
                       rarity=2) #Mets rarity=2 pour dire un skill, c'est purement visuel
    _firestorm = Node("firestorm", "firestorm", 600, 250, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _firebolter)
    _meteor = Node("meteor", "tree_a", 700, 250, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _firestorm)
    _pyrotechnics = Node("pyrotechnics", "pyrotechnics", 700, 350, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _fire_mastery)
    _cone_of_flames = Node("cone_of_flames", "cone_of_flames", 500, 450, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _fire_mastery)
    _inferno = Node("inferno", "inferno", 600, 450, [[FIRE_NODE_1], [FIRE_NODE_2], [FIRE_NODE_3],
                                [FIRE_NODE_4], [FIRE_NODE_5, FIRE_NODE_5B]], _cone_of_flames)
    tree_b = Node("skil_a", "tree_b", 500, 500, [[]], None)
    _ice_mastery = Node("ice_mastery", "ice_mastery", 500, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], sorceress_start)
    _congelation = Node("congelation", "congelation", 600, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_mastery)
    _icebolt = Node("icebolt", "icebolt", 700, 700, [[ICE_NODE_1], [ICE_NODE_2], [ICE_NODE_3],
                                [ICE_NODE_4], [ICE_NODE_5, ICE_NODE_5B]], _ice_mastery)
    tree_c = Node("skil_b", "tree_b", 650, 500, [[]], tree_b)
    _lightning_mastery = Node("lightning_mastery", "lightning_mastery", 500, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], sorceress_start)
    _shock = Node("shock", "shock", 600, 1200, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery, ["shock"])
    _lightning_bolt = Node("lightning_bolt", "lightning_bolt", 600, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery, ["lightning_bolt"])
    _conduction = Node("conduction", "conduction", 600, 1000, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_mastery)
    _lightning_sphere = Node("lightning_sphere", "tree_a", 700, 1100, [[LIGHTNING_NODE_1], [LIGHTNING_NODE_2], [LIGHTNING_NODE_3],
                                [LIGHTNING_NODE_4], [LIGHTNING_NODE_5, LIGHTNING_NODE_5B]], _lightning_bolt)
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
        Classes.WARRIOR: None,
        Classes.ESSENTIALIST: None,
        Classes.ARCANIST: None,
        Classes.SUMMONER: None
    }
