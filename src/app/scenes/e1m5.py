from engine import game
from app import defaults, scene_list, utils
from app.entities import Image, TargetItem, TargetMask
from app.mission import Mission
from app.dialog import DialogSide

from .interrogation import InterrogationConversation, InterrogationMenu

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
            game.scenes.set_scene("e1m5talk")

        self.entities = {
            "prop_people": prop_people,
        }

scene_list.add_mission(E1M5Scene())

class E1M5Talk(InterrogationConversation):
    def __init__(self):
        super().__init__(
            1,
            5,
            "talk",
            "Interrogation - Talk",
            "e1m5_tree",
            "e1m5questions",
            "e1m5comic",
            "joe",
            "dan",
            side=DialogSide.BOTTOM
        )

    def load_content(self):
        super().load_content()
        utils.set_music("e1m5", 0.15)
        active_branch = self.find_switch(self.SW_ACTIVE_BRANCH)
        if active_branch not in ("joe", "dan"):
            active_branch = "joe"
        self._apply_outro_cutout(active_branch)

    def _get_outro_visual(self, character):
        if character == "joe":
            return {
                "background": "joe-bg",
                "cutout": "joe-talk2",
                "cutout_pos": (474, 90),
            }
        if character == "dan":
            return {
                "background": "dan-bg",
                "cutout": "dan-talk1",
                "cutout_pos": (550, 70),
                "prop": "dan-prop-people",
                "prop_pos": (205, 103),
            }
        return None

class E1M5Questions(InterrogationMenu):
    def __init__(self):
        super().__init__(1, 5, "questions", "Interrogation - IGQ", "e1m5_tree", "e1m5talk", pos=(450, 95))

    def load_content(self):
        self.entities["hand"] = defaults.hand_left
        super().load_content()
        utils.set_music("e1m5", 0.15)
        self.background.set_surface(self.get_image("main-bg"))
        self._set_review_clues_button_visible(True)

scene_list.add_mission(E1M5Talk())
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
        
        for slice_item in [slice1, slice2, slice3, slice4]:
            slice_surface = slice_item.get_surface()
            if slice_surface:
                slice_surface.set_alpha(0)

        def allow_next():
            target1 = TargetMask(self, self.get_image("comic-tm"))
            target1.leftclick += lambda sender: game.scenes.set_scene("e1m6")
            self.entities["target1"] = target1 # type: ignore

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
