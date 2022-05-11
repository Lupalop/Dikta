from engine import *
from engine.ui import *
from engine.entities import *

import pygame

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("Main Menu")

    def update(self):
        super().update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print('stage 2')
                if event.key == pygame.K_x:
                    self.state = 'main_game'

    def draw(self, window):
        super().draw(window)

        WHITE = (255, 255, 255)
        START_GAME_FONT = pygame.font.SysFont('bodoniblack', 13)
        LANDING_NEW_GAME_TEXT = START_GAME_FONT.render(
            "PRESS X FOR NEW GAME", 1, WHITE)
        window.blit(LANDING_NEW_GAME_TEXT, (500, 110))

    def load_content(self):
        background = Entity(content.load_asset('mainBG.png'), None, (0, 0))
        
        self.entities = {
            "bg": Entity(content.load_asset('mainBG.png'), None, (0, 0)),
            "logo": Entity(content.load_asset('logoName.png'), (300, 80), (70, 80))
        }

        pass
