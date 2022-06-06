from engine import *
from app import utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M1Scene(Mission):
    def __init__(self):
        super().__init__(1, 1, "Dialogue 1", DialogSide.BOTTOM)

    def load_content(self):
        self.emitter.add("joe", 1)
        self.emitter.add("joe", 2, callback=lambda: game.scenes.set_scene(E1M1BScene()))

        self.background.set_surface(self.get_image("bg-joe"))

class E1M1BScene(Mission):
    def __init__(self):
        super().__init__(1, 1, "Desk - Outside", DialogSide.TOP)

    def load_content(self):
        self.emitter.add("joe", "tut1", "joe-faceright", callback=lambda: game.scenes.set_scene(""))

        target1 = ClickableEntity(self, pygame.Rect(0, 0, 700, 320), hit_rect=True)
        target1.click += lambda sender, state: print("test")
        self.background.set_surface(self.get_image("bg-main"))

        self.entities = {
            "bulletin_board": target1,
        }
