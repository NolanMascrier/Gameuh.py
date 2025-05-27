"""A class that allows creation and display of text on the screen."""

from data.constants import TEXT_TRACKER, SYSTEM
from data.damage import Damage

class TextGenerator():
    def __init__(self):
        pass

    def generate_damage_text(self, x, y, color, crit, dmg):
        """Shows a damage pop up."""
        if crit:
            text = SYSTEM["font_crit"].render(f'{dmg} !', False, color)
        else:
            text = SYSTEM["font"].render(f'{dmg}', False, color)
        TEXT_TRACKER.append([text, x, y, 255])
