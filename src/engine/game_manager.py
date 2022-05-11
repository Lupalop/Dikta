from engine import *

import pygame

class GameManager():
    def __init__(self):
        print("Initialized: Game Manager")
        self.viewport_bounds = (800, 600)
        self.window = pygame.display.set_mode(self.viewport_bounds)
        self.scenes = SceneManager(self.window)
        self.fps_limit = 60
        self._clock = pygame.time.Clock()
        self._title = ""
        self._icon = None

    def run(self):
        pygame.font.init()

        self.running = True

        while self.running:
            self._clock.tick(self.fps_limit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.scenes.update()
            self.scenes.draw()

            pygame.display.update()

        pygame.quit()

    def get_window_title(self):
        return self._title

    def set_window_title(self, title):
        self._title = title
        pygame.display.set_caption(title)

    def set_window_icon(self, icon):
        self._icon = icon
        pygame.display.set_icon(icon)
