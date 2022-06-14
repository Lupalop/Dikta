from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app.entities import Label
from app import utils

import pygame

class Button(ClickableEntity):
    def __init__(self, owner, bg_list, label, position_or_rect = (0, 0), size = None):
        super().__init__(owner, position_or_rect, size)

        if not "normal" in bg_list:
            raise ValueError("A 'normal' state should be present in the specified button states.")

        self._bg_list = bg_list
        self._bg_current = "normal"

        is_zero_size = (self.get_size() == (0, 0))
        if is_zero_size:
            self._rect.size = self._bg_list[self._bg_current].get_size()    

        self.set_label(label)
        self._on_entity_dirty(is_zero_size)

    @classmethod
    def from_entity(cls, owner, entity, text, copy_handlers = False):
        label = Label.from_entity(owner, entity.get_label())
        if text:
            label.set_text(text)
        entity_copy = cls(owner,
                          entity._bg_list,
                          label,
                          entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    # Label
    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label
        self._label.entity_dirty += self._on_label_dirty

    def _on_label_dirty(self, sender, resize):
        if not resize:
            return
        self._on_entity_dirty(resize)

    # Overridden base entity setter functions
    def _on_entity_dirty(self, resize):
        if resize:
            self._mask = None
            for key in self._bg_list:
                surface = self._bg_list[key]
                surface_rz = pygame.transform.scale(surface, self._rect.size)
                self._bg_list[key] = surface_rz

        if self.get_label():
            label_pos = (self.get_rect().centerx - (self.get_label().get_rect().width / 2),
                         self.get_rect().centery - (self.get_label().get_rect().height / 2))
            self.get_label().set_position(label_pos)

        self.entity_dirty(self, resize)

    def get_surface(self):
        return self._bg_list[self._bg_current]

    def set_surface(self, texture):
        print("Changing the surface of a Button entity is not allowed.")

    # Event handlers
    def _on_click(self, button):
        super()._on_click(button)
        utils.play_sfx("click")

    def _on_state_changed(self, state):
        if state == ClickState.HOVER and \
           "hover" in self._bg_list:
            self._bg_current = "hover"
        elif state == ClickState.ACTIVE and \
             "active" in self._bg_list:
            self._bg_current = "active"
        elif state == ClickState.RELEASED:
            pass
        else:
            self._bg_current = "normal"
        super()._on_state_changed(state)

    def draw(self, layer):
        super().draw(layer)
        if self.get_label():
            self.get_label().draw(layer)
