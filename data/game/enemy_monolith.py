"""Special class for the Monolith Pinnacle boss."""

import numpy

from data.constants import SYSTEM
from data.game.enemy import Enemy

LIGHTSHARD = 1
SPEARS = 2
LASER = 3


class Monolith(Enemy):
    """Defines a Monolith enemy. Unlike normal enemies, a pinnacle boss has phase switchs
    and different (scripted) behaviours."""
    def __init__(self, entity, creature, abilities, power=1, timer=2, exp_value=10, gold_value=10,
                 behaviours=None, tier=1, delay=0, destination=None):
        super().__init__(entity, creature, abilities, power, timer, exp_value, gold_value,
                         behaviours, tier, delay, destination)
        self._phase = -1
        self._subphase = 0
        self._phase_switchs = [0.85, 0.75, 0.5, 0.2]
        self._counter = 2
        self._use = 0

    def phase_0(self):
        """
        Phase 0 - 

        Boss shoots simple abilities.
        """
        if self._subphase == 0:
            self._subphase = numpy.random.randint(1, 4)
        if self._counter <= 0:
            if self._subphase == LIGHTSHARD:
                SYSTEM["spells"]["e_lightshard"].cast(self._creature, self._entity,\
                                                True, self._aim_right, True)
                self._counter = 0.2
                self._use += 1
                if self._use >= 10:
                    self._subphase = 0
                    self._counter = 1
                    self._use = 0
            elif self._subphase == SPEARS:
                SYSTEM["spells"]["e_lightspear"].cast(self._creature, self._entity,\
                                                True, self._aim_right, True)
                self._counter = 2
                self._use += 1
                if self._use >= 3:
                    self._subphase = 0
                    self._counter = 1
                    self._use = 0
            elif self._subphase == LASER:
                SYSTEM["spells"]["e_lazer"].cast(self._creature, self._entity,\
                                                True, self._aim_right, True)
                self._counter = 5
                self._subphase = 0

    def tick(self, player):
        """Ticks down the creature."""
        self._counter -= 0.016
        if self._exploded:
            return
        if self._creature.stats["life"].current_value <= 0:
            self._entity.detach("die", True)
            self.explode()
            return
        if self._phase == -1:
            self._destination = [1500, 340]
            self._entity.move((1500, 340))
            if self.distance_to_destination() < 500 or self._counter <= -3:
                self._phase = 0
                self._counter = 2
                SYSTEM["level"].boss = self
                SYSTEM["post_effects"].stop_shaking()
            return
        if self._phase == 0:
            self.phase_0()
        self._entity.tick(self)
        self._creature.tick()
        if self._counter <= 0:
            pass
