from engine import *
from app import utils, scene_list
from app.entities import *
from app.mission import Mission
from app.dialog import DialogSide, DialogFlags

import pygame

class E0MTestScene(Mission):
    def __init__(self):
        super().__init__(0, "test")

    def update(self, game, events):
        super().update(game, events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self._test_dialog()
                elif event.key == pygame.K_F2:
                    self._test_choices()
                elif event.key == pygame.K_F3:
                    self._test_note()
                elif event.key == pygame.K_F4:
                    pass
                elif event.key == pygame.K_F5:
                    pass
                break

    def draw(self, layer):
        super().draw(layer)

    def _test_note(self):
        notebg = Image(self, utils.load_ui_image("note-bg"), (5, 5))

        RECT_LISTBOX_TITLE = pygame.Rect(0, 0, 400, 84)

        title = Label(
            self, "ITEMS", utils.get_comic_font(32), pygame.Color("black"),
        )
        title.set_position((
            5 + (RECT_LISTBOX_TITLE.width / 2) - (title.get_rect().width / 2),
            5 + (RECT_LISTBOX_TITLE.height / 2) - (title.get_rect().height / 2)
        ))

        listitem1 = ListItem(
            self, (5, 89), {
                "text": "Pen",
                "value": "pen"
            }
        )
        listitem2 = ListItem(
            self, (5, 121), {
                "text": "Press Card",
                "value": "press-card"
            }
        )
        listitem3 = ListItem(
            self, (5, 153), {
                "text": "Wallet",
                "value": "wallet"
            }
        )

        data_title = "ITEMS"
        data = [
            {
                "text": "Pen",
                "value": "pen"
            },
            {
                "text": "Press Card",
                "value": "press-card"
            },
        ]

        listbox = ListBox(
            self,
            (400, 150),
            data_title,
            data
        )
        listbox2 = ListBox(
            self,
            (800, 150),
            data_title,
            data,
            True
        )

        self.entities = {
            #"notebg": notebg,
            #"title": title,
            #"listitem1": listitem1,
            #"listitem2": listitem2,
            #"listitem3": listitem3,
            "listbox": listbox,
            "listbox2": listbox2
        }

    def _test_dialog(self):
        self.emitter.add("joe", 1, callback=lambda:print("test"))
        self.emitter.add("joe", 2, "joe-faceright", flags=DialogFlags.CLOSEABLE)
        self.emitter.add("joe", 3)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.TOP_RIGHT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.MIDDLE_RIGHT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM_LEFT)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM)
        self.emitter.add("joe", 2, "joe-faceright", side=DialogSide.BOTTOM_RIGHT)

        print(self.get_string("joe", 1))
        print(utils.get_ep_string(1, 1, "joe", 1))
        #print(utils.get_item_string("pbadge"))

    def _test_choices(self):
        choice1 = ChoiceButton(
            self,
            (50, 50),
            1,
            "Luneta Park"
        )
        choice2 = ChoiceButton(
            self,
            (50, 125),
            2,
            "Congress"
        )
        choice3 = ChoiceButton(
            self,
            (50, 200),
            3,
            "Home"
        )

        choiceset = ChoiceSet(
            self,
            (350, 150),
            ["Luneta Park", "Congress", "Home"]
        )
        choiceset2 = ChoiceSet(
            self,
            (650, 150),
            ["Luneta Park", "Congress", "Home"],
            True
        )
        choiceset2 = ChoiceSet(
            self,
            (650, 150),
            [
                utils.load_ui_image("fda-fact"),
                utils.load_ui_image("fda-doubt"),
                utils.load_ui_image("fda-accuse")
            ],
            True,
            True,
            0
        )

        self.entities = {
            "choice1": choice1,
            "choice2": choice2,
            "choice3": choice3,
            "choiceset": choiceset,
            "choiceset2": choiceset2
        }

    def load_content(self):
        super().load_content()
        self.background.set_surface(utils.load_em_image(1, 1, "bg-main"))

scene_list.add_mission(E0MTestScene())
