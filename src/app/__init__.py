from engine import game
from app.scenes import scene_list

game.scenes.all_scenes = game.scenes.all_scenes | scene_list
game.scenes.add_overlay("debug", scene_list["debug"])

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
