"""Constant list for input keys"""

import pygame.constants as cs
from data.api.surface import get_keys
from data.constants import SYSTEM

K_A       = cs.K_a
K_B       = cs.K_b
K_C       = cs.K_c
K_D       = cs.K_d
K_E       = cs.K_e
K_F       = cs.K_f
K_G       = cs.K_g
K_H       = cs.K_h
K_I       = cs.K_i
K_J       = cs.K_j
K_K       = cs.K_k
K_L       = cs.K_l
K_M       = cs.K_m
K_N       = cs.K_n
K_O       = cs.K_o
K_P       = cs.K_p
K_Q       = cs.K_q
K_R       = cs.K_r
K_S       = cs.K_s
K_T       = cs.K_t
K_U       = cs.K_u
K_V       = cs.K_v
K_W       = cs.K_w
K_X       = cs.K_x
K_Y       = cs.K_y
K_Z       = cs.K_z
K_0       = cs.K_0
K_1       = cs.K_1
K_2       = cs.K_2
K_3       = cs.K_3
K_4       = cs.K_4
K_5       = cs.K_5
K_6       = cs.K_6
K_7       = cs.K_7
K_8       = cs.K_8
K_9       = cs.K_9
K_KP0     = cs.K_KP0
K_KP1     = cs.K_KP1
K_KP2     = cs.K_KP2
K_KP3     = cs.K_KP3
K_KP4     = cs.K_KP4
K_KP5     = cs.K_KP5
K_KP6     = cs.K_KP6
K_KP7     = cs.K_KP7
K_KP8     = cs.K_KP8
K_KP9     = cs.K_KP9
K_KF1     = cs.K_F1
K_KF2     = cs.K_F2
K_KF3     = cs.K_F3
K_KF4     = cs.K_F4
K_KF5     = cs.K_F5
K_KF6     = cs.K_F6
K_KF7     = cs.K_F7
K_KF8     = cs.K_F8
K_KF9     = cs.K_F9
K_KF10    = cs.K_F10
K_KF11    = cs.K_F11
K_KF12    = cs.K_F12
K_UP      = cs.K_UP
K_DOWN    = cs.K_DOWN
K_LEFT    = cs.K_LEFT
K_RIGHT   = cs.K_RIGHT
K_ESCAPE  = cs.K_ESCAPE
K_LSHIFT  = cs.K_LSHIFT
K_RSHIFT  = cs.K_RSHIFT
K_LALT    = cs.K_LALT
K_RALT    = cs.K_RALT
QUIT       = cs.QUIT
MOUSEWHEEL = cs.MOUSEWHEEL
RMB        = 0
LMB        = 1
MMB        = 2

KEY_EVENT = {
    "spell_L": (LMB, None),
    "spell_R": (RMB, None),
    "spell_M": (MMB, None),
    "spell_1": (K_Q, None),
    "spell_2": (K_E, None),
    "spell_3": (K_F, None),
    "spell_4": (K_T, None),
    "spell_5": (K_R, None),
    "spell_6": (K_X, None),
    "spell_7": (K_G, None),
    "dash": (K_LSHIFT, None),
    "potion_life": (K_1, None),
    "potion_mana": (K_2, None),
    "up": (K_UP, K_Z),
    "down": (K_DOWN, K_S),
    "left": (K_LEFT, K_A),
    "right": (K_RIGHT, K_D),
    "pause": (K_ESCAPE, None),
    "alt_popup": (K_LALT, K_RALT),
    "shift": (K_LSHIFT, K_RSHIFT),
}

def get_key_event():
    """Returns the list of key events."""
    keys = get_keys()
    events = set()
    for k, binds in KEY_EVENT.items():
        if (binds[0] is not None and keys[binds[0]]) or\
            (binds[1] is not None and keys[binds[1]]):
            events.add(k)
        if LMB in (binds[0], binds[1]) and SYSTEM["mouse_click"][0]:
            events.add(k)
        if MMB in (binds[0], binds[1]) and SYSTEM["mouse_click"][1]:
            events.add(k)
        if RMB in (binds[0], binds[1]) and SYSTEM["mouse_click"][2]:
            events.add(k)
    return events
