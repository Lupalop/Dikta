from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app import utils

import pygame

class TargetItem(ClickableEntity):
    def __init__(self, owner, surface, position_or_rect = (0, 0), size = None, removable = True, grabbable = True):
        super().__init__(owner, position_or_rect, size, surface)
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
    def _on_leftclick(self):
        if self.removable:
            self.owner.animator.fadeout(self, 500)
            self.removed = True
        super()._on_leftclick()

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
                self.is_ghosting = True
        elif state == ClickState.RELEASED:
            if self.grabbable:
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

        if self.get_state() == ClickState.ACTIVE and self.is_ghosting:
            scaled_pos = game.get_mouse_pos()
            self._ghost_rect.x = scaled_pos[0] - self._ghost_offset[0]
            self._ghost_rect.y = scaled_pos[1] - self._ghost_offset[1]

        super().update(game, events)

    def draw(self, layer):
        if self.is_ghosting:
            layer.blit(self.get_surface(), self._ghost_rect)
            return

        super().draw(layer)
