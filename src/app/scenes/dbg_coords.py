from engine import *
from engine.entities import *

import pygame

class CoordinatesDebugOverlay(Scene):
    def __init__(self):
        super().__init__("DBGO - Coordinates")

    def update(self, game, events):
        super().update(game, events)

        scaled_pos = str(game.get_mouse_pos())
        self.entities["xy"].set_text(scaled_pos)

    def load_content(self):
        counter_font = content.load_font("arial", 12)
        xy_counter = Label("0, 0", counter_font, pygame.Color("white"), (0, 0))

        self.entities = {
            "xy": xy_counter
        }
