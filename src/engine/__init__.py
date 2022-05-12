from . import entities

from .scene import Scene

from .content_manager import ContentManager
from .scene_manager import SceneManager
from .game_manager import GameManager

content = ContentManager()
game = GameManager()

# TODO: Move these constants to their own module (e.g., utils.py)
MB_LEFT = 1
MB_MID = 2
MB_RIGHT = 3
