"""For spells"""

import pygame
from data.projectile import Projectile
from data.creature import Creature
from data.physics.entity import Entity
from data.numerics.stat import Stat
from data.slash import Slash
from data.numerics.damage import Damage
from data.constants import Flags, PROJECTILE_TRACKER, SYSTEM, SLASH_TRACKER, trad
from data.numerics.affliction import Affliction
from data.image.hoverable import Hoverable, Text
from data.image.tile import Tile

class Spell():
    """Creates a spell. A spell is how creature interact with each other
    and themselves.
    
    Args:
        name (str): Name of the spell.
        icon (Image|Animation): Icon of the spell.
        attack_anim (Image|Animation): Image or animation for the\
        attack.
        base_damage (Damage): Base damage of the spell.
        mana_cost (float, optionnal): Mana cost of the spell. Defaults\
        to 0.
        life_cost (float, optionnal): Life cost of the spell. Defaults\
        to 0.
        delay (int, optionnal): Delay between the spell's animation\
        start and when its effect start. Defaults to 0.
        distance (float, optionnal): Maximum distance of the spell.\
        Used for dashes. Defaults to 0.
        cooldown (float, optionnal): Cooldown in seconds of the spell.\
        Defaults to 0.1.
        projectiles (int, optionnal): Number of projectiles to launch.\
        Defaults to 1.
        flags (list, optionnal): List of flags of the spell. Defaults to\
        `[]` (no flags) but flags SHOULD be given for the spell to work.
        afflictions (list, optionnal): List of afflictions that the spell\
        will inflict. Defaults to `[]`.
    """
    def __init__(self, name, icon, attack_anim, base_damage:Damage, mana_cost = 0, life_cost = 0,\
                 bounces = 0, delay = 0, distance = 0,\
                 cooldown = 0.1, projectiles = 1, flags = None, afflictions = None):
        self._name = name
        self._icon = icon
        self._attack_anim = attack_anim
        self._base_damage = base_damage
        self._level = 1
        self._stats = {
            "mana_cost": Stat(mana_cost, "mana_cost"),
            "life_cost": Stat(life_cost, "life_cost"),
            "bounces": Stat(bounces, "bounces"),
            "delay": Stat(delay, "delay"),
            "cooldown": Stat(cooldown, "cooldown"),
            "projectiles": Stat(projectiles, "projectiles"),
            "distance": Stat(distance, "distance")
        }
        self._cooldown = 0
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags

        if afflictions is None or not isinstance(afflictions, list):
            self._afflictions = []
        else:
            self._afflictions = afflictions
        self._surface = None
        self.generate_surface()

    def generate_surface(self):
        """Creates the hoverable surface of the spell."""
        if self._icon is None:
            return
        img = self._icon.get_image()
        title = Text(trad('spells_name', self._name), size=35, font="item_titles")
        desc = Text(trad('spells_desc', self._name), size=20, font="item_desc")
        title_h = max(img.get_height(), title.height)
        title_w = img.get_width() + 5 + title.width
        real_w = max(title_w, desc.width)
        title_card = SYSTEM["images"]["ui_rare"]\
                    .duplicate(real_w, title_h)
        affix_card = SYSTEM["images"]["item_desc"].duplicate(real_w, desc.height)
        sfc = pygame.Surface((title_card.get_width(), title_card.get_height()\
                                + affix_card.get_height()), pygame.SRCALPHA)
        icon_pos = (title_card.get_width() / 2 - title_w / 2,\
            title_card.get_height() / 2 - img.get_height() / 2)
        title_pos = (title_card.get_width() / 2 - title_w / 2 + img.get_width() + 3,\
            title_card.get_height() / 2 - title.height / 2)
        desc_pos = (affix_card.get_width() / 2 - desc.width / 2,\
            affix_card.get_height() / 2 - desc.height / 2 + title_card.get_height())
        sfc.blit(title_card, (0, 0))
        sfc.blit(affix_card, (0, title_card.get_height()))
        sfc.blit(img, icon_pos)
        sfc.blit(title.surface, title_pos)
        sfc.blit(desc.surface, desc_pos)
        self._surface = sfc

    def tick(self):
        """Ticks down the spell's cooldown."""
        self._cooldown -= float(SYSTEM["options"]["fps"])
        self._cooldown = max(self._cooldown, 0)

    def reset(self):
        """Resets the spell's data."""
        self._cooldown = 0

    def __damage_describe(self, caster):
        """Describes the damage and buffs components."""
        descript = ""
        if self._base_damage is not None:
            descript += self._base_damage.describe(caster, Flags.MELEE in self._flags,\
                Flags.RANGED in self._flags, Flags.SPELL in self._flags)
        if Flags.DASH in self._flags:
            descript += f"{trad('meta_words', 'dash')} {self._stats['distance'].c_value}" +\
                f" {trad('meta_words', 'meters')}\n"
        return descript

    def __describe_afflictions(self):
        """Describe the spell's buff and debuff components."""
        buffs = []
        if Flags.BUFF in self._flags:
            for afflic in self._afflictions:
                buffs.append(afflic.describe(True))
        if Flags.DEBUFF in self._flags:
            for afflic in self._afflictions:
                buffs.append(afflic.describe(True))
        if Flags.CUTS_PROJECTILE in self._flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'cut_proj'), None, (0,0,0)))
        return buffs

    def describe(self):
        """Returns a description of the spell."""
        data = {
            "name": trad('spells_name', self._name),
            "desc": trad('spells_desc', self._name),
            "level": str(self._level),
            "damage": self.__damage_describe(SYSTEM["player"].creature),
            "buffs": self.__describe_afflictions()
        }
        return data

    def cast(self, caster: Creature, entity: Entity, evil: bool, aim_right = True, force = False):
        """Shoots the spell."""
        mana_cost = caster.get_efficient_value(self._stats["mana_cost"].c_value)
        life_cost = caster.get_efficient_value(self._stats["life_cost"].c_value)

        if not force:
            if self._cooldown > 0:
                return
            if caster.stats["mana"].current_value < mana_cost:
                return
            if caster.stats["life"].current_value < life_cost:
                return
        self._cooldown = self._stats["cooldown"].c_value * caster.stats["cast_speed"].c_value
        caster.consume_mana(self._stats["mana_cost"].c_value)
        caster.stats["life"].current_value -= life_cost
        if Flags.PROJECTILE in self._flags:
            if Flags.BARRAGE in self._flags:
                for i in range (0, self._stats["projectiles"].c_value):
                    proj = Projectile(entity.center[0], entity.center[1] + i * 20, 0 ,\
                                      self._attack_anim.clone(),\
                                      self._base_damage, caster, evil,\
                                      delay=self._stats["delay"].c_value * (i + 1),\
                                      bounces=self._stats["bounces"].c_value, \
                                      behaviours=self._flags, caster=entity)
                    PROJECTILE_TRACKER.append(proj)
            elif Flags.SPREAD in self._flags:
                if self._stats["projectiles"].c_value == 1:
                    proj = Projectile(entity.center[0], entity.center[1], 0,\
                                      self._attack_anim.clone(), self._base_damage, caster, evil,\
                                      delay=self._stats["delay"].c_value,\
                                      bounces=self._stats["bounces"].c_value, \
                                      behaviours=self._flags, caster=entity)
                    PROJECTILE_TRACKER.append(proj)
                else:
                    spread = 90 / self._stats["projectiles"].c_value
                    for i in range(0, self._stats["projectiles"].c_value):
                        proj = Projectile(entity.center[0], entity.center[1], -45 + spread * i,\
                                        self._attack_anim.clone(), self._base_damage, caster, evil,\
                                        delay=self._stats["delay"].c_value * (i + 1),\
                                        bounces=self._stats["bounces"].c_value, \
                                        behaviours=self._flags, caster=entity)
                        PROJECTILE_TRACKER.append(proj)
        if Flags.BUFF in self._flags:
            for afflic in self._afflictions:
                if not isinstance(afflic, Affliction):
                    continue
                caster.afflict(afflic.clone())
        if Flags.DASH in self._flags:
            entity.dash(self._stats["distance"].c_value)
        if Flags.MELEE in self._flags:
            sl = Slash(entity, caster, self._attack_anim, self._base_damage,\
                       aim_right, evil, self._flags)
            SLASH_TRACKER.append(sl)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def cooldown(self):
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats = value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def surface(self):
        return self._surface
