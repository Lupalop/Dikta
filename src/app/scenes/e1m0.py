from engine import *
from engine.entities import *
from app import utils
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M0Scene(Mission):
    def __init__(self):
        super().__init__(1, 0)

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

        animator.entity_fadein(
            intro1,
            1000,
            lambda: animator.entity_fadeout(
                intro1,
                1000,
                lambda: animator.entity_fadein(
                    intro2,
                    1000,
                    lambda: animator.entity_fadeout(
                        intro2,
                        1000,
                        lambda: game.scenes.set_scene("e1m1")
                    ),
                    2000
                )
            ),
            2000
        )

        self.entities = {
            "intro1": intro1,
            "intro2": intro2,
        }
