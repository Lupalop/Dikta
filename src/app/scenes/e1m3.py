from engine import *
from app import defaults, scene_list
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M3Scene(Mission):
    def __init__(self):
        super().__init__(1, 3, "", "Congress - Outside", DialogSide.TOP)

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("main-bg"))

        self.entities = {
            #"bg_main": bg_main,
        }

scene_list.add_mission(E1M3Scene())
