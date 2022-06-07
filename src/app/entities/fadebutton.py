from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app import utils

import pygame

class FadeButton(ClickableEntity):
    def __init__(self, owner, surface, position_or_rect = (0, 0), size = None):
        super().__init__(owner, position_or_rect, size, surface)
        self._timer = self.owner.timers.add(1000)
        self.get_surface().set_alpha(100)

    @classmethod
    def from_entity(cls, owner, entity, copy_handlers = False):
        entity_copy = cls(owner, entity.get_surface(), entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.NORMAL:
            self._timer.reset(True)
            self._timer.tick.clear()
            self._timer.tick += lambda sender: self.owner.animator.to_alpha( \
                self.get_surface(), 100, self._timer)
            self._timer.start()
            utils.reset_cursor()
        elif state == ClickState.HOVER:
            self._timer.reset(True)
            self._timer.tick.clear()
            self._timer.tick += lambda sender: self.owner.animator.to_alpha( \
                self.get_surface(), 255, self._timer)
            self._timer.start()
            utils.set_cursor("select")
        elif state == ClickState.ACTIVE:
            self._timer.reset(True)
            self._timer.tick.clear()
            self._timer.tick += lambda sender: self.owner.animator.to_alpha( \
                self.get_surface(), 175, self._timer)
            self._timer.start()
        elif state == ClickState.RELEASED:
            pass
        else:
            raise ValueError("unexpected button state")
        super()._on_state_changed(state)