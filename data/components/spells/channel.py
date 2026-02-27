"""Generic spell class for channeling spells."""

from data.game.creature import Creature
from data.physics.entity import Entity
from data.components.spells.spell import Spell

class Channel(Spell):
    """Generic channeling spell."""
    def __init__(self, name, icon, attack_anim, base_damage, mana_cost=0, life_cost=0, bounces=0,
                 delay=0, distance=0, chains=0, spread=90, explosion=None, sequence=None, 
                 cooldown=0.1, projectiles=1, flags=None, buffs=None, debuffs=None, offset_x=0, 
                 offset_y=0, proj_speed=20, effective_frames=None, anim_on_hit=None, 
                 alterations=None, debuff_chance=1, trail=None, impact=None, 
                 level_list=None, reset_rate = 1):
        super().__init__(name, icon, attack_anim, base_damage, mana_cost, life_cost, 
                         bounces, delay, distance, chains, spread, explosion, sequence, cooldown, 
                         projectiles, flags, buffs, debuffs, offset_x, offset_y, proj_speed, 
                         effective_frames, anim_on_hit, alterations, debuff_chance, trail, 
                         impact, level_list, reset_rate)
        self._channeled = 0
        self._is_channeling = False

    def on_cast(self, caster, entity, evil, aim_right=True, force=False, ignore_team=False,
            victim: Creature = None, victim_entity: Entity = None):
        self._is_channeling = True
        return super().on_cast(caster, entity, evil, aim_right, force, ignore_team,
                               victim, victim_entity)

    def tick(self, caster=None):
        if not self._is_channeling:
            self._channeled = 0
        super().tick(caster)
        self._is_channeling = False
