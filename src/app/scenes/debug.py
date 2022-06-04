from engine import Scene
from engine.entities import *
from app import utils

import pygame

class DebugOverlay(Scene):
    def __init__(self):
        super().__init__("Debug Overlay")

    def update(self, game, events):
        super().update(game, events)

        if "xy" in self.entities:
            scaled_pos = str(game.get_mouse_pos())
            self.entities["xy"].set_text(scaled_pos)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKQUOTE:
                    self.reset()
                elif event.key == pygame.K_F1:
                    self.generate_xy_counter()
                elif event.key == pygame.K_F2:
                    self.generate_scene_list(game)
                elif event.key == pygame.K_F3:
                    self.generate_test_button()

    def load_content(self):
        pass

    def generate_test_button(self):
        btn_test = Button.from_entity(utils.button_default, "Test")
        btn_test.set_position((510, 100))
        def on_btn_test_click(sender, button):
            import uuid
            sender.get_label().set_text(str(uuid.uuid4()))
        btn_test.click += on_btn_test_click
        self.entities["btn_test"] = btn_test

    def generate_scene_list(self, game):
        current_y = 20
        t = False
        for key in game.scenes.all_scenes:
            btn_tp = LabelButton(
                Label(
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
            "0, 0",
            utils.get_font(16),
            pygame.Color("white"),
            (0, 0)
        )

    def reset(self):
        self.entities = {}
