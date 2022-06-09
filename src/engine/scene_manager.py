from engine import animator, prefs

import pygame

class SceneManager:
    def __init__(self):
        print("Initialized: Scene Manager")
        self.all = {}
        self._scene = None
        self._switching = False
        self._overlays = []
        self.fade_surface = pygame.Surface(prefs.default.get("app.display.layer_size", (0, 0)))
        self.fade_surface.fill(pygame.Color("black"))
        self.fade_surface.set_alpha(255)
        self.fade_duration = prefs.default.get("app.misc.fade_duration", 1000)

    def _toggle_switching(self):
        self._switching = not self._switching

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        if self._switching:
            print("Cannot switch to another scene while a scene switch is in progress.")
            return

        pending_scene = scene

        if isinstance(scene, str):
            if pending_scene in self.all:
                pending_scene = self.all[scene]
            else:
                return

        self._toggle_switching()

        def _fade_in_done():
            if self._scene:
                self._scene.dispose()
            pending_scene.load_content()

            self._scene = pending_scene
            animator.default.fadeout(
                self.fade_surface,
                self.fade_duration,
                self._toggle_switching
            )

        if self._scene:
            animator.default.fadein(
                self.fade_surface,
                self.fade_duration,
                _fade_in_done
            )
        else:
            _fade_in_done()

    def add_overlay(self, scene_id, topmost = False):
        if scene_id not in self.all:
            return False

        overlay = self.all[scene_id]
        if overlay in self._overlays:
            return False
        overlay.load_content()

        if topmost:
            self._overlays.append(overlay)
        else:
            self._overlays.insert(0, overlay)

    def remove_overlay(self, scene_id):
        if scene_id not in self.all:
            return False

        overlay = self.all[scene_id]
        if overlay in self._overlays:
            return self._overlays.remove(overlay)

        return False

    def update(self, game, events):
        if self._scene and \
           self._scene.enabled and not \
           self._switching:
            self._scene.update(game, events)

        for overlay in self._overlays:
            if not overlay.enabled:
                continue
            overlay.update(game, events)

    def draw(self, layer):
        if self._scene:
            self._scene.draw(layer)

        for overlay in self._overlays:
            overlay.draw(layer)

        layer.blit(self.fade_surface, (0, 0))
