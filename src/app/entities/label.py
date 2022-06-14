from engine import Entity

import pygame

class Label(Entity):
    def __init__(self, owner, text, font, color, position_or_rect = (0, 0), size = None, outline_color = (0, 0, 0), outline_width = 0, ignore_newline = False):
        super().__init__(owner, position_or_rect, size)
        self._font = font
        self._color = color
        self._text = text
        self._outline_color = outline_color
        self._outline_width = outline_width
        self._outline_padding = (2 * outline_width)
        self.line_height = 13
        self.ignore_newline = ignore_newline
        if not font or not color or not text:
            self._surface = None
            return
        self._on_entity_dirty()

    @classmethod
    def from_entity(cls, owner, entity):
        return cls(owner, entity._text, entity._font, entity._color, entity._rect)

    _circle_cache = {}

    @classmethod
    def _get_circle_points(cls, width):
        width = int(round(width))
        if width in cls._circle_cache:
            return cls._circle_cache[width]
        x = width
        y = 0
        e = 1 - width
        points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        cls._circle_cache[width] = points
        return points

    def _reset_placeholder_suface(self):
        self._surface = pygame.Surface(self._render_size, pygame.SRCALPHA, 32)

    def _render_lines(self):
        # XXX For now, we'll just check for the presence of newline
        # characters as markers for breaking.
        textlines = None
        if self.ignore_newline:
            textlines = [self._text.replace("\n", "")]
        else:
            textlines = self._text.split("\n")
        self._renders = []
        self._outline_renders = []
        height = 0
        width = 0

        # Render each line of text and adjust the line height
        for i in range(len(textlines)):
            text_render = self._font.render(textlines[i], self._color)
            text_render[1].y = self._outline_width
            text_render[1].x = self._outline_width
            # Add spacing between lines only if we're not the last line
            if i >= 1 and i < len(textlines):
                height += self.line_height
                text_render[1].y = height + self._outline_width
            # Adjust label surface dimensions
            height += text_render[1].height
            if text_render[1].width > width:
                width = text_render[1].width
            # Render a copy for the outline only if we have a non-zero width
            if self._outline_width > 0:
                text_outline_render = self._font.render(
                    textlines[i],
                    self._outline_color
                )
                text_outline_render[1].x = text_render[1].x
                text_outline_render[1].y = text_render[1].y
                self._outline_renders.append(text_outline_render)
            # Append the rendered regular text
            self._renders.append(text_render)

        self._render_size = (
            width + self._outline_padding,
            height + self._outline_padding
        )
        self._reset_placeholder_suface()

    def _blit_lines(self):
        # Render outline
        if self._outline_width > 0:
            for dx, dy in Label._get_circle_points(self._outline_width):
                for render in self._outline_renders:
                    render_position = (
                        render[1][0] + dx,
                        render[1][1] + dy
                    )
                    self._surface.blit(
                        render[0],
                        render_position
                    )
        # Render text
        for text_render in self._renders:
            self._surface.blit(
                text_render[0],
                text_render[1]
            )

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
