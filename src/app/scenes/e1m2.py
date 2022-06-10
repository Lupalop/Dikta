from engine import *
from app import defaults, scene_list
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

# E1M2 - Intermezzo

class E1M2Intermezzo(Mission):
    def __init__(self):
        super().__init__(1, 2, "intermezzo", "Intermezzo", DialogSide.TOP)

    def _next(self):
        game.scenes.set_scene("e1m2taxi_joe")

    def _puppet_taximove_out(self):
        self.animator.to_position_x(
            self.entities["taxi"],
            1500,
            1500,
            delta=True,
            callback=self._next,
            callback_delay=500
        )
        self.animator.to_position_x(
            self.entities["taxi_driver"],
            1500,
            1500,
            delta=True
        )
        self.animator.to_position_x(
            self.entities["taxi_joe"],
            1500,
            1500,
            delta=True
        )

    def _puppet_entertaxi(self):
        self.entities.pop("joe_standing")
        self.entities["taxi_joe"].get_surface().set_alpha(255)
        delay_timer = self.timers.add(500, True)
        delay_timer.elapsed += lambda sender: self._puppet_taximove_out()

    def _puppet_taximove_in(self):
        self.animator.to_position_x(
            self.entities["taxi"],
            1500,
            -10,
            callback=self._puppet_entertaxi,
            callback_delay=1000
        )
        self.animator.to_position_x(
            self.entities["taxi_driver"],
            1500,
            615,
        )

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("outside-bg"))
        self.emitter.add(
            "joe",
            "call_taxi",
            "joe-faceright",
            callback=self._puppet_taximove_in
        )

        joe_standing = Image(self, self.get_image("outside-prop-joe-waiting"), (540, 265))
        taxi_driver = Image(self, self.get_image("outside-prop-driver"), (-735, 317))
        taxi_joe = Image(self, self.get_image("outside-prop-joe"), (458, 323))
        taxi_joe.get_surface().set_alpha(0)
        taxi = Image(self, self.get_image("outside-prop-taxi"), (-1360, 105))

        self.entities = {
            "joe_standing": joe_standing,
            "taxi_driver": taxi_driver,
            "taxi_joe": taxi_joe,
            "taxi": taxi,
        }

scene_list.add_mission(E1M2Intermezzo())

# E1M2 - Taxi - Inside (Joe)

class E1M2TaxiInsideJoe(Mission):
    def __init__(self):
        super().__init__(1, 2, "taxi_joe", "Taxi - Inside (Joe)", DialogSide.BOTTOM_LEFT)

    def _choice_handle(self, sender, value):
        # Choice 0: Leave
        if value[0] == 0:
            game.scenes.set_scene("e1m2intermezzo")
        # Choice 1: Stay
        else:
            self.emitter.add("joe", "return")
        self.emitter.next()

    def _choice_create(self, sender):
        self.current_choiceset = ChoiceSet(self, (64, 64), ["Luneta Park", "Congress", "Home"], True)
        self.current_choiceset.selected += self._choice_handle
        self.current_choiceset.hidden += self._clear_choiceset

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("taxi-bg-joe"))
        initial_dialog = self.emitter.add(
            "joe",
            "initial_question",
            flags=DialogFlags.SKIPPABLE
        )
        initial_dialog.label_speech.completed += self._choice_create
"""
        joe_standing = Image(self, self.get_image("outside-prop-joe-waiting"), (540, 265))
        taxi_driver = Image(self, self.get_image("outside-prop-driver"), (-735, 317))
        taxi_joe = Image(self, self.get_image("outside-prop-joe"), (458, 323))
        taxi_joe.get_surface().set_alpha(0)
        taxi = Image(self, self.get_image("outside-prop-taxi"), (-1360, 105))

        self.entities = {
            "joe_standing": joe_standing,
            "taxi_driver": taxi_driver,
            "taxi_joe": taxi_joe,
            "taxi": taxi,
        }
"""
scene_list.add_mission(E1M2TaxiInsideJoe())
