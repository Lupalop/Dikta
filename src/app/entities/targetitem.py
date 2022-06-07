from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app import utils

import pygame

class TargetItem(ClickableEntity):
    def __init__(self, owner, surface, position_or_rect = (0, 0), size = None, removable = True, grabbable = True):
        super().__init__(owner, position_or_rect, size, surface, False)
        self._timer = self.owner.timers.add(1000)
        self.removable = removable
        self.removed = False
        self.grabbable = grabbable
        self.is_ghosting = False
        self._ghost_rect = None

    @classmethod
    def from_entity(cls, owner, entity, copy_handlers = False):
        entity_copy = cls(owner, entity.get_surface(), entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    # Event handlers
    def _on_click(self, button):
        if self.removable:
            self._timer.reset(True)
            self._timer.tick.clear()
            self._timer.tick += lambda sender: self.owner.animator.to_alpha( \
                self.get_surface(), 0, self._timer)
            self._timer.start()
            self.removed = True
        super()._on_click(button)

    def _on_state_changed(self, state):
        if self.removed:
            return
        if state == ClickState.NORMAL:
            utils.reset_cursor()
        elif state == ClickState.ACTIVE:
            utils.set_cursor("grabbing")
            if self.grabbable:
                self._ghost_rect = self.get_rect().copy()
                self._ghost_offset = self.intersection_offset
        elif state == ClickState.RELEASED:
            self.is_ghosting = False
            self._ghost_rect = None

        super()._on_state_changed(state)

    def _on_mousemove(self):
        if self.removed:
            return
        if self.get_state() == ClickState.HOVER:
            utils.set_cursor("grab")
        super()._on_mousemove()

    def update(self, game, events):
        if self.removed:
            return

        if self.get_state() == ClickState.ACTIVE and self.grabbable:
            # Begin ghosting only if the mouse is out of the entity's bounds.
            if not self.is_hovered:
                self.is_ghosting = True
            if self.is_ghosting:
                scaled_pos = game.get_mouse_pos()
                self._ghost_rect.x = scaled_pos[0] - self._ghost_offset[0]
                self._ghost_rect.y = scaled_pos[1] - self._ghost_offset[1]

        super().update(game, events)

    def draw(self, layer):
        if self.is_ghosting:
            layer.blit(self.get_surface(), self._ghost_rect)
            return

        super().draw(layer)
