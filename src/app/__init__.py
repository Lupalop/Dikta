from engine import game
from app.scenes import scene_list
from app import utils

utils.set_cursor("default")
game.scenes.all_scenes = game.scenes.all_scenes | scene_list
game.scenes.add_overlay("debug", scene_list["debug"])
game.scenes.add_overlay("mouse", scene_list["mouse"])

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
