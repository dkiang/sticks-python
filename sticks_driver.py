"""Driver for the Sticks game.

Creates player instances and runs the game loop. Players take turns taking
1, 2, or 3 sticks from a pile. The player who takes the last stick loses.

Based on The Game of Sticks:
http://nifty.stanford.edu/2014/laaksonen-vihavainen-game-of-sticks/
"""

import random

from simple_sticks import SimpleSticks
from human_sticks import HumanSticks
from kiang_sticks import KiangSticks


def make_player_pools() -> tuple[list[SimpleSticks], list[SimpleSticks]]:
    """Create two independent pools of players (so two instances of the same
    class don't share state)."""
    pool1 = [HumanSticks(), SimpleSticks(), KiangSticks()]
    pool2 = [HumanSticks(), SimpleSticks(), KiangSticks()]
    return pool1, pool2


def get_int(prompt: str) -> int:
    """Prompt the user for an integer, retrying on invalid input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def select_player(pool: list[SimpleSticks], label: str) -> SimpleSticks:
    """Display the player menu and return the selected player."""
    print(f"\nPlease select {label}:")
    for i, player in enumerate(pool):
        print(f"  {i}. {player}")
    return pool[get_int("Choice: ")]


def main():
    pool1, pool2 = make_player_pools()

    # --- Setup ---
    init_pile = get_int("Pick a pile size (0 = Random): ")

    random_pile = init_pile == 0
    random_max = 0
    if random_pile:
        random_max = get_int("Random pile size range: 3 to ___? ")

    player1 = select_player(pool1, "first player (player 1 goes first)")
    player2 = select_player(pool2, "second player")

    num_games = get_int("How many games? ")

    show_text = input("Show game text? true/false: ").strip().lower() in (
        "t", "true", "1", "yes",
    )

    # Handle duplicate names
    p1_name = str(player1)
    p2_name = str(player2)
    if p1_name == p2_name:
        p1_name = f"Good {p1_name}"
        p2_name = f"Evil {p2_name}"

    # --- Stats ---
    p1_wins = p2_wins = 0
    p1_forfeit = p2_forfeit = 0

    # --- Main Game Loop ---
    for game_num in range(1, num_games + 1):
        pile = init_pile if not random_pile else random.randint(3, random_max)
        player1_turn = True
        print(f"\nGame No. {game_num} ({pile} Sticks)")

        player1.game(0)  # Signal game start
        player2.game(0)

        error = False
        while pile > 0:
            if show_text:
                print(f"Pile size = {pile}")

            if player1_turn:
                next_play = player1.play(pile)
                if show_text:
                    print(f"{p1_name} took {next_play} sticks.")
            else:
                next_play = player2.play(pile)
                if show_text:
                    print(f"{p2_name} took {next_play} sticks.")

            # Check for illegal moves
            if next_play > pile:
                pile = 0
                error = True
                if player1_turn:
                    print(f"{p1_name} made an illegal play.")
                    print(f"{p2_name} wins!")
                    p2_wins += 1
                    p1_forfeit += 1
                else:
                    print(f"{p2_name} made an illegal play.")
                    print(f"{p1_name} wins!")
                    p1_wins += 1
                    p2_forfeit += 1

            pile -= next_play
            player1_turn = not player1_turn

        # End of game — determine winner
        if not player1_turn:
            # player1 made the last move and took the last stick → loses
            print(f"{p2_name} wins!")
            p2_wins += 1
            player2.game(1)
        else:
            print(f"{p1_name} wins!")
            p1_wins += 1
            player1.game(1)

    # --- Final Stats ---
    print(f"\nPile size:{init_pile} Games:{num_games}")
    print(f"{p1_name} won {p1_wins} times (went first)")
    if p1_forfeit:
        print(f"{p1_name} forfeited {p1_forfeit} game(s).")
    if p2_forfeit:
        print(f"{p2_name} forfeited {p2_forfeit} game(s).")


if __name__ == "__main__":
    main()
