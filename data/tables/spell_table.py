"""List of damage sources."""

from data.slash import Slash
from data.projectile import DummyEntity
from data.numerics.damage import Damage
from data.constants import Flags, SYSTEM
from data.image.animation import Animation, Image
from data.numerics.affliction import Affliction
from data.game.spell import Spell

FIREBOLT = Damage(1.5, fire=2, flags=[Flags.SPELL])
FIREBALL = Damage(2, fire=5, flags=[Flags.SPELL])
FIREBALL_EXPLOSION = Damage(2, fire=7, flags=[Flags.SPELL])

DARKBOLT = Damage(1, dark=1, flags=[Flags.SPELL])
VOIDBOLT = Damage(0.1, dark=1, flags=[Flags.SPELL])
ARC = Damage(0.8, elec=5, flags=[Flags.SPELL], lower_bound=0.1, upper_bound=2)
ICEBOLT = Damage(5, 2, ice=1, flags=[Flags.SPELL])
CHARGE = Damage(1.5, phys=10, flags=[Flags.MELEE])
EXULT = Damage(2, phys=7, flags=[Flags.MELEE])
FURYSLASH = Damage(0.8, phys=5, flags=[Flags.MELEE])

MASTER_1 = Damage(1.2, phys=6, flags=[Flags.MELEE])
MASTER_2 = Damage(1.2, phys=8, flags=[Flags.MELEE])
MASTER_3 = Damage(1.2, phys=12, flags=[Flags.MELEE], is_crit=True)

BLEED_DMG = Damage(1, pp=0.5, phys=5, ignore_block=True, ignore_dodge=True)
BLEED = Affliction("bleed", 0, 3, [Flags.LIFE, Flags.FLAT], True, False, BLEED_DMG)

ELEFURY = Affliction("elemental_fury", 0.35, 5, flags=[Flags.BLESS, Flags.FIRE_DMG,\
                                        Flags.ICE_DMG, Flags.ELEC_DMG], stackable=False)
CELERITY = Affliction("celerity", 3, 0.5, flags=[Flags.BLESS, Flags.SPEED])
FURY = Affliction("fury", 0.15, 1, flags=[Flags.BLESS, Flags.MELEE],\
                stackable=True, refreshable=True)

def generate_spell_list():
    """Generates the spells and add them to stuff"""
    firebolt_icon = Image("icons/firebolt.png").scale(64, 64)
    fireball_icon = Image("icons/fireball.png").scale(64, 64)
    icebolt_icon = Image("icons/icebolt.png").scale(64, 64)
    voidbolt_icon = Image("icons/darkbolt.png").scale(64, 64)
    elefury_icon = Image("icons/elementalfury.png").scale(64, 64)
    heal_icon = Image("icons/heal.png").scale(64, 64)
    fury_icon = Image("icons/furyslash.png").scale(64, 64)
    arc_icon = Image("icons/arc.png").scale(64, 64)
    exult_icon = Image("icons/exult.png").scale(64, 64)
    m1_icon = Image("icons/masterstrike_a.png").scale(64, 64)
    m2_icon = Image("icons/masterstrike_b.png").scale(64, 64)
    m3_icon = Image("icons/masterstrike_c.png").scale(64, 64)

    SYSTEM["images"]["firebolt_proj_img"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["arc_proj_img"] = Animation("arc.png", 64, 64, frame_rate=0.25)
    SYSTEM["images"]["icebolt_proj_img"] = Animation("icespear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    SYSTEM["images"]["voidbolt_proj_img"] = Animation("pew.png", 13, 13, frame_rate=0.25)
    SYSTEM["images"]["fireball_proj_img"] = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(76, 128)
    SYSTEM["images"]["fireball_expl_img"] = Animation("anims/fireball_explosion.png", 64, 64, frame_rate=0.25, plays_once=True, loops=False).scale(256, 256)
    SYSTEM["images"]["darkbolt_img"] = Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["furyslash_img"] = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(58, 40)
    SYSTEM["images"]["exult_img"] = Animation("exult.png", 64, 64, frame_rate=0.25, loops=False, plays_once=True).scale(256, 256)
    SYSTEM["images"]["furyslash_alt"] = Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True).scale(87, 60).flip(False, True)
    SYSTEM["images"]["master1_img"] = Animation("anims/master1.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True)
    SYSTEM["images"]["master2_img"] = Animation("anims/master2.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True)
    SYSTEM["images"]["master3_img"] = Animation("anims/master3.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True).scale(128, 128)

    fireball_explosion = Slash(DummyEntity(0,0, None), None, "fireball_expl_img", FIREBALL_EXPLOSION)

    master_1 = Spell("", m1_icon, "master1_img", MASTER_1, 5, 0, cooldown=0.5, flags=[Flags.MELEE], offset_x=60)
    master_2 = Spell("", m2_icon, "master2_img", MASTER_2, 0, 0, cooldown=0.5, flags=[Flags.MELEE], offset_x=60)
    master_3 = Spell("", m3_icon, "master3_img", MASTER_3, 0, 0, cooldown=0.5, flags=[Flags.MELEE], offset_x=60)
    masterstrike = Spell("masterstrike", m1_icon, "master1_img", MASTER_3, 5, 0, cooldown=3, flags=[Flags.MELEE,Flags.COMBO_SPELL], sequence=[master_1, master_2, master_3])

    firebolt = Spell("firebolt", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3, cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    firebolt2 = Spell("firebolt2", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3, cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    fireball = Spell("fireball", fireball_icon, "fireball_proj_img", FIREBALL, 0, cooldown=3, flags=[Flags.EXPLODES, Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE], explosion=fireball_explosion, proj_speed=12)
    icebolt = Spell("icebolt", icebolt_icon, "icebolt_proj_img", ICEBOLT, 40, cooldown=10, projectiles=3, delay=0.8, flags=[Flags.PHYS, Flags.BARRAGE, Flags.PROJECTILE, Flags.DELAYED, Flags.PIERCING])
    exult = Spell("exult", exult_icon, "exult_img", EXULT, 0, cooldown=0.25, projectiles=3, flags=[Flags.PHYS, Flags.SPREAD, Flags.MELEE, Flags.TRIGGER, Flags.TRIGGER_ON_CRIT, Flags.DEBUFF], debuffs=[BLEED])
    voidolt = Spell("voidbolt", voidbolt_icon, "voidbolt_proj_img", VOIDBOLT, 1, cooldown=0.1, projectiles=5, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE])
    arc = Spell("arc", arc_icon, "arc_proj_img", ARC, 3, cooldown=0.35, projectiles=1, chains=3, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_CLOSEST, Flags.CHAINS])
    elementalfury = Spell("elefury", elefury_icon, None, None, 20, cooldown=60, flags=[Flags.BUFF], buffs=[ELEFURY])
    dash_basic = Spell("wdash", heal_icon, None, None, 5, distance=6, cooldown=3, flags=[Flags.BUFF, Flags.DASH], buffs=[CELERITY])
    furyslash = Spell("fslash", fury_icon, "furyslash_img", FURYSLASH, 5, 0, cooldown=0.5, flags=[Flags.MELEE, Flags.CUTS_PROJECTILE, Flags.BUFF], buffs=[FURY], offset_x=60)
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
    SYSTEM["spells"]["masterstrike"] = masterstrike
    SYSTEM["spells"]["fireball"] = fireball
    #Enemy spells
    SYSTEM["spells"]["e_charge"] = charge
    SYSTEM["spells"]["e_voidbolt"] = voidbolt_enemy
