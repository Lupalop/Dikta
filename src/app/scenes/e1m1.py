from engine import *
from app import defaults, scene_list
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

# E1M1 - Introduction

class E1M1Scene(Mission):
    def __init__(self):
        super().__init__(1, 1, "", "", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.emitter.add("joe", "intro1", repeat = False)
        self.emitter.add("joe", "intro2", callback=lambda: game.scenes.set_scene("e1m1desk_outside"))

        self.background.set_surface(self.get_image("bg-joe"))

scene_list.add_mission(E1M1Scene())

# E1M1 - Desk - Outside

class E1M1DeskOutside(Mission):
    def __init__(self):
        super().__init__(1, 1, "desk_outside", "Desk - Outside", DialogSide.BOTTOM)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("bg-main"))
        self.emitter.add("tut", "hovercursor", repeat = False)

        target1 = TargetMask(self, self.get_image("tm-main-bulletinboard"))
        target1.leftclick += lambda sender: self.emitter.add("joe", "target_board", "joe-faceright")

        target2 = TargetMask(self, self.get_image("tm-main-newspapers"))
        target2.leftclick += lambda sender: self.emitter.add("joe", "newspapers", "joe-faceright")

        target3 = TargetMask(self, self.get_image("tm-main-joe"))
        target3.leftclick += lambda sender: self.emitter.add("joe", ["joe", "tut2"], "joe-faceright")

        target4 = TargetMask(self, self.get_image("tm-main-nmdesk"))
        target4.leftclick += lambda sender: self.emitter.add("joe", "nmdesk", "joe-faceright")

        target5 = TargetMask(self, self.get_image("tm-main-desk"))
        target5.leftclick += lambda sender: game.scenes.set_scene("e1m1desk_inside")

        target6 = TargetMask(self, self.get_image("tm-main-light"))
        target6.leftclick += lambda sender: self.emitter.add("joe", ["light1", "light2"], "joe-faceright")

        self.entities = {
            "target1": target1,
            "target2": target2,
            "target3": target3,
            "target4": target4,
            "target5": target5,
            "target6": target6,
        }

        if len(self.get_items()) > 0:
            self.emitter.add("joe", "exit", flags = DialogFlags.SKIPPABLE)
            def _handle_choice(sender, value):
                # Choice 1: Leave
                if value[0] == 1:
                    game.scenes.set_scene("e1m2intermezzo")
                # Choice 2: Stay
                else:
                    self.emitter.add("joe", "return")
                self.emitter.next()
            self.emitter.current_selector = ChoiceSet(self, (64, 64), ["Leave the office", "Stay here"], True)
            self.emitter.current_selector.selected += _handle_choice
            self.emitter.current_selector.hidden += self.emitter.clear_choiceset

scene_list.add_mission(E1M1DeskOutside())

# E1M1 - Desk - Inside (HO)

class E1M1DeskInside(Mission):
    def __init__(self):
        super().__init__(1, 1, "desk_inside", "Desk - Inside", DialogSide.TOP)

    def load_content(self):
        super().load_content()
        self.background.set_surface(self.get_image("bg-desk"))
        self.emitter.add("tut", "rightclickreturn", repeat = False)
        self.emitter.add("joe", "desk", "joe-faceright", repeat = False)
        self.entities = {}

        self.return_scene = "e1m1desk_outside"
        target_escape = TargetMask(self, self.get_image("tm-desk"), zoomin = False)
        target_escape.click += lambda sender, button: game.scenes.set_scene(self.return_scene)
        self.entities["target_escape"] = target_escape

        item1 = TargetItem(self, self.get_image("item-stapler"), (263, 19), removable = False)
        item1.leftclick += lambda sender: self.emitter.add("joe", "item_stapler", "joe-faceright")
        self.entities["item_stapler"] = item1

        if not self.exists_item("wallet"):
            item2 = TargetItem(self, self.get_image("item-wallet"), (320, 120))
            self.attach_item(item2, "wallet")
            item2.leftclick += lambda sender: self.emitter.add("joe", "item_wallet", "joe-faceright")
            self.entities["item_wallet"] = item2

        item3 = TargetItem(self, self.get_image("item-reports"), (160, 130), removable = False)
        item3.leftclick += lambda sender: self.emitter.add("joe", "item_reports", "joe-faceright")
        self.entities["item_reports"] = item3

        item4 = TargetItem(self, self.get_image("item-typewriter"), (386, 10), removable = False, grabbable = False)
        item4.leftclick += lambda sender: self.emitter.add("joe", "item_typewriter", "joe-faceright")
        self.entities["item_typewriter"] = item4

        if not self.exists_item("press-card"):
            item5 = TargetItem(self, self.get_image("item-press-card"), (26, 302))
            item5.leftclick += lambda sender: game.scenes.set_scene("e1m1popup_presscard")
            self.entities["item_press_card"] = item5

        item6 = TargetItem(self, self.get_image("item-papers"), (916, 363), removable = False, grabbable = False)
        item6.leftclick += lambda sender: self.emitter.add("joe", "item_papers", "joe-faceright")
        self.entities["item_papers"] = item6

        item7 = TargetItem(self, self.get_image("item-mail"), (1050, 109), removable = False, grabbable = False)
        def item7_leftclick(sender):
            if not self.exists_item("note"):
                game.scenes.set_scene("e1m1popup_note")
            else:
                self.emitter.add("joe", "item_mail", "joe-faceright")
        item7.leftclick += item7_leftclick
        self.entities["item_mail"] = item7

        item8 = TargetItem(self, self.get_image("item-pencils"), (994, 318), removable = False)
        def item8_leftclick(sender):
            if self.exists_item("pen"):
                self.emitter.add("joe", "item_pencils_empty", "joe-faceright")
            else:
                self.add_item("pen")
                self.emitter.add("joe", "item_pencils", "joe-faceright")
        item8.leftclick += item8_leftclick
        self.entities["item_pencils"] = item8

        if not self.exists_item("journal"):
            item9 = TargetItem(self, self.get_image("item-journal"), (1139, 601))
            self.attach_item(item9, "journal")
            item9.leftclick += lambda sender: self.emitter.add("joe", "item_journal", "joe-faceright")
            self.entities["item_journal"] = item9

        drawer = TargetMask(self, self.get_image("tm-desk-drawer"))
        def drawer_leftclick(sender):
            if self.exists_item("flashlight"):
                self.emitter.add("joe", "drawer_empty", "joe-faceright")
            else:
                game.scenes.set_scene("e1m1popup_flashlight")
        drawer.leftclick += drawer_leftclick
        self.entities["drawer"] = drawer

