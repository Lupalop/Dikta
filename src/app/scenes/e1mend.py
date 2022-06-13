from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame
import webbrowser

URL_RESOURCE = "https://philippinesfreepress.wordpress.com/1970/02/06/the-january-26-confrontation-a-highly-personal-account-february-7-1970/"

class E1End(Mission):
    def __init__(self):
        super().__init__(1, "end", "", "End Game")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def _to_ep2(self, sender, button):
        game.scenes.set_scene("e2m1")

    def _to_resource(self, sender, button):
        webbrowser.open(URL_RESOURCE)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("bg"))

        btn_view = Button.from_entity(self, defaults.button_default, "View")
        btn_view.set_position((588, 497))
        btn_view.click += self._to_resource

        btn_exit = KeyedButton(self, (545, 650), "Continue", pygame.K_x, "X")
        btn_exit.click += self._to_ep2

        self.entities = {
            "btn_exit": btn_exit,
            "btn_view": btn_view,
        }

scene_list.add_mission(E1End())
