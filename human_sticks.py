"""A human-controlled Sticks player that reads moves from the console.

Prompts the user for input each turn and validates that the move
is within the allowed range (1-3 sticks, not exceeding the pile).
"""

from simple_sticks import SimpleSticks


class HumanSticks(SimpleSticks):
    """A human player that reads moves from stdin."""

    def __str__(self):
        return "Human"

    def play(self, pile: int) -> int:
        """Prompts the human player to choose how many sticks to take.
        Repeats the prompt until the player enters a valid number.

        Args:
            pile: the number of sticks remaining.

        Returns:
            The number of sticks the player chose to take.
        """
        max_take = min(3, pile)

        while True:
            print(f"There are {pile} sticks.")
            try:
                choice = int(input(f"How many sticks would you like to take? (1-{max_take}) "))
            except ValueError:
                print("Please enter a number.")
                continue

            # Validate the move
            if 1 <= choice <= max_take:
                return choice
            print(f"Invalid choice. You must take between 1 and {max_take} sticks.")
