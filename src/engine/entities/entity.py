import pygame

class Entity():
    def __init__(self, position_or_rect, size):
        self._rect = pygame.Rect(0, 0, 0, 0)
        position = position_or_rect

        if isinstance(position_or_rect, pygame.Rect):
            position = (position_or_rect.x, position_or_rect.y)
            size = position_or_rect.size

        self._rect.x = position[0]
        self._rect.y = position[1]
        if size:
            self._rect.size = size

    def get_size(self):
        return self._rect.size

    def set_size(self, size):
        self._rect.size = size

    def get_rect(self):
        return self._rect

    def set_rect(self, rect):
        self._rect = rect

    def get_position(self):
        return (self._rect.x, self._rect.y)

    def set_position(self, position):
        self._rect.x = position[0]
        self._rect.y = position[1]

    def update(self, game, events):
        pass
        
    def draw(self, layer):
        pass
