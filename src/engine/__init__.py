from . import entities
from . import content

from .enums import *
from .scene import Scene
from .event_handler import EventHandler

from . import timer
from .scene_manager import SceneManager
from .game_manager import GameManager

game = GameManager()
game.scenes = SceneManager()

game.updateable.add(timer.default)
game.updateable.add(game.scenes)
game.drawable.add(game.scenes)
