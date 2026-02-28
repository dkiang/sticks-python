"""Basic class template for a Sticks game player."""

import random


class SimpleSticks:
    """A player that picks a random number of sticks (1-3) each turn."""

    def __str__(self):
        return "SimpleSticks"

    def play(self, pile: int) -> int:
        """Return a random valid number of sticks to take from the pile."""
        return random.randint(1, min(3, pile))

    def game(self, result: int):
        """Called at start or end of game.

        Args:
            result: 0 for game start, 1 if game was won, -1 if game was lost.
        """
        pass
