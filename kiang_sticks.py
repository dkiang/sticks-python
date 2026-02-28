"""Machine learning Sticks player that improves by recording winning moves.

Uses the model from The Game of Sticks activity:
http://nifty.stanford.edu/2014/laaksonen-vihavainen-game-of-sticks/
"""

import bisect
import random
from pathlib import Path

from simple_sticks import SimpleSticks

MOVES_FILE = Path("moves.txt")
MAX_BUCKETS = 20


class KiangSticks(SimpleSticks):
    """An AI player that learns from its wins by reinforcing successful move choices.

    Each pile size (1-20) has a 'bucket' of possible moves. When KiangSticks
    wins, the moves it made are added back into the buckets, making those
    choices more likely in the future.
    """

    def __init__(self):
        self.buckets: list[list[int]] = []
        self.moves: list[int] = [0] * MAX_BUCKETS
        self._load()

    def __str__(self):
        return "Mr. Kiang"

    def play(self, pile: int) -> int:
        """Choose a move by sampling from the learned distribution for this pile size."""
        if pile > MAX_BUCKETS:
            return 3
        if pile == 1:
            return 1

        index = pile - 1
        bucket = self.buckets[index]
        self.moves[index] = random.choice(bucket)
        return self.moves[index]

    def game(self, result: int):
        """Handle game start/end. On a win, reinforce the moves that were played."""
        if result == 0:
            self.moves = [0] * MAX_BUCKETS
        elif result == 1:
            for i in range(MAX_BUCKETS):
                if self.moves[i] > 0:
                    bisect.insort(self.buckets[i], self.moves[i])
            self._save()

    def _load(self):
        """Load learned move distributions from the moves file."""
        try:
            with open(MOVES_FILE) as f:
                for line in f:
                    bucket = [int(x) for x in line.strip().split(",")]
                    self.buckets.append(bucket)
            print(self.buckets)
        except FileNotFoundError:
            # Initialize with uniform distribution if no file exists
            self.buckets = [[1, 2, 3] for _ in range(MAX_BUCKETS)]

    def _save(self):
        """Save current move distributions to the moves file."""
        with open(MOVES_FILE, "w") as f:
            for bucket in self.buckets:
                f.write(",".join(str(x) for x in bucket) + "\n")
