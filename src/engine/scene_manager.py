class SceneManager:
    def __init__(self):
        print("Initialized: Scene Manager")
        self._scene = None
        self._overlays = {}

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        if self._scene:
            self._scene.dispose()

        self._scene = scene
        scene.load_content()

    def add_overlay(self, id, scene):
        scene.load_content()
        self._overlays[id] = scene

    def remove_overlay(self, id):
        return self._overlays.pop(id, None)

    def get_overlay(self, id):
        return self._overlays.get(id, None)

    def update(self, events):
        if self._scene and self._scene.enabled:
            self._scene.update(events)

        for overlay in self._overlays.values():
            if not overlay.enabled:
                continue
            overlay.update(events)

    def draw(self, layer):
        if self._scene:
            self._scene.draw(layer)

        for overlay in self._overlays.values():
            overlay.draw(layer)
