from engine.entities import ClickableEntity, Label
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame

class LabelButton(ClickableEntity):
    def __init__(self, owner, label, position_or_rect = (0, 0), size = None):
        super().__init__(owner, position_or_rect, size)
        self.set_label(label)
        self._on_entity_dirty(True)
        self.hit_rect = True

    @classmethod
    def from_entity(cls, owner, entity, text, copy_handlers = False):
        label = Label.from_entity(owner, entity.get_label())
        if text:
            label.set_text(text)
        entity_copy = cls(owner,
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
            self._rect.size = self.get_label().get_size()
            self._mask = None

        if self.get_label():
            self.get_label().set_position(self.get_position())

        self.entity_dirty(self, resize)

    def get_surface(self):
        return self.get_label().get_surface()

    def set_surface(self, texture):
        print("Changing the surface of a LabelButton entity is not allowed.")

    def draw(self, layer):
        super().draw(layer)
