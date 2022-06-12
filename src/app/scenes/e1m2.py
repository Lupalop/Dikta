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
            callback_delay=1000
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

    def _to_driver(self):
        game.scenes.set_scene("e1m2taxi_driver")

    def _handle_choice(self, sender, value):
        i = value[0]
        self.set_switch("taxi_choice", i)
        # Choice 1: Luneta Park
        if i == 1:
            self.emitter.add("joe", "choice1", callback=self._to_driver)
        # Choice 2: Congress
        elif i == 2:
            self.emitter.add("joe", "choice2", callback=self._to_driver)
        # Choice 3: Home
        elif i == 3:
            self.emitter.add("joe", "choice3_1")
            self.emitter.add("joe", "choice3_2", callback=self._to_driver)
        self.emitter.next()

    def _choice_create(self, sender):
        choiceset = self.emitter.add_choiceset(["Luneta Park", "Congress", "Home"])
        choiceset.selected += self._handle_choice

    def _next(self):
        game.scenes.set_scene("e1m3")

    def _item_selected(self, sender, data):
        if data["value"] == "wallet":
            self.emitter.add("joe", "pay2a", callback=self._next)
            self.emitter.next()
        else:
            self.emitter.add("joe", "pay2b", callback=self.to_gameover)
            self.emitter.next()

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("taxi-bg-joe"))

        taxi_choice = self.find_switch("taxi_choice")
        if not taxi_choice:
            initial_dialog = self.emitter.add(
                "joe",
                "choice_initial",
                flags=DialogFlags.SKIPPABLE
            )
            initial_dialog.label_speech.completed += self._choice_create
            return

        taxi_pre_reset = self.find_switch("taxi_pre_reset")
        if taxi_pre_reset:
            self.emitter.add("joe", "choice3_4", callback=self._to_driver)
            self.set_switch("taxi_reset", True)
            self.clear_switch("taxi_choice")
            self.clear_switch("taxi_pre_reset")
            return

        taxi_pay = self.find_switch("taxi_pay")
        if taxi_pay:
            self.emitter.add("joe", "pay1", flags=DialogFlags.SKIPPABLE)
            items = self.emitter.add_itemselector()
            items.selected += self._item_selected
            return

scene_list.add_mission(E1M2TaxiInsideJoe())

# E1M2 - Taxi - Inside (Driver)

class E1M2TaxiInsideDriver(Mission):
    def __init__(self):
        super().__init__(1, 2, "taxi_driver", "Taxi - Inside (Driver)", DialogSide.BOTTOM_RIGHT)

    def _to_pay(self):
        self.set_switch("taxi_pay", True)
        game.scenes.set_scene("e1m2taxi_driver")

    def _to_joe(self):
        taxi_reset = self.find_switch("taxi_reset")
        if taxi_reset:
            self.clear_switch("taxi_reset")
        game.scenes.set_scene("e1m2taxi_joe")

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("taxi-bg-driver"))

        taxi_pay = self.find_switch("taxi_pay")
        if taxi_pay:
            self.emitter.add("driver", "pay1", "taxidriver-main", callback=self._to_joe)
            return

        taxi_reset = self.find_switch("taxi_reset")
        if taxi_reset:
            self.emitter.add("driver", "choice3_5", "taxidriver-main", callback=self._to_joe)
            return

        taxi_choice = self.find_switch("taxi_choice")
        if taxi_choice:
            if taxi_choice == 1:
                self.emitter.add("driver", "choice1", "taxidriver-main", callback=self._to_pay)
            elif taxi_choice == 2:
                self.emitter.add("driver", "choice2", "taxidriver-main", callback=self._to_pay)
            elif taxi_choice == 3:
                self.emitter.add("driver", "choice3_3", "taxidriver-main", callback=self._to_joe)
                self.set_switch("taxi_pre_reset", True)

scene_list.add_mission(E1M2TaxiInsideDriver())
