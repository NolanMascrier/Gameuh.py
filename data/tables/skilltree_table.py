"""Skills for the skill tree."""

from data.constants import SYSTEM, Flags, Classes
from data.numerics.affliction import Affliction
from data.game.tree import Node

STR_NODE = Affliction("tree_str", 5, -1, [Flags.FLAT, Flags.STR], True)

def generate_tree():
    """Creates the tree."""

    #ICI, AJOUTE CHAQUE NODE UNE PAR UNE
    #SI UNE NODE EST UNE FEUILLE, ELLE N'AS PAS BESOIN D'AVOIR DE NOM
    tree_start = Node("start", "tree_start", 250, 250, [STR_NODE], None)
    _ = Node("buffa", "tree_a", 500, 250, [], tree_start, ["firebolt2"])
    tree_b = Node("skil_a", "tree_b", 500, 500, [], tree_start)
    tree_c = Node("skil_b", "tree_b", 650, 500, [], tree_b)
    _ = Node("skil_d", "tree_b", 825, 500, [], tree_c)
    _ = Node("skil_c", "tree_b", 825, 350, [], tree_c)
    _ = Node("skil_e", "tree_b", 825, 650, [], tree_c)
    #ENSUITE, AJOUTE UNE ENTREE DANS LE FICHIER DE LOCALISATION (./ressources/locales/EN_US.json)
    #CORRESPONDANT AU name DE LA NODE DANS tree

    #CHANGE LA CLASSE DANS character.py POUR VOIR L'ARBRE DES AUTRES CLASSES
    #FOCUS SUR UNE CLASSE ET QUE LES MECHANIQUES
    #POUR LE DECOR ON VERA APRES

    #ICI, AJOUTE LA PREMIERE NODE DE L'ARBRE POUR CHAQUE CLASSE
    SYSTEM["tree"] = {
        Classes.SORCERESS: tree_start,
        Classes.WARRIOR: None,
        Classes.ESSENTIALIST: None,
        Classes.ARCANIST: None,
        Classes.SUMMONER: None
    }
