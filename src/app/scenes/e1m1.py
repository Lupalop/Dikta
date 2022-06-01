from engine import *
from engine.entities import *
from app import utils

import pygame

class E1M1Scene(Scene):
    def __init__(self):
        super().__init__("E1M1")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        bg_main = Image(
            utils.load_em_image(1, 1, "bg-main"))

        self.entities = {
            "bg_main": bg_main,
        }
