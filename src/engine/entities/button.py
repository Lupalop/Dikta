from engine.entities import ClickableEntity, Label
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame

class Button(ClickableEntity):
    def __init__(self, bg_list, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)

        if not "normal" in bg_list:
            raise ValueError("A 'normal' state should be present in the specified button states.")

        self._bg_list = bg_list
        self._bg_current = "normal"

        is_zero_size = (self.get_size() == (0, 0))
        if is_zero_size:
            self._rect.size = self._bg_list[self._bg_current].get_size()    

        self.label = Label(text, font, color, (0, 0))
        self.entity_dirty(is_zero_size)

    @classmethod
    def from_entity(cls, entity, text, copy_handlers = False):
        if not text:
            text = entity.label.get_text()
        entity_copy = cls(entity._bg_list,
                          text,
                          entity.label.get_font(),
                          entity.label.get_color(),
                          entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    # Overridden base entity setter functions
    def entity_dirty(self, resize):
        if resize:
            self._mask = None
            for key in self._bg_list:
                surface = self._bg_list[key]
                surface_rz = pygame.transform.scale(surface, self._rect.size)
                self._bg_list[key] = surface_rz

        if not self.label:
            return

        label_pos = (self.get_rect().centerx - (self.label.get_rect().width / 2),
                     self.get_rect().centery - (self.label.get_rect().height / 2))
        self.label.set_position(label_pos)

    def get_surface(self):
        return self._bg_list[self._bg_current]

    def set_surface(self, texture):
        print("Changing the surface of a Button entity is not allowed.")

    # Event handlers
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
        if self.label:
            self.label.draw(layer)
