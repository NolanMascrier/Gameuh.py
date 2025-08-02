import unittest
import json
import pygame
from data.image.image import Image
from data.constants import Flags, change_language
from data.numerics.affliction import Affliction
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix
from data.numerics.stat import Stat
from data.numerics.rangestat import RangeStat
from data.numerics.ressource import Ressource
from data.item import Item
from data.creature import Creature

pygame.init()
change_language("EN_us.json")

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
