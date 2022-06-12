from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

# E1M4 - Congress - Inside (Police)

SW_TALK1 = "e1m4_mac_talk1"
SW_CLUE_SELECTED = "e1m4_clue_selected"
SW_CHOSE_PRESSCARD = "e1m4_chose_presscard"

class E1M4CongressPolice(Mission):
    def __init__(self):
        super().__init__(1, 4, "talk_police", "Congress - Inside (Police)", DialogSide.BOTTOM_LEFT)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("bg-mac"))

        ca_mac = Image(self, utils.load_ca_image("mac-talk1"), (318, 66))
        self.entities = {
            "ca_mac": ca_mac,
        }

        mac_talk1 = self.find_switch(SW_TALK1)
        if not mac_talk1:
            self.emitter.add("police_mac", "intro", callback=self._to_joe)
            self.set_switch(SW_TALK1, True)
            return

        is_press_card = self.find_switch(SW_CHOSE_PRESSCARD)
        if is_press_card:
            self.emitter.add("police_mac", "wp_1")
            self.emitter.add("police_mac", "wp_2", callback=self._next)
        else:
            self.emitter.add("police_mac", "np_1")
            self.emitter.add("police_mac", "np_2", callback=self._next)

    def _to_joe(self):
        game.scenes.set_scene("e1m4talk_joe")

    def _next(self):
        game.scenes.set_scene("e1m5")

scene_list.add_mission(E1M4CongressPolice())

# E1M4 - Congress - Inside (Joe)

class E1M4CongressJoe(Mission):
    def __init__(self):
        super().__init__(1, 4, "talk_joe", "Congress - Inside (Joe)", DialogSide.BOTTOM_LEFT)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("bg-joe"))

        ca_joe = Image(self, utils.load_ca_image("joe-talk1"), (830, 100))
        self.entities = {
            "ca_joe": ca_joe,
        }

        clue_selected = self.find_switch(SW_CLUE_SELECTED)
        if not clue_selected:
            self.emitter.add("joe", "intro", flags=DialogFlags.SKIPPABLE)
            items = self.emitter.add_clues_selector()
            items.selected += self._clue_selected
            return

    def _clue_selected(self, sender, data):
        is_press_card = (data["id"] == "press_card")
        
        self.set_switch(SW_CHOSE_PRESSCARD, is_press_card)
        if is_press_card:
            self.emitter.next()
            self._to_police()
        else:
            self.emitter.add("joe", "np_1", callback=self._to_police)
            self.emitter.next()

    def _to_police(self):
        game.scenes.set_scene("e1m4talk_police")

scene_list.add_mission(E1M4CongressJoe())
