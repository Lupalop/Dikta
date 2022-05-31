from engine.entities import Entity, Image, Label, ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame

class Button(ClickableEntity):
    def __init__(self, button_states, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)

        if not "normal" in button_states:
            raise ValueError("A 'normal' state should be present in the specified button states.")

        self._button_states = button_states

        self._imageset = {}
        for key in button_states:
            surface = button_states[key]
            self._imageset[key] = Image(surface, position_or_rect, size)

        self._image = self._imageset["normal"]

        is_zero_size = (self.get_size() == (0, 0))
        if is_zero_size:
            self._rect.size = self._image.get_size()    

        self._label = Label(text, font, color, (0, 0))
        self._entity_dirty(is_zero_size)

    @classmethod
    def from_entity(cls, entity):
        return self.from_button(entity, entity._label.get_text())

    @classmethod
    def from_button(cls, entity, text, copy_handlers = False):
        entity_copy = cls(entity._button_states,
                          text,
                          entity._label.get_font(),
                          entity._label.get_color(),
                          entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    def get_surface(self):
        return self._image.get_surface()

    def set_surface(self, surface):
        print("Changing the surface of a Button entity is not allowed.")

    def get_mask(self):
        return self._image.get_mask()

    def intersects_rect(self, point):
        return self._image.intersects_rect(point)

    def intersects_mask(self, point):
        return self._image.intersects_mask(point)

    # Overridden base entity setter functions
    def _entity_dirty(self, is_position_only = False):
        if is_position_only:
            for image in self._imageset.values():
                image.set_position(self.get_position())
        else:
            for image in self._imageset.values():
                image.set_size(self.get_size())
                image.set_position(self.get_position())

        if not self._label:
            return

        label_pos = (self._image.get_rect().centerx - (self._label.get_rect().width / 2),
                     self._image.get_rect().centery - (self._label.get_rect().height / 2))
        self._label.set_position(label_pos)

    def set_size(self, size):
        super().set_size(size)
        self._entity_dirty()

    def set_rect(self, rect):
        super().set_rect(rect)
        self._entity_dirty()

    def set_position(self, position):
        super().set_position(position)
        self._entity_dirty(True)

    # Label
    def get_text(self):
        return self._label.get_text()

    def set_text(self, text):
        self._label.set_text(text)

    def get_font(self):
        return self._label.get_font()

    def set_font(self, font):
        self._label.set_font(font)

    def get_color(self):
        return self._label.get_color()

    def set_color(self, color):
        self._label.set_color(color)

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.HOVER and \
           "hover" in self._imageset:
            self._image = self._imageset["hover"]
        elif state == ClickState.ACTIVE and \
             "active" in self._imageset:
            self._image = self._imageset["active"]
        elif state == ClickState.RELEASED:
            pass
        else:
            self._image = self._imageset["normal"]
        super()._on_state_changed(state)

    def draw(self, layer):
        self._image.draw(layer)
        self._label.draw(layer)
