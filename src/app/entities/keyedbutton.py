from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app.entities import Label, Image
from app import utils

import pygame

KB_BACKGROUNDS = {
    "normal": utils.load_ui_image("btn_k_normal"),
    "hover": utils.load_ui_image("btn_k_hover"),
    "active": utils.load_ui_image("btn_k_active")
}

KB_RECT = pygame.Rect(0, 0, 250, 40)
KB_KEY_RECT = pygame.Rect(3, 3, 70, 34)
KB_MAIN_RECT = pygame.Rect(73, 3, 174, 34)

FONT_SIZE = 28

class KeyedButton(ClickableEntity):
    def __init__(self, owner, position = (0, 0), main_text = "", key = None, key_text = ""):
        super().__init__(owner, position, size=KB_RECT.size, tor = False)

        self.main_text = main_text
        self.key_text = key_text
        self.key = key

        self._bg_current = "normal"
        self._redraw_surface()

    def _redraw_surface(self):
        self._bg_list = {}
        for key in KB_BACKGROUNDS:
            surface = pygame.Surface(KB_RECT.size, pygame.SRCALPHA, 32)

            base_bg = Image(
                self.owner,
                KB_BACKGROUNDS[key]
            )
            base_bg.draw(surface)
            label_key = Label(
                self.owner,
                self.key_text,
                utils.get_font(FONT_SIZE),
                pygame.Color("white")
            )
            label_key.set_position((
                KB_KEY_RECT.x + (KB_KEY_RECT.width / 2) - (label_key.get_rect().width / 2),
                KB_KEY_RECT.y + (KB_KEY_RECT.height / 2) - (label_key.get_rect().height / 2)
            ))
            label_key.draw(surface)
            label_main = Label(
                self.owner,
                self.main_text,
                utils.get_font(FONT_SIZE),
                pygame.Color("white")
            )
            label_main.set_position((
                KB_MAIN_RECT.x + (KB_MAIN_RECT.width / 2) - (label_main.get_rect().width / 2),
                KB_MAIN_RECT.y + (KB_MAIN_RECT.height / 2) - (label_main.get_rect().height / 2)
            ))
            label_main.draw(surface)

            self._bg_list[key] = surface

    # Overridden base entity setter functions
    def _on_entity_dirty(self, resize):
        self.entity_dirty(self, resize)

    def get_surface(self):
        return self._bg_list[self._bg_current]

    def set_surface(self, texture):
        print("Changing the surface of a KeyedButton entity is not allowed.")

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.HOVER:
            self._bg_current = "hover"
        elif state == ClickState.ACTIVE:
            self._bg_current = "active"
        else:
            self._bg_current = "normal"

        super()._on_state_changed(state)

    def update(self, game, events):
        super().update(game, events)
        # Ignore if we don't have a key.
        if not self.key:
            return
        # Simulate a left mouse click if our key got pressed.
        for event in events:
            if event.type == pygame.KEYUP and \
               event.key == self.key:
                self._on_click(MouseButton.LEFT)
