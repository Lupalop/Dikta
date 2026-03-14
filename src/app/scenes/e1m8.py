from app import utils
from app.entities import Image
from app.mission import Mission

class E1M8Scene(Mission):
    def __init__(self):
        super().__init__(1, 8)

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        bg_main = Image(
            self, utils.load_em_image(1, 1, "bg-main"))

        self.entities = {
            "bg_main": bg_main,
        }
