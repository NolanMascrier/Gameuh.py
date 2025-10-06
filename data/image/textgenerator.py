"""A class that allows creation and display of text on the screen."""

from functools import lru_cache
from data.constants import TEXT_TRACKER, SYSTEM
from data.image.text import Text

LEVEL_COLOR = (252, 161, 3)
WHITE = (255,255,255)

@lru_cache(maxsize=64)
def make_text(text, color = WHITE, bold = False, size = 35):
    """Generates the text."""
    return Text(text, default_color=color, bold=bold, size=size, font="item_desc")

class TextGenerator():
    """Generator of text."""
    def generate_damage_text(self, x, y, color, crit, dmg):
        """Shows a damage pop up."""
        if not isinstance(color, tuple):
            color = (255, 255, 255)
        if crit:
            text = make_text(f"{dmg} !", color, True, 35)
        else:
            text = make_text(f"{dmg}", color, False, 25)
        TEXT_TRACKER.append([text, x, y, 255])

    def generate_level_up(self):
        """Shows a damage pop up."""
        text = make_text("Level Up !", LEVEL_COLOR, True, 35)
        TEXT_TRACKER.append([text, SYSTEM["player.x"], SYSTEM["player.y"], 255])

    def generate_fps(self):
        """Generates the FPS counter."""
        SYSTEM["fps_counter"] = make_text(f"{round(SYSTEM['clock'].get_fps())}", WHITE, True, 50)
