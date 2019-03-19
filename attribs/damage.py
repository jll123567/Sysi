"""Define for damage profile."""


class dmg:
    """Hold damages."""

    def __init__(self, damages=None):
        """Damages: dictionary"""
        if damages is None:
            self.damages = {"health": 0}
        else:
            self.damages = damages

    def newDamage(self, stat, amount):
        """Add {stat: amount}."""
        self.damages.update({stat: amount})

    def removeDamage(self, stat):
        """Remove the first damage that modifies stat."""
        self.damages.pop(stat)
