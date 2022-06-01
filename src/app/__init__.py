from engine import game
from app.scenes import *

game.scenes.add_overlay("debug", DebugOverlay())
game.scenes.all_scenes["main_menu"] = MainMenuScene()

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
