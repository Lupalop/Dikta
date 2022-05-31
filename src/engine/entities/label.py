from . import *

import pygame

class Label(Entity):
    def __init__(self, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)
        self._font = font
        self._color = color
        self._text = text
        if not font or not color or not text:
            self._surface = None
            return
        self._on_entity_dirty()

    @classmethod
    def from_entity(cls, entity):
        return cls(entity._text, entity._font, entity._color, entity._rect)

    def _on_entity_dirty(self, resize = True):
        rendered_text = self._font.render(self._text, self._color)
        self._surface = rendered_text[0]

        if resize:
            self._mask = None
            self._rect.size = rendered_text[1].size

        self.entity_dirty(self, resize)

    def get_surface(self):
        return self._surface

    def set_surface(self, texture):
        print("Changing the surface of a Label entity is not allowed.")

    def set_text(self, text):
        self._text = text
        self._on_entity_dirty()

    def get_text(self):
        return self._text

    def get_font(self):
        return self._font

    def set_font(self, font):
        self._font = font
        self._on_entity_dirty()

    def set_color(self, color):
        self._color = color
        self._on_entity_dirty(False)

    def get_color(self):
        return self._color

    def draw(self, layer):
        if not self.get_surface():
            return

        layer.blit(self.get_surface(), self._rect)
