import importlib
import pkgutil

from engine import game
from app import utils, scene_list
from app import scenes

import pygame

# Dynamically import all modules in app.scenes to register scenes.
for _, module_name, is_pkg in pkgutil.walk_packages(scenes.__path__):
	if not is_pkg:
		importlib.import_module(f".{module_name}", scenes.__package__)

pygame.display.set_icon(utils.load_ui_image("icon"))

utils.set_cursor("default")

if not game.scenes.all:
	game.scenes.all = scene_list.all
else:
	game.scenes.all.update(scene_list.all)

game.scenes.add_overlay("debug")
game.scenes.add_overlay("mouse", True)
game.scenes.add_overlay("ig_escmenu")
game.scenes.add_overlay("ig_clues")
game.scenes.add_overlay("ig_options")

game.scenes.set_scene("main_menu")
game.set_window_title("Dikta")
