from data.creature import Creature
from data.damage import Damage
from data.numerics.affliction import Affliction
from data.constants import Flags
import unittest

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
        sword = Affliction("sword", 10, 1, [Flags.STR, Flags.GEAR])
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

if __name__ == '__main__':
    unittest.main()