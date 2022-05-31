from engine.entities import Image
from engine.enums import MouseButton, ButtonState
from engine.timer import Timer

import pygame

class FadeButton(Image):
    def __init__(self, surface, position_or_rect, size = None):
        super().__init__(surface, position_or_rect, size)
        self._timer = Timer(1000)
        self.state = ButtonState.NORMAL
        self.get_surface().set_alpha(70)

    @classmethod
    def from_entity(cls, entity):
        return self.from_fadebutton(entity)

    @classmethod
    def from_fadebutton(cls, entity, copy_handlers = False):
        copiedEntity = cls(entity.get_surface(), entity._rect)
        if copy_handlers:
            copiedEntity.on_left_click = entity.on_left_click
            copiedEntity.on_middle_click = entity.on_middle_click
            copiedEntity.on_right_click = entity.on_right_click
        return copiedEntity

    # Event handlers

    def on_left_click(self):
        pass

    def on_middle_click(self):
        pass

    def on_right_click(self):
        pass

    def _fade_to_target(self, target):
        alpha = self.get_surface().get_alpha()
        time_ratio = self._timer.get_elapsed() / self._timer.interval
        alpha += ((target - alpha) * time_ratio)
        self.get_surface().set_alpha(alpha)

    def update(self, game, events):
        is_mb_down = False
        is_mb_up = False
        mb_target = None

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mb_down = True
                mb_target = event.button
            if event.type == pygame.MOUSEBUTTONUP:
                is_mb_up = True
                mb_target = event.button

        is_hovered = self.intersects_mask(game.get_mouse_pos())

        if self.state == ButtonState.ACTIVE:
            if is_mb_up:
                self.state = ButtonState.RELEASED
                # Execute click handlers only if the mouse button was
                # released while hovering on this button.
                if is_hovered:
                    if mb_target == MouseButton.LEFT:
                        self.on_left_click()
                    elif mb_target == MouseButton.MIDDLE:
                        self.on_middle_click()
                    elif mb_target == MouseButton.RIGHT:
                        self.on_right_click()
            else:
                return

        if is_hovered:
            if self.state != ButtonState.HOVER:
                self.state = ButtonState.HOVER
                self._timer.reset(True)
                self._timer.on_tick = lambda: self._fade_to_target(255)
                self._timer.start()
            elif is_mb_down:
                self.state = ButtonState.ACTIVE
                self._timer.reset(True)
                self._timer.on_tick = lambda: self._fade_to_target(175)
                self._timer.start()
        elif self.state != ButtonState.NORMAL:
            self.state = ButtonState.NORMAL
            self._timer.reset(True)
            self._timer.on_tick = lambda: self._fade_to_target(100)
            self._timer.start()

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
