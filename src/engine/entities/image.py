from . import *

import pygame

class Image(Entity):
    def __init__(self, texture, position, size = None):
        self._sprite = TextureSprite(texture, size)
        super().__init__(position, size)

    def get_size(self):
        return self._sprite.get_size()

    def set_size(self, size):
        self._sprite.set_size(size)

    def get_texture(self):
        return self._sprite.get_texture()

    def set_texture(self, texture):
        self._sprite.set_texture(texture)

    def get_sprite(self):
        return self._sprite

    def draw(self, window):
        window.blit(self._sprite.get_texture(), self._position)
