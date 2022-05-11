class SceneManager:
    def __init__(self, window):
        print("Initialized: Scene Manager")
        self._window = window
        self._scene = None

    def get_scene(self):
        return self._scene

    def set_scene(self, scene):
        if self._scene:
            self._scene.dispose()

        self._scene = scene
        scene.load_content()

    def update(self):
        if not self._scene or not self._scene.enabled:
            return

        self._scene.update()

    def draw(self):
        if not self._scene:
            return

        self._scene.draw(self._window)
