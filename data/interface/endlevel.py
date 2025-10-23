"""Handles the defeat and the victory screen."""

from data.constants import SYSTEM, GAME_VICTORY, SCREEN_HEIGHT,\
    SCREEN_WIDTH, TICKER_TIMER, GAME_DEATH, trad, ENNEMY_TRACKER, ANIMATION_TRACKER,\
    PROJECTILE_TRACKER, BLACK_TRANSP
from data.image.showcase import ShowCase
from data.image.text import Text
from data.interface.render import render, renders
from data.interface.general import draw_game, logic_tick

def generate_victory():
    """Generates the victory screen."""
    x = SCREEN_WIDTH / 2 - SYSTEM["images"]["tile_panel_small"].width / 2
    y = SCREEN_HEIGHT / 2 - SYSTEM["images"]["tile_panel_small"].height / 2
    SYSTEM["ui"]["showcase"] = ShowCase(x, y, background=SYSTEM["images"]["tile_panel_small"],\
        default=SYSTEM["level"].loot)
    SYSTEM["ui"]["notice"] = Text(trad('descripts', 'victory'), font="item_titles", size=80,\
                                  default_color=BLACK_TRANSP)
    SYSTEM["ui"]["notice_state"] = (SCREEN_WIDTH / 2 - SYSTEM["ui"]["notice"].width / 2, 200, 100)
    SYSTEM["game_state"] = GAME_VICTORY

def generate_defeat():
    """Generates the game over screen."""
    x = SCREEN_WIDTH / 2 - SYSTEM["images"]["tile_panel_small"].width / 2
    y = SCREEN_HEIGHT / 2 - SYSTEM["images"]["tile_panel_small"].height / 2
    SYSTEM["ui"]["showcase"] = ShowCase(x, y, background=SYSTEM["images"]["tile_panel_small"],\
        default=SYSTEM["level"].loot)
    SYSTEM["ui"]["notice"] = Text(trad('descripts', 'defeat'), font="item_titles", size=80,\
                                  default_color=BLACK_TRANSP)
    SYSTEM["ui"]["notice_state"] = (SCREEN_WIDTH / 2 - SYSTEM["ui"]["notice"].width / 2, 200, 100)
    SYSTEM["game_state"] = GAME_DEATH

def draw_end(events):
    """Draws the victory screen."""
    for event in events:
        if event.type == TICKER_TIMER:
            logic_tick()
    SYSTEM["level"].background.draw(True)
    draw_game()
    renders([b.get_image(), b.get_pos()] for b in ENNEMY_TRACKER)
    renders([p[0].get_image(), (p[1], p[2])] for p in ANIMATION_TRACKER)
    renders([p.get_image(), p.get_pos()] for p in PROJECTILE_TRACKER)
    render(SYSTEM["ui"]["notice"].image, (SYSTEM["ui"]["notice_state"][0],
                                          SYSTEM["ui"]["notice_state"][1]))
    x_offset = SCREEN_WIDTH / 2 - SYSTEM["images"]["menu_bg"].width / 2
    y_offset = SCREEN_HEIGHT / 2 - SYSTEM["images"]["menu_bg"].height / 2
    render(SYSTEM["images"]["menu_bg"].image, (x_offset, y_offset))
    SYSTEM["buttons"]["button_continue"].set(x_offset + 200, y_offset + 450)
    SYSTEM["buttons"]["button_continue"].tick().draw(SYSTEM["windows"])
    SYSTEM["ui"]["showcase"].tick().draw()
