import pygame
from . import scene_manager

class Game():
    def __init__(self):
        self.viewport_bounds = (800, 600)
        self.window = pygame.display.set_mode(self.viewport_bounds)
        self.scenes = scene_manager.SceneManager(self.window)
        self.fps_limit = 60
        self.clock = pygame.time.Clock()

    def run(self):
        pygame.font.init()
        pygame.display.set_caption("DIKTA")
        # MAIN_LOGO = content.load_asset('mainBG.png')
        # pygame.display.set_icon(MAIN_LOGO)

        self.running = True

        while self.running:
            self.clock.tick(self.fps_limit)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.scenes.update()
            self.scenes.draw()
            pygame.display.update()

        pygame.quit()
