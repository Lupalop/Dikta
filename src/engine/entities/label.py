from . import *

import pygame

class Label(Entity):
    def __init__(self, text, font, color, position, size = None):
        self._sprite = TextSprite(text, font, color)
        super().__init__(position, size)

    def get_size(self):
        return self._sprite.get_size()

    def set_size(self, size):
        pass

    def get_texture(self):
        return self._sprite.get_texture()

    def set_texture(self, texture):
        pass

    def set_text(self, text):
        self._sprite.set_text(text)

    def get_text(self):
        return self._sprite.get_text()

    def set_color(self, color):
        self._sprite.set_color(color)

    def get_color(self):
        return self._sprite.get_color()

    def get_sprite(self):
        return self._sprite

    def draw(self, window):
        window.blit(self._sprite.get_texture(), self._position)
