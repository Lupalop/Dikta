from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M3Scene(Mission):
    def __init__(self):
        super().__init__(1, 3, "", "Congress - Outside", DialogSide.TOP)

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        super().load_content()
        utils.set_music("e1m3", 0.15)
        self.ambient_sound = utils.play_sfx("street_amb", 0.5, True)
        self.background.set_surface(self.get_image("main-bg"))
        self.emitter.add("joe", "text1", "joe-faceright", repeat = False)
        self.emitter.add("joe", "text2", "joe-faceright", repeat = False)

        target_entrance = TargetMask(self, self.get_image("main-tm-entrance"))
        def _clue0(sender):
            game.scenes.set_scene("e1m4talk_police")
        target_entrance.leftclick += _clue0

        target_speakers = TargetItem(
            self,
            self.get_image("main-target-speakers"),
            (314, 65),
            removable = False,
            grabbable = False
        )
        target_speakers.leftclick += lambda sender: \
            self.emitter.add("joe", "target_speaker", "joe-faceright")

        target_people_count = TargetItem(
            self,
            self.get_image("main-target-people_left"),
            (-83, 190),
            removable = False,
            grabbable = False
        )
        def _clue1(sender):
            self.emitter.add("joe", "target_estimate_count", "joe-faceright")
            self.add_clue("estimate_count")
        target_people_count.leftclick += _clue1

        target_no_guns = TargetItem(
            self,
            self.get_image("main-target-people_right"),
            (770, 150),
            removable = False,
            grabbable = False
        )
        def _clue2(sender):
            self.emitter.add("joe", "target_no_guns", "joe-faceright")
            self.add_clue("no_guns")
        target_no_guns.leftclick += _clue2

        target_police = TargetItem(
            self,
            self.get_image("main-target-police"),
            (422, 256),
            removable = False,
            grabbable = False
        )
        def _clue3(sender):
            if self.find_switch("e1m3_police_encountered"):
                _clue0(sender)
            else:
                self.emitter.add("joe", "target_police", "joe-faceright")
                self.set_switch("e1m3_police_encountered", True)
        target_police.leftclick += _clue3

        target_podium = TargetItem(
            self,
            self.get_image("main-target-podium"),
            (388, 277),
            removable = False,
            grabbable = False
        )
        def _clue4(sender):
            self.emitter.add_popup_image(self.get_image("main-zoom-podium"))
            self.emitter.add("joe", "target_person_speaking1", "joe-faceright")
            self.emitter.add("joe", "target_person_speaking2", "joe-faceright", callback=self.emitter.next_popup_image)
            self.add_clue("podium_nusp")
        target_podium.leftclick += _clue4

        target_coffin = TargetItem(
            self,
            self.get_image("main-target-coffin_effigy"),
            (450, 613),
            removable = False,
            grabbable = False
        )
        def _clue5(sender):
            self.emitter.add_popup_image(self.get_image("main-zoom-effigy"))
            self.emitter.add("joe", "target_effigies", "joe-faceright", callback=self.emitter.next_popup_image)
            self.add_clue("effigies_general")
        target_coffin.leftclick += _clue5

        self.entities = {
            "target_entrance": target_entrance,
            "target_speakers": target_speakers,
            "target_podium": target_podium,
            "target_people_count": target_people_count,
            "target_no_guns": target_no_guns,
            "target_police": target_police,
            "target_coffin": target_coffin,
        }

scene_list.add_mission(E1M3Scene())
