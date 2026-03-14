from engine import game
from app import scene_list
from app.entities import Image
from app.mission import Mission

class E2M1(Mission):
    def __init__(self):
        super().__init__(2, 1, "", "")
        self.fade_timer = None

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def _to_credits(self):
        game.scenes.set_scene("credits")

    def load_content(self):
        super().load_content()
        intro1 = Image(
            self, self.get_image("bg"))
        intro1_surface = intro1.get_surface()
        if intro1_surface:
            intro1_surface.set_alpha(0)

        def fadeout_intro1():
            self.fade_timer = self.animator.fadeout(
                intro1,
                750,
                self._to_credits,
            )

        def fadein_intro1():
            self.fade_timer = self.animator.fadein(
                intro1,
                750,
                fadeout_intro1,
                2000
            )

        fadein_intro1()

        self.entities = {
            "intro1": intro1,
        }

scene_list.add_mission(E2M1())
