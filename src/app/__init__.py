from engine import game
from app import utils, scene_list
from app.scenes import *

utils.set_cursor("default")
game.scenes.all = game.scenes.all | scene_list.all
game.scenes.add_overlay("debug")
game.scenes.add_overlay("mouse", True)
game.scenes.add_overlay("ig_escmenu")

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
