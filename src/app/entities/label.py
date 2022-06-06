from engine import Entity

import pygame

class Label(Entity):
    def __init__(self, owner, text, font, color, position_or_rect = (0, 0), size = None):
        super().__init__(owner, position_or_rect, size)
        self._font = font
        self._color = color
        self._text = text
        self.line_height = 13
        if not font or not color or not text:
            self._surface = None
            return
        self._on_entity_dirty()

    @classmethod
    def from_entity(cls, owner, entity):
        return cls(owner, entity._text, entity._font, entity._color, entity._rect)

    def _reset_placeholder_suface(self):
        self._surface = pygame.Surface(self._render_size, pygame.SRCALPHA, 32)

    def _render_lines(self):
        # XXX For now, we'll just check for the presence of newline
        # characters as markers for breaking.
        textlines = self._text.split("\n")
        self._renders = []
        height = 0
        width = 0

        # Render each line of text and adjust the line height
        for i in range(len(textlines)):
            text_render = self._font.render(textlines[i], self._color)
            text_render[1].y = 0
            text_render[1].x = 0
            if i >= 1 and i < len(textlines):
                height += self.line_height
                text_render[1].y = height
            self._renders.append(text_render)
            height += text_render[1].height
            if text_render[1].width > width:
                width = text_render[1].width

        self._render_size = (width, height)
        self._reset_placeholder_suface()

    def _blit_lines(self):
        for text_render in self._renders:
            self._surface.blit(text_render[0], text_render[1])

    def _on_entity_dirty(self, resize = True):
        self._render_lines()
        self._blit_lines()

        if resize:
            self._mask = None
            self._rect.size = self._render_size

        self.entity_dirty(self, resize)

    def get_surface(self):
        return self._surface

    def set_surface(self, texture):
        print("Changing the surface of a Label entity is not allowed.")

    def set_text(self, text):
        self._text = text
        self._on_entity_dirty()

    def get_text(self):
        return self._text

    def get_font(self):
        return self._font

    def set_font(self, font):
        self._font = font
        self._on_entity_dirty()

    def set_color(self, color):
        self._color = color
        self._on_entity_dirty(False)

    def get_color(self):
        return self._color
