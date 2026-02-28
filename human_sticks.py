"""Provides text input for a human Sticks player."""

from simple_sticks import SimpleSticks


class HumanSticks(SimpleSticks):
    """A human-controlled player that reads moves from stdin."""

    def __str__(self):
        return "Human"

    def play(self, pile: int) -> int:
        """Prompt the human player for their move."""
        print(f"There are {pile} sticks")
        print("You can take between 1 and 3 sticks.")
        return int(input("How many sticks would you like to take? "))
