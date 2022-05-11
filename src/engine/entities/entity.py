import pygame

class Entity():
    def __init__(self, texture, size, position):
        self.set_texture(texture)
        if size:
            self.set_size(size)
        self._position = position

    def get_texture(self):
        return self._texture

    def set_texture(self, texture):
        self._texture_original = texture
        self._texture = texture
        self._size = texture.get_rect()

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size
        self._texture = pygame.transform.scale(self._texture_original, size)

    def get_position(self):
        return self._position

    def set_position(self, position):
        self._position = position

    def update(self):
        pass
        
    def draw(self, window):
        window.blit(self._texture, self._position)
