from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M7Joe(Mission):
    def __init__(self):
        super().__init__(1, 7, "joe", "PGH - Talk (Joe)", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.emitter.add("joe", "intro1", repeat = False, callback=lambda: game.scenes.set_scene("e1m7doc"))

        self.background.set_surface(self.get_image("joe-bg"))

scene_list.add_mission(E1M7Joe())

class E1M7Doc(Mission):
    def __init__(self):
        super().__init__(1, 7, "doc", "PGH - Talk (Doc)", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.emitter.add("doc", "intro1", repeat = False, callback=lambda: game.scenes.set_scene("e1m7"))

        self.background.set_surface(self.get_image("doc-bg"))

scene_list.add_mission(E1M7Doc())


class E1M7Scene(Mission):
    def __init__(self):
        super().__init__(1, 7, "", "PGH - Main", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("main-bg"))
        self.emitter.add("joe", "intro2", "joe-faceright", repeat = False)

        target1 = TargetMask(self, self.get_image("main-target-cop2"))
        target1.leftclick += lambda sender: self.emitter.add("joe", "target_police_talk1", "joe-faceright")

        target2 = TargetMask(self, self.get_image("main-target-dan"))
        target2.leftclick += lambda sender: self.emitter.add("joe", "target_nusp_talk1", "joe-faceright")

        target3 = TargetMask(self, self.get_image("main-target-demonstrator"))
        target3.leftclick += lambda sender: self.emitter.add("joe", "target_demonstrator", "joe-faceright")

        target4 = TargetMask(self, self.get_image("main-target-doctor"))
        target4.leftclick += lambda sender: self.emitter.add("joe", "target_doctor_talk1", "joe-faceright")

        target5 = TargetMask(self, self.get_image("main-target-mac"))
        target5.leftclick += lambda sender: self.emitter.add("joe", "target_police_talk1", "joe-faceright")

        target6 = TargetMask(self, self.get_image("main-target-door"))
        def _end():
            game.scenes.set_scene("e1end")
        target6.leftclick += lambda sender: self.emitter.add("joe", "target_door_talk1", "joe-faceright", callback=_end)

        self.entities = {
            "target1": target1,
            "target2": target2,
            "target3": target3,
            "target4": target4,
            "target5": target5,
            "target6": target6,
        }

scene_list.add_mission(E1M7Scene())
