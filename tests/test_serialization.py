import unittest
import json
from data.constants import Flags
from data.numerics.affliction import Affliction
from data.numerics.affix import Affix
from data.numerics.double_affix import DoubleAffix
from data.numerics.stat import Stat
from data.numerics.rangestat import RangeStat
from data.numerics.ressource import Ressource

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

    def test_affliction(self):
        test = Affliction("truc", 50, -8, [Flags.STR, Flags.ARMOR], True, False)
        json_data = test.export()
        read = Affliction.imports(json.loads(json_data))
        self.assertEqual(test.name, read.name)
        self.assertEqual(test.flags, read.flags)
        self.assertEqual(test.value, read.value)
        self.assertEqual(test.stackable, read.stackable)

    def test_affix(self):
        test = Affix("machin", 5, [Flags.FIRE, Flags.AIMED_AT_PLAYER], 0.5, 1.8)
        json_data = test.export()
        read = Affix.imports(json.loads(json_data))
        self.assertEqual(test.name, read.name)
        self.assertEqual(test.flags, read.flags)
        self.assertEqual(test.value, read.value)
        self.assertEqual(test._bounds, read._bounds)

    def test_double_affix(self):
        test = DoubleAffix("machin", 5, 15, [Flags.FIRE, Flags.AIMED_AT_PLAYER], 0.5, 1.8, 0.7, 1.9)
        json_data = test.export()
        read = DoubleAffix.imports(json.loads(json_data))
        self.assertEqual(test.name, read.name)
        self.assertEqual(test.flags, read.flags)
        self.assertEqual(test._value_min, read._value_min)
        self.assertEqual(test._value_max, read._value_max)
        self.assertEqual(test._bounds_max, read._bounds_max)
        self.assertEqual(test._bounds_min, read._bounds_min)

    def test_stat(self):
        stat = Stat(10, "Truc", 500, 0, 2, 5, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        stat.tick()
        self.assertEqual(stat.get_value(), 11)
        json_data = stat.export()
        read = Stat.imports(json.loads(json_data))
        self.assertEqual(read.get_value(), 11)
        self.assertEqual(stat.value, read.value)
        self.assertEqual(stat.name, read.name)
        self.assertEqual(stat._cap, read._cap)
        self.assertEqual(stat._round, read._round)
        self.assertEqual(stat._scaling_value, read._scaling_value)

    def test_rangestat(self):
        stat = RangeStat(0, 25, "truc", 999, -999, 3, 8, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        json_data = stat.export()
        read = RangeStat.imports(json.loads(json_data))
        self.assertEqual(stat.name, read.name)
        self.assertEqual(stat._cap, read._cap)
        self.assertEqual(stat._precision, read._precision)
        self.assertEqual(stat._scaling_value, read._scaling_value)
        self.assertEqual(stat.upper.get_value(), read.upper.get_value())
        self.assertEqual(stat.lower.get_value(), read.lower.get_value())

    def test_ressources(self):
        stat = Ressource(10, "Truc", 0.01, 500, 0, 1, True)
        afl = Affliction("machin", 1, 5, [Flags.ABS_DEF, Flags.FLAT])
        stat.afflict(afl)
        stat.tick()
        self.assertEqual(stat.get_value(), 11)
        json_data = stat.export()
        read = Ressource.imports(json.loads(json_data))
        self.assertEqual(read.get_value(), 11)
        self.assertEqual(stat.rate.get_value(), read.rate.get_value())
        self.assertEqual(stat.value, read.value)
        self.assertEqual(stat.name, read.name)
        self.assertEqual(stat._cap, read._cap)
        self.assertEqual(stat._round, read._round)
        self.assertEqual(stat._scaling_value, read._scaling_value)
