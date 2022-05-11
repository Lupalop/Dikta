from engine import *

import pygame

class GameManager():
    def __init__(self):
        print("Initialized: Game Manager")
        self.viewport_size = (800, 600)
        self.window = pygame.display.set_mode(self.viewport_size)
        self.scenes = SceneManager()
        self.fps_limit = 60
        self._clock = pygame.time.Clock()
        self._title = ""
        self._icon = None

    def run(self):
        self.running = True
        # Main game loop
        while self.running:
            # Consume the quit event first.
            for event in pygame.event.get(pygame.QUIT):
                self.running = False
            # Consume all the remaining events and store them in a variable
            # for use by the current scene.
            events = pygame.event.get()

            self.scenes.update(events)
            self.scenes.draw(self.window)

            pygame.display.update()

            self._clock.tick(self.fps_limit)

        pygame.quit()

    def get_window_title(self):
        return self._title

    def set_window_title(self, title):
        self._title = title
        pygame.display.set_caption(title)

    def set_window_icon(self, icon):
        self._icon = icon
        pygame.display.set_icon(icon)
