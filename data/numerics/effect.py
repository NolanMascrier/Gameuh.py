"""An effect is a status that is triggered on
multiple conditions. Like an affliction, it has
a duration."""

class Effect():
    def __init__(self, name, duration, flags = None, target = None):
        self._name = name
        self._duration = duration
        if flags is None:
            self._flags = []
        else:
            self._flags = flags
        self.on_creation(target)
        
    def tick(self, target = None):
        """Ticks down the duration.
        
        Args:
            target (creature): target of the effect.
        """
        if self._duration > 0:
            self._duration -= 1
            if self._duration == 0:
                self.on_expiration(target)
        if self._duration != 0:
            self.on_tick(target)
    
    def on_tick(self, target = None):
        """Action to call on ticks.
        
        Args:
            target (creature): target of the effect.
        """

    def on_creation(self, target = None):
        """Action to call when the effect is applied to\
        a creature.
        
        Args:
            target (creature): target of the effect.
        """

    def on_expiration(self, target = None):
            """Action to call when the effect is removed from\
            a creature.
            
            Args:
                target (creature): target of the effect.
            """

    def on_damage(self, target = None):
            """Action to call when the creature is dealt \
            damage.
            
            Args:
                target (creature): target of the effect.
            """

    def on_heal(self, target = None):
            """Action to call when the creature is healing \
            damage.
            
            Args:
                target (creature): target of the effect.
            """

    def on_reload(self, target = None):
            """Action to call when the creature is reloading \
            a gun.
            
            Args:
                target (creature): target of the effect.
            """
            
    def on_effect(self, effect = None, target = None):
            """Action to call when the creature is afflicted
            with an effect
            
            Args:
                target (creature): target of the effect.
            """