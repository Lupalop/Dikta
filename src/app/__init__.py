from engine import *
from app.scenes import *

game.scenes.add_overlay("dbg_coords", CoordinatesDebugOverlay())
game.scenes.all_scenes["main_menu"] = MainMenuScene()

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
