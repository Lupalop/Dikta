from engine import game
from app import utils, scene_list
from app.scenes import *

import pygame

pygame.display.set_icon(utils.load_ui_image("icon"))

utils.set_cursor("default")

if not game.scenes.all:
	game.scenes.all = scene_list.all
else:
	game.scenes.all = game.scenes.all.update(scene_list.all)

game.scenes.add_overlay("debug")
game.scenes.add_overlay("mouse", True)
game.scenes.add_overlay("ig_escmenu")
game.scenes.add_overlay("ig_clues")
game.scenes.add_overlay("ig_options")

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
game.run()
