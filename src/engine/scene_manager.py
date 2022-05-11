class SceneManager:
    def __init__(self):
        print("Initialized: Scene Manager")
        self._scene = None

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        if self._scene:
            self._scene.dispose()

        self._scene = scene
        scene.load_content()

    def update(self, events):
        if not self._scene or not self._scene.enabled:
            return

        self._scene.update(events)

    def draw(self, window):
        if not self._scene:
            return

        self._scene.draw(window)
