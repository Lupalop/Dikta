from engine.event_handler import EventHandler

import pygame

# Defines the base class for entities.
class Entity:
    def __init__(self, position_or_rect = (0, 0), target_size = None, surface = None):
        # Initialize this entity instance
        self._surface = surface
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._mask = None
        position = position_or_rect
        size = target_size
        # Populate position and size values if we're given a rectangle
        if isinstance(position_or_rect, pygame.Rect):
            position = (position_or_rect.x, position_or_rect.y)
            size = position_or_rect.size
        # Update rectangle position
        self._rect.x = position[0]
        self._rect.y = position[1]
        # Update rectangle size with the correct value
        if size and size != (0, 0):
            self._rect.size = size
            # Resize surface to given size if available
            if surface:
                self._surface = pygame.transform.scale(surface, self._rect.size)
        # Assume surface size if the entity is sized to zero
        elif surface:
            self._rect.size = surface.get_rect().size
        self.entity_dirty = EventHandler()

    @classmethod
    def from_entity(cls, entity):
        return cls(entity.get_surface(), entity._rect)

    def _on_entity_dirty(self, resize):
        if resize:
            self._surface = pygame.transform.scale(self.get_surface(), self._rect.size)
            self._mask = None

        self.entity_dirty(self, resize)

    def get_size(self):
        return self._rect.size

    def set_size(self, size, resize = True):
        self._rect.size = size
        self._on_entity_dirty(resize)

    def get_rect(self):
        return self._rect

    def set_rect(self, rect, resize = True):
        self._rect = rect
        self._on_entity_dirty(resize)

    def get_position(self):
        return (self._rect.x, self._rect.y)

    def set_position(self, position):
        self._rect.x = position[0]
        self._rect.y = position[1]
        self._on_entity_dirty(False)

    def get_surface(self):
        return self._surface

    def set_surface(self, surface, resize = True):
        self._surface = surface
        if resize:
            self._rect.size = surface.get_rect().size
            self._mask = None

    def get_mask(self):
        if self.get_surface() and not self._mask:
            self._mask = pygame.mask.from_surface(self.get_surface(), 0)
        return self._mask

    def intersects(self, point, use_rect = False):
        if use_rect:
            return self._rect.collidepoint(point)

        maskPosition = point[0] - self._rect.x, point[1] - self._rect.y
        return self._rect.collidepoint(point) and \
               self.get_mask().get_at(maskPosition)

    def update(self, game, events):
        pass

    def draw(self, layer):
        if self.get_surface():
            layer.blit(self.get_surface(), self._rect)
