from engine import Scene, game

class Overlay(Scene):
    def __init__(self, name):
        super().__init__(name)
        self.visible = False

    def set_visibility(self, is_visible):
        self.visible = is_visible
        
    def draw(self, layer):
        if self.visible:
            super().draw(layer)

    def update(self, game, events):
        if self.visible:
            super().update(game, events)

    def toggle_visibility(self):
        self.set_visibility(not self.visible)
        current_scene = game.scenes.get_scene()
        if current_scene:
            current_scene.enabled = (not self.visible)
