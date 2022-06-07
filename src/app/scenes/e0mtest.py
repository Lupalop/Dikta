from engine import *
from app import utils, scene_list
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E0MTestScene(Mission):
    def __init__(self):
        super().__init__(0, "test")

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        self.emitter.add("joe", 1, callback=lambda:print("test"))
        self.emitter.add("joe", 2, "joe-faceright", flags=DialogFlags.CLOSEABLE)
        self.emitter.add("joe", 3)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP_RIGHT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE_RIGHT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM_RIGHT)

        print(self.get_string("joe", 1))
        print(utils.get_ep_string(1, 1, "joe", 1))
        print(utils.get_item_string("pbadge"))

        bg_main = Image(
            self,
            utils.load_em_image(1, 1, "bg-main"))

        self.entities = {
            "bg_main": bg_main,
        }

scene_list.add_mission(E0MTestScene())
