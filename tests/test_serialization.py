import unittest
import json
import pygame
from data.image.image import Image
from data.image.animation import Animation
from data.constants import Flags, change_language, SYSTEM
from data.loading import load
from data.numerics.affliction import Affliction
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix
from data.numerics.stat import Stat
from data.numerics.rangestat import RangeStat
from data.numerics.ressource import Ressource
from data.item import Item
from data.creature import Creature
from data.character import Character
from data.numerics.damage import Damage
from data.game.spell import Spell
from data.game.tree import Node,GENERATE_SURFACES

pygame.init()
SYSTEM["keys"] = pygame.key.get_pressed()
change_language("EN_us")
load()

class TestingImages(unittest.TestCase):
    def test_stack_serialization(self):
        afx = Affix("a", 0, [Flags.FIRE])
        afl = Affliction("b", 1, 0, [Flags.PHYS])
        tab = [
            afx.export(),
            afl.export()
        ]
        tab_json = json.dumps(tab)
        restored_tab = json.loads(tab_json)
        restored_afx = Affix.imports(json.loads(restored_tab[0]))
        restored_afl = Affliction.imports(json.loads(restored_tab[1]))
        self.assertEqual(afx.name, restored_afx.name)
        self.assertEqual(afl.name, restored_afl.name)

    def cmp_affliction(self, a:Affliction, b:Affliction):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.flags, b.flags)
        self.assertEqual(a.value, b.value)
        self.assertEqual(a.stackable, b.stackable)

    def test_affliction(self):
        test = Affliction("truc", 50, -8, [Flags.STR, Flags.ARMOR], True, False)
        json_data = test.export()
        read = Affliction.imports(json.loads(json_data))
        self.cmp_affliction(test, read)

    def cmp_affix(self, a:Affix, b:Affix):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.flags, b.flags)
        self.assertEqual(a.value, b.value)
        self.assertEqual(a._bounds, b._bounds)

    def test_affix(self):
        test = Affix("machin", 5, [Flags.FIRE, Flags.AIMED_AT_PLAYER], 0.5, 1.8)
        json_data = test.export()
        read = Affix.imports(json.loads(json_data))
        self.cmp_affix(test, read)

    def cmp_double_affix(self, a:DoubleAffix, b:DoubleAffix):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.flags, b.flags)
        self.assertEqual(a._value_min, b._value_min)
        self.assertEqual(a._value_max, b._value_max)
        self.assertEqual(a._bounds_max, b._bounds_max)
        self.assertEqual(a._bounds_min, b._bounds_min)

    def test_double_affix(self):
        test = DoubleAffix("machin", 5, 15, [Flags.FIRE, Flags.AIMED_AT_PLAYER], 0.5, 1.8, 0.7, 1.9)
        json_data = test.export()
        read = DoubleAffix.imports(json.loads(json_data))
        self.cmp_double_affix(test, read)

    def cmp_stat(self, a, b):
        self.assertEqual(a.get_value(), b.get_value())
        self.assertEqual(a.value, b.value)
        self.assertEqual(a.name, b.name)
        self.assertEqual(a._cap, b._cap)
        self.assertEqual(a._round, b._round)
        self.assertEqual(a._scaling_value, b._scaling_value)

    def test_stat(self):
        stat = Stat(10, "Truc", 500, 0, 2, 5, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        self.assertEqual(stat.get_value(), 11)
        json_data = stat.export()
        read = Stat.imports(json.loads(json_data))
        self.cmp_stat(stat, read)

    def cmp_rangestat(self, a, b):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a._cap, b._cap)
        self.assertEqual(a._precision, b._precision)
        self.assertEqual(a._scaling_value, b._scaling_value)
        self.assertEqual(a.upper.get_value(), b.upper.get_value())
        self.assertEqual(a.lower.get_value(), b.lower.get_value())

    def test_rangestat(self):
        stat = RangeStat(0, 25, "truc", 999, -999, 3, 8, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        json_data = stat.export()
        read = RangeStat.imports(json.loads(json_data))

    def cmp_ressource(self, a, b):
        self.assertEqual(a.get_value(), b.get_value())
        self.assertEqual(a.rate.get_value(), b.rate.get_value())
        self.assertEqual(a.value, b.value)
        self.assertEqual(a.name, b.name)
        self.assertEqual(a._cap, b._cap)
        self.assertEqual(a._round, b._round)
        self.assertEqual(a._scaling_value, b._scaling_value)

    def test_ressources(self):
        stat = Ressource(10, "Truc", 0.01, 500, 0, 1, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        stat.tick()
        self.assertEqual(stat.get_value(), 11)
        json_data = stat.export()
        read = Ressource.imports(json.loads(json_data))
        self.cmp_ressource(stat, read)

    def cmp_item(self, a, b):
        if a is None or b is None:
            self.assertEqual(a, b)
            return
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.base, b.base)
        self.assertEqual(a.flags, b.flags)
        self.assertEqual(a.price, b.price)
        list_affx1, list_affx2 = a.affixes, b.affixes
        list_imp1, list_imp2 = a.implicits, b.implicits
        i = 0
        for _ in list_affx1:
            self.cmp_affix(list_affx1[i], list_affx2[i])
        i = 0
        for _ in list_imp1:
            self.cmp_affix(list_imp1[i], list_imp2[i])

    def test_item(self):
        afx1 = Affix("test1", 3, [Flags.FLAT, Flags.DEF])
        afx2 = Affix("test2", 5, [Flags.BOON, Flags.DEF])
        imp1 = Affix("test3", 3, [Flags.BLESS, Flags.DEF])
        it = Item("Bob's armor", "Armor", 12, 0, 1, Image("a"), 3, [Flags.ARMOR], [afx1, afx2], [imp1])
        it.name = "Bob's armor"
        json_data = it.export()
        read = Item.imports(json.loads(json_data))
        self.cmp_item(it, read)

    def cmp_creatures(self, a: Creature, b: Creature):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.ap, b.ap)
        self.assertEqual(a.exp, b.exp)
        self.assertEqual(a.exp_to_next, b.exp_to_next)
        self.assertEqual(a.level, b.level)
        for f in a.stats:
            if isinstance(a.stats[f], Stat):
                self.cmp_stat(a.stats[f], b.stats[f])
            elif isinstance(a.stats[f], RangeStat):
                self.cmp_rangestat(a.stats[f], b.stats[f])
            elif isinstance(a.stats[f], Ressource):
                self.cmp_ressource(a.stats[f], b.stats[f])
        for g in a.gear:
            if isinstance(a.gear[g], dict):
                for gg in a.gear[g]:
                    self.cmp_item(a.gear[g][gg], b.gear[g][gg])
            else:
                self.cmp_item(a.gear[g], b.gear[g])
        i = 0
        for _ in a.buffs:
            self.cmp_affliction(a.buffs[i], b.buffs[i])
            i+=1

    def test_creatures(self):
        bob = Creature("bob")
        afx1 = Affix("test1", 3, [Flags.FLAT, Flags.DEF])
        afx2 = Affix("test2", 5, [Flags.BOON, Flags.DEF])
        imp1 = Affix("test3", 3, [Flags.BLESS, Flags.DEF])
        it = Item("Bob's armor", "Armor", 12, 0, 1, Image("a"), 3, [Flags.ARMOR], [afx1, afx2], [imp1])
        bob.equip(Flags.ARMOR, it)
        json_data = bob.export()
        read = Creature.imports(json.loads(json_data))
        self.cmp_creatures(bob, read)

    def cmp_character(self, a:Character, b:Character):
        self.assertEqual(a.gold, b.gold)
        self.assertEqual(a.runes, b.runes)
        self.assertEqual(a.spellbook, b.spellbook)
        self.assertEqual(a.equipped_spells, b.equipped_spells)
        self.cmp_creatures(a.creature, b.creature)
        i = 0
        for item in a.inventory:
            self.cmp_item(a.inventory[i], b.inventory[i])
            i+=1
    
    def test_character(self):
        bob = Character(0, 0, "witch", 12)
        it = Item("Bob's armor", "Armor", 12, 0, 1, Image("a"), 3, [Flags.ARMOR], [], [])
        it2 = Item("Bob's gloves", "Armor", 12, 0, 1, Image("a"), 3, [Flags.HANDS], [], [])
        it3 = Item("Bob's boots", "Armor", 12, 0, 1, Image("a"), 3, [Flags.BOOTS], [], [])
        bob.inventory.extend([it, it2, it3])
        bob.equipped_spells = {
            "spell_1": "truc",
            "spell_2": "machin",
            "spell_3": None,
            "spell_4": None,
            "spell_5": None,
            "dash": "thing"
        }
        bob.spellbook = ["truc", "machin", "thing"]
        bob.gold = 151848181
        bob.runes = [1, 2, 3, 4, 5, 6, 7, 8]
        json_data = bob.export()
        read = Character.imports(json.loads(json_data))
        self.cmp_character(bob, read)

    def cmp_nodes(self, a:Node, b:Node):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.icon, b.icon)
        self.assertEqual(a._skills, b._skills)
        self.assertEqual(a.x, b.x)
        self.assertEqual(a.y, b.y)
        i = 0
        for _ in a.effects:
            self.cmp_affliction(a.effects[i], b.effects[i])
            i += 1
        i = 0
        for _ in a.connected:
            self.cmp_nodes(a.connected[i], b.connected[i])
            i+=1

    def test_nodes(self):
        tree = Node("TreeA", "rune_0", 0, 0, [], None, ["firebolt"], 3)
        afx1 = Affliction("test1", 3, 5, [Flags.FLAT, Flags.DEF])
        afx2 = Affliction("test2", 5, 3, [Flags.BOON, Flags.DEF])
        tree2 = Node("TreeB", "rune_1", 10, 0, [afx1], tree, [])
        tree3 = Node("TreeC", "rune_5", 20, 10 , [afx2], tree, ["icebolt", "voidbolt"])
        json_data = tree.export()
        read = Node.imports(json.loads(json_data))
        self.cmp_nodes(tree, read)

    def cmp_damage(self, a:Damage, b:Damage):
        self.assertEqual(a.coeff, b.coeff)
        self.assertEqual(a._bounds, b._bounds)
        self.assertEqual(a.flags, b.flags)
        self.assertEqual(a.ignore_block, b.ignore_block)
        self.assertEqual(a.ignore_dodge, b.ignore_dodge)
        self.assertEqual(a.types, b.types)
        self.assertEqual(a.penetration, b.penetration)
        self.assertEqual(a.crit_mult, b.crit_mult)

    def test_damage(self):
        dmg = Damage(5, fire=10, dark=5, fp=0.8, flags=[Flags.FIRE, Flags.DARK], ignore_block=True, upper_bound=5.5)
        json_data = dmg.export()
        read = Damage.imports(json.loads(json_data))
        self.cmp_damage(dmg, read)

    def cmp_spell(self, a:Spell, b:Spell):
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.level, b.level)
        self.cmp_damage(a._base_damage, b._base_damage)
        self.assertEqual(a.flags, b.flags)
        i = 0
        for _ in a._buffs:
            self.cmp_affliction(a._buffs[i], b._buffs[i])
            i += 1
        self.assertEqual(a.icon.uri, b.icon.uri)
        i = 0
        for i in a.stats:
            if isinstance(a.stats[i], Stat):
                self.cmp_stat(a.stats[i], b.stats[i])
            if isinstance(a.stats[i], RangeStat):
                self.cmp_rangestat(a.stats[i], b.stats[i])
            if isinstance(a.stats[i], Ressource):
                self.cmp_ressource(a.stats[i], b.stats[i])
    
    def test_spell(self):
        spell = SYSTEM["spells"]["firebolt"]
        json_data = spell.export()
        read = Spell.imports(json.loads(json_data))
        self.cmp_spell(spell, read)
