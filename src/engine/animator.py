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

    # Animator: Position
    def tick_to_position(self, sender, entity, anim_timer, val_to_x, val_to_y):
        position = entity.get_position()
        ratio = anim_timer.get_ratio()
        position_x = position[0]
        position_y = position[1]
        if val_to_x:
            position_x += int((val_to_x - position[0]) * ratio)
        if val_to_y:
            position_y += int((val_to_y - position[1]) * ratio)
        position = (position_x, position_y)
        entity.set_position(position)
        # XXX this closes the animation timer early if the current position is
        # essentially the same as the target position. 3 is an arbitrary,
        # made-up number to determine if we're "close enough" to the target.
        should_close = False
        if val_to_x:
            should_close = int(position[0]) >= (val_to_x - 3)
        if val_to_y:
            should_close = int(position[1]) >= (val_to_y - 3)
        if should_close:
            sender.on_elapsed()
            sender.close()

    def to_position(self, entity, duration, val_to_x = None, val_to_y = None, delta = False, callback = None, callback_delay = None):
        anim_timer = self.timers.add(duration, True)
        final_val_to_x = val_to_x
        final_val_to_y = val_to_y
        if delta:
            position = entity.get_position()
            if val_to_x:
                final_val_to_x += position[0]
            if val_to_y:
                final_val_to_y += position[1]
        anim_timer.tick += lambda sender: \
            self.tick_to_position(sender, entity, anim_timer, final_val_to_x, final_val_to_y)

        if callback:
            anim_timer.elapsed += lambda sender, callback_bound=callback: \
                self._cleanup_and_call(sender, callback, callback_delay)

        return anim_timer

    # Animator: Alpha
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
