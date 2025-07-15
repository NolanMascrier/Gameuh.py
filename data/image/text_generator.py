"""A class that allows creation and display of text on the screen."""

from data.constants import TEXT_TRACKER, SYSTEM
from data.image.text import Text

class TextGenerator():
    def __init__(self):
        pass

    def generate_damage_text(self, x, y, color, crit, dmg):
        """Shows a damage pop up."""
        if not isinstance(color, tuple):
            color = (255, 255, 255)
        if crit:
            text = Text(f"#c#{color}{dmg} !", size=35, bold=True)
        else:
            text = Text(f"#c#{color}{dmg}", size=25)
        TEXT_TRACKER.append([text, x, y, 255])

    def generate_level_up(self):
        """Shows a damage pop up."""
        text = SYSTEM["font_crit"].render('Level up !', False, (252, 161, 3))
        TEXT_TRACKER.append([text, SYSTEM["player.x"], SYSTEM["player.y"], 255])
