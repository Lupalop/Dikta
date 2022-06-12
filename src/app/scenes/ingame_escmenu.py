from engine import Scene, prefs, game
from app import utils, scene_list
from app.mission import Mission
from app.entities import *

import pygame

class InGameEscMenuOverlay(Scene):
    def __init__(self):
        super().__init__("In-Game Overlay - Paused")
        self.visible = False

    def set_visibility(self, is_visible):
        self.visible = is_visible

    def toggle_visibility(self):
        current_scene = game.scenes.get_scene()

        # Prevent the menu from showing up on regular scenes.
        if not isinstance(current_scene, Mission):
            return
        # Prevent the menu from showing up on missions where it's blocked.
        if current_scene.menu_blocked:
            return

        self.set_visibility(not self.visible)
        current_scene.enabled = not current_scene.enabled
        utils.set_cursor("default")

        ig_blocked = (
            current_scene.emitter.current_dialog or \
            current_scene.emitter.current_selector or \
            game.scenes._switching
        )

        if self.visible:
            scene_list.all["ig_items"].set_visibility(False)

        self.entities["action_items"].hidden = self.entities["action_items"].disabled = ig_blocked
        self.entities["action_clues"].hidden = self.entities["action_clues"].disabled = ig_blocked

    def load_content(self):
        bg_solid = pygame.Surface(prefs.default.get("app.display.layer_size", (0, 0)))
        bg_solid.fill(pygame.Color("black"))
        bg_solid.set_alpha(230)
        background = Image(
            self,
            bg_solid,
            (0, 0))

        action_continue = FadeButton(self, utils.load_ui_image("igesc-action-continue"), (762, 85))
        action_continue.click += lambda sender, button: self.toggle_visibility()

        def to_items(sender, button):
            self.toggle_visibility()
            scene_list.all["ig_items"].toggle_visibility()
        action_items = FadeButton(self, utils.load_ui_image("igesc-action-items"), (868, 233))
        action_items.click += to_items

        def to_clues(sender, button):
            print("FIXME: Not yet implemented")
        action_clues = FadeButton(self, utils.load_ui_image("igesc-action-clues"), (868, 333))
        action_clues.click += to_clues

        def to_options(sender, button):
            print("FIXME: Not yet implemented")
        action_options = FadeButton(self, utils.load_ui_image("igesc-action-options"), (802, 407))
        action_options.click += to_options

        def to_main_menu(sender, button):
            prefs.savedgame.save()
            game.scenes.set_scene("main_menu")
            self.toggle_visibility()
        action_exit = FadeButton(self, utils.load_ui_image("igesc-action-exit"), (924, 559))
        action_exit.click += to_main_menu

        self.entities = {
            "background": background,
            "action_continue": action_continue,
            "action_items": action_items,
            "action_clues": action_clues,
            "action_options": action_options,
            "action_exit": action_exit,
        }

    def update(self, game, events):
        if self.visible:
            super().update(game, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_visibility()
                    break

    def draw(self, layer):
        if self.visible:
            super().draw(layer)

scene_list.all["ig_escmenu"] = InGameEscMenuOverlay()
