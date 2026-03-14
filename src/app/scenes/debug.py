from engine import Scene, prefs
from app import utils, defaults, scene_list
from app.entities import *
from app.dialog import DialogEmitter, DialogSide

import pygame

class DebugOverlay(Scene):
    def __init__(self):
        super().__init__("Debug Overlay")

    def update(self, game, events):
        super().update(game, events)
        self.emitter.update(game, events)

        if "xy" in self.entities:
            scaled_pos = str(game.get_mouse_pos())
            self.entities["xy"].set_text(scaled_pos)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_SHIFT:
                    if event.key == pygame.K_BACKQUOTE:
                        self.reset()
                    elif event.key == pygame.K_F1:
                        self.generate_xy_counter()
                    elif event.key == pygame.K_F2:
                        self.generate_scene_list(game)
                    elif event.key == pygame.K_F3:
                        self.generate_test_button()
                    elif event.key == pygame.K_F4:
                        self.get_captured_action(game)
                    elif event.key == pygame.K_F5:
                        self.clear_prefs()
                    elif event.key == pygame.K_F6:
                        self.grant_all_clues(game)
                    break

    def load_content(self):
        self.emitter = DialogEmitter(self, DialogSide.TOP)

    def draw(self, layer):
        super().draw(layer)
        self.emitter.draw(layer)

    def generate_test_button(self):
        btn_test = Button.from_entity(self, defaults.button_default, "Test")
        btn_test.set_position((510, 100))
        def on_btn_test_click(sender, button):
            import uuid
            sender.get_label().set_text(str(uuid.uuid4()))
        btn_test.click += on_btn_test_click
        self.entities["btn_test"] = btn_test

    def generate_scene_list(self, game):
        current_y = 20
        t = False
        for key in game.scenes.all:
            btn_tp = LabelButton(
                self,
                Label(
                    self,
                    key,
                    utils.get_font(20),
                    pygame.Color("white"),
                ),
                (5, current_y)
            )
            btn_tp.click += lambda sender, state, bound_key=key: \
                game.scenes.set_scene(bound_key)
            current_y += 30
            btn_key = "scb_{}".format(key)
            self.entities[btn_key] = btn_tp

    def generate_xy_counter(self):
        self.entities["xy"] = Label(
            self,
            "0, 0",
            utils.get_font(16),
            pygame.Color("white"),
            (0, 0)
        )

    def reset(self):
        self.entities = {}

    def get_captured_action(self, game):
        owner = game.scenes.get_scene()
        print("owner: ", owner)
        print("captured action: ", owner._captured_action)

    def clear_prefs(self):
        prefs.default.clear()
        prefs.savedgame.clear()

    def grant_all_clues(self, game):
        current_scene = game.scenes.get_scene()
        from app.mission import Mission
        if not isinstance(current_scene, Mission):
            self.emitter.add_custom(
                "cheat_clues_fail",
                "DEBUG",
                "Cheat failed: Not currently in a mission."
            )
            return

        episode_id = prefs.savedgame.get("user.episode_id", 1)
        clues_key = utils.get_clues_key(episode_id)
        
        # Get all clue keys from strings.json
        all_clue_ids = list(utils.strings.get("clues", {}).keys())
        
        # Merge with existing clues
        current_clues = prefs.savedgame.get(clues_key, [])
        new_clues = list(set(current_clues + all_clue_ids))
        
        prefs.savedgame.set(clues_key, new_clues)
        self.emitter.add_custom(
            "cheat_clues_success",
            "DEBUG",
            f"Granted {len(all_clue_ids)} clues for episode {episode_id}."
        )

scene_list.all["debug"] = DebugOverlay()
