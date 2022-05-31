from engine.entities import ClickableEntity, Image
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from engine.timer import Timer

import pygame

class FadeButton(ClickableEntity):
    def __init__(self, surface, position_or_rect, size = None):
        super().__init__(position_or_rect, size)
        self._timer = Timer(1000)

        image = Image(surface, position_or_rect, size)
        image.set_position(self.get_position())
        if self.get_size() == (0, 0):
            self._rect.size = image.get_size()
        else:
            image.set_size(self.get_size())
        image.get_surface().set_alpha(70)

        self._image = image

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

    def get_surface(self):
        return self._image.get_surface()

    def set_surface(self, surface):
        print("Changing the surface of a Button entity is not allowed.")

    def get_mask(self):
        return self._image.get_mask()

    def intersects_rect(self, point):
        return self._image.intersects_rect(point)

    def intersects_mask(self, point):
        return self._image.intersects_mask(point)

    # Overridden base entity setter functions
    def _entity_dirty(self, is_position_only = False):
        if is_position_only:
            self._image.set_position(self.get_position())
            return
        self._image.set_size(self.get_size())
        self._image.set_position(self.get_position())

    def set_size(self, size):
        super().set_size(size)
        self._entity_dirty()

    def set_rect(self, rect):
        super().set_rect(rect)
        self._entity_dirty()

    def set_position(self, position):
        super().set_position(position)
        self._entity_dirty(True)

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

    def draw(self, layer):
        layer.blit(self.get_surface(), self._rect)
