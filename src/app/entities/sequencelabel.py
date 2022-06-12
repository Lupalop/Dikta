from engine import Entity
from app.entities import Label
from engine.event_handler import EventHandler

import pygame

PIXEL_INCREMENT = 5

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

    def _add_char_to_surface(self, sender):
        render = self._renders[self._render_index]
        render_dest = self._render_dests[self._render_index]
        render_area = self._render_areas[self._render_index]

        if render_dest.x >= self._render_size[0]:
            if self._render_index >= len(self._renders) - 1:
                sender.close()
                self._on_completed()
                return
            self._render_index += 1

        self._surface.blit(render[0], render_dest, render_area)
        render_dest.x += PIXEL_INCREMENT
        render_area.x += PIXEL_INCREMENT

    def _render_lines(self):
        super()._render_lines()
        # Generate render offsets
        self._render_index = 0
        self._render_dests = []
        self._render_areas = []
        desty = self._outline_width
        for i in range(len(self._renders)):
            if i >= 1 and i < len(self._renders):
                desty += self.line_height
            dest_rect = pygame.Rect(self._renders[i][1].x, desty, PIXEL_INCREMENT, self._renders[i][1].height)
            area_rect = pygame.Rect(0, 0, PIXEL_INCREMENT, self._renders[i][1].height)
            desty += self._renders[i][1].height
            self._render_dests.append(dest_rect)
            self._render_areas.append(area_rect)

    def _on_entity_dirty(self, resize = True):
        self._render_lines()

        self._timer = self.owner.timers.add(1, False, True)
        self._timer.elapsed += self._add_char_to_surface
        self.is_completed = False

        if resize:
            self._mask = None
            self._rect.size = self._render_size

        self.entity_dirty(self, resize)

    def update(self, game, events):
        if not self.is_completed and not self._timer.enabled:
            self._timer.start()
