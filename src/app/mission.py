from engine import Scene, ClickableEntity, prefs

from app.utils import get_ep_string, load_em_image, get_inventory_key
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

    def get_items(self):
        return prefs.savedgame.get(get_inventory_key(self.episode_id), {})

    def add_item(name_id, image_id):
        items = self.get_items()
        if name_id in items:
            print("item already in inventory")
            return False
        items[name_id] = {
            "name": name_id,
            "image": image_id
        }
        prefs.savedgame.set(get_inventory_key(self.episode_id), items)
        return True

    def remove_item(name_id):
        items = self.get_items()
        if not name_id in items:
            print("item not in inventory")
            return False
        items.pop(name_id)
        prefs.savedgame.set(get_inventory_key(self.episode_id), items)
        return True

    def get_clues(self):
        return prefs.savedgame.get(get_clues_key(self.episode_id), [])

    def add_clue(clue_id):
        clues = self.get_clues()
        if clue_id in clues:
            print("clue already found")
            return False
        clues.append(clue_id)
        prefs.savedgame.set(get_clues_key(self.episode_id), clues)
        return True

    def update(self, game, events):
        # Only timers can update if a dialog is currently on-screen.
        if not self.emitter.current:
            if self.background:
                self.background.update(game, events)
            super().update(game, events)
        else:
            self.timers.update(game, events)
            self._call_captured()
        self.emitter.update(game, events)

    def draw(self, layer):
        if self.background:
            self.background.draw(layer)
        super().draw(layer)
        self.emitter.draw(layer)
