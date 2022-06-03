from engine import game
from app.scenes import *

game.scenes.add_overlay("debug", DebugOverlay())
game.scenes.all_scenes["main_menu"] = MainMenuScene()
game.scenes.all_scenes["test"] = E0MTestScene()
game.scenes.all_scenes["e1m0"] = E1M0Scene()
game.scenes.all_scenes["e1m1"] = E1M1Scene()
game.scenes.all_scenes["e1m2"] = E1M2Scene()
game.scenes.all_scenes["e1m3"] = E1M3Scene()
game.scenes.all_scenes["e1m4"] = E1M4Scene()
game.scenes.all_scenes["e1m5"] = E1M5Scene()
game.scenes.all_scenes["e1m6"] = E1M6Scene()
game.scenes.all_scenes["e1m7"] = E1M7Scene()
game.scenes.all_scenes["e1m8"] = E1M8Scene()
game.scenes.all_scenes["e1m9"] = E1M9Scene()

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
