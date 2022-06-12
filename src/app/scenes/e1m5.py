from engine import *
from app import defaults, scene_list, utils
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E1M5Scene(Mission):
    def __init__(self):
        super().__init__(1, 5, "", "Congress - Outside 2", DialogSide.TOP)

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        super().load_content()

        self.background.set_surface(self.get_image("main-bg"))
        self.emitter.add("joe", "intro", "joe-faceright", repeat = False)

        prop_people = TargetItem(
            self,
            self.get_image("main-prop-people"),
            removable = False,
            grabbable = False
        )
        prop_people.leftclick += lambda sender: \
            game.scenes.set_scene("e1m5talk_joe")

        self.entities = {
            "prop_people": prop_people,
        }

scene_list.add_mission(E1M5Scene())

SW_TALK1 = "e1m5_talk1"
SW_TALK2 = "e1m5_talk2"

class E1M5Joe(Mission):
    def __init__(self):
        super().__init__(1, 5, "talk_joe", "Interrogation - Joe", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("joe-bg"))

        ca_joe = Image(self, utils.load_ca_image("joe-talk2"), (474, 90))
        self.entities = {
            "ca_joe": ca_joe,
        }

        talk1 = self.find_switch(SW_TALK1)
        if not talk1:
            self.emitter.add("joe", "talk1", callback=self._to_dan)
            return

        current_question = self.find_switch(SW_QUESTION_CURRENT)
        current_choice = self.find_switch(SW_FDA_CHOICE)
        # Affiliation
        if current_question == 0:
            self.emitter.add("joe", "q1_text1", callback=self._to_dan, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("joe", "q1_doubt_talk1", callback=self._to_dan)
            # ACCUSE
            elif current_choice == 3:
                self._accuse()
        # Demonstration objective
        elif current_question == 1:
            self.emitter.add("joe", "q2_talk1", callback=self._to_dan)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("joe", "q2_doubt_talk1", callback=self._to_dan)
            # ACCUSE
            elif current_choice == 3:
                self._accuse()
        # Effigies
        elif current_question == 2:
            self.emitter.add("joe", "q3_talk1", callback=self._to_dan, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("joe", "q1_doubt_talk1", callback=self._to_dan)
            # ACCUSE
            elif current_choice == 3:
                self._accuse()
        # Organizations
        elif current_question == 3:
            self.emitter.add("joe", "q4_talk1", callback=self._to_dan, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("joe", "q1_doubt_talk1", callback=self._to_dan)
            # ACCUSE
            elif current_choice == 3:
                self._accuse()
        # Cops
        elif current_question == 4:
            self.emitter.add("joe", "q5_talk1", callback=self._to_dan, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("joe", "q1_doubt_talk1", callback=self._to_dan)
            # ACCUSE
            elif current_choice == 3:
                self._accuse()

    def _to_dan(self):
        game.scenes.set_scene("e1m5talk_dan")

    def _accuse(self):
        items = self.emitter.add_clues_selector()
        # XXX we're not processing the clue result here, so default to the
        # negative response from the interviewee. This is fine, since E1M5
        # correct choices for FDA are all truth.
        items.selected += lambda sender, data: self._to_dan()

    def _next(self):
        game.scenes.set_scene("e1m5")

scene_list.add_mission(E1M5Joe())

class E1M5Dan(Mission):
    def __init__(self):
        super().__init__(1, 5, "talk_dan", "Interrogation - Dan", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("dan-bg"))

        prop_people = Image(
            self,
            self.get_image("dan-prop-people"),
            (205, 103)
        )
        ca_dan = Image(self, utils.load_ca_image("dan-talk1"), (550, 70))
        self.entities = {
            "prop_people": prop_people,
            "ca_dan": ca_dan,
        }

        talk1 = self.find_switch(SW_TALK1)
        if not talk1:
            self.emitter.add("dan", "talk1", callback=self._to_questions)
            self.set_switch(SW_TALK1, True)
            return

        current_question = self.find_switch(SW_QUESTION_CURRENT)
        current_choice = self.find_switch(SW_FDA_CHOICE)
        # Affiliation
        if current_question == 0:
            self.emitter.add("dan", "q1_text1", callback=self._show_fda, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("dan", "q1_doubt_talk1", callback=self._to_questions)
            # ACCUSE
            elif current_choice == 3:
                self.emitter.add("dan", "q1_accuse_talk1", callback=self._to_questions)
        # Demonstration objective
        elif current_question == 1:
            self.emitter.add("dan", "q2_talk1", callback=self._show_fda, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("dan", "q2_doubt_talk1", callback=self._to_questions)
            # ACCUSE
            elif current_choice == 3:
                self.emitter.add("dan", "q2_accuse_talk1", callback=self._to_questions)
        # Effigies
        elif current_question == 2:
            self.emitter.add("dan", "q3_talk1", callback=self._show_fda, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("dan", "q3_doubt_talk1", callback=self._to_questions)
            # ACCUSE
            elif current_choice == 3:
                self.emitter.add("dan", "q3_accuse_talk1", callback=self._to_questions)
        # Organizations
        elif current_question == 3:
            self.emitter.add("dan", "q4_talk1", callback=self._show_fda, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("dan", "q4_doubt_talk1", callback=self._to_questions)
            # ACCUSE
            elif current_choice == 3:
                self.emitter.add("dan", "q4_accuse_talk1", callback=self._to_questions)
        # Cops
        elif current_question == 4:
            self.emitter.add("dan", "q5_talk1", callback=self._show_fda, repeat = False)
            # FACT
            if current_choice == 1:
                # XXX never reached
                pass
            # DOUBT
            elif current_choice == 2:
                self.emitter.add("dan", "q5_doubt_talk1", callback=self._to_questions)
            # ACCUSE
            elif current_choice == 3:
                self.emitter.add("dan", "q5_accuse_talk1", callback=self._to_questions)

    def _show_fda(self):
        choiceset = ChoiceSet.from_entity(self, defaults.FDA_CHOICESET)
        choiceset.selected += self._handle_choice
        self.entities["fda"] = choiceset

        btn_clues = KeyedButton(self, (64, 64), "Review clues", pygame.K_TAB, "TAB")
        self.entities["btn_clues"] = btn_clues

    def _handle_choice(self, sender, value):
        i = value[0]
        self.set_switch(SW_FDA_CHOICE, i)
        # XXX since all fact dialog trees don't have any speech, we will
        # skip to the question selection instead.
        def _to_scene(sender):
            if i == 1:
                self._to_questions()
            else:
                self._to_joe()
        self.entities["fda"].hidden += _to_scene

    def _to_joe(self):
        game.scenes.set_scene("e1m5talk_joe")

    def _to_questions(self):
        questions = self.find_switch(SW_QUESTIONS)
        has_remaining_questions = True
        if questions:
            for item in questions:
                has_remaining_questions = not ("disabled" in item)
        if not questions or has_remaining_questions:
            game.scenes.set_scene("e1m5questions")
        else:
            self._next()

    def _next(self):
        game.scenes.set_scene("e1m5comic")

scene_list.add_mission(E1M5Dan())

SW_QUESTIONS = "e1m5_fda_questions"
SW_QUESTION_CURRENT = "e1m5_fda_question_id"
SW_FDA_CHOICE = "e1m5_fda_choice"

class E1M5Questions(Mission):
    def __init__(self):
        super().__init__(1, 5, "questions", "Interrogation - IGQ", DialogSide.TOP)
        self.questions = []

    def load_content(self):
        super().load_content()

        self.background.set_surface(self.get_image("main-bg"))

        self._load_questions()
        listbox = ListBox(self, (450, 95), "QUESTIONS", self.questions)
        listbox.selected += self._listbox_on_selected

        btn_clues = KeyedButton(self, (64, 64), "Review clues", pygame.K_TAB, "TAB")

        self.entities = {
            "hand": defaults.hand_left,
            "listbox": listbox,
            "btn_clues": btn_clues,
        }

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def _load_questions(self):
        self.questions = self.find_switch(SW_QUESTIONS)
        if not self.questions:
            self.questions = [
                {
                    "text": "Affiliation",
                    "value": 0
                },
                {
                    "text": "Demonstration objective",
                    "value": 1
                },
                {
                    "text": "Coffin and other effigies",
                    "value": 2
                },
                {
                    "text": "Invited organizations",
                    "value": 3
                },
                {
                    "text": "Surrounding cops",
                    "value": 4
                }
            ]
            self.set_switch(SW_QUESTIONS, self.questions)

    def _listbox_on_selected(self, sender, data):
        self.questions[data["value"]]["disabled"] = True
        self.set_switch(SW_QUESTION_CURRENT, data["value"])
        self.set_switch(SW_QUESTIONS, self.questions)
        self.set_switch(SW_FDA_CHOICE, None)
        game.scenes.set_scene("e1m5talk_joe")

scene_list.add_mission(E1M5Questions())


class E1M5Comic(Mission):
    def __init__(self):
        super().__init__(1, 5, "comic", "Comic", menu_blocked = True)
        self.fade_timer = None

    def update(self, game, events):
        super().update(game, events)

    def draw(self, layer):
        super().draw(layer)

    def load_content(self):
        super().load_content()
        slice1 = Image(
            self, self.get_image("comic-1"), (-11.333, -21.943))
        slice2 = Image(
            self, self.get_image("comic-2"), (29.495, 298.054))
        slice3 = Image(
            self, self.get_image("comic-3"), (757.344, 16.017))
        slice4 = Image(
            self, self.get_image("comic-4"), (797.388, 432.636))
        slice1.get_surface().set_alpha(0)
        slice2.get_surface().set_alpha(0)
        slice3.get_surface().set_alpha(0)
        slice4.get_surface().set_alpha(0)

        def allow_next():
            target1 = TargetMask(self, self.get_image("comic-tm"))
            target1.leftclick += lambda sender: game.scenes.set_scene("e1m6")
            self.entities["target1"] = target1

        def fadein_slice4():
            self.fade_timer = self.animator.fadein(
                slice4,
                750,
                allow_next
            )

        def fadein_slice3():
            self.fade_timer = self.animator.fadein(
                slice3,
                750,
                fadein_slice4,
                2000
            )

        def fadein_slice2():
            self.fade_timer = self.animator.fadein(
                slice2,
                750,
                fadein_slice3,
                2000
            )

        def fadein_slice1():
            self.fade_timer = self.animator.fadein(
                slice1,
                750,
                fadein_slice2,
                2000
            )

        fadein_slice1()

        self.entities = {
            "slice1": slice1,
            "slice2": slice2,
            "slice3": slice3,
            "slice4": slice4,
        }

scene_list.add_mission(E1M5Comic())
