import pygame

class TextSprite():
    def __init__(self, text, font, color):
        self._font = font
        self._color = color
        self._text = text
        self._update_texture()

    def _update_texture(self, compute_size = True):
        self._texture = self._font.render(self._text, True, self._color, None)
        self._mask = pygame.mask.from_surface(self._texture)
        if compute_size:
            self._size = self._font.size(self._text)

    def get_texture(self):
        return self._texture

    def get_mask(self):
        return self._mask

    def set_text(self, text):
        self._text = text
        self._update_texture()

    def get_text(self):
        return self._text

    def set_color(self, color):
        self._color = color
        self._update_texture(False)

    def get_color(self):
        return self._color

    def get_size(self):
        return self._size
