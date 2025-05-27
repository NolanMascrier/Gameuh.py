"""List of damage sources."""

from data.damage import Damage
from data.projectile import Projectile
from data.creature import Creature
from data.physics.entity import Entity
from data.constants import Flags, PROJECTILE_TRACKER, SYSTEM
from data.image.animation import Animation
from data.numerics.affliction import Affliction

FIREBOLT = Damage(2, 1.5, fire=1, flags=[Flags.SPELL])
DARKBOLT = Damage(1, 0.9, dark=1, flags=[Flags.SPELL])
ICEBOLT = Damage(5, 2, ice=1, flags=[Flags.SPELL])
CHARGE = Damage(3, 1, phys=1, flags=[Flags.MELEE])

ELEFURY = Affliction("elemetal_fury", 1.25, 5, flags=[Flags.BLESS, Flags.FIRE_DMG,\
                                        Flags.ICE_DMG, Flags.ELEC_DMG], stackable=False)

class Spell():
    def __init__(self, name, icon, proj_image, base_damage:Damage, mana_cost = 0, life_cost = 0,\
                 bounces = 0, delay = 0,\
                 cooldown = 0, projectiles = 1, flags = None, afflictions = None):
        self._name = name
        self._icon = icon
        self._proj_image = proj_image
        self._base_damage = base_damage
        self._mana_cost = mana_cost
        self._life_cost = life_cost
        self._cooldown = 0
        self._max_cooldown = cooldown
        self._projectiles = projectiles
        self._bounces = bounces
        self._delay = delay
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        if afflictions is None or not isinstance(afflictions, list):
            self._afflictions = []
        else:
            self._afflictions = afflictions

    def tick(self):
        self._cooldown -= 0.016
        if self._cooldown <= 0:
            self._cooldown = 0

    def cast(self, caster: Creature, entity: Entity, evil: bool):
        """Shoots the spell."""
        if self._cooldown > 0:
            return
        if caster.stats["mana"].current_value < self._mana_cost:
            return
        if caster.stats["life"].current_value < self._life_cost:
            return
        self._cooldown = self._max_cooldown
        caster.consume_mana(self._mana_cost)
        caster.stats["life"].current_value -= self._life_cost
        if Flags.PROJECTILE in self._flags:
            if Flags.BARRAGE in self._flags:
                for i in range (0, self._projectiles):
                    proj = Projectile(entity.center[0], entity.center[1] + i * 20, 0 ,\
                                      self._proj_image.clone(),\
                                      self._base_damage, caster, evil,\
                                      delay=self._delay * (i + 1), bounces=self._bounces, \
                                      behaviours=self._flags, caster=entity)
                    PROJECTILE_TRACKER.append(proj)
            elif Flags.SPREAD in self._flags:
                if self._projectiles == 1:
                    proj = Projectile(entity.center[0], entity.center[1], 0,\
                                      self._proj_image.clone(), self._base_damage, caster, evil,\
                                      delay=self._delay, bounces=self._bounces, \
                                      behaviours=self._flags, caster=entity)
                    PROJECTILE_TRACKER.append(proj)
                else:
                    spread = 90 / self._projectiles
                    for i in range(0, self._projectiles):
                        proj = Projectile(entity.center[0], entity.center[1], -45 + spread * i,\
                                        self._proj_image.clone(), self._base_damage, caster, evil,\
                                        delay=self._delay, bounces=self._bounces, \
                                        behaviours=self._flags, caster=entity)
                        PROJECTILE_TRACKER.append(proj)
        if Flags.BUFF in self._flags:
            for afflic in self._afflictions:
                if not isinstance(afflic, Affliction):
                    continue
                caster.afflict(afflic)

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def mana_cost(self):
        return self._mana_cost

    @mana_cost.setter
    def mana_cost(self, value):
        self._mana_cost = value

    @property
    def life_cost(self):
        return self._life_cost

    @life_cost.setter
    def life_cost(self, value):
        self._life_cost = value

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    @property
    def max_cooldown(self):
        return self._max_cooldown

    @max_cooldown.setter
    def max_cooldown(self, value):
        self._max_cooldown = value

def generate_spell_list():
    """Generates the spells and add them to stuff"""
    firebolt_icon = Animation("icons/firebolt.png", 64, 64, loops=False)
    icebolt_icon = Animation("icons/icebolt.png", 64, 64, loops=False)
    voidbolt_icon = Animation("icons/darkbolt.png", 64, 64, loops=False)
    elefury_icon = Animation("icons/elementalfury.png", 64, 64, loops=False)
    heal_icon = Animation("icons/heal.png", 64, 64, loops=False)
    firebolt_proj_img = Animation("fireball.png", 32, 19, frame_rate=0.25).scale(38, 64)
    icebolt_proj_img = Animation("icespear.png", 24, 9, frame_rate=0.05, loops=False).scale(18, 48)
    voidbolt_proj_img = Animation("pew.png", 13, 13, frame_rate=0.25)
    firebolt = Spell("Firebolt", firebolt_icon, firebolt_proj_img, FIREBOLT, 2, cooldown=0.5, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE])
    icebolt = Spell("Ice lance", icebolt_icon, icebolt_proj_img, ICEBOLT, 50, cooldown=10, projectiles=3, delay=0.5, flags=[Flags.ICE, Flags.BARRAGE, Flags.PROJECTILE, Flags.DELAYED, Flags.PIERCING])
    voidolt = Spell("Voidbolt", voidbolt_icon, voidbolt_proj_img, DARKBOLT, 1, cooldown=0.1, projectiles = 3, flags=[Flags.FIRE, Flags.SPREAD, Flags.PROJECTILE])
    elementalfury = Spell("Elemental Fury", elefury_icon, None, None, 20, 0, cooldown=60, flags=[Flags.BUFF], afflictions=[ELEFURY])
    SYSTEM["spells"]["firebolt"] = firebolt
    SYSTEM["spells"]["icebolt"] = icebolt
    SYSTEM["spells"]["voidbolt"] = voidolt
    SYSTEM["spells"]["elefury"] = elementalfury
