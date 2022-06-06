from engine import Scene
from engine.entities import ClickableEntity

from app.utils import get_ep_string, load_em_image
from app.dialog import Dialog, DialogSide, DialogEmitter

class Mission(Scene):
    def __init__(self, episode_id, mission_id, mission_child_id = "", default_side = DialogSide.TOP):
        self.episode_id = episode_id
        self.mission_id = mission_id
        self.emitter = DialogEmitter(self, default_side)
        self.background = ClickableEntity(self, hit_rect = True)
        if mission_child_id:
            name = "Episode {} - Mission {} - {}".format(episode_id, mission_id, mission_child_id)
        else:
            name = "Episode {} - Mission {}".format(episode_id, mission_id)
        super().__init__(name)

    def get_string(self, character_id, text_id):
        return get_ep_string(self.episode_id, self.mission_id, character_id, text_id)

    def get_image(self, image_name):
        return load_em_image(self.episode_id, self.mission_id, image_name)

    def update(self, game, events):
        if self.background:
            self.background.update(game, events)
        super().update(game, events)
        self.emitter.update(game, events)

    def draw(self, layer):
        if self.background:
            self.background.draw(layer)
        super().draw(layer)
        self.emitter.draw(layer)
