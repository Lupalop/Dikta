from engine import *
from app.scenes import *

game.scenes.add_overlay("dbg_coords", CoordinatesDebugOverlay())
game.scenes.set_scene(MainMenuScene())
game.set_window_title("Dikta")
game.run()
