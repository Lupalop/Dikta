from engine.entities import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from engine.timer import Timer

import pygame

class FadeButton(ClickableEntity):
    def __init__(self, surface, position_or_rect = (0, 0), size = None):
        super().__init__(position_or_rect, size, surface)
        self._timer = Timer(1000)
        self.get_surface().set_alpha(70)

    @classmethod
    def from_entity(cls, entity, copy_handlers = False):
        copiedEntity = cls(entity.get_surface(), entity._rect)
        if copy_handlers:
            copiedEntity.click = entity.click
            copiedEntity.state_changed = entity.state_changed
        return copiedEntity

    def get_state(self):
        return self._state

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.NORMAL:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(100)
            self._timer.start()
        elif state == ClickState.HOVER:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(255)
            self._timer.start()
        elif state == ClickState.ACTIVE:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(175)
            self._timer.start()
        elif state == ClickState.RELEASED:
            pass
        else:
            raise ValueError("unexpected button state")
        super()._on_state_changed(state)

    def _fade_to_target(self, target):
        alpha = self.get_surface().get_alpha()
        time_ratio = self._timer.get_elapsed() / self._timer.interval
        alpha += ((target - alpha) * time_ratio)
        self.get_surface().set_alpha(alpha)