scene_list.add_mission(E1M1DeskInside())

# E1M1 - Popup - Press Card

class E1M1PopupPressCardScene(Mission):
    def __init__(self):
        super().__init__(1, 1, "popup_presscard", "Popup - Press Card", DialogSide.TOP)

    def load_content(self):
        super().load_content()

        self.emitter.add("tut", "rightclickreturn", repeat = False)

        if not self.exists_item("press-card"):
            self.add_item("press-card")

        self.background.set_surface(self.get_image("bg-item"))

        hand = Image.from_entity(self, defaults.hand_right)
        item_press_card = TargetItem(
            self,
            self.get_image("item-press-card-popup"),
            (374, 198),
            removable = False
        )
        item_press_card.leftclick += lambda sender: self.emitter.add("joe", "item_press_card", "joe-faceright")

        self.return_scene = "e1m1desk_inside"
        target_escape = TargetMask(self, self.get_image("tm-popup-pcard"), zoomin = False)
        target_escape.click += lambda sender, button: game.scenes.set_scene(self.return_scene)

        self.entities = {
            "target_escape": target_escape,
            "hand": hand,
            "item_press_card": item_press_card,
        }

scene_list.add_mission(E1M1PopupPressCardScene())

# E1M1 - Popup - Note

class E1M1PopupNoteScene(Mission):
    def __init__(self):
        super().__init__(1, 1, "popup_note", "Popup - Note", DialogSide.TOP)

    def load_content(self):
        super().load_content()

        self.emitter.add("tut", "rightclickreturn", repeat = False)

        if not self.exists_item("note"):
            self.add_item("note")

        self.background.set_surface(self.get_image("bg-item"))

        hand = Image.from_entity(self, defaults.hand_right)
        item_note = TargetItem(
            self,
            self.get_image("item-note-popup"),
            (467, 170),
            removable = False
        )
        item_note.leftclick += lambda sender: self.emitter.add("joe", "item_note", "joe-faceright")

        self.return_scene = "e1m1desk_inside"
        target_escape = TargetMask(self, self.get_image("tm-popup-note"), zoomin = False)
        target_escape.click += lambda sender, button: game.scenes.set_scene(self.return_scene)

        self.entities = {
            "target_escape": target_escape,
            "hand": hand,
            "item_note": item_note,
        }

scene_list.add_mission(E1M1PopupNoteScene())

# E1M1 - Popup - Flashlight

class E1M1PopupFlashlightScene(Mission):
    def __init__(self):
        super().__init__(1, 1, "popup_flashlight", "Popup - Flashlight", DialogSide.TOP)

    def load_content(self):
        super().load_content()

        self.emitter.add("tut", "rightclickreturn", repeat = False)

        if not self.exists_item("flashlight"):
            self.add_item("flashlight")

        self.background.set_surface(self.get_image("bg-drawer"))

        hand = Image.from_entity(self, defaults.hand_right)
        item_flashlight = TargetItem(
            self,
            self.get_image("item-flashlight-popup"),
            (372, 74),
            removable = False
        )
        item_flashlight.leftclick += lambda sender: self.emitter.add("joe", "item_flashlight", "joe-faceright")

        self.return_scene = "e1m1desk_inside"
        target_escape = TargetMask(self, self.get_image("tm-popup-flashlight"), zoomin = False)
        target_escape.click += lambda sender, button: game.scenes.set_scene(self.return_scene)

        self.entities = {
            "target_escape": target_escape,
            "hand": hand,
            "item_flashlight": item_flashlight,
        }

scene_list.add_mission(E1M1PopupFlashlightScene())
