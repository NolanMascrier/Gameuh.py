"""List of damage sources."""

from data.numerics.damage import Damage
from data.constants import Flags, SYSTEM
from data.image.animation import Animation
from data.numerics.affliction import Affliction
from data.game.spell import Spell

FIREBOLT = Damage(1.5, fire=2, flags=[Flags.SPELL])
DARKBOLT = Damage(1, dark=1, flags=[Flags.SPELL])
VOIDBOLT = Damage(0.1, dark=1, flags=[Flags.SPELL])
ICEBOLT = Damage(5, 2, ice=1, flags=[Flags.SPELL])
CHARGE = Damage(1.5, phys=10, flags=[Flags.MELEE])
FURYSLASH = Damage(0.8, phys=5, flags=[Flags.MELEE])

ELEFURY = Affliction("elemetal_fury", 1.25, 5, flags=[Flags.BLESS, Flags.FIRE_DMG,\
                                        Flags.ICE_DMG, Flags.ELEC_DMG], stackable=False)
CELERITY = Affliction("celerity", 3, 0.5, flags=[Flags.BLESS, Flags.SPEED])
FURY = Affliction("FURY", 0.15, 1, flags=[Flags.BLESS, Flags.MELEE],\
                stackable=True, refreshable=True)

def generate_spell_list():
    """Generates the spells and add them to stuff"""
    firebolt_icon = Animation("icons/firebolt.png", 64, 64, loops=False)
    icebolt_icon = Animation("icons/icebolt.png", 64, 64, loops=False)
    voidbolt_icon = Animation("icons/darkbolt.png", 64, 64, loops=False)
    elefury_icon = Animation("icons/elementalfury.png", 64, 64, loops=False)
    heal_icon = Animation("icons/heal.png", 64, 64, loops=False)
    fury_icon = Animation("icons/furyslash.png", 64, 64, loops=False)
    firebolt_proj_img = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    icebolt_proj_img = Animation("icespear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    voidbolt_proj_img = Animation("pew.png", 13, 13, frame_rate=0.25)
    darkbolt_img = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    furyslash_img = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(58, 40)
    furyslash_alt = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(87, 60).flip(False, True)
    firebolt = Spell("firebolt", firebolt_icon, firebolt_proj_img, FIREBOLT, 3, cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    icebolt = Spell("icebolt", icebolt_icon, icebolt_proj_img, ICEBOLT, 40, cooldown=10, projectiles=3, delay=0.8, flags=[Flags.ICE, Flags.BARRAGE, Flags.PROJECTILE, Flags.DELAYED, Flags.PIERCING])
    voidolt = Spell("voidbolt", voidbolt_icon, voidbolt_proj_img, VOIDBOLT, 1, cooldown=0.1, projectiles=5, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE])
    elementalfury = Spell("elefury", elefury_icon, None, None, 20, cooldown=60, flags=[Flags.BUFF], afflictions=[ELEFURY])
    dash_basic = Spell("wdash", heal_icon, None, None, 5, distance=200, cooldown=3, flags=[Flags.BUFF, Flags.DASH], afflictions=[CELERITY])
    furyslash = Spell("fslash", fury_icon, furyslash_img, FURYSLASH, 5, 0, cooldown=0.5, flags=[Flags.MELEE, Flags.CUTS_PROJECTILE, Flags.BUFF], afflictions=[FURY])
    charge = Spell("Charge", fury_icon, furyslash_alt, CHARGE, flags=[Flags.MELEE])
    voidbolt_enemy = Spell("VoidboltE", None, darkbolt_img, DARKBOLT, projectiles=1, flags=[Flags.PROJECTILE, Flags.SPREAD, Flags.DARK, Flags.AIMED_AT_PLAYER])
    SYSTEM["spells"]["firebolt"] = firebolt
    SYSTEM["spells"]["icebolt"] = icebolt
    SYSTEM["spells"]["voidbolt"] = voidolt
    SYSTEM["spells"]["elefury"] = elementalfury
    SYSTEM["spells"]["winddash"] = dash_basic
    SYSTEM["spells"]["furyslash"] = furyslash
    #Enemy spells
    SYSTEM["spells"]["e_charge"] = charge
    SYSTEM["spells"]["e_voidbolt"] = voidbolt_enemy
