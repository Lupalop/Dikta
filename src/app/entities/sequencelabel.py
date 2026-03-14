from app.entities import Label
from engine.event_handler import EventHandler

import pygame

# Milliseconds between each revealed character
CHAR_INTERVAL_MS = 30

class SequenceLabel(Label):
    def __init__(self, owner, text, font, color, position_or_rect = (0, 0), size = None):
        super().__init__(owner, text, font, color, position_or_rect, size)
        self.completed = EventHandler()

    def _on_completed(self):
        self.is_completed = True
        self.completed(self)

    def skip(self):
        if self.is_completed:
            return

        self._timer.close()
        self._on_completed()
        self._reset_placeholder_suface()
        self._blit_lines()

    def _blit_partial(self):
        self._reset_placeholder_suface()
        chars_remaining = self._char_index

        for i, line in enumerate(self._textlines):
            if chars_remaining <= 0:
                break

            chars_in_line = len(line)
            visible_count = min(chars_remaining, chars_in_line)

            # Compute the pixel width of the visible substring
            if visible_count >= chars_in_line:
                clip_width = self._renders[i][1].width
            else:
                clip_width = self._font.get_rect(line[:visible_count]).width

            clip_area = pygame.Rect(0, 0, clip_width, self._renders[i][1].height)
            dest = self._render_dests[i]

            # Blit outline first (if enabled)
            if self._outline_width > 0:
                for dx, dy in Label._get_circle_points(self._outline_width):
                    if self._surface:
                        self._surface.blit(
                            self._outline_renders[i][0],
                            (dest.x + dx, dest.y + dy),
                            clip_area
                        )

            # Blit the text
            if self._surface:
                self._surface.blit(self._renders[i][0], dest, clip_area)
            chars_remaining -= chars_in_line

    def _add_char_to_surface(self, sender):
        self._char_index += 1

        if self._char_index >= self._total_chars:
            sender.close()
            self._on_completed()
            self._reset_placeholder_suface()
            self._blit_lines()
            return

        self._blit_partial()

    def _render_lines(self):
        super()._render_lines()

        # Store lines for per-character indexing
        if self.ignore_newline:
            self._textlines = [self._text.replace("\n", "")]
        else:
            self._textlines = self._text.split("\n")

        self._total_chars = sum(len(line) for line in self._textlines)
        self._char_index = 0

        # Build destination rects from the already-computed render rects
        self._render_dests = [
            pygame.Rect(r[1].x, r[1].y, r[1].width, r[1].height)
            for r in self._renders
        ]

    def _on_entity_dirty(self, resize = True):
        self._render_lines()
        # Start with a blank surface; typewriter will fill it in tick by tick
        self._reset_placeholder_suface()

        self._timer = self.owner.timers.add(CHAR_INTERVAL_MS, False, True)
        self._timer.elapsed += self._add_char_to_surface
        self.is_completed = False

        if resize:
            self._mask = None
            self._rect.size = self._render_size

        self.entity_dirty(self, resize)

    def update(self, game, events):
        if not self.is_completed and not self._timer.enabled:
            self._timer.start()
