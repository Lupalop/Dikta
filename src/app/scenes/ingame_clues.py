from engine import prefs, game
from engine.overlay import Overlay
from app import utils, scene_list, defaults
from app.mission import Mission
from app.entities import ListBox, Image, Label, KeyedButton

import pygame

DT_PLACEHOLDER = "Select a clue to view more details."

class InGameCluesOverlay(Overlay):
    def __init__(self):
        super().__init__("In-Game Overlay - Clues")

    def _listbox_on_marked(self, sender, data):
        value = data["value"]
        description = None
        if value and "desc" in value:
            description = value["desc"]
        if description:
            self._details_text.set_text(description)
        else:
            self._details_text.set_text(DT_PLACEHOLDER)

        image = None
        if value and "image" in value:
            image = value["image"]
        if image:
            self._listbox_image.set_surface(utils.load_clue_image(image))
            self._listbox_image.hidden = False
        else:
            self._listbox_image.hidden = True

    def toggle_visibility(self):
        current_scene = game.scenes.get_scene()

        # Prevent the menu from showing up on regular scenes.
        if not isinstance(current_scene, Mission):
            return
        # Prevent the menu from showing up on situations where it's blocked.
        if current_scene.menu_blocked or \
           current_scene.emitter.current_dialog or \
           scene_list.all["ig_escmenu"].visible or \
           scene_list.all["ig_options"].visible or \
           game.scenes._switching:
            return

        super().toggle_visibility()
        utils.reset_cursor()

        dataset = current_scene.get_clues_dataset()
        listbox = ListBox(self, (450, 95), "CLUES", dataset)
        listbox.marked += self._listbox_on_marked
        self.entities["listbox_items"] = listbox

    def load_content(self):
        bg_solid = pygame.Surface(prefs.default.get("app.display.layer_size", (0, 0)))
        bg_solid.fill(pygame.Color("black"))
        bg_solid.set_alpha(100)
        background = Image(
            self,
            bg_solid,
            (0, 0))
        details_bg = Image(
            self,
            utils.load_ui_image("note-details-bg"),
            (870, 95))
        self._details_text = Label(
            self,
            DT_PLACEHOLDER,
            utils.get_comic_font(24),
            pygame.Color("white"),
            (895, 125))
        self._listbox_image = Image(
            self,
            None,
            (745, 525))
        btn_return = KeyedButton(self, (64, 64), "Return", pygame.K_F12, "TAB")
        btn_return.leftclick += lambda sender: self.toggle_visibility()

        self.entities = {
            "background": background,
            "hand": defaults.hand_left,
            "listbox_items": None,
            "details_bg": details_bg,
            "details_text": self._details_text,
            "listbox_image": self._listbox_image,
            "btn_return": btn_return,
        }

    def update(self, game, events):
        if not self.visible:
            return

        super().update(game, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.toggle_visibility()
                    break
            if event.type == pygame.MOUSEBUTTONUP and \
               event.button == pygame.BUTTON_RIGHT and \
               self.visible:
                self.toggle_visibility()
                break

scene_list.all["ig_clues"] = InGameCluesOverlay()
