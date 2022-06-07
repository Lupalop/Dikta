from engine import game
from app.scenes import scene_list
from app import utils

utils.set_cursor("default")
game.scenes.all = game.scenes.all | scene_list
game.scenes.add_overlay("debug")
game.scenes.add_overlay("mouse", True)

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
