import pygame

class TextureSprite():
    def __init__(self, texture, size = None):
        self.set_texture(texture)
        if size:
            self.set_size(size)

    def get_texture(self):
        return self._texture

    def set_texture(self, texture):
        self._texture_base = texture
        self._texture = texture
        self._size_base = texture.get_rect()
        self._size = texture.get_rect()

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size
        self._texture = pygame.transform.scale(self._texture_base, size)

    def reset(self):
        self._texture = self._texture_base
        self._size = self._size_base
