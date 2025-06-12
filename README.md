# Flappy Bird

A simple Flappy Bird clone written in Python using Pygame.
The bird sprite and Mario-style pipes are drawn with higher quality graphics.

## Requirements
- Python 3.12 or later
- `pygame` library
- `sounddevice` and `numpy` libraries

Install dependencies with:

```bash
pip install pygame sounddevice numpy
```

## Running the Game

```bash
python3 flappy.py
```

Press **space** on the start screen to begin the game. Tap **space** while playing to flap the bird upward and fly through the Mario-like pipes. Passing a set of pipes awards one point. Colliding with a pipe or the ground ends the round and shows a game over screen where pressing **space** will start a new round. Simple beep sound effects for flapping and collisions are generated using the `sounddevice` module.
