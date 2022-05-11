import pygame

class Entity():
    def __init__(self, position, size = None):
        if size:
            self.set_size(size)
        self._position = position

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def update(self):
        pass
        
    def draw(self, window):
        pass
