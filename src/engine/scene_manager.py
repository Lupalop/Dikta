from engine.timer import Timer

import pygame

class SceneManager:
    def __init__(self):
        print("Initialized: Scene Manager")
        self.all_scenes = {}
        self._scene = None
        self._overlays = {}
        self.fade_surface = pygame.Surface((1360, 765)) # FIXME: Resolution should not be hardcoded
        self.fade_surface.fill(pygame.Color("black"))
        self.fade_surface.set_alpha(255)

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        pending_scene = scene

        if isinstance(scene, str):
            if pending_scene in self.all_scenes:
                pending_scene = self.all_scenes[scene]
            else:
                return

        # TODO: Should be in a utility/animation/transition module
        def _fade_to_target(target_alpha):
            alpha = self.fade_surface.get_alpha()
            time_ratio = self.fade_timer.get_elapsed() / self.fade_timer.interval
            alpha += ((target_alpha - alpha) * time_ratio)
            self.fade_surface.set_alpha(alpha)

        def _fade_in_done():
            pending_scene.load_content()
            self._scene = pending_scene

            self.fade_timer = Timer(1000)
            self.fade_timer.tick += lambda: _fade_to_target(0)
            self.fade_timer.start()

        if self._scene:
            self._scene.dispose()

            self.fade_timer = Timer(1000)
            self.fade_timer.tick += lambda: _fade_to_target(255)
            self.fade_timer.elapsed += _fade_in_done
            self.fade_timer.start()
        else:
            _fade_in_done()

    def add_overlay(self, id, scene):
        scene.load_content()
        self._overlays[id] = scene

    def remove_overlay(self, id):
        return self._overlays.pop(id, None)

    def get_overlay(self, id):
        return self._overlays.get(id, None)

    def update(self, game, events):
        if self._scene and self._scene.enabled:
            self._scene.update(game, events)

        for overlay in self._overlays.values():
            if not overlay.enabled:
                continue
            overlay.update(game, events)

    def draw(self, layer):
        if self._scene:
            self._scene.draw(layer)

        for overlay in self._overlays.values():
            overlay.draw(layer)

        layer.blit(self.fade_surface, (0, 0))
