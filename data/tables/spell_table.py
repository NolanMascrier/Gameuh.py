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

KAMIKAZE = Damage(3, fire=30, flags=[Flags.MELEE])

DARKBOLT = Damage(1, dark=1, flags=[Flags.SPELL])
LIGHTSHARD = Damage(1, light=5, flags=[Flags.SPELL])
MAGICMISSILE = Damage(1.25, light=4, flags=[Flags.SPELL], ignore_dodge=True, crit_rate=0,\
                      crit_mult=0)
VOIDBOLT = Damage(0.1, dark=1, flags=[Flags.SPELL])
VOIDBOLT_ALT = Damage(2, dark=5, flags=[Flags.SPELL])
ARC = Damage(0.8, elec=5, flags=[Flags.SPELL], lower_bound=0.1, upper_bound=2)
ICEBOLT = Damage(5, 2, ice=1, flags=[Flags.SPELL])
VOIDSPEAR = Damage(10, dark=15, flags=[Flags.SPELL])
LIGHTSPEAR = Damage(10, light=25, flags=[Flags.SPELL])
CHARGE = Damage(1.5, phys=6, fire=4, flags=[Flags.MELEE])
EXULT = Damage(2, phys=7, flags=[Flags.MELEE])
FURYSLASH = Damage(0.8, phys=5, flags=[Flags.MELEE])

MASTER_1 = Damage(1.2, phys=6, flags=[Flags.MELEE])
MASTER_2 = Damage(1.2, phys=8, flags=[Flags.MELEE])
MASTER_3 = Damage(1.2, phys=12, flags=[Flags.MELEE], is_crit=True)

BLEED_DMG = Damage(1, pp=0.5, phys=5, ignore_block=True, ignore_dodge=True)
BLEED = Affliction("bleed", 0, 3, [Flags.LIFE, Flags.FLAT], True, False, BLEED_DMG)

BURN_DMG = Damage(2, fire=4, ignore_block=True, ignore_dodge=True)
BURN = Affliction("burn", 0, 5, [Flags.LIFE, Flags.FLAT], True, False, BURN_DMG)

ELEFURY = Affliction("elemental_fury", 0.35, 5, flags=[Flags.BLESS, Flags.FIRE_DMG,\
                                        Flags.ICE_DMG, Flags.ELEC_DMG], stackable=False)
CELERITY = Affliction("celerity", 3, 0.5, flags=[Flags.BLESS, Flags.SPEED])
FURY = Affliction("fury", 0.15, 1, flags=[Flags.DAMAGE_MOD, Flags.BLESS],\
                stackable=True, refreshable=True)
FURY_SPEED = Affliction("fury2", 0.05, 1, flags=[Flags.ANIMATION_SPEED, Flags.BLESS],
                        stackable=True, refreshable=True)
