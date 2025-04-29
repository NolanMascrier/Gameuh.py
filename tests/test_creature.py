from data.creature import Creature
from data.damage import Damage
from data.numerics.affliction import Affliction
from data.constants import Flags
from data.numerics.affix import Affix
from data.item import Item
import unittest

def print_gear(c: Creature):
    print("############")
    for it in c.gear:
        if it == "ring":
            print(f"Left ring: {None if c.gear[it]['left'] is None else c.gear[it]['left'].name}")
            print(f"Left ring: {None if c.gear[it]['right'] is None else c.gear[it]['right'].name}")
        else:
            print(f"{it} = {None if c.gear[it] is None else c.gear[it].name}")

class TestingCreatureDamage(unittest.TestCase):
    def test_damage(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1)
        bob.damage(fireball)
        self.assertEqual(bob.stats["life"].current_value, 88.0)
    
    def test_damage_penetrative(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1, fp=0.5)
        bob.damage(fireball)
        self.assertEqual(bob.stats["life"].current_value, 82.0)
    
    def test_healing(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1)
        bob.damage(fireball)
        bob.heal(12)
        self.assertEqual(bob.stats["life"].current_value, 100.0)
    
    def test_overhealing(self):
        bob = Creature("Bob")
        bob.heal(9999)
        self.assertEqual(bob.stats["life"].current_value, 100.0)

    def test_name(self):
        bob = Creature("Bob")
        bob.name = "Jean"
        self.assertEqual(bob.name, "Jean")

    def test_dot(self):
        bob = Creature("Bob")
        dot = ["bobo_feu", 5, 3]

    def test_affliction(self):
        bob = Creature("Bob")
        poison = Affliction("poison", -10, 3, [Flags.LIFE, Flags.DOT])
        bob.afflict(poison)
        self.assertEqual(len(bob._buffs), 1)
        bob.tick()
        bob.tick()
        bob.tick()
        bob.tick()
        bob.tick()
        self.assertEqual(bob.stats["life"].current_value, 70)
        self.assertEqual(len(bob._buffs), 0)

    def test_buff(self):
        bob = Creature("Bob")
        self.assertEqual(bob.stats["str"].value, 10)
        potion = Affliction("potion", 0.10, 1, [Flags.STR, Flags.BOON], True)
        benediction = Affliction("holy smite", 2, 1, [Flags.STR, Flags.BLESS])
        sword = Affliction("sword", 10, 1, [Flags.STR, Flags.FLAT])
        bob.afflict(sword)
        self.assertEqual(bob.stats["str"].get_value(), 20)
        bob.afflict(sword)
        self.assertEqual(bob.stats["str"].get_value(), 20)
        bob.afflict(potion)
        self.assertEqual(bob.stats["str"].get_value(), 22.0)
        bob.afflict(potion)
        self.assertEqual(bob.stats["str"].get_value(), 24.0)
        bob.afflict(benediction)
        self.assertEqual(bob.stats["str"].get_value(), 48.0)

    def test_level_up(self):
        bob = Creature("Bob")
        self.assertEqual(bob.level, 1)
        self.assertEqual(bob.exp, 0)
        bob.grant_experience(100)
        self.assertEqual(bob.level, 2)
        bob.grant_experience(100000)
        self.assertGreater(bob.level, 3)
        self.assertLess(bob.exp, bob.exp_to_next)

    def test_equip(self):
        bob = Creature("Bob")
        self.assertEqual(bob.stats["str"].get_value(), 10)
        aff = Affix("def", 10, [Flags.STR, Flags.FLAT])
        armor = Item("Bob's armor", 999, 0, 1, [Flags.GEAR, Flags.ARMOR], [aff])
        bob.equip(Flags.ARMOR, armor)
        self.assertEqual(bob.stats["str"].get_value(), 20)
        self.assertEqual(bob.gear["armor"], armor)
        bob.unequip(Flags.ARMOR)
        self.assertEqual(bob.stats["str"].get_value(), 10)
        self.assertEqual(bob.gear["armor"], None)

    def test_mana(self):
        bob = Creature("Bob")
        self.assertEqual(bob.stats["mana"].current_value, 50)
        bob.consume_mana(20)
        self.assertEqual(bob.stats["mana"].current_value, 30)
        bob.restore_mana(20)
        self.assertEqual(bob.stats["mana"].current_value, 50)
        bob.restore_mana(50)
        self.assertEqual(bob.stats["mana"].current_value, 50)
        bob.consume_mana(30)
        bob.tick()
        self.assertEqual(bob.stats["mana"].current_value, 22.5)
        bob.consume_mana(999999)
        self.assertEqual(bob.stats["mana"].current_value, 0)

if __name__ == '__main__':
    unittest.main()
