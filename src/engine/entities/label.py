from . import *

import pygame

class Label(Entity):
    def __init__(self, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)
        self._font = font
        self._color = color
        self._text = text
        self._update_surface()

    def _update_surface(self, compute_size = True):
        self._surface = self._font.render(self._text, True, self._color, None)
        if compute_size:
            self._mask = pygame.mask.from_surface(self._surface)
            if self._rect.size == (0, 0):
                self.set_size(self._font.size(self._text))

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

    def set_color(self, color):
        self._color = color
        self._update_surface(False)

    def get_color(self):
        return self._color

    def intersects_point(self, point):
        maskPosition = point[0] - self._rect.x, point[1] - self._rect.y
        return self._rect.collidepoint(point) and \
               self._mask.get_at(maskPosition)

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
