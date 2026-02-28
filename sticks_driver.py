"""Driver for the Sticks game.

RULES: Players take turns removing 1, 2, or 3 sticks from a pile.
The player who is forced to take the LAST stick loses.

This driver handles:
  - Setup: pile size, player selection, number of games
  - Running the game loop for each game
  - Tracking and displaying win/loss statistics

STUDENTS: To add your own player:
  1. Create a class that extends SimpleSticks
  2. Override play(pile) with your strategy
  3. Override __str__() with your player's name
  4. Optionally override game(result) to learn from wins/losses
  5. Register your player in the build_player_menu() function below

Based on The Game of Sticks:
http://nifty.stanford.edu/2014/laaksonen-vihavainen-game-of-sticks/
"""

import random

from simple_sticks import SimpleSticks
from human_sticks import HumanSticks
from kiang_sticks import KiangSticks


# =============================================================================
#  PLAYER REGISTRATION
# =============================================================================

def build_player_menu() -> list[SimpleSticks]:
    """Builds the list of available player types.

    STUDENTS: Add your player class here to make it selectable in the menu.
    Each call creates fresh instances so two players of the same type
    don't accidentally share state.

    Returns:
        A list of player instances to choose from.
    """
    return [
        HumanSticks(),
        SimpleSticks(),
        KiangSticks(),
        # Add new players here, e.g.:
        # YourSticks(),
    ]


# =============================================================================
#  INPUT HELPERS
# =============================================================================

