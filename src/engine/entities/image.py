from . import *

import pygame

class Image(Entity):
    def __init__(self, surface, position_or_rect, size = None):
        super().__init__(position_or_rect, size)
        self._surface_base = surface
        self._size_base = surface.get_rect().size
        self._surface = self._surface_base
        if self._rect.size == (0, 0):
            self._rect.size = self._size_base
        else:
            self._surface = pygame.transform.scale(self._surface_base, self._rect.size)
        self._update_mask()

    @classmethod
    def from_entity(cls, entity):
        return cls(entity._surface_base, entity._rect)

    def get_surface(self):
        return self._surface

    def set_surface(self, surface):
        self._surface_base = surface
        self._size_base = surface.get_rect().size
        self.reset()

    def get_mask(self):
        return self._mask

    def _update_mask(self):
        self._mask = pygame.mask.from_surface(self._surface, 0)

    def set_size(self, size):
        super().set_size(size)
        self._surface = pygame.transform.scale(self._surface_base, size)
        self._update_mask()

    def reset(self):
        self._surface = self._surface_base
        self._rect.size = self._size_base
        self._update_mask()

    def intersects_mask(self, point):
        maskPosition = point[0] - self._rect.x, point[1] - self._rect.y
        return self._rect.collidepoint(point) and \
               self._mask.get_at(maskPosition)

    def intersects_rect(self, point):
        return self._rect.collidepoint(point)

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
