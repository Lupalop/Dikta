from engine import *
from engine.entities import *
from app import utils
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M7Scene(Mission):
    def __init__(self):
        super().__init__(1, 7)

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
