from engine.entities import Image
from engine.enums import MouseButton, ButtonState
from engine.event_handler import EventHandler
from engine.timer import Timer

import pygame

class FadeButton(Image):
    def __init__(self, surface, position_or_rect, size = None):
        super().__init__(surface, position_or_rect, size)
        self._timer = Timer(1000)
        self._state = ButtonState.NORMAL
        self.get_surface().set_alpha(70)
        # Event handlers
        self.click = EventHandler()
        self.state_changed = EventHandler()

    @classmethod
    def from_entity(cls, entity):
        return self.from_fadebutton(entity)

    @classmethod
    def from_fadebutton(cls, entity, copy_handlers = False):
        copiedEntity = cls(entity.get_surface(), entity._rect)
        if copy_handlers:
            copiedEntity.click = entity.click
            copiedEntity.state_changed = entity.state_changed
        return copiedEntity

    def get_state(self):
        return self._state

    # Event handlers
    def _on_click(self, button):
        self.click(self, button)

    def _on_state_changed(self, state):
        if state == ButtonState.NORMAL:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(100)
            self._timer.start()
        elif state == ButtonState.HOVER:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(255)
            self._timer.start()
        elif state == ButtonState.ACTIVE:
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(175)
            self._timer.start()
        elif state == ButtonState.RELEASED:
            pass
        else:
            raise ValueError("unexpected button state")
        self._state = state
        self.state_changed(self, state)

    def _fade_to_target(self, target):
        alpha = self.get_surface().get_alpha()
        time_ratio = self._timer.get_elapsed() / self._timer.interval
        alpha += ((target - alpha) * time_ratio)
        self.get_surface().set_alpha(alpha)

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
        is_hovered = self.intersects_mask(game.get_mouse_pos())

        # Handle if the a mouse button is being pressed and if it's released.
        if self._state == ButtonState.ACTIVE:
            if is_mb_up:
                self._on_state_changed(ButtonState.RELEASED)
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
            if self._state != ButtonState.HOVER:
                self._on_state_changed(ButtonState.HOVER)
            elif is_mb_down:
                self._on_state_changed(ButtonState.ACTIVE)
        elif self._state != ButtonState.NORMAL:
            self._on_state_changed(ButtonState.NORMAL)

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
