import unittest
import pygame
import enum
from time import sleep
from data.constants import *
from data.filesystem import change_language

class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertIsInstance(SCREEN_WIDTH, int)
        self.assertIsInstance(SCREEN_HEIGHT, int)
        self.assertIsInstance(PROJECTILE_TRACKER, list)
        self.assertIsNone(FONT)

    def test_language(self):
        change_language("DD_dd")
        self.assertIsNone(SYSTEM["lang"])
        change_language("FR_fr")
        self.assertEqual(SYSTEM["lang"]["fire_dot"], "Brulures")
        change_language("EN_us")
        self.assertEqual(SYSTEM["lang"]["fire_dot"], "Burning")

class TestImports(unittest.TestCase):
    def test_import_pygame(self):
        self.assertTrue(pygame, "pygame import failed")
        
    def test_import_sleep(self):
        self.assertTrue(sleep, "time.sleep import failed")

    def test_import_enum(self):
        self.assertTrue(enum, "enum import failed")
        
if __name__ == '__main__':
    unittest.main()