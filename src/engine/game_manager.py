from engine import prefs

import pygame

class GameManager():
    def __init__(self):
        print("Initialized: Game Manager")
        prefs.default.load()
        self._init_display()
        self.fps_limit = 60
        self.clock = None
        self._title = ""
        self._mouse_pos = (0, 0)
        self._icon = None
        self.running = False
        self.updateable = set()
        self.drawable = set()

    def run(self):
        self.running = True
        # We need to initialize this before running the main loop to ensure
        # that PyGame returns the right delta time if requested on startup.
        # This is necessary to prevent sudden skips for timers.
        self.clock = pygame.time.Clock()
        # Main game loop
        while self.running:
            # Consume all events and store them for later use.
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    self._mouse_pos = event.pos
                    break
                elif event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.VIDEORESIZE:
                    self.window_size = event.size
                    self.update_display(True, False)
                    break

            for component in self.updateable:
                component.update(self, events)

            self.render_layer.fill(pygame.Color("black"))
            
            for component in self.drawable:
                component.draw(self.render_layer)
            
            self.scaler(self.render_layer,
                        self.window.get_rect().size,
                        self.window)

            pygame.display.update()
            self.clock.tick(self.fps_limit)

        pygame.quit()
        prefs.default.save()

    def exit(self):
        self.running = False

    def _init_display(self):
        self.window_size = prefs.default.get("app.display.window_size", (1360, 765))
        self.layer_size = prefs.default.get("app.display.layer_size", (1360, 765))
        self.is_fullscreen = prefs.default.get("app.display.fullscreen", False)
        self.is_resizable = prefs.default.get("app.display.resizable", False)
        self.is_dpi_aware = prefs.default.get("app.display.dpi_aware", True)
        self.is_scale_smooth = prefs.default.get("app.display.use_smoothscale", True)
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
