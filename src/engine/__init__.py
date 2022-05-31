from . import entities
from . import content

from .scene import Scene
from .timer import Timer
from .timer import timers

from .scene_manager import SceneManager
from .game_manager import GameManager

game = GameManager()

# TODO: Move these constants to their own module (e.g., utils.py)
MB_LEFT = 1
MB_MID = 2
MB_RIGHT = 3
