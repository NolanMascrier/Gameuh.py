import unittest
import pygame
import os
from data.image.image import Image
from data.image.text import Text
from data.image.text_generator import TextGenerator
from data.image.animation import Animation
from data.image.hoverable import Hoverable
from data.image.parallaxe import Parallaxe
from data.constants import RESSOURCES, SYSTEM, TEXT_TRACKER
from data.loading import load_tiles
from data.api.surface import Surface

RESSOURCES = "ressources/"
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
SYSTEM["windows"] = pygame.display.set_mode((1, 1))
load_tiles()
SYSTEM["mouse"] = (0, 0)
SYSTEM["player.x"] = 0
SYSTEM["player.y"] = 0

class TestingImages(unittest.TestCase):
    def test_image_basic(self):
        img = Image("default.png")
        self.assertEqual(img.width, 96)
        self.assertEqual(img.height, 96)
        self.assertEqual(img.visible, True)
        img.visible = False
        self.assertEqual(img.visible, False)
        self.assertIsInstance(img.get_image(), Surface)

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
        img2.opacity(125)
        self.assertEqual(img2.image.get_alpha(), 125)

class TestingText(unittest.TestCase):
    def test_text_basic(self):
        txt = Text("Truc", True, "tiny")
        self.assertIsInstance(txt.image, Surface)
        self.assertIsInstance(txt.surface, Surface)
        txt.draw(0,0)
        self.assertEqual(txt.get_size(), txt.surface.get_size())
        txt = Text(None, True, "tiny")
        txt = Text(["#c#(255,255,255)#s#(35)Truc", "#b#(1)#i#(1)machin", "wiwi#c#(255, 125, 125)wi"], True, "tiny")

    def test_text_adv(self):
        txt = Text("Truc\nMachin", True, "tiny", 100, 200, 20, True, True, (155,155,155))
        self.assertEqual(txt.width, 100)
        self.assertEqual(txt.height, 200)
        txt.opacity(125)
        self.assertEqual(txt.surface.get_alpha(), 125)

class TestingAnimation(unittest.TestCase):
    def test_anim_basic(self):
        anim = Animation("default.png", 24, 24, lines=4)
        self.assertEqual(anim.width, 24)
        self.assertEqual(anim.height, 24)
        self.assertEqual(len(anim._sequence), 16)
        self.assertEqual(anim.get_image().get_width(), 24)
        self.assertEqual(anim._current_frame, 0)
        anim.tick()
        self.assertEqual(anim.frame, 1)
        for _ in range(100):
            anim.tick()
    
    def test_no_loop(self):
        anim = Animation("default.png", 48, 96, plays_once=True, loops=False)
        anim.tick()
        anim.tick()
        anim.tick()
        self.assertEqual(anim.finished, True)
        anim = Animation("default.png", 48, 96, animated=False)
        anim.tick()

    def test_clone(self):
        anim = Animation("default.png", 24, 24, lines=4)
        anim2 = anim.clone()
        self.assertEqual(anim2.width, 24)
        self.assertEqual(anim2.height, 24)
        self.assertEqual(len(anim2._sequence), 16)
        self.assertEqual(anim2.get_image().get_width(), 24)
    
    def test_manipulation(self):
        anim = Animation("default.png", 24, 24, lines=4)
        anim.scale(100, 100)
        self.assertEqual(len(anim._sequence), 16)
        anim.rotate(90)
        anim.flip(True, True)

class TestingHoverable(unittest.TestCase):
    def test_basic(self):
        hv = Hoverable(0, 0, "truc", "shit")
        hv.set(0, 0).tick().draw()

    def test_override(self):
        sfc = Surface(100, 100, 100, 100)
        SYSTEM["images"]["hoverable"].get_image()
        hv = Hoverable(0, 0, "truc", "shit", surface=sfc)
        self.assertEqual(hv.height, 100)
        self.assertEqual(hv.width, 100)

class TestingParallaxes(unittest.TestCase):
    def test_parallaxe(self):
        para = Parallaxe("cybercity.png", 576, 324, speeds = [0.2, 0.5, 1, 1.2, 2])
        para.invert()
        para = Parallaxe("cybercity.png", 576, 324)

class TestingTextGenerator(unittest.TestCase):
    def test_generator(self):
        tg = TextGenerator()
        tg.generate_damage_text(0,0,(255,255,255), False, 5)
        tg.generate_damage_text(0,0, None, True, 5)
        tg.generate_level_up()
        self.assertIsInstance(TEXT_TRACKER[0][0], Text)