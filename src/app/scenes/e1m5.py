from engine import game
from app import defaults, scene_list, utils
from app.entities import Image, TargetItem, KeyedButton, TargetMask
from app.mission import Mission
from app.dialog import DialogSide

from .interrogation import InterrogationInterrogator, InterrogationRespondent, InterrogationMenu

import pygame

class E1M5Scene(Mission):
    def __init__(self):
        super().__init__(1, 5, "", "Congress - Outside 2", DialogSide.TOP)

    def load_content(self):
        super().load_content()
        utils.set_music("e1m5", 0.15)
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

class E1M5Joe(InterrogationInterrogator):
    def __init__(self):
        super().__init__(1, 5, "talk_joe", "Interrogation - Joe", "e1m5_tree", "e1m5talk_dan", "e1m5questions", "e1m5comic")
        self.interrogator_branch = "joe"

    def load_content(self):
        super().load_content()
        utils.set_music("e1m5", 0.15)
        self.background.set_surface(self.get_image("joe-bg"))
        self.entities["ca_joe"] = Image(self, utils.load_ca_image("joe-talk2"), (474, 90))

class E1M5Dan(InterrogationRespondent):
    def __init__(self):
        super().__init__(1, 5, "talk_dan", "Interrogation - Dan", "e1m5_tree", "e1m5talk_joe", "e1m5questions", "e1m5comic", side=DialogSide.BOTTOM)
        self.respondent_branch = "dan"

    def load_content(self):
        super().load_content()
        utils.set_music("e1m5", 0.15)
        self.background.set_surface(self.get_image("dan-bg"))
        prop_people = Image(self, self.get_image("dan-prop-people"), (205, 103))
        self.entities["prop_people"] = prop_people
        self.entities["ca_dan"] = Image(self, utils.load_ca_image("dan-talk1"), (550, 70))

class E1M5Questions(InterrogationMenu):
    def __init__(self):
        super().__init__(1, 5, "questions", "Interrogation - IGQ", "e1m5_tree", "e1m5talk_joe", pos=(450, 95))

    def load_content(self):
        self.entities["hand"] = defaults.hand_left
        super().load_content()
        utils.set_music("e1m5", 0.15)
        self.background.set_surface(self.get_image("main-bg"))
        btn_clues = KeyedButton(self, (64, 64), "Review clues", pygame.K_F12, "TAB")
        from .interrogation import _toggle_clues
        btn_clues.leftclick += _toggle_clues
        self.entities["btn_clues"] = btn_clues

scene_list.add_mission(E1M5Joe())
scene_list.add_mission(E1M5Dan())
scene_list.add_mission(E1M5Questions())

class E1M5Comic(Mission):
    def __init__(self):
        super().__init__(1, 5, "comic", "Comic", menu_blocked = True)
        self.fade_timer = None

    def load_content(self):
        super().load_content()
        utils.set_music("e1m5comic", 0.5)
        slice1 = Image(self, self.get_image("comic-1"), (-11.333, -21.943))
        slice2 = Image(self, self.get_image("comic-2"), (29.495, 298.054))
        slice3 = Image(self, self.get_image("comic-3"), (757.344, 16.017))
        slice4 = Image(self, self.get_image("comic-4"), (797.388, 432.636))
        
        slice1.get_surface().set_alpha(0)
        slice2.get_surface().set_alpha(0)
        slice3.get_surface().set_alpha(0)
        slice4.get_surface().set_alpha(0)

        def allow_next():
            target1 = TargetMask(self, self.get_image("comic-tm"))
            target1.leftclick += lambda sender: game.scenes.set_scene("e1m6")
            self.entities["target1"] = target1

        def fadein_slice4():
            self.fade_timer = self.animator.fadein(slice4, 750, allow_next)

        def fadein_slice3():
            self.fade_timer = self.animator.fadein(slice3, 750, fadein_slice4, 5000)

        def fadein_slice2():
            self.fade_timer = self.animator.fadein(slice2, 750, fadein_slice3, 5000)

        def fadein_slice1():
            self.fade_timer = self.animator.fadein(slice1, 750, fadein_slice2, 5000)

        fadein_slice1()

        self.entities = {
            "slice1": slice1,
            "slice2": slice2,
            "slice3": slice3,
            "slice4": slice4,
        }

scene_list.add_mission(E1M5Comic())
