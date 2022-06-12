from engine import Scene, prefs, game
from app import utils, scene_list, defaults
from app.mission import Mission
from app.entities import *

import pygame

class InGameItemsOverlay(Scene):
    def __init__(self):
        super().__init__("In-Game Overlay - Items")
        self.visible = False

    def set_visibility(self, is_visible):
        self.visible = is_visible

    def toggle_visibility(self):
        current_scene = game.scenes.get_scene()

        # Prevent the menu from showing up on regular scenes.
        if not isinstance(current_scene, Mission):
            return
        # Prevent the menu from showing up on situations where it's blocked.
        if current_scene.menu_blocked or \
           current_scene.emitter.current_dialog or \
           current_scene.emitter.current_selector or \
           scene_list.all["ig_escmenu"].visible or \
           game.scenes._switching:
            return

        self.set_visibility(not self.visible)
        current_scene.enabled = not current_scene.enabled
        utils.set_cursor("default")

        dataset = current_scene.get_clues_dataset()
        listbox = ListBox(self, (450, 95), "CLUES", dataset)
        self.entities["listbox_items"] = listbox

    def load_content(self):
        bg_solid = pygame.Surface(prefs.default.get("app.display.layer_size", (0, 0)))
        bg_solid.fill(pygame.Color("black"))
        bg_solid.set_alpha(100)
        background = Image(
            self,
            bg_solid,
            (0, 0))

        self.entities = {
            "background": background,
            "hand": defaults.hand_left,
        }

    def update(self, game, events):
        if self.visible:
            super().update(game, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.toggle_visibility()
                    break

    def draw(self, layer):
        if self.visible:
            super().draw(layer)

scene_list.all["ig_items"] = InGameItemsOverlay()
