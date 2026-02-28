"""Base class for all Sticks players.

This class defines the interface that every player must implement:
  - __str__(): returns the player's display name
  - play(pile): given the current pile size, returns how many sticks to take
  - game(result): called at the start and end of each game

By default, SimpleSticks plays randomly — it picks 1, 2, or 3 sticks
with equal probability. Subclasses override these methods to implement
smarter strategies (see KiangSticks) or human input (see HumanSticks).

STUDENTS: To create your own player, write a new class that extends
SimpleSticks, override play(), and add it to sticks_driver.py's player list.
"""

import random


class SimpleSticks:
    """A player that picks a random number of sticks (1-3) each turn."""

    def __str__(self):
        """Returns the display name of this player.
        Used in game output like 'SimpleSticks took 2 sticks.'
        """
        return "SimpleSticks"

    def play(self, pile: int) -> int:
        """Decides how many sticks to take this turn.

        Args:
            pile: the number of sticks remaining in the pile.

        Returns:
            The number of sticks to take (must be 1, 2, or 3 and <= pile).
        """
        # Pick a random number from 1 to 3, but don't exceed the pile size.
        # For example, if only 2 sticks remain, pick from 1-2.
        return random.randint(1, min(3, pile))

    def game(self, result: int):
        """Called by the driver to signal game events.

        Args:
            result: 0 = game is starting (reset your state),
                    1 = you won this game (learn from it),
                   -1 = you lost this game.
        """
        # Base class does nothing — subclasses can override to learn or reset.
        pass
