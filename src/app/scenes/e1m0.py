from engine import *
from engine.entities import *
from app import utils

import pygame

class E1M0Scene(Scene):
    def __init__(self):
        super().__init__("E1M0")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        intro1 = Image(
            utils.load_em_image(1, 0, "intro-1"))
        intro2 = Image(
            utils.load_em_image(1, 0, "intro-2"))
        intro1.get_surface().set_alpha(0)
        intro2.get_surface().set_alpha(0)

        def _fade_in_done2():
            self.fade_timer.close()
            self.fade_timer = Timer(2000, True)
            self.fade_timer.elapsed += _fade_out2

        def _fade_in2():
            self.fade_timer.close()
            self.fade_timer = Timer(1000, True)
            self.fade_timer.tick += lambda: animator.entity_to_alpha( \
                intro2, 255, self.fade_timer)
            self.fade_timer.elapsed += _fade_in_done2
        def _fade_out2():
            self.fade_timer.close()
            self.fade_timer = Timer(1000, True)
            self.fade_timer.tick += lambda: animator.entity_to_alpha( \
                intro2, 0, self.fade_timer)
            self.fade_timer.elapsed += lambda: game.scenes.set_scene("e1m1")

        def _fade_in_done1():
            self.fade_timer.close()
            self.fade_timer = Timer(2000, True)
            self.fade_timer.elapsed += _fade_out1

        def _fade_in1():
            self.fade_timer = Timer(1000, True)
            self.fade_timer.tick += lambda: animator.entity_to_alpha( \
                intro1, 255, self.fade_timer)
            self.fade_timer.elapsed += _fade_in_done1

        def _fade_out1():
            self.fade_timer.close()
            self.fade_timer = Timer(1000, True)
            self.fade_timer.tick += lambda: animator.entity_to_alpha( \
               intro1, 0, self.fade_timer)
            self.fade_timer.elapsed += _fade_in2

        _fade_in1()

        self.entities = {
            "intro1": intro1,
            "intro2": intro2,
        }
