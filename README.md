# Sticks (Python)

A Python port of the [Sticks](https://github.com/dkiang/Sticks) game.

Simulates the game of Sticks in which players take turns taking 1, 2, or 3 sticks. The player taking the last stick loses. `KiangSticks` uses a machine learning model to store moves in a text file every time it wins. `sticks_driver.py` runs the game with a menu-driven front-end that allows a Human player to play against KiangSticks, an AI player.

Initially, KiangSticks is equally likely to choose 1, 2, or 3 sticks when it is its turn because the distribution of possible numbers is equal. As it wins it keeps track of the winning numbers more frequently, such that it becomes much smarter the more it plays. Play 100 games against two different instances of KiangSticks, and the `moves.txt` file will grow rapidly to the point where it should be quite difficult, or impossible, to beat.

This uses the model written about in The Game of Sticks activity at <http://nifty.stanford.edu/2014/laaksonen-vihavainen-game-of-sticks/>.

## Running

```bash
python sticks_driver.py
```

Requires Python 3.10+.

## Files

| File | Description |
|------|-------------|
| `simple_sticks.py` | Base player class — picks randomly |
| `human_sticks.py` | Human player — reads moves from stdin |
| `kiang_sticks.py` | ML player — learns from wins |
| `sticks_driver.py` | Main game loop and menu |
| `moves.txt` | Learned move distributions (updated as KiangSticks wins) |
