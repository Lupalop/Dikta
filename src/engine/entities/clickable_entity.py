from engine.entities import Entity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame

class ClickableEntity(Entity):
    def __init__(self, position_or_rect = (0, 0), size = None, surface = None):
        super().__init__(position_or_rect, size, surface)
        self._state = ClickState.NORMAL
        # Event handlers
        self.click = EventHandler()
        self.state_changed = EventHandler()

    @classmethod
    def from_entity(cls, entity):
        return self.from_clickable_entity(entity)

    @classmethod
    def from_clickable_entity(cls, entity, copy_handlers = False):
        entity_copy = cls(entity._rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    def get_state(self):
        return self._state

    # Event handlers
    def _on_click(self, button):
        self.click(self, button)

    def _on_state_changed(self, state):
        self._state = state
        self.state_changed(self, state)

    def update(self, game, events):
        is_mb_down = False
        is_mb_up = False
        mb_target = None

        # Determine if a mouse button is being pressed and its state.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mb_down = True
                mb_target = event.button
            if event.type == pygame.MOUSEBUTTONUP:
                is_mb_up = True
                mb_target = event.button

        # Determine if the pointer is hovering over the button.
        is_hovered = self.intersects(game.get_mouse_pos())

        # Handle if the a mouse button is being pressed and if it's released.
        if self._state == ClickState.ACTIVE:
            if is_mb_up:
                self._on_state_changed(ClickState.RELEASED)
                # Execute click handlers only if the mouse button was
                # released while hovering on this button.
                if is_hovered:
                    self._on_click(mb_target)
            else:
                # Return early to prevent unwanted state changes.
                return

        # Handle if the pointer is hovering over the button, if a mouse button
        # is being pressed while hovering, and restoring the normal state.
        if is_hovered:
            if self._state != ClickState.HOVER:
                self._on_state_changed(ClickState.HOVER)
            elif is_mb_down:
                self._on_state_changed(ClickState.ACTIVE)
        elif self._state != ClickState.NORMAL:
            self._on_state_changed(ClickState.NORMAL)
