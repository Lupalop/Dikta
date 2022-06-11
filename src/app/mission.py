from engine import Scene, ClickableEntity, prefs
from engine.enums import MouseButton

from app.utils import get_ep_string, load_em_image, get_inventory_key, reset_cursor
from app.dialog import Dialog, DialogSide, DialogEmitter

import pygame

KEY_SWITCHES = "switches"

class Mission(Scene):
    def __init__(self, episode_id, mission_id, mission_child_id = "", mission_desc = "", default_side = DialogSide.TOP, menu_blocked = False):
        self.episode_id = episode_id
        self.mission_id = mission_id
        self.mission_child_id = mission_child_id
        self.mission_key = "e{}m{}{}".format(episode_id, mission_id, mission_child_id)
        self.dialog_key = "dialog.{}".format(self.mission_key)
        self.menu_blocked = menu_blocked
        self.default_side = default_side
        self.return_scene = None

        if mission_desc:
            name = "Episode {} - Mission {} - {}".format(episode_id, mission_id, mission_desc)
        else:
            name = "Episode {} - Mission {}".format(episode_id, mission_id)
        super().__init__(name)

    def get_string(self, character_id, text_id):
        return get_ep_string(self.episode_id, self.mission_id, character_id, text_id)

    def get_image(self, image_name):
        return load_em_image(self.episode_id, self.mission_id, image_name)

    def get_items(self):
        return prefs.savedgame.get(get_inventory_key(self.episode_id), [])

    def exists_item(self, item_id):
        items = self.get_items()
        return (item_id in items)

    def add_item(self, item_id):
        items = self.get_items()
        if item_id in items:
            print("item already in inventory")
            return False
        items.append(item_id)
        prefs.savedgame.set(get_inventory_key(self.episode_id), items)
        self.emitter.add_popup(item_id)
        return True

    def remove_item(self, item_id):
        items = self.get_items()
        if not item_id in items:
            print("item not in inventory")
            return False
        items.pop(item_id)
        prefs.savedgame.set(get_inventory_key(self.episode_id), items)
        return True

    def attach_item(self, entity, item_id):
        entity.leftclick += lambda sender: self.add_item(item_id)

    def get_clues(self):
        return prefs.savedgame.get(get_clues_key(self.episode_id), [])

    def exists_clue(self, clue_id):
        clues = self.get_clues()
        return (clue_id in clues)

    def add_clue(self, clue_id):
        clues = self.get_clues()
        if clue_id in clues:
            print("clue already found")
            return False
        clues.append(clue_id)
        prefs.savedgame.set(get_clues_key(self.episode_id), clues)
        return True

    def attach_clue(self, entity, clue_id):
        entity.leftclick += lambda sender: self.add_clue(item_id)

    def get_switches(self):
        return prefs.savedgame.get(KEY_SWITCHES, {})

    def find_switch(self, switch_id):
        switches = self.get_switches()
        if not switch_id in switches:
            return None
        return switches[switch_id]

    def set_switch(self, switch_id, value):
        switches = self.get_switches()
        switches[switch_id] = value
        prefs.savedgame.set(KEY_SWITCHES, switches)

    def clear_switch(self, switch_id):
        switches = self.get_switches()
        if not switch_id in switches:
            print("attempted to clear non-existent switch")
            return False
        switches.pop(switch_id)
        prefs.savedgame.set(KEY_SWITCHES, switches)

    def update(self, game, events):
        # Prevent other entities from updating if a dialog or a choice set
        # is currently on-screen.
        if self.emitter.current_dialog or self.emitter.current_choiceset:
            # Keep this in sync with base update function
            self.timers.update(game, events)
            self._call_captured()
        else:
            if self.background:
                self.background.update(game, events)
            super().update(game, events)
            if self.return_scene:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP and \
                       event.button == MouseButton.RIGHT:
                        game.scenes.set_scene(self.return_scene)
                        break
        self.emitter.update(game, events)

    def draw(self, layer):
        if self.background:
            self.background.draw(layer)
        super().draw(layer)
        self.emitter.draw(layer)

    def load_content(self):
        reset_cursor()
        self.emitter = DialogEmitter(self, self.default_side)
        self.background = ClickableEntity(self, hit_rect = True)
        # Update mission-episode in save file
        prefs.savedgame.set("user.episode_id", self.episode_id)
        prefs.savedgame.set("user.mission_id", self.mission_id)
        prefs.savedgame.set("user.mission_key", self.mission_key)
