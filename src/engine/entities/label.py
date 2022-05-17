from . import *

import pygame

class Label(Entity):
    def __init__(self, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)
        self._font = font
        self._color = color
        self._text = text
        self._update_surface()

    @classmethod
    def from_entity(cls, entity):
        return cls(entity._text, entity._font, entity._color, entity._rect)

    def _update_surface(self, compute_size = True):
        rendered_text = self._font.render(self._text, self._color)
        self._surface = rendered_text[0]
        if compute_size:
            self._mask = pygame.mask.from_surface(self._surface, 0)
            if self._rect.size == (0, 0):
                self.set_size(rendered_text[1].size)

    def get_surface(self):
        return self._surface

    def set_surface(self, texture):
        print("Changing the surface of a Label entity is not allowed.")

    def get_mask(self):
        return self._mask

    def set_text(self, text):
        self._text = text
        self._update_surface()

    def get_text(self):
        return self._text

    def get_font(self):
        return self._font

    def set_font(self, font):
        self._font = font
        self._update_surface()

    def set_color(self, color):
        self._color = color
        self._update_surface(False)

    def get_color(self):
        return self._color

    def intersects_mask(self, point):
        maskPosition = point[0] - self._rect.x, point[1] - self._rect.y
        return self._rect.collidepoint(point) and \
               self._mask.get_at(maskPosition)

    def intersects_rect(self, point):
        return self._rect.collidepoint(point)

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
