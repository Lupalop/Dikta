from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E2M1(Mission):
    def __init__(self):
        super().__init__(2, 1, "", "")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def _to_main_menu(self):
        game.scenes.set_scene("main_menu")

    def load_content(self):
        super().load_content()
        intro1 = Image(
            self, self.get_image("bg"))
        intro1.get_surface().set_alpha(0)

        def fadeout_intro1():
            self.fade_timer = self.animator.fadeout(
                intro1,
                750,
                self._to_main_menu,
            )

        def fadein_intro1():
            self.fade_timer = self.animator.fadein(
                intro1,
                750,
                fadeout_intro1,
                2000
            )

        fadein_intro1()

        self.entities = {
            "intro1": intro1,
        }

scene_list.add_mission(E2M1())
