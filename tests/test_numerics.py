from data.creature import Creature
from data.numerics.damage import Damage
from data.numerics.affliction import Affliction
from data.constants import Flags
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix
from data.numerics.rangestat import Stat, RangeStat
from data.numerics.ressource import Ressource
import unittest

class TestingNumerics(unittest.TestCase):
    def test_affliction(self):
        a = Affliction("test", 1, 3, [Flags.ABS_DEF])
        b = a.clone()
        c = Affliction("test", 1, 3, None)
        d = Affliction("test", 2, 3, [Flags.ABS_DEF])
        e = Affliction("test", 1, 4, [Flags.ABS_DEF])
        f = Affliction("truc", 5, 5, [Flags.STR], True, True, 1)
        self.assertNotEqual(a, "b")
        self.assertFalse(a == "b")
        self.assertEqual(a, b)
        self.assertEqual(str(a), str(b))
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertNotEqual(a, f)
        a.name = "truc"
        a.value = 5
        a.duration = 5
        a.flags = [Flags.STR]
        a.stackable = True
        a.refreshable = True
        a.damage = 1
        self.assertEqual(a, f)
        a.tick()
        self.assertNotEqual(5, a.elapsed)
        self.assertIsNotNone(a.describe())

    def test_affix(self):
        a = Affix("test", 10, [Flags.STR], 0.5, 1.5)
        b = Affix("testa", 10, [Flags.STR], 0.5, 1.5)
        c = Affix("test", 13, [Flags.STR], 0.9, 1.1)
        d = Affix("test", 10, [Flags.INT, Flags.DESC_PERCENT], 0.5, 1.5)
        e = Affix("truc_2", 0, [Flags.INT], 1, 1)
        g = Affix("truc_2", -2, [Flags.INT, Flags.FLAT], 1, 1)
        h = Affix("truc_2", 3, [Flags.INT, Flags.HEX], 1, 1)
        i = Affix("truc_2", 3, [Flags.INT, Flags.CURSE], 1, 1)
        self.assertNotEqual(a, "b")
        self.assertFalse(a == "b")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        a.name = "truc_2"
        a.value = 0
        a.flags = [Flags.INT]
        a._bounds = (1, 1)
        self.assertEqual(a, e)
        self.assertEqual(a.flag_key, e.flag_key)
        self.assertEqual(a.price_factor, e.price_factor)
        f = c.roll()
        b.seal(True)
        a.reroll()
        a.seal(True)
        a.reroll()
        a.flags = []
        self.assertIsNone(a.flag_key)
        self.assertAlmostEqual(c.value, f.value, delta=0.1 * c.value)
        self.assertIsNotNone(f.describe())
        self.assertIsNotNone(a.describe())
        self.assertIsNotNone(b.describe())
        self.assertIsNotNone(g.describe())
        self.assertIsNotNone(h.describe())
        self.assertIsNotNone(i.describe())
        self.assertIsNotNone(f.describe())
        self.assertIsNotNone(a.describe_details())
        self.assertIsNotNone(b.describe_details())
        self.assertIsNotNone(g.describe_details())
        self.assertIsNotNone(h.describe_details())
        self.assertIsNotNone(i.describe_details())
        self.assertEqual(type(a.as_affliction()), Affliction)


    def test_doubleaffix(self):
        a = DoubleAffix("test", 10, 15, [Flags.STR], 0.5, 1.5, 0.5, 1.5)
        b = DoubleAffix("testa", 10, 15, [Flags.STR], 0.5, 1.5, 0.5, 1.5)
        c = DoubleAffix("test", 13, 20, [Flags.STR], 0.9, 1.1, 0.9, 1.1)
        d = DoubleAffix("test", 10, 15, [Flags.INT], 0.5, 1.5, 0.5, 1.5)
        e = DoubleAffix("truc_2", 0, 0, [Flags.INT], 1, 1, 1, 1)
        g = DoubleAffix("truc_2", 0, 0, [], 1, 1, 1, 1)
        h = DoubleAffix("truc_2", -10, -5, [Flags.DESC_UNIQUE], 1, 1, 1, 1)
        h.seal(True)
        self.assertNotEqual(a, "b")
        self.assertFalse(a == "b")
        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertIsNone(g.flag_key)
        a.name = "truc_2"
        a.value = (0, 0)
        a._bounds_min = (1, 1)
        a._bounds_max = (1, 1)
        a.flags = [Flags.INT]
        self.assertEqual(a, e)
        self.assertEqual(a.flag_key, e.flag_key)
        self.assertEqual(a.price_factor, e.price_factor)
        f = c.roll()
        b.seal(True)
        self.assertAlmostEqual(c.value[0], f.value[0], delta=0.1 * c.value[0])
        self.assertAlmostEqual(c.value[1], f.value[1], delta=0.1 * c.value[1])
        self.assertIsNotNone(f.describe())
        self.assertIsNotNone(a.describe())
        self.assertIsNotNone(b.describe())
        self.assertIsNotNone(h.describe())
        self.assertIsNotNone(f.describe_details())
        self.assertIsNotNone(a.describe_details())
        self.assertIsNotNone(b.describe_details())
        self.assertIsNotNone(h.describe_details())
        self.assertEqual(type(a.as_affliction()), tuple)
        a.reroll()
        a.seal(True)
        a.reroll()

    def test_damage(self):
        d = Damage(10, 10)
        c = Creature("bob")
        d.flags = [Flags.MELEE, Flags.RANGED, Flags.SPELL]
        d.origin = None
        d.ignore_block = True
        d.ignore_dodge = True
        self.assertEqual(type(d.describe(c, True, True, True)), str)

    def test_stat(self):
        a = Stat(10, "test", 1000, 0, 2, 1, False)
        b = Stat(0, "test", 1000, 0, 2, 2, True)
        g = Stat(100, "test", 1000, 0, 2, 1, False)
        h = Stat(10, "teset", 1000, 0, 2, 1, False)
        c = a.clone()
        b.name = "truc"
        b.value = 10
        self.assertNotEqual(a, "b")
        self.assertFalse(a == "b")
        self.assertEqual(a, c)
        self.assertNotEqual(a, g)
        self.assertNotEqual(a, h)
        self.assertEqual(b.mults, [])
        self.assertEqual(b.incr, [])
        self.assertEqual(b.flats, [])
        b.mults = []
        b.flats = []
        b.flats = []
        a.scale(10)
        b.scale(10)
        self.assertEqual(a.value, 20)
        self.assertEqual(b.value, 200)
        b.scale(999)
        self.assertEqual(b.get_value(), 1000)
        af1 = Affliction("a", 1, 0, [Flags.BOON])
        af2 = Affliction("b", 1, 0, [Flags.BLESS])
        af3 = Affliction("c", 1, 0, [Flags.FLAT])
        af4 = Affliction("d", 1, 0, [Flags.FLAT], stackable=True, refreshable=True)
        af5 = Affliction("a", 1, 0, [Flags.HEX])
        af6 = Affliction("b", 1, 0, [Flags.CURSE])
        a.afflict(af1)
        a.afflict(af2)
        a.afflict(af3)
        self.assertEqual(a.c_value, 84)
        self.assertEqual(len(a.gather_afflictions()), 3)
        a.tick()
        self.assertEqual(len(a.gather_afflictions()), 0)
        a.afflict(af1)
        self.assertEqual(len(a.gather_afflictions()), 1)
        a.reset()
        self.assertEqual(len(a.gather_afflictions()), 0)
        self.assertEqual(type(a.describe()), tuple)
        self.assertEqual(type(a.describe(False, True)), tuple)
        a.afflict(af1)
        a.afflict(af2)
        a.afflict(af3)
        a.remove_affliction(af1)
        a.remove_affliction(af2)
        a.remove_affliction(af3)
        a.afflict(af4)
        a.afflict(af4)
        a.incr = [af1]
        a.reset()
        a.afflict(af5)
        a.afflict(af6)
        self.assertEqual(a.c_value, 0)

    def test_rangestat(self):
        a = RangeStat(0, 5, "a", 100, 0)
        b = RangeStat(0, 5, "a", 100, 0)
        a.name = "aa"
        a.lower = b.lower
        a.upper = b.upper
        self.assertEqual(a.lower, b.lower)
        self.assertEqual(a.upper, b.upper)
        a.lower.value = 5
        a.upper.value = 10
        b = a.roll()
        self.assertTrue(b >= 5)
        self.assertTrue(b <= 10)
        self.assertEqual(type(a.describe()), tuple)
        self.assertEqual(type(a.describe(True, True)), tuple)
        a.scale(10)
        af1 = Affliction("test_min", 1, 5, flags=[Flags.BLESS])
        af2 = Affliction("test_max", 1, 5, flags=[Flags.BLESS])
        a.afflict(af1)
        a.afflict(af2)
        self.assertEqual(len(a.upper.gather_afflictions()), 1)
        self.assertEqual(len(a.lower.gather_afflictions()), 1)
        a.remove_affliction(af1)
        a.remove_affliction(af2)
        self.assertEqual(len(a.upper.gather_afflictions()), 0)
        self.assertEqual(len(a.lower.gather_afflictions()), 0)
        a.afflict(af1)
        a.afflict(af2)
        self.assertEqual(len(a.upper.gather_afflictions()), 1)
        self.assertEqual(len(a.lower.gather_afflictions()), 1)
        a.reset()
        self.assertEqual(len(a.upper.gather_afflictions()), 0)
        self.assertEqual(len(a.lower.gather_afflictions()), 0)
        self.assertEqual(a.get_value(), (10, 5))

    def test_ressources(self):
        a = Ressource(100, "test")
        c = Ressource(10, "test")
        d = Ressource(100, "teste")
        self.assertNotEqual(a, "e")
        self.assertFalse(a == "e")
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        d.current_value = c.current_value
        af1 = Affliction("test_min", -1, 5, flags=[Flags.DOT])
        af2 = Affliction("test2_min", -1, 5, flags=[Flags.MDOT])
        af3 = Affliction("test3_min", -1, 0, flags=[Flags.MDOT])
        self.assertEqual(a.buffs, [])
        self.assertEqual(a.buffs_multi, [])
        a.buffs = [af1]
        self.assertEqual(len(a.gather_afflictions()), 1)
        a.buffs_multi = [af1]
        self.assertEqual(len(a.gather_afflictions()), 2)
        a.reset()
        self.assertEqual(len(a.gather_afflictions()), 0)
        b = a.clone()
        self.assertNotEqual(a, "b")
        self.assertFalse(a == "b")
        self.assertEqual(a, b)
        a.afflict(af1)
        a.afflict(af2)
        a.afflict(af3)
        af3.tick()
        a.tick()
        a.remove_affliction(af1)
        a.remove_affliction(af2)
        self.assertEqual(len(a.gather_afflictions()), 0)
        self.assertEqual(type(a.describe()), tuple)
        self.assertEqual(type(a.describe(False)), tuple)
        
