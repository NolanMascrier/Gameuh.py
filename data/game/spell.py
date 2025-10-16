"""For spells"""

import json
import numpy

from data.api.surface import Surface

from data.image.animation import Image
from data.projectile import Projectile
from data.item import Item
from data.creature import Creature
from data.physics.entity import Entity
from data.numerics.stat import Stat
from data.numerics.rangestat import RangeStat
from data.numerics.ressource import Ressource
from data.slash import Slash
from data.numerics.damage import Damage
from data.constants import Flags, PROJECTILE_TRACKER, SYSTEM, trad
from data.numerics.affliction import Affliction
from data.image.hoverable import Hoverable, Text

BLACK = (0,0,0)

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
        buffs (list, optionnal): List of afflictions that the spell\
        will inflict. Defaults to `[]`.
        debuffs
    """
    def __init__(self, name, icon, attack_anim, base_damage:Damage, mana_cost = 0, life_cost = 0,\
                 bounces = 0, delay = 0, distance = 0, chains = 0, spread = 90,\
                 explosion = None, sequence = None,\
                 cooldown = 0.1, projectiles = 1, flags = None, buffs = None,\
                 debuffs = None, offset_x = 0, offset_y = 0, proj_speed = 20,\
                 effective_frames = None, anim_on_hit = None, alterations = None):
        self._name = name
        self._icon = icon
        self._attack_anim = attack_anim
        self._base_damage = base_damage
        self._real_damage = base_damage.clone() if base_damage is not None else None
        self._level = 1
        self._exp = 0
        self._exp_to_next = 3000
        self._effective_frames = effective_frames
        self._afflicts = []
        self._stats = {
            "mana_cost": Stat(mana_cost, "mana_cost"),
            "life_cost": Stat(life_cost, "life_cost"),
            "bounces": Stat(bounces, "bounces"),
            "delay": Stat(delay, "delay"),
            "cooldown": Stat(cooldown, "cooldown", min_cap=0.1),
            "projectiles": Stat(projectiles, "projectiles"),
            "distance": Stat(distance, "distance"),
            "chains": Stat(chains, "chains"),
            "spread": Stat(spread, "spread"),
            "projectile_speed": Stat(proj_speed, "proj_speed"),
            "damage_mod": Stat(1, "damage_mod"),
            "area": Stat(1, "area", min_cap=0.2),
            "crit_rate": Stat(base_damage.crit_rate if base_damage is not None else 0,\
                            "crit_rate", 1, 0),
            "crit_dmg": Stat(base_damage.crit_mult if base_damage is not None else 0,\
                            "crit_dmg"),
            "anim_speed": Stat(1, "anim_speed")
        }
        self._jewels = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None
        }
        self._modifiers = []
        self._changed = set()
        self._cooldown = 0
        self._anim_on_hit = anim_on_hit
        if flags is None or not isinstance(flags, list):
            self._flags = []
        else:
            self._flags = flags
        if buffs is None or not isinstance(buffs, list):
            self._buffs = []
        else:
            self._buffs = buffs
        if debuffs is None or not isinstance(debuffs, list):
            self._debuffs = []
        else:
            self._debuffs = debuffs
        if alterations is None or not isinstance(alterations, list):
            self._alterations = []
        else:
            self._alterations = alterations
        if sequence is None or not isinstance(sequence, list):
            self._sequence = []
        else:
            self._sequence = sequence
        self._gathered_flags = []
        self._sequence_timer = 0
        self._sequence_step = 0
        self._explosion = explosion
        self._surface = None
        self._offset = (offset_x, offset_y)
        self._started = False
        self.generate_surface()
        self.update()
        self._counter = 0
        self._releasing = False
        self._to_release = 0

    def update(self):
        """Updates the data of the spell."""
        dmg = Affliction("DAMGE_FROM_LEVEL", 1.02 * (self._level - 1), -1,\
            [Flags.DAMAGE_MOD, Flags.BOON])
        hp = Affliction("LIFE_COST_PER_LEVEL",  1 - 0.01 * (self._level - 1), -1,\
            [Flags.LIFE_COST, Flags.BLESS])
        mana = Affliction("MANA_COST_PER_LEVEL",  1 - 0.01 * (self._level - 1), -1,\
            [Flags.MANA_COST, Flags.BLESS])
        self.afflict((dmg, hp, mana))
        self.recalculate_damage()
        for step in self._sequence:
            step.update()
        self._gathered_flags = []
        for _, j in self._jewels.items():
            if j is not None:
                self._gathered_flags.extend(j.flags)

    def recalculate_damage(self):
        """Recalculates the damage using the spell's stats."""
        if self._base_damage is None:
            return
        mod = self._stats["damage_mod"].get_value()
        self._real_damage.mod = mod
        self._real_damage.crit_mult = self._stats["crit_dmg"].c_value
        self._real_damage.crit_rate = self._stats["crit_rate"].c_value
        if self._explosion is not None and isinstance(self._explosion, Slash):
            self._explosion.damage.mod = mod
            self._explosion.damage.crit_mult = self._stats["crit_dmg"].c_value
            self._explosion.damage.crit_rate = self._stats["crit_rate"].c_value

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
        sfc = Surface(title_card.get_width(), title_card.get_height()\
                                + affix_card.get_height())
        icon_pos = (title_card.get_width() / 2 - title_w / 2,\
            title_card.get_height() / 2 - img.get_height() / 2)
        title_pos = (title_card.get_width() / 2 - title_w / 2 + img.get_width() + 3,\
            title_card.get_height() / 2 - title.height / 2)
        desc_pos = (affix_card.get_width() / 2 - desc.width / 2,\
            affix_card.get_height() / 2 - desc.height / 2 + title_card.get_height())
        sfc.blit(title_card, (0, 0), True)
        sfc.blit(affix_card, (0, title_card.get_height()), True)
        sfc.blit(img, icon_pos, True)
        sfc.blit(title.surface, title_pos, True)
        sfc.blit(desc.surface, desc_pos, True)
        self._surface = sfc
        self._alternate = False

    def gain_exp(self, amount: int):
        """Grants the skill experience."""
        if self._level >= 20:
            return
        self._exp += amount
        while self._exp >= self._exp_to_next:
            self._level += 1
            self.update()
            self._exp -= self._exp_to_next
            self._exp_to_next = round(self._exp_to_next * 1.68)
            if self._level >= 20:
                self._exp_to_next = 9999999999
                break

    def tick(self, caster = None):
        """Ticks down the spell's cooldown."""
        self._cooldown -= 0.016
        self._cooldown = max(self._cooldown, 0)
        for _, stat in self._stats.items():
            stat.tick()
        for buff in self._afflicts:
            buff.tick()
            if buff.expired:
                self._afflicts.remove(buff)
        if self._releasing:
            self._counter -= 0.016
            if self._counter <= 0:
                self._to_release -= 1
                self._counter = self._stats["delay"].c_value
                self.spawn_projectile(caster.entity, caster.creature, False, 0, 0,\
                                          self._stats["delay"].c_value * 10,\
                                          numpy.random.randint(0, 361))
            if self._to_release <= 0:
                self._releasing = False
        if Flags.COMBO_SPELL in self.all_flags:
            for s in self._sequence:
                s.tick(caster)
            if self._started:
                self._sequence_timer += 0.016
            if (self._sequence_step >= len(self._sequence) or self._sequence_timer >= 3)\
                and self._started:
                self._cooldown = self._stats["cooldown"].c_value *\
                    caster.creature.stats["cast_speed"].c_value
                self._sequence_step = 0
                self._sequence_timer = 0
                self._started = False

    def __apply_afflict(self, affliction: Affliction):
        """Applies the affliction."""
        for flag in affliction.flags:
            stat_key = flag.value
            if stat_key in self._stats:
                self._stats[stat_key].afflict(affliction)
                self._changed.add(stat_key)
        if affliction.stackable:
            self._modifiers.append(affliction)
        else:
            for i, existing_aff in enumerate(self._modifiers):
                if existing_aff.name == affliction.name:
                    self._modifiers[i] = affliction
                    return
            self._modifiers.append(affliction)
        if affliction.stackable:
            self._afflicts.append(affliction)
        else:
            for i, existing_aff in enumerate(self._afflicts):
                if existing_aff.name == affliction.name:
                    self._afflicts[i] = affliction
                    return
            self._afflicts.append(affliction)

    def afflict(self, affliction):
        """Afflicts the spell with an affliction from a jewel.
        Jewels being gear-like, there's no need to tick them.
        
        Args:
            affliction (Affliction): Affliction to afflict.
        """
        if isinstance(affliction, tuple):
            for a in affliction:
                self.__apply_afflict(a)
        elif isinstance(affliction, Affliction):
            self.__apply_afflict(affliction)
        for step in self._sequence:
            if isinstance(step, Spell):
                step.afflict(affliction)

    def __remove_afflic(self, affliction: Affliction):
        """Removes an affliction from the spell.
        
        Args:
            affliction (Affliction): Affliction to remove.
        """
        for f in affliction.flags:
            stat_key = f.value
            if stat_key in self._stats:
                self._changed.add(stat_key)
        for d in self._modifiers.copy():
            if d == affliction:
                self._modifiers.remove(d)
        for st in self._stats:
            self._stats[st].remove_affliction(affliction)

    def remove_affliction(self, affliction: Affliction):
        """Removes an affliction from the spell.
        
        Args:
            affliction (Affliction): Affliction to remove.
        """
        if isinstance(affliction, tuple):
            for a in affliction:
                self.__remove_afflic(a)
        elif isinstance(affliction, Affliction):
            self.__remove_afflic(affliction)
        for step in self._sequence:
            if isinstance(step, Spell):
                step.remove_affliction(affliction)

    def equip(self, slot: int, item: Item) -> Item | None:
        """Equips a jewel in the slot. Returns the
        equipped jewel if the slot is already occupied.
        
        Args:
            slot (int):Index of the slot to equip.
            item (Item): Item to equip. The item needs the JEWEL flag !
            left_hand (bool, optionnal): If the slot is\
            a ring, `True` will indicate the left ring\
            and `False` the right ring. Defaults to `False`.
        """
        if item is None or Flags.JEWEL not in item.flags:
            return None
        if slot not in self._jewels:
            return None
        old = self.unequip(slot)
        self._jewels[slot] = item
        for affix in item.affixes:
            self.afflict(affix.as_affliction())
        for affix in item.implicits:
            self.afflict(affix.as_affliction())
        self.update()
        return old

    def unequip(self, slot: int) -> Item | None:
        """Removes an item from the user's gear, and returns it.
        
        Args:
            slot (int): Index of the slot to empty.
        
        Returns:
            item: Item removed. `None` if the slot was\
            empty.
        """
        if slot not in self._jewels:
            return None
        item = self._jewels[slot]
        self._jewels[slot] = None
        if item is not None:
            for affix in item.affixes :
                self.remove_affliction(affix.as_affliction())
            for affix in item.implicits :
                self.remove_affliction(affix.as_affliction())
        self.update()
        return item

    def reset(self):
        """Resets the spell's data."""
        self._cooldown = 0

    def __damage_describe(self, caster):
        """Describes the damage and buffs components."""
        descript = ""
        if self._real_damage is not None:
            descript += self._real_damage.describe(caster, Flags.MELEE in self.all_flags,\
                Flags.RANGED in self.all_flags, Flags.SPELL in self.all_flags)
        if Flags.DASH in self.all_flags:
            descript += f"{trad('meta_words', 'dash')} {self._stats['distance'].c_value}" +\
                f" {trad('meta_words', 'meters')}\n"
        return descript

    def __explosion_describe(self, caster):
        """Describes the damage and buffs components."""
        if self._explosion is None:
            return None
        descript = ""
        if self._explosion.damage is not None:
            descript += self._explosion.damage.describe(caster,\
                Flags.MELEE in self._explosion.flags,\
                Flags.RANGED in self._explosion.flags, Flags.SPELL in self._explosion.flags)
        return descript

    def __describe_afflictions(self):
        """Describe the spell's buff and debuff components."""
        buffs = []
        if Flags.BUFF in self.all_flags:
            for afflic in self._buffs:
                buffs.append(afflic.describe(True))
        if Flags.DEBUFF in self.all_flags:
            for afflic in self._debuffs:
                buffs.append(afflic.describe(False))
        if Flags.CUTS_PROJECTILE in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'cut_proj'), None, BLACK))
        if Flags.TRIGGER in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'trigger'), None, BLACK))
        if Flags.TRIGGER_ON_CRIT in self.all_flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'trigger_on_crit'), None, BLACK))
        return buffs

    def __explosion_afflictions(self):
        """Describe the spell's buff and debuff components."""
        if self._explosion is None:
            return None
        buffs = []
        if Flags.DEBUFF in self._explosion.flags:
            for afflic in self._explosion.flags:
                buffs.append(afflic.describe(False))
        if Flags.CUTS_PROJECTILE in self._explosion.flags:
            buffs.append(Hoverable(0, 0, trad('meta_words', 'cut_proj'), None, BLACK))
        return buffs

    def describe(self):
        """Returns a description of the spell."""
        sequence = None if len(self._sequence) == 0 else self._sequence
        explosion = None if self._explosion is None else {
            "damage": self.__explosion_describe(SYSTEM["player"].creature),
            "buffs": self.__explosion_afflictions(),
            "name": trad('spells_name', f"{self._name}_explosion"),
            "desc": trad('spells_desc', f"{self._name}_explosion"),
            "level": str(self._level),
            "cooldown": None,
            "projectiles": None,
            "area": self._explosion.area,
            "costs": (0, 0),
            "crit_rate": 1 + self._explosion.damage.crit_rate,
            "crit_dmg": 1 + self._explosion.damage.crit_mult,
            "dmg_effic": Hoverable(0, 0, f"{trad('descripts', 'dmg_effic')}:" +\
                f"{round(self._explosion.damage.coeff * 100, 2)}%",\
                trad('dmg_effic'), BLACK) if self._explosion.damage is not None else None,
            "sequence": None,
            "explosion": None
        }
        data = {
            "name": trad('spells_name', self._name),
            "desc": trad('spells_desc', self._name),
            "level": str(self._level),
            "damage": self.__damage_describe(SYSTEM["player"].creature),
            "buffs": self.__describe_afflictions(),
            "cooldown": str(self._stats["cooldown"].get_value() *\
                            SYSTEM["player"].creature.stats["cast_speed"].c_value),
            "costs": (self._stats["life_cost"].c_value, self._stats["mana_cost"].c_value),
            "projectiles": self._stats["projectiles"].c_value\
                if Flags.PROJECTILE in self.all_flags else None,
            "dmg_effic": Hoverable(0, 0, f"{trad('descripts', 'dmg_effic')}:" +\
                f"{round(self._base_damage.coeff * 100, 2)}%",\
                trad('dmg_effic'), BLACK) if self._base_damage is not None else None,
            "area": self._stats['area'].c_value,
            "crit_rate": self._stats['crit_rate'].c_value if\
                (self._real_damage is not None and not self._real_damage.is_crit) else True,
            "crit_dmg": self._stats['crit_dmg'].c_value,
            "sequence": sequence,
            "explosion": explosion
        }
        return data

    def on_hit(self, value):
        """Called when the creature is hit."""

    def on_crit(self, caster: Creature, entity: Entity,
            evil: bool, aim_right = True, force = False):
        """Called when the creature crits."""
        if Flags.TRIGGER_ON_CRIT in self.all_flags:
            self.on_cast(caster, entity, evil, aim_right, force)

    def on_dodge(self):
        """Called when the creature dodges."""

    def on_block(self):
        """Called when the creature blocks."""

    def on_damage(self, value):
        """Called when the creature inflicts damage."""

    def cast(self, caster: Creature, entity: Entity, evil: bool, aim_right = True, force = False,\
             ignore_team = False):
        """Launches the spell."""
        if Flags.AURA in self.all_flags:
            return
        if Flags.TRIGGER in self.all_flags:
            return
        if Flags.COMBO_SPELL in self.all_flags:
            if self._cooldown > 0:
                return
            if self._sequence[self._sequence_step].on_cast(caster, entity, evil, aim_right, force):
                self._started = True
                self._sequence_step += 1
                self._sequence_timer = 0
                if self._sequence_step < len(self._sequence):
                    self._sequence[self._sequence_step].start_cooldown(0.5, caster)
        else:
            self.on_cast(caster, entity, evil, aim_right, force, ignore_team)

    def spawn_projectile(self, entity, caster, evil = False,\
            x_diff = 0, y_diff = 0, delay = 1, angle = 0, ignore_team = False):
        """Spanws a projectile."""
        if evil and entity.x > SYSTEM["player"].entity.x:
            angle += 180
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        proj = Projectile(entity.center[0] + x_diff, entity.center[1] + y_diff, angle,\
                        self._attack_anim,\
                        self._real_damage, caster, evil,\
                        speed=self._stats["projectile_speed"].c_value,\
                        delay=self._stats["delay"].c_value * delay,\
                        bounces=self._stats["bounces"].c_value, \
                        chains=self._stats["chains"].c_value, \
                        behaviours=self._flags, caster=entity, debuffs=self._debuffs,
                        explosion=self._explosion, area=area,\
                        ignore_team=ignore_team, anim_on_hit=self._anim_on_hit,
                        anim_speed=self._stats["anim_speed"].c_value)
        PROJECTILE_TRACKER.append(proj)

    def spawn_slash(self, entity, caster, evil = False, aim_right = False, ignore_team = False):
        """Spawns a slash."""
        area = self._stats["area"].c_value + caster.stats["area"].c_value
        sl = Slash(entity, caster, self._attack_anim, self._real_damage,\
                       not aim_right, evil, self._flags, self._offset[0],\
                       self._offset[1], debuffs=self._debuffs, area=area,\
                       ignore_team=ignore_team, effective_frames=self._effective_frames,\
                       anim_on_hit=self._anim_on_hit, anim_speed=self._stats["anim_speed"].c_value)
        PROJECTILE_TRACKER.append(sl)

    def on_cast(self, caster: Creature, entity: Entity, evil: bool,\
            aim_right = True, force = False, ignore_team = False):
        """Shoots the spell."""
        mana_cost = caster.get_efficient_value(self._stats["mana_cost"].c_value)
        life_cost = caster.get_efficient_value(self._stats["life_cost"].c_value)
        if not force:
            if self._cooldown > 0:
                return False
            if caster.stats["mana"].current_value < mana_cost:
                return False
            if caster.stats["life"].current_value < life_cost:
                return False
        for b in self._alterations:
            print(f"AFFLIC {str(b)}")
            self.afflict(b)
        self._cooldown = self._stats["cooldown"].c_value * caster.stats["cast_speed"].c_value
        caster.consume_mana(self._stats["mana_cost"].c_value)
        caster.stats["life"].current_value -= life_cost
        if Flags.FLURRY_RELEASE in self.all_flags:
            self._releasing = True
            self._to_release = self._stats["projectiles"].c_value
            self._counter = 0.1
        if Flags.PROJECTILE in self.all_flags:
            if Flags.BARRAGE in self.all_flags:
                for i in range (0, int(self._stats["projectiles"].c_value)):
                    self.spawn_projectile(entity, caster, evil, 0, i * (20 + self._offset[1]),\
                                          i + 1, 0, ignore_team)
            elif Flags.SPREAD in self.all_flags:
                if self._stats["projectiles"].c_value == 1:
                    self.spawn_projectile(entity, caster, evil)
                else:
                    spread = self._stats["spread"].c_value / self._stats["projectiles"].c_value
                    for i in range(0, int(self._stats["projectiles"].c_value)):
                        self.spawn_projectile(entity, caster, evil, 0, 0, i + 1, -45 + spread * i)
            elif Flags.CIRCULAR_BLAST in self.all_flags:
                if self._stats["projectiles"].c_value == 1:
                    self.spawn_projectile(entity, caster, evil)
                else:
                    self._counter = (self._counter + 5) % 360
                    spread = 360 / self._stats["projectiles"].c_value
                    for i in range(0, int(self._stats["projectiles"].c_value)):
                        self.spawn_projectile(entity, caster, evil,
                                              0, 0, i + 1, self._counter + -spread * i)
        if Flags.BUFF in self.all_flags:
            for afflic in self._buffs:
                if not isinstance(afflic, Affliction):
                    continue
                caster.afflict(afflic.clone())
        if Flags.DASH in self.all_flags:
            entity.dash(self._stats["distance"].c_value)
        if Flags.MELEE in self.all_flags:
            self.spawn_slash(entity, caster, evil, aim_right)
        return True

    def start_cooldown(self, reduce_factor = 0, caster = None):
        """Starts the spell's cooldown.
        
        Args:
            reduce_factor (float, optional): Starts the cooldown\
            with a fraction of the time already elapsed. Defaults to 0.
        """
        self._cooldown = self._stats["cooldown"].c_value * caster.stats["cast_speed"].c_value
        self._cooldown *= 1 - reduce_factor

    def export(self) -> str:
        """Serialize the spell as JSON."""
        stats = {}
        buffs = []
        debuffs = []
        sequence = []
        jewels = {}
        for s in self._stats:
            stats[s] = self._stats[s].export()
        for a in self._buffs:
            buffs.append(a.export())
        for a in self._debuffs:
            debuffs.append(a.export())
        for s in self._sequence:
            sequence.append(s.export())
        for j in self._jewels:
            if self._jewels[j] is None:
                jewels[j] = None
            else:
                jewels[j] = self._jewels[j].export()
        data = {
            "type": "spell",
            "name": self._name,
            "level": self._level,
            "stats": stats,
            "icon": self._icon.uri if self._icon  is not None else None,
            "animation": self._attack_anim if self._attack_anim is not None else None,
            "damage": self._base_damage.export() if self._base_damage is not None else None,
            "flags": self._flags,
            "buffs": buffs,
            "debuffs": debuffs,
            "offset": self._offset,
            "sequence": sequence,
            "explosion": self._explosion.export() if self._explosion is not None else None,
            "jewels": jewels,
            "exp": self._exp,
            "exp_next": self._exp_to_next
        }
        return json.dumps(data)

    @staticmethod
    def imports(data):
        """Reads a json data and creates a spell."""
        stats = {}
        buffs = []
        debuffs = []
        sequence = []
        jewels = {}
        for s in data["stats"]:
            val = json.loads(data["stats"][s])
            if val["type"] == "stat":
                stats[s] = Stat.imports(val)
            elif val["type"] == "ressource":
                stats[s] = Ressource.imports(val)
            elif val["type"] == "rangestat":
                stats[s] = RangeStat.imports(val)
        for a in data["buffs"]:
            buffs.append(Affliction.imports(json.loads(a)))
        for a in data["debuffs"]:
            debuffs.append(Affliction.imports(json.loads(a)))
        for s in data["sequence"]:
            sequence.append(Spell.imports(json.loads(s)))
        for j in data["jewels"]:
            if data["jewels"][j] is not None:
                jewels[j] = Item.imports(json.loads(data["jewels"][j]))
            else:
                jewels[j] = None
        spell = Spell(
            data["name"],
            Image(data["icon"]).scale(64, 64) if data["icon"] is not None else None,
            data["animation"],
            Damage.imports(json.loads(data["damage"])) if data["damage"] is not None else None,
            flags=data["flags"],
            buffs=buffs,
            debuffs=debuffs,
            explosion=Slash.imports(json.loads(data["explosion"]))\
                if data["explosion"] is not None else None,
            sequence=sequence,
            offset_x=int(data["offset"][0]),
            offset_y=int(data["offset"][1])
        )
        spell.level = int(data["level"])
        spell.exp = int(data["exp"])
        spell.exp_to_next = int(data["exp_next"])
        spell.stats = stats
        spell.jewels = jewels
        return spell

    @property
    def name(self):
        """Returns the spell's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def icon(self):
        """Returns the spell's icon."""
        if Flags.COMBO_SPELL in self.all_flags:
            return self._sequence[self._sequence_step].icon
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def cooldown(self):
        """Returns the spell's cooldown."""
        return self._cooldown

    @cooldown.setter
    def cooldown(self, value):
        self._cooldown = value

    @property
    def stats(self):
        """Returns the spell's stats."""
        return self._stats

    @stats.setter
    def stats(self, value):
        self._stats = value

    @property
    def flags(self):
        """Returns the spell's flags."""
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def level(self):
        """Returns the spell's level."""
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def surface(self):
        """Returns the spell's description surface."""
        return self._surface

    @property
    def exp(self):
        """Return's the spell experience."""
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value

    @property
    def exp_to_next(self):
        """Return's the spell's needed experience for the next level."""
        return self._exp_to_next

    @exp_to_next.setter
    def exp_to_next(self, value):
        self._exp_to_next = value

    @property
    def jewels(self):
        """Return's the spell's slotted jewels."""
        return self._jewels

    @jewels.setter
    def jewels(self, value):
        self._jewels = value

    @property
    def sequence(self):
        """Returns the spell's sequence."""
        return self._sequence

    @property
    def all_flags(self):
        """Returns the spell's flags native and from jewels."""
        fl = []
        fl.extend(self._flags)
        fl.extend(self._gathered_flags)
        return fl
