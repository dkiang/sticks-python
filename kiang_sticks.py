"""Machine learning Sticks player that improves by recording winning moves.

HOW THE LEARNING MODEL WORKS:

KiangSticks maintains 20 "buckets" — one for each possible pile size
from 1 to 20. Each bucket is a list of numbers (1, 2, or 3) representing
move choices. Initially, every bucket contains [1, 2, 3], so each move
is equally likely.

When KiangSticks WINS a game, the moves it made during that game are
added back into their respective buckets. For example, if it took 2
sticks when the pile was 9 and won, an extra "2" is added to bucket 9.
Now bucket 9 might look like [1, 2, 2, 3], making "2" twice as likely
to be chosen next time the pile is 9.

Over many games, winning patterns are reinforced and losing patterns
fade in relative probability. The buckets are saved to moves.txt so
learning persists across sessions.

Uses the model from The Game of Sticks activity:
http://nifty.stanford.edu/2014/laaksonen-vihavainen-game-of-sticks/
"""

import bisect
import random
from pathlib import Path

from simple_sticks import SimpleSticks

# The file where learned move distributions are saved
MOVES_FILE = Path("moves.txt")

# The number of pile sizes we track (buckets for pile sizes 1 through MAX_PILE)
MAX_PILE = 20


class KiangSticks(SimpleSticks):
    """An AI player that learns from its wins by reinforcing successful move choices.

    Each pile size (1-20) has a 'bucket' of possible moves. When KiangSticks
    wins, the moves it made are added back into the buckets, making those
    choices more likely in the future.
    """

    def __init__(self):
        # Records the move made at each pile size during the current game.
        # moves[i] = the number of sticks taken when the pile was (i+1),
        # or 0 if no move was made at that pile size.
        self.moves: list[int] = [0] * MAX_PILE

        # buckets[i] holds the list of candidate moves for when the pile
        # size is (i+1). More copies of a number = higher probability of
        # choosing it.
        self.buckets: list[list[int]] = []
        self._load()

    def __str__(self):
        return "Mr. Kiang"

    def play(self, pile: int) -> int:
        """Chooses a move by randomly sampling from the bucket for this pile size.

        For pile sizes larger than MAX_PILE (which we don't have learned data
        for), always take 3 to reduce the pile into the learned range quickly.

        Args:
            pile: the number of sticks remaining.

        Returns:
            The number of sticks to take.
        """
        # For very large piles, take the max to get into the learned range
        if pile > MAX_PILE:
            return 3

        # Only one stick left — must take it
        if pile == 1:
            return 1

        # Buckets are 0-indexed: pile size 1 → index 0, pile size 20 → index 19
        index = pile - 1

        # Pick a random move from this pile size's bucket.
        # Moves that have been reinforced by past wins appear more often
        # in the bucket, so they're more likely to be selected.
        self.moves[index] = random.choice(self.buckets[index])
        return self.moves[index]

    def game(self, result: int):
        """Handles game start and end signals.

        On game start (result == 0): clears the move history for the new game.
        On win (result == 1): reinforces winning moves by adding them back
            into their buckets, then saves to disk.
        On loss (result == -1): does nothing — losing moves are not reinforced,
            so they gradually become less likely as winning moves accumulate.
        """
        if result == 0:
            # New game starting — clear the move record
            self.moves = [0] * MAX_PILE
        elif result == 1:
            # We won! Reinforce every move we made by inserting it back into
            # the appropriate bucket (in sorted position to keep buckets tidy).
            for i in range(MAX_PILE):
                if self.moves[i] > 0:
                    bisect.insort(self.buckets[i], self.moves[i])
            self._save()
        # result == -1 means we lost — we intentionally do nothing,
        # which lets winning moves dominate over time.

    def _load(self):
        """Loads learned move distributions from the moves file.

        Each line in the file represents one bucket: comma-separated integers.
        If the file doesn't exist, initializes all buckets with [1, 2, 3]
        (uniform probability).
        """
        try:
            with open(MOVES_FILE) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue  # skip blank lines
                    bucket = [int(x) for x in line.split(",")]
                    self.buckets.append(bucket)
        except FileNotFoundError:
            # No saved data — start fresh with uniform distributions
            print("No moves.txt found — starting with fresh buckets.")
            self.buckets = [[1, 2, 3] for _ in range(MAX_PILE)]

        # Safety check: if the file existed but was empty or incomplete,
        # fill in any missing buckets with defaults
        while len(self.buckets) < MAX_PILE:
            self.buckets.append([1, 2, 3])

    def _save(self):
        """Saves the current move distributions to disk so learning persists
        across sessions."""
        try:
            with open(MOVES_FILE, "w") as f:
                for bucket in self.buckets:
                    f.write(",".join(str(x) for x in bucket) + "\n")
        except IOError:
            print(f"Warning: could not save moves to {MOVES_FILE}")