FURY_COST = Affliction("fury3", 0.025, 1, flags=[Flags.MANA_COST, Flags.COOLDOWN, Flags.HEX],
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
    magicmissile_icon = Image("icons/magicmissile.png").scale(64, 64)

    SYSTEM["images"]["firebolt_proj_img"] =\
        Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    SYSTEM["images"]["arc_proj_img"] =\
        Animation("arc.png", 64, 64, frame_rate=0.25)
    SYSTEM["images"]["icebolt_proj_img"] =\
        Animation("icespear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    SYSTEM["images"]["voidspear_proj_img"] =\
        Animation("anims/voidspear.png", 24, 9, frame_rate=0.05, loops=False).scale(54, 144)
    SYSTEM["images"]["lightspear_proj_img"] =\
        Animation("anims/lightspear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    SYSTEM["images"]["voidbolt_proj_img"] =\
        Animation("pew.png", 13, 13, frame_rate=0.25)
    SYSTEM["images"]["voidbolt_proj2_img"] =\
        Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["fireball_proj_img"] =\
        Animation("fireball.png", 32, 19, frame_rate=0.25).scale(76, 128)
    SYSTEM["images"]["fireball_expl_img"] =\
        Animation("anims/fireball_explosion.png", 64, 64, frame_rate=0.25,\
        plays_once=True, loops=False).scale(256, 256)
    SYSTEM["images"]["darkbolt_img"] =\
        Animation("pew.png", 13, 13, frame_rate=0.25).scale(32, 32)
    SYSTEM["images"]["furyslash_img"] =\
        Animation("anims/furyslash.png", 64, 60, frame_rate=0.35, loops=False, plays_once=True)
    SYSTEM["images"]["exult_img"] =\
        Animation("exult.png", 64, 64, frame_rate=0.25, loops=False, plays_once=True)\
        .scale(256, 256)
    SYSTEM["images"]["furyslash_alt"] =\
        Animation("slash.png", 29, 20, frame_rate=0.25, loops=False, plays_once=True)\
        .scale(87, 60).flip(False, True)
    SYSTEM["images"]["master1_img"] =\
        Animation("anims/master1.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True)
    SYSTEM["images"]["master2_img"] =\
        Animation("anims/master2.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True)
    SYSTEM["images"]["master3_img"] =\
        Animation("anims/master3.png", 64, 64, frame_rate=0.5, loops=False, plays_once=True)\
        .scale(128, 128)
    SYSTEM["images"]["kamikaze_img"] =\
        Animation("anims/kamikaze.png", 64, 64, frame_rate=0.2, loops=False, plays_once=True,
                lines=4).scale(256, 256)
    SYSTEM["images"]["lightshards"] = Animation("anims/lightshard.png", 16, 10, frame_rate=0.1)\
        .scale(20, 32)
    SYSTEM["images"]["magicmissile"] = Animation("anims/magicmissile.png", 16, 9, frame_rate=0.1)\
        .scale(18, 32)
    SYSTEM["images"]["eldritchlaser"] = Animation("anims/lazor.png", 116, 10, frame_rate=0.15,\
        loops=8, plays_once=True, lines=4).scale(720, 1980)

    light_strike = Animation("anims/lightningfall.png", 64, 64, frame_rate=0.25,\
        plays_once=True, loops=False).scale(128, 128)
    missile_impact = Animation("anims/magicmissile_explosion.png", 64, 72, frame_rate=0.25,\
        plays_once=True, loops=False)
    firebolt_impact = Animation("anims/firebolt_impact.png", 64, 64, frame_rate=0.25,\
        plays_once=True, loops=False)

    fireball_explosion =\
        Slash(DummyEntity(0,0, None), None, "fireball_expl_img",\
              FIREBALL_EXPLOSION, effective_frames=3)

    master_1 = Spell("", m1_icon, "master1_img", MASTER_1, 5, 0,\
        cooldown=0.5, flags=[Flags.MELEE], offset_x=60, effective_frames=8)
    master_2 = Spell("", m2_icon, "master2_img", MASTER_2, 0, 0,\
        cooldown=0.5, flags=[Flags.MELEE], offset_x=60, effective_frames=8)
    master_3 = Spell("", m3_icon, "master3_img", MASTER_3, 0, 0,\
        cooldown=0.5, flags=[Flags.MELEE], offset_x=60, effective_frames=5)
    masterstrike = Spell("masterstrike", m1_icon, "master1_img", MASTER_3, 5, 0,\
        cooldown=3, flags=[Flags.MELEE,Flags.COMBO_SPELL], sequence=[master_1, master_2, master_3])

    firebolt = Spell("firebolt", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3,\
        cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE],\
        anim_on_hit=firebolt_impact)
    firebolt2 = Spell("firebolt2", firebolt_icon, "firebolt_proj_img", FIREBOLT, 3,\
        cooldown=0.4, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE, Flags.AIMED_AT_MOUSE])
    fireball = Spell("fireball", fireball_icon, "fireball_proj_img", FIREBALL, 0,\
        cooldown=3, flags=[Flags.EXPLODES, Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE,\
        Flags.AIMED_AT_MOUSE], explosion=fireball_explosion, proj_speed=12, effective_frames=3)
    icebolt = Spell("icebolt", icebolt_icon, "icebolt_proj_img", ICEBOLT, 10,\
        cooldown=10, projectiles=3, delay=0.8, flags=[Flags.PHYS, Flags.BARRAGE, Flags.PROJECTILE,\
        Flags.DELAYED, Flags.PIERCING])
    voidspear = Spell("voidspear", icebolt_icon, "voidspear_proj_img", VOIDSPEAR, 0,\
        cooldown=0, projectiles=3, delay=2, flags=[Flags.PHYS, Flags.BARRAGE, Flags.PROJECTILE,\
        Flags.DELAYED, Flags.PIERCING, Flags.UNNATACH, Flags.WARN], offset_y=50)
    lightspear = Spell("lighstpear", icebolt_icon, "lightspear_proj_img", LIGHTSPEAR, 0,\
        cooldown=0, projectiles=5, delay=1.2, flags=[Flags.PHYS, Flags.BARRAGE, Flags.PROJECTILE,\
        Flags.DELAYED, Flags.PIERCING, Flags.UNNATACH, Flags.WARN, Flags.AIMED_AT_PLAYER,\
        Flags.RANDOM_POSITION, Flags.AIMED_AT_PLAYER], proj_speed=65)
    exult = Spell("exult", exult_icon, "exult_img", EXULT, 0,\
        cooldown=0.25, projectiles=3, flags=[Flags.PHYS, Flags.SPREAD, Flags.MELEE, Flags.TRIGGER,\
        Flags.TRIGGER_ON_CRIT, Flags.DEBUFF], debuffs=[BLEED], effective_frames=4)
    voidolt = Spell("voidbolt", voidbolt_icon, "voidbolt_proj_img", VOIDBOLT, 1,\
        cooldown=0.1, projectiles=5, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE])
    voidoltflurry = Spell("voidbolt_boss", voidbolt_icon, "voidbolt_proj2_img", VOIDBOLT_ALT, 0,\
        cooldown=0.1, projectiles=9, flags=[Flags.DARK, Flags.SPREAD, Flags.PROJECTILE])
    arc = Spell("arc", arc_icon, "arc_proj_img", ARC, 3,\
        cooldown=0.35, projectiles=1, chains=3, flags=[Flags.DARK, Flags.SPREAD,\
        Flags.PROJECTILE, Flags.AIMED_AT_CLOSEST, Flags.CHAINS], anim_on_hit=light_strike)
    lightshard = Spell("lightshard", arc_icon, "lightshards", LIGHTSHARD, 3,\
        cooldown=0.01, projectiles=64, flags=[Flags.LIGHT, Flags.CIRCULAR_BLAST,\
        Flags.PROJECTILE])
    magicmissile = Spell("magicmissile", magicmissile_icon, "magicmissile", MAGICMISSILE, 20,\
        cooldown=4, projectiles=4, delay=0.2, flags=[Flags.LIGHT, Flags.WANDER,\
        Flags.PROJECTILE, Flags.HARD_TRACKING, Flags.AIMED_AT_CLOSEST, Flags.FLURRY_RELEASE,
        Flags.IMPACT_ANIMATION_RANDOM], anim_on_hit=missile_impact)
    elementalfury = Spell("elefury", elefury_icon, None, None, 20,\
        cooldown=60, flags=[Flags.BUFF], buffs=[ELEFURY])
    dash_basic = Spell("wdash", heal_icon, None, None, 5, distance=6,\
        cooldown=3, flags=[Flags.BUFF, Flags.DASH], buffs=[CELERITY])
    furyslash = Spell("fslash", fury_icon, "furyslash_img", FURYSLASH, 5, 0,\
        cooldown=0.5, flags=[Flags.MELEE, Flags.CUTS_PROJECTILE, Flags.BUFF],
        buffs=[FURY], offset_x=60, alterations=[FURY, FURY_COST, FURY_SPEED])
    charge = Spell("Charge", fury_icon, "furyslash_alt", CHARGE,
        flags=[Flags.MELEE], offset_x=120)
    voidbolt_enemy = Spell("VoidboltE", None, "darkbolt_img", DARKBOLT, projectiles=1,
        flags=[Flags.PROJECTILE, Flags.SPREAD, Flags.DARK, Flags.AIMED_AT_PLAYER])
    kamikaze = Spell("boom", exult_icon, "kamikaze_img", KAMIKAZE, 0,\
        cooldown=0, flags=[Flags.FIRE, Flags.MELEE, Flags.DEBUFF, Flags.CUTS_PROJECTILE],\
        debuffs=[BURN], effective_frames=4)
    lazoor = Spell("fslash", fury_icon, "eldritchlaser", FURYSLASH, 5, 0,\
        cooldown=0.5, flags=[Flags.MELEE, Flags.CUTS_PROJECTILE, Flags.CAN_TICK], offset_x=-1064)
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
    SYSTEM["spells"]["magicmissile"] = magicmissile
    #Enemy spells
    SYSTEM["spells"]["e_charge"] = charge
    SYSTEM["spells"]["e_voidbolt"] = voidbolt_enemy
    SYSTEM["spells"]["e_kamikaze"] = kamikaze
    SYSTEM["spells"]["e_voidflurry"] = voidoltflurry
    SYSTEM["spells"]["e_voidspear"] = voidspear
    SYSTEM["spells"]["e_lightshard"] = lightshard
    SYSTEM["spells"]["e_lightspear"] = lightspear
    SYSTEM["spells"]["e_lazer"] = lazoor
    SYSTEM["spells"][None] = None
