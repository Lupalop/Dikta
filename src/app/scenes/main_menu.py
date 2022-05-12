from engine import *
from engine.entities import *

import pygame

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("Main Menu")

    def update(self, events):
        super().update(events)

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                print('x pressed')

    def draw(self, window):
        super().draw(window)

    def load_content(self):
        background = Image(
            content.load_asset('mainBG.png'), (0, 0))
        logo = Image(
            content.load_asset('logoName.png'), (70, 80), (300, 80))
        menu_font = content.load_font('ocraextended', 20)
        landing_ng_text = Label(
            "PRESS X FOR NEW GAME", menu_font,
            pygame.Color("white"), (500, 110))
        
        self.entities = {
            "bg": background,
            "logo": logo,
            "landing_ng_text": landing_ng_text
        }
