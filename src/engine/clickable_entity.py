from engine import Entity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler

import pygame

class ClickableEntity(Entity):
    def __init__(self, owner, position_or_rect = (0, 0), size = None, surface = None, hit_rect = False):
        super().__init__(owner, position_or_rect, size, surface)
        self._state = ClickState.NORMAL
        self.hit_rect = hit_rect
        # Event handlers
        self.click = EventHandler()
        self.leftclick = EventHandler()
        self.middleclick = EventHandler()
        self.rightclick = EventHandler()
        self.state_changed = EventHandler()
        self.mousemove = EventHandler()

    @classmethod
    def from_entity(cls, owner, entity, copy_handlers = False):
        entity_copy = cls(owner, entity._rect, None, entity.surface, entity.hit_rect)
        if copy_handlers:
            entity_copy.click = entity.click
            entity_copy.state_changed = entity.state_changed
        return entity_copy

    def get_state(self):
        return self._state

    # Event handlers
    def _on_leftclick(self):
        self.leftclick(self)

    def _on_middleclick(self):
        self.middleclick(self)

    def _on_rightclick(self):
        self.rightclick(self)

    def _on_click(self, button):
        if button == MouseButton.LEFT:
            self._on_leftclick()
        elif button == MouseButton.MIDDLE:
            self._on_middleclick()
        elif button == MouseButton.RIGHT:
            self._on_rightclick()
        self.click(self, button)

    def _on_state_changed(self, state):
        self._state = state
        self.state_changed(self, state)

    def _on_mousemove(self):
        self.mousemove(self)

    def update(self, game, events):
        # Determine if the pointer is hovering over the button.
        is_hovered = self.intersects(game.get_mouse_pos(), self.hit_rect)
        # This will be handled only if this is the topmost entity, which will
        # be processed by the owner scene.
        if is_hovered:
            self.owner._captured_action = lambda: self._handle_input(is_hovered, game, events)
        else:
            self._handle_input(is_hovered, game, events)

    def _handle_input(self, is_hovered, game, events):
        self.is_hovered = is_hovered
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

        # Handle if the a mouse button is being pressed and if it's released.
        if self._state == ClickState.ACTIVE:
            if is_mb_up:
                self._on_state_changed(ClickState.RELEASED)
                # Execute click handlers only if the mouse button was
                # released while hovering on this button.
                if self.is_hovered:
                    self._on_click(mb_target)
                return
            else:
                # Return early to prevent unwanted state changes.
                return

        # Handle if the pointer is hovering over the button, if a mouse button
        # is being pressed while hovering, and restoring the normal state.
        if self.is_hovered:
            self._on_mousemove()
            if self._state != ClickState.HOVER:
                self._on_state_changed(ClickState.HOVER)
            elif is_mb_down:
                self._on_state_changed(ClickState.ACTIVE)
        elif self._state != ClickState.NORMAL:
            self._on_state_changed(ClickState.NORMAL)
