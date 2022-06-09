import pygame
from engine import timer, Entity

class Animator:
    def __init__(self, timer_manager):
        self.timers = timer_manager

    def _cleanup_and_call(self, sender, callback, callback_delay):
        sender.close()
        if not callback_delay:
            callback()
            return
        anim_timer = self.timers.add(callback_delay, True)
        anim_timer.elapsed += lambda sender: callback()

    def tick_to_alpha(self, surface, val_to, anim_timer):
        alpha = surface.get_alpha()
        alpha += ((val_to - alpha) * anim_timer.get_ratio())
        surface.set_alpha(alpha)

    def fromto_alpha(self, surface_or_entity, duration, val_from, val_to, callback = None, callback_delay = None):
        surface = surface_or_entity
        if isinstance(surface_or_entity, Entity):
            surface = surface_or_entity.get_surface()

        if val_from:
            surface.set_alpha(val_from)
        anim_timer = self.timers.add(duration, True)
        anim_timer.tick += lambda sender: \
            self.tick_to_alpha(surface, val_to, anim_timer)

        if callback:
            anim_timer.elapsed += lambda sender, callback_bound=callback: \
                self._cleanup_and_call(sender, callback, callback_delay)

        return anim_timer

    def to_alpha(self, surface_or_entity, duration, val_to, callback = None, callback_delay = None):
        return self.fromto_alpha(surface_or_entity, duration, None, val_to, callback, callback_delay)

    def fadein(self, surface_or_entity, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(surface_or_entity, duration, 0, 255, callback, callback_delay)

    def fadeout(self, surface_or_entity, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(surface_or_entity, duration, 255, 0, callback, callback_delay)

default = Animator(timer.default)
