import unittest
import pygame
import enum
from time import sleep
from data.constants import *

class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertIsInstance(SCREEN_WIDTH, int)
        self.assertIsInstance(SCREEN_HEIGHT, int)
        self.assertIsInstance(PROJECTILE_TRACKER, list)
        self.assertIsInstance(FIREBALL_IMAGE, str)
        self.assertIsInstance(UI_JAUGE, str)
        self.assertIsInstance(UI_JAUGE_L, str)
        self.assertIsInstance(UI_JAUGE_C, str)
        self.assertIsInstance(UI_JAUGE_M, str)
        self.assertIsInstance(JAUGE_L, str)
        self.assertIsInstance(JAUGE_C, str)
        self.assertIsInstance(JAUGE_M, str)
        self.assertIsNone(FONT)

    def test_language(self):
        global LANGUAGE
        self.assertIsNone(LANGUAGE)
        LANGUAGE = change_language("ressources/locales/RU_ru")
        self.assertIsNone(LANGUAGE)
        LANGUAGE = change_language("ressources/locales/FR_fr")
        self.assertEqual(LANGUAGE["fire_dot"], "Brulures")
        LANGUAGE = change_language("ressources/locales/EN_us")
        self.assertEqual(LANGUAGE["fire_dot"], "Burning")

class TestImports(unittest.TestCase):
    def test_import_pygame(self):
        self.assertTrue(pygame, "pygame import failed")
        
    def test_import_sleep(self):
        self.assertTrue(sleep, "time.sleep import failed")

    def test_import_enum(self):
        self.assertTrue(enum, "enum import failed")
        
if __name__ == '__main__':
    unittest.main()