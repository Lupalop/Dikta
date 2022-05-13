from engine import *

import pygame

class GameManager():
    def __init__(self):
        print("Initialized: Game Manager")
        self._init_display()
        self.scenes = SceneManager()
        self.fps_limit = 60
        self._clock = pygame.time.Clock()
        self._title = ""
        self._icon = None

    def run(self):
        self.running = True
        # Main game loop
        while self.running:
            # Consume all events and store them for later use.
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self._mouse_pos = event.pos
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    self.window_size = event.size
                    self.update_display(True, False)

            self.scenes.update(self, events)

            self.render_layer.fill(pygame.Color("black"))
            self.scenes.draw(self.render_layer)
            self.scaler(self.render_layer,
                        self.window.get_rect().size,
                        self.window)
            pygame.display.update()

            self._clock.tick(self.fps_limit)

        pygame.quit()

    def _init_display(self):
        # TODO: This should be configurable via preferences (pending impl)
        self.window_size = (1024, 768)
        self.layer_size = (800, 600)
        self.is_fullscreen = False
        self.is_resizable = False
        self.is_dpi_aware = True
        self.is_scale_smooth = True
        # Prevent automatic scaling
        if self.is_dpi_aware:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        # Update display mode and render layer surface
        self.update_display(True, True)

    def update_display(self, is_window, is_layer):
        if is_window:
            # Determine flags to be used in current display mode
            flags = pygame.SHOWN
            if self.is_fullscreen:
                flags |= pygame.FULLSCREEN
            if self.is_resizable:
                flags |= pygame.RESIZABLE

            self.window = pygame.display.set_mode(self.window_size, flags)
            ratio_x = self.window_size[0] / self.layer_size[0]
            ratio_y = self.window_size[1] / self.layer_size[1]
            self.ratio = (ratio_x, ratio_y)
        if is_layer:
            self.render_layer = pygame.Surface(self.layer_size)
        if self.is_scale_smooth:
            self.scaler = pygame.transform.smoothscale
        else:
            self.scaler = pygame.transform.scale

    def get_window_title(self):
        return self._title

    def set_window_title(self, title):
        self._title = title
        pygame.display.set_caption(title)

    def get_window_icon(self):
        return self._icon

    def set_window_icon(self, icon):
        self._icon = icon
        pygame.display.set_icon(icon)

    # The following functions belong to an InputManager class
    def get_scaled_pos(self, position):
        if self.ratio[0] == 1 and self.ratio[1] == 1:
            return position
        return (position[0] / self.ratio[0], position[1] / self.ratio[1])

    def get_mouse_pos(self):
        return self.get_scaled_pos(self._mouse_pos)
