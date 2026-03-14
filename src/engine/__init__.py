from .entity import Entity
from .clickable_entity import ClickableEntity

from . import content

from .enums import MouseButton, ClickState
from .scene import Scene
from .event_handler import EventHandler

from . import timer
from .scene_manager import SceneManager
from . import prefs
from .game_manager import GameManager

game = GameManager()
game.scenes = SceneManager()

game.updateable.add(timer.default)
game.updateable.add(game.scenes)
game.drawable.add(game.scenes)
