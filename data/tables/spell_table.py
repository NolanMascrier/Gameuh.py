"""List of damage sources."""

from data.numerics.damage import Damage
from data.constants import Flags, SYSTEM
from data.image.animation import Animation, Image
from data.numerics.affliction import Affliction
from data.game.spell import Spell

FIREBOLT = Damage(1.5, fire=2, flags=[Flags.SPELL])
DARKBOLT = Damage(1, dark=1, flags=[Flags.SPELL])
VOIDBOLT = Damage(0.1, dark=1, flags=[Flags.SPELL])
ARC = Damage(0.8, elec=2, flags=[Flags.SPELL])
ICEBOLT = Damage(5, 2, ice=1, flags=[Flags.SPELL])
CHARGE = Damage(1.5, phys=10, flags=[Flags.MELEE])
EXULT = Damage(2, phys=7, flags=[Flags.MELEE])
FURYSLASH = Damage(0.8, phys=5, flags=[Flags.MELEE])

BLEED_DMG = Damage(1, pp=0.5, phys=5, ignore_block=True, ignore_dodge=True)
BLEED = Affliction("bleed", 0, 3, [Flags.LIFE, Flags.FLAT], True, False, BLEED_DMG)

ELEFURY = Affliction("elemetal_fury", 0.35, 5, flags=[Flags.BLESS, Flags.FIRE_DMG,\
                                        Flags.ICE_DMG, Flags.ELEC_DMG], stackable=False)
CELERITY = Affliction("celerity", 3, 0.5, flags=[Flags.BLESS, Flags.SPEED])
FURY = Affliction("fury", 0.15, 1, flags=[Flags.BLESS, Flags.MELEE],\
                stackable=True, refreshable=True)

def generate_spell_list():
    """Generates the spells and add them to stuff"""
    firebolt_icon = Image("icons/firebolt.png").scale(64, 64)
    icebolt_icon = Image("icons/icebolt.png").scale(64, 64)
    voidbolt_icon = Image("icons/darkbolt.png").scale(64, 64)
    elefury_icon = Image("icons/elementalfury.png").scale(64, 64)
    heal_icon = Image("icons/heal.png").scale(64, 64)
    fury_icon = Image("icons/furyslash.png").scale(64, 64)
    arc_icon = Image("icons/arc.png").scale(64, 64)
    exult_icon = Image("icons/exult.png").scale(64, 64)
    SYSTEM["images"]["firebolt_proj_img"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["arc_proj_img"] = Animation("arc.png", 64, 64, frame_rate=0.25)
    SYSTEM["images"]["icebolt_proj_img"] = Animation("icespear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    SYSTEM["images"]["voidbolt_proj_img"] = Animation("pew.png", 13, 13, frame_rate=0.25)
    SYSTEM["images"]["darkbolt_img"] = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["furyslash_img"] = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(58, 40)
    SYSTEM["images"]["exult_img"] = Animation("exult.png", 64, 64, frame_rate=0.25, loops=False, plays_once=True).scale(256, 256)
    SYSTEM["images"]["furyslash_alt"] = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(87, 60).flip(False, True)
    firebolt = Spell("firebolt", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3, cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    firebolt2 = Spell("firebolt2", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3, cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    icebolt = Spell("icebolt", icebolt_icon, "icebolt_proj_img", ICEBOLT, 40, cooldown=10, projectiles=3, delay=0.8, flags=[Flags.PHYS, Flags.BARRAGE, Flags.PROJECTILE, Flags.DELAYED, Flags.PIERCING])
    exult = Spell("exult", exult_icon, "exult_img", EXULT, 0, cooldown=0.25, projectiles=3, flags=[Flags.PHYS, Flags.SPREAD, Flags.MELEE, Flags.TRIGGER, Flags.TRIGGER_ON_CRIT, Flags.DEBUFF], debuffs=[BLEED])
    voidolt = Spell("voidbolt", voidbolt_icon, "voidbolt_proj_img", VOIDBOLT, 1, cooldown=0.1, projectiles=5, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE])
    arc = Spell("arc", arc_icon, "arc_proj_img", ARC, 3, cooldown=0.35, projectiles=1, chains=3, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_CLOSEST, Flags.CHAINS])
    elementalfury = Spell("elefury", elefury_icon, None, None, 20, cooldown=60, flags=[Flags.BUFF], afflictions=[ELEFURY])
    dash_basic = Spell("wdash", heal_icon, None, None, 5, distance=6, cooldown=3, flags=[Flags.BUFF, Flags.DASH], afflictions=[CELERITY])
    furyslash = Spell("fslash", fury_icon, "furyslash_img", FURYSLASH, 5, 0, cooldown=0.5, flags=[Flags.MELEE, Flags.CUTS_PROJECTILE, Flags.BUFF], afflictions=[FURY], offset_x=60)
    charge = Spell("Charge", fury_icon, "furyslash_alt", CHARGE, flags=[Flags.MELEE], offset_x=60)
    voidbolt_enemy = Spell("VoidboltE", None, "darkbolt_img", DARKBOLT, projectiles=1, flags=[Flags.PROJECTILE, Flags.SPREAD, Flags.DARK, Flags.AIMED_AT_PLAYER])
    SYSTEM["spells"]["firebolt"] = firebolt
    SYSTEM["spells"]["firebolt2"] = firebolt2
    SYSTEM["spells"]["icebolt"] = icebolt
    SYSTEM["spells"]["exult"] = exult
    SYSTEM["spells"]["voidbolt"] = voidolt
    SYSTEM["spells"]["arc"] = arc
    SYSTEM["spells"]["elefury"] = elementalfury
    SYSTEM["spells"]["winddash"] = dash_basic
    SYSTEM["spells"]["furyslash"] = furyslash
    #Enemy spells
    SYSTEM["spells"]["e_charge"] = charge
    SYSTEM["spells"]["e_voidbolt"] = voidbolt_enemy
