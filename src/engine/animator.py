import pygame
from engine import timer

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

    def base_to_alpha(self, surface, target_alpha, anim_timer):
        alpha = surface.get_alpha()
        time_ratio = anim_timer.get_elapsed() / anim_timer.interval
        alpha += ((target_alpha - alpha) * time_ratio)
        surface.set_alpha(alpha)

    def fromto_alpha(self, surface, duration, val_from, val_to, callback = None, callback_delay = None):
        if val_from:
            surface.set_alpha(val_from)
        anim_timer = self.timers.add(duration, True)
        anim_timer.tick += lambda sender: \
            self.base_to_alpha(surface, val_to, anim_timer)
        if callback:
            anim_timer.elapsed += lambda sender, callback_bound=callback: \
                self._cleanup_and_call(sender, callback, callback_delay)
        return anim_timer

    def to_alpha(self, surface, duration, val_to, callback = None, callback_delay = None):
        return self.fromto_alpha(surface, duration, None, val_to, callback, callback_delay)

    def fadein(self, surface, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(surface, duration, 0, 255, callback, callback_delay)

    def fadeout(self, surface, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(surface, duration, 255, 0, callback, callback_delay)

    def entity_to_alpha(self, entity, duration, val_to, callback = None, callback_delay = None):
        return self.to_alpha(entity.get_surface(), duration, val_to, callback, callback_delay)

    def entity_fromto_alpha(self, entity, duration, val_from, val_to, callback = None, callback_delay = None):
        return self.fromto_alpha(entity.get_surface(), duration, val_from, val_to, callback, callback_delay)

    def entity_fadein(self, entity, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(entity.get_surface(), duration, 0, 255, callback, callback_delay)

    def entity_fadeout(self, entity, duration, callback = None, callback_delay = None):
        return self.fromto_alpha(entity.get_surface(), duration, 255, 0, callback, callback_delay)

default = Animator(timer.default)
