from engine import Scene, prefs, game
from app import utils, scene_list, defaults
from app.mission import Mission
from app.entities import *

import pygame

DT_PLACEHOLDER = "Select an option to view more details."

class InGameOptionsOverlay(Scene):
    def __init__(self):
        super().__init__("In-Game Overlay - Options")
        self.visible = False

    def set_visibility(self, is_visible):
        self.visible = is_visible

    def _update_desc(self, data):
        description = ""
        if "desc" in data["value"]:
            description = data["value"]["desc"]

        pref = self._get_pref(data)
        if pref:
            pref_value = prefs.default.get(pref)
            pref_value_string = "N/A"
            if pref_value == True:
                pref_value_string = "Enabled"
            elif pref_value == False:
                pref_value_string = "Disabled"
            value_string = "\n\nCurrent setting: {}".format(pref_value_string)
            description += value_string
        
        if description:
            self._details_text.set_text(description)
        else:
            self._details_text.set_text(DT_PLACEHOLDER)

    def _get_pref(self, data):
        pref = None
        if "pref" in data["value"]:
            pref = data["value"]["pref"]
        return pref

    def _listbox_on_marked(self, sender, data):
        self._update_desc(data)

    def _listbox_on_selected(self, sender, data):
        pref = self._get_pref(data)
        if pref:
            new_value = (not prefs.default.get(pref, True))
            prefs.default.set(pref, new_value)
        self._update_desc(data)

        refresh = False
        if "refresh" in data["value"]:
            refresh = data["value"]["refresh"]
        if refresh:
            game._init_display()

    def toggle_visibility(self):
        current_scene = game.scenes.get_scene()

        # Prevent the menu from showing up on situations where it's blocked.
        if isinstance(current_scene, Mission) and ( \
           current_scene.menu_blocked or \
           current_scene.emitter.current_dialog or \
           current_scene.emitter.current_selector):
            return

        if scene_list.all["ig_clues"].visible or \
           scene_list.all["ig_escmenu"].visible or \
           game.scenes._switching:
            return

        self.set_visibility(not self.visible)
        current_scene.enabled = (not self.visible)
        utils.set_cursor("default")

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
        btn_return = KeyedButton(self, (64, 64), "Return", pygame.K_TAB, "TAB")
        btn_return.leftclick += lambda sender: self.toggle_visibility()

        self._dataset = [
            {
                "text": "Toggle fullscreen",
                "value": {
                    "desc": "Set whether the game will occupy the\nfull screen or not.",
                    "pref": "app.display.fullscreen",
                    "refresh": True
                }
            },
            {
                "text": "Toggle smooth scaling",
                "value": {
                    "desc": "Set whether smooth scaling will be used.",
                    "pref": "app.display.use_smoothscale",
                    "refresh": True
                }
            },
            {
                "text": "Toggle resizable",
                "value": {
                    "desc": "Set whether the window can be resized.",
                    "pref": "app.display.resizable",
                    "refresh": True
                }
            },
            {
                "text": "Toggle dialog skip",
                "value": {
                    "desc": "Set whether dialog speeches can\nbe skipped.",
                    "pref": "game.dialog.can_skip",
                    "refresh": False
                }
            },
            {
                "text": "Toggle music",
                "value": {
                    "desc": "Set whether the game should play\nmusic.",
                    "pref": "audio.music.enabled",
                    "refresh": False
                }
            },
            {
                "text": "Toggle sound effects",
                "value": {
                    "desc": "Set whether the game should play\nsound effects.",
                    "pref": "audio.sfx.enabled",
                    "refresh": False
                }
            },
            {
                "text": "Toggle speech/voices",
                "value": {
                    "desc": "Set whether the game should play\nspeech dialogue.",
                    "pref": "audio.vox.enabled",
                    "refresh": False
                }
            }
        ]
        listbox = ListBox(self, (450, 95), "OPTIONS", self._dataset)
        listbox.marked += self._listbox_on_marked
        listbox.selected += self._listbox_on_selected

        self.entities = {
            "background": background,
            "hand": defaults.hand_left,
            "details_bg": details_bg,
            "details_text": self._details_text,
            "listbox_image": self._listbox_image,
            "btn_return": btn_return,
            "listbox": listbox,
        }

    def update(self, game, events):
        if self.visible:
            super().update(game, events)

    def draw(self, layer):
        if self.visible:
            super().draw(layer)

scene_list.all["ig_options"] = InGameOptionsOverlay()
