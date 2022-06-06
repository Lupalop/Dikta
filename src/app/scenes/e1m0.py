from engine import *
from app import utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M0Scene(Mission):
    def __init__(self):
        super().__init__(1, 0)
        self.fade_timer = None

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        utils.hide_cursor()
        intro1 = Image(
            self, utils.load_em_image(1, 0, "intro-1"))
        intro2 = Image(
            self, utils.load_em_image(1, 0, "intro-2"))
        intro1.get_surface().set_alpha(0)
        intro2.get_surface().set_alpha(0)

        def fadeout_intro2():
            self.fade_timer = self.animator.entity_fadeout(
                intro2,
                1000,
                lambda: game.scenes.set_scene("e1m1")
            )
            utils.reset_cursor()

        def fadein_intro2():
            self.fade_timer = self.animator.entity_fadein(
                intro2,
                1000,
                fadeout_intro2,
                2000
            )

        def fadeout_intro1():
            self.fade_timer = self.animator.entity_fadeout(
                intro1,
                1000,
                fadein_intro2,
            )

        def fadein_intro1():
            self.fade_timer = self.animator.entity_fadein(
                intro1,
                1000,
                fadeout_intro1,
                2000
            )

        fadein_intro1()

        self.entities = {
            "intro1": intro1,
            "intro2": intro2,
        }
