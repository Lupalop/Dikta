from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app import utils

import pygame

class TargetRect(ClickableEntity):
    def __init__(self, owner, position_or_rect = (0, 0), size = None, zoomin = True):
        super().__init__(owner, position_or_rect, size, None, hit_rect = True)
        self.zoomin = zoomin

    @classmethod
    def from_entity(cls, owner, entity, copy_handlers = False):
        entity_copy = cls(owner, entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.NORMAL:
            utils.reset_cursor()

        super()._on_state_changed(state)

    def _on_mousemove(self):
        if self.zoomin:
            utils.set_cursor("zoomin")
        else:
            utils.set_cursor("zoomout")
        super()._on_mousemove()

    def draw(self, layer):
        # Prevent drawing a target area.
        pass
