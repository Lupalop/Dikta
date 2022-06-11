from engine import *
from app import utils, scene_list
from app.entities import *

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
            self,
            utils.load_mm_image("bg-main"),
            (0, 0))
        logo = Image(
            self,
            utils.load_mm_image("logo"),
            (930, 590))
        label_version = Label(
            self,
            "Version 1.0.0a2",
            utils.get_font(14),
            pygame.Color("white"),
            (20, 690))
        logo_company = Image(
            self,
            utils.load_mm_image("logo-company-alt"),
            (20, 710))

        def to_newgame(sender, button):
            prefs.savedgame.clear()
            game.scenes.set_scene("e1m0")
        btn_new = FadeButton(self, utils.load_mm_image("btn-new"), (475, 665))
        btn_new.click += to_newgame

        def to_loadgame(sender, button):
            prefs.savedgame.load()
            mission_toload = prefs.savedgame.get("user.mission_key", "e1m0")
            game.scenes.set_scene(mission_toload)
        btn_load = FadeButton(self, utils.load_mm_image("btn-load"), (610, 595))
        btn_load.click += to_loadgame

        btn_options = FadeButton(self, utils.load_mm_image("btn-options"), (740, 500))

        btn_credits = FadeButton(self, utils.load_mm_image("btn-credits"), (1105, 335))

        btn_exit = FadeButton(self, utils.load_mm_image("btn-exit"), (1280, 280))
        btn_exit.click += lambda sender, button: game.exit()

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
        }

scene_list.all["main_menu"] = MainMenuScene()
