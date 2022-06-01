from engine import *
from engine.entities import *
from app import utils

import pygame

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__("Main Menu")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        background = Image(
            utils.load_mm_image("bg-main"),
            (0, 0))
        logo = Image(
            utils.load_mm_image("logo"),
            (930, 590))
        label_version = Label(
            "Version 1.0.0a1 - For testing purposes only.",
            utils.fonts["sm"],
            pygame.Color("white"),
            (20, 690))
        logo_company = Image(
            utils.load_mm_image("logo-company"),
            (20, 710))

        btn_new = FadeButton(utils.load_mm_image("btn-new"), (475, 665))
        btn_new.click += lambda sender, button: game.scenes.set_scene("e1m0")

        btn_load = FadeButton(utils.load_mm_image("btn-load"), (610, 595))

        btn_options = FadeButton(utils.load_mm_image("btn-options"), (740, 500))

        btn_credits = FadeButton(utils.load_mm_image("btn-credits"), (1105, 335))

        btn_exit = FadeButton(utils.load_mm_image("btn-exit"), (1280, 280))
        btn_exit.click += lambda sender, button: game.exit()

        btn_test = Button.from_entity(utils.button_default, "Test")
        btn_test.set_position((510, 100))
        def on_btn_test_click(sender, button):
            import uuid
            btn_test.get_label().set_text(str(uuid.uuid4()))
        btn_test.click += on_btn_test_click

        self.entities = {
            "background": background,
            "logo": logo,
            "logo_company": logo_company,
            "label_version": label_version,
            "btn_new": btn_new,
            "btn_load": btn_load,
            "btn_options": btn_options,
            "btn_credits": btn_credits,
            "btn_exit": btn_exit,
            #"btn_test": btn_test,
        }
