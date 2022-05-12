from engine import *
from engine.entities import *

import pygame

class CoordinatesDebugOverlay(Scene):
    def __init__(self):
        super().__init__("DBGO - Coordinates")

    def update(self, events):
        super().update(events)

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.entities["xy"].set_text(str(event.pos))

    def draw(self, window):
        super().draw(window)

    def load_content(self):
        counter_font = content.load_font('arial', 12)
        xy_counter = Label("0, 0", counter_font, pygame.Color("white"), (0, 0))

        self.entities = {
            "xy": xy_counter
        }
