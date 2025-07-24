import unittest
import pygame
import os
from data.image.image import Image
from data.constants import RESSOURCES

RESSOURCES = "ressources/"
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.display.set_mode((1, 1))

class TestingImages(unittest.TestCase):
    def test_image_basic(self):
        img = Image("default.png")
        self.assertEqual(img.width, 96)
        self.assertEqual(img.height, 96)
        self.assertEqual(img.visible, True)
        img.visible = False
        self.assertEqual(img.visible, False)
        self.assertIsInstance(img.get_image(), pygame.Surface)

    def test_image_not_exist(self):
        img = Image("apyr.xvg")
        self.assertEqual(img._uri, "default.png")

    def test_image_copy(self):
        img = Image("default.png")
        img2 = Image(img)
        self.assertEqual(img._uri, img2._uri)

    def test_manipulations(self):
        img = Image("default.png")
        img.scale(100, 100)
        self.assertEqual(img.height, 100)
        self.assertEqual(img.width, 100)
        img.rotate(90)
        self.assertEqual(img.height, 100)
        self.assertEqual(img.width, 100)
        img.flip(True, True)
        img2 = img.extracts(0, 0, 25, 25)
        self.assertEqual(img2.height, 25)
        self.assertEqual(img2.width, 25)