def get_int(prompt: str) -> int:
    """Prompts the user for an integer, repeating until valid input is given."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_int_in_range(prompt: str, low: int, high: int) -> int:
    """Prompts the user for an integer within a specific range.

    Args:
        prompt: the message to display.
        low: minimum acceptable value (inclusive).
        high: maximum acceptable value (inclusive).

    Returns:
        A valid integer in [low, high].
    """
    while True:
        value = get_int(prompt)
        if low <= value <= high:
            return value
        print(f"Please enter a number between {low} and {high}.")


def get_yes_no(prompt: str) -> bool:
    """Prompts the user for a yes/no answer.

    Returns:
        True if the user answered yes/true, False otherwise.
    """
    response = input(prompt).strip().lower()
    return response in ("t", "true", "y", "yes", "1")


def select_player(pool: list[SimpleSticks], label: str) -> SimpleSticks:
    """Displays a numbered menu of players and returns the user's choice.

    Args:
        pool: the list of available players.
        label: description of which player is being selected.

    Returns:
        The selected player instance.
    """
    print(f"\nSelect {label}:")
    for i, player in enumerate(pool):
        print(f"  {i}. {player}")
    choice = get_int_in_range("Choice: ", 0, len(pool) - 1)
    return pool[choice]


# =============================================================================
#  GAME LOGIC
# =============================================================================

def play_one_game(player1: SimpleSticks, player2: SimpleSticks,
                  p1_name: str, p2_name: str,
                  pile: int, show_text: bool) -> int:
    """Plays a single game of Sticks between two players.

    The game alternates turns, starting with player 1. Each player calls
    play(pile) to decide how many sticks to take. The player who takes
    the last stick loses.

    Args:
        player1: the first player (goes first).
        player2: the second player.
        p1_name: display name for player 1.
        p2_name: display name for player 2.
        pile: the starting number of sticks.
        show_text: whether to print each move as it happens.

    Returns:
        Positive for normal win, negative for forfeit win:
         1 = player 1 wins,  2 = player 2 wins (normal)
        -1 = player 1 wins, -2 = player 2 wins (opponent forfeited)
    """
    # Signal both players that a new game is starting
    player1.game(0)
    player2.game(0)

    player1_turn = True

    while pile > 0:
        if show_text:
            print(f"  Pile: {pile}")

        # Current player makes their move
        current_name = p1_name if player1_turn else p2_name
        current_player = player1 if player1_turn else player2
        taken = current_player.play(pile)

        if show_text:
            print(f"  {current_name} took {taken} sticks.")

        # --- Validate the move ---
        # A legal move takes 1-3 sticks and doesn't exceed the pile.
        if taken < 1 or taken > 3 or taken > pile:
            # Illegal move → forfeit. The OTHER player wins.
            print(f"  {current_name} made an illegal play "
                  f"({taken} from pile of {pile}). Forfeit!")

            # Signal both players: winner gets 1, loser gets -1
            if player1_turn:
                player2.game(1)
                player1.game(-1)
                return -2  # player 2 wins by forfeit
            else:
                player1.game(1)
                player2.game(-1)
                return -1  # player 1 wins by forfeit

        # Legal move — remove sticks from the pile
        pile -= taken

        # Did the current player just take the last stick? If so, they LOSE.
        if pile == 0:
            winner_name = p2_name if player1_turn else p1_name
            print(f"  {winner_name} wins!")

            # Signal both players
            if player1_turn:
                # Player 1 took the last stick → player 1 loses, player 2 wins
                player2.game(1)
                player1.game(-1)
                return 2
            else:
                # Player 2 took the last stick → player 2 loses, player 1 wins
                player1.game(1)
                player2.game(-1)
                return 1

        # Switch turns
        player1_turn = not player1_turn

    # This should never be reached because the game always ends when
    # pile hits 0, but just in case:
    return 0


# =============================================================================
#  MAIN
# =============================================================================

def main():
    # --- Build two separate player pools ---
    # We need two pools so that if the user picks the same player type for
    # both slots (e.g., KiangSticks vs KiangSticks), they are separate
    # instances with independent state.
    pool1 = build_player_menu()
    pool2 = build_player_menu()

    # --- Setup: pile size ---
    init_pile = get_int("Pick a pile size (0 = Random): ")
    random_pile = (init_pile == 0)
    random_max = 0

    if random_pile:
        random_max = get_int_in_range("Random pile size range: 3 to ___? ", 4, 1000)

    # --- Setup: player selection ---
    player1 = select_player(pool1, "Player 1 (goes first)")
    player2 = select_player(pool2, "Player 2")

    # --- Setup: game options ---
    num_games = get_int_in_range("How many games? ", 1, 100000)
    show_text = get_yes_no("Show game text? (yes/no): ")

    # --- Handle duplicate names ---
    # If the same player type is chosen for both, distinguish them
    p1_name = str(player1)
    p2_name = str(player2)
    if p1_name == p2_name:
        p1_name = f"Good {p1_name}"
        p2_name = f"Evil {p2_name}"

    # --- Stats tracking ---
    p1_wins = 0
    p2_wins = 0
    p1_forfeit = 0
    p2_forfeit = 0

    # =================================================================
    #  MAIN GAME LOOP
    # =================================================================

    for game_num in range(1, num_games + 1):
        # Determine pile size for this game
        if random_pile:
            # Random pile between 3 and random_max (inclusive)
            pile = random.randint(3, random_max)
        else:
            pile = init_pile

        print(f"\n--- Game {game_num} ({pile} sticks) ---")

        # Play the game and record the result
        # Positive = normal win, negative = forfeit win (see play_one_game docs)
        result = play_one_game(player1, player2, p1_name, p2_name, pile, show_text)

        if result == 1:
            p1_wins += 1                     # P1 wins normally
        elif result == 2:
            p2_wins += 1                     # P2 wins normally
        elif result == -1:
            p1_wins += 1; p2_forfeit += 1    # P1 wins, P2 forfeited
        elif result == -2:
            p2_wins += 1; p1_forfeit += 1    # P2 wins, P1 forfeited

    # =================================================================
    #  FINAL RESULTS
    # =================================================================

    print("\n========================================")
    print("  RESULTS")
    print("========================================")

    # Show pile size info
    if random_pile:
        print(f"  Pile size: Random (3-{random_max})")
    else:
        print(f"  Pile size: {init_pile}")
    print(f"  Games played: {num_games}")
    print()

    # Results table
    print(f"  {'Player':<20s} {'Wins':>6s} {'Win %':>8s}")
    print(f"  {'------':<20s} {'----':>6s} {'-----':>8s}")
    print(f"  {p1_name + ' (P1)':<20s} {p1_wins:>6d} {100.0 * p1_wins / num_games:>7.1f}%")
    print(f"  {p2_name + ' (P2)':<20s} {p2_wins:>6d} {100.0 * p2_wins / num_games:>7.1f}%")

    # Forfeit info (only if applicable)
    if p1_forfeit:
        print(f"\n  {p1_name} forfeited {p1_forfeit} game(s).")
    if p2_forfeit:
        print(f"  {p2_name} forfeited {p2_forfeit} game(s).")

    print("========================================")


if __name__ == "__main__":
    main()
