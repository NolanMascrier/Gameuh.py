from data.item import Item
from data.constants import Flags
from data.numerics.damage import Damage
import unittest
from data.api.surface import init_engine

init_engine()

class TestItems(unittest.TestCase):
    def test_fields(self):
        potion = Item("potion", "", 250, 999, 256, None, 0)
        self.assertEqual(potion.name, "potion")
        self.assertEqual(potion.price, 250)
        self.assertEqual(potion.power, 999)
        self.assertEqual(potion.max_held, 256)
        self.assertEqual(potion.flags, [])
        self.assertEqual(potion.affixes, [])

    def test_modif(self):
        potion = Item("potion", "", 250, 999, 256, None, 0)
        potion.name = "piki piki piman"
        self.assertEqual(potion.name, "piki piki piman")
        potion.price = 252525
        self.assertEqual(potion.price, 252525)
        potion.power = -2
        self.assertEqual(potion.power, -2)
        potion.max_held = 5
        self.assertEqual(potion.max_held, 5)
        potion.flags = [Flags.CURSE]
        self.assertEqual(potion.flags, [Flags.CURSE])
        potion.affixes = [Flags.DARK]
        self.assertEqual(potion.affixes, [Flags.DARK])

class TestDamage(unittest.TestCase):
    def test_fields(self):
        dmg = Damage(20, dark = 1, dp=0.2)
        self.assertEqual(dmg.coeff, 20)
        self.assertEqual(dmg.types["dark"], 1)
        self.assertEqual(dmg.penetration["dark"], 0.2)
    
    def test_modif(self):
        dmg = Damage(20, dark = 1, dp=0.2)
        dmg.coeff = 5
        self.assertEqual(dmg.coeff, 5)
        dmg.coeff = 20
        self.assertEqual(dmg.coeff, 20)
        dmg.types["fire"] = 0.5
        self.assertEqual(dmg.types["fire"], 0.5)
        dmg.penetration["fire"] = 1
        self.assertEqual(dmg.penetration["fire"], 1)

if __name__ == '__main__':
    unittest.main()
