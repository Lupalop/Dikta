from engine import *
from app import utils, scene_list
from app.entities import *

import pygame

class GameOverScene(Scene):
    def __init__(self):
        super().__init__("Game Over")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def _to_main_menu(self, sender, button):
        game.scenes.set_scene("main_menu")

    def load_content(self):
        background = Image(
            self,
            utils.load_ui_image("fsc-static-gameover"),
            (0, 0))

        btn_exit = FadeButton(self, utils.load_mm_image("btn-exit"), (1280, 280))
        btn_exit.click += self._to_main_menu

        self.entities = {
            "background": background,
            "btn_exit": btn_exit,
        }

scene_list.all["game_over"] = GameOverScene()
