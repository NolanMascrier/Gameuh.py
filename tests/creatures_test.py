from data.Creature import Creature
from data.Damage import Damage
import unittest

bob = Creature("Bob")
fireball = Damage(10, 1.2, fire=1)
fireball_pen = Damage(10, 1.2, fire=1, fp=0.25)
heal = 9999

print("Launching")

class TestingCreatureDamage(unittest.TestCase):
    def test_damage(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1)
        bob.damage(fireball)
        self.assertEqual(bob.life._value, 88.0)
    
    def test_damage_penetrative(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1, fp=0.5)
        bob.damage(fireball)
        self.assertEqual(bob.life._value, 82.0)
    
    def test_healing(self):
        bob = Creature("Bob")
        fireball = Damage(10, 1.2, fire=1)
        bob.damage(fireball)
        bob.heal(12)
        self.assertEqual(bob.life._value, 100.0)
    
    def test_overhealing(self):
        bob = Creature("Bob")
        bob.heal(9999)
        self.assertEqual(bob.life._value, 100.0)

if __name__ == '__main__':
    unittest.main()