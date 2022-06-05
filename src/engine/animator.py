from engine import timer as utils_timer

import pygame

def _cleanup_and_call(sender, callback, callback_delay):
    sender.close()
    if not callback_delay:
        callback()
        return
    timer = utils_timer.default.add(callback_delay, True)
    timer.elapsed += lambda sender: callback()

def to_alpha(surface, target_alpha, timer):
    alpha = surface.get_alpha()
    time_ratio = timer.get_elapsed() / timer.interval
    alpha += ((target_alpha - alpha) * time_ratio)
    surface.set_alpha(alpha)

def fromto_alpha(surface, duration, val_from, val_to, callback, callback_delay = None):
    surface.set_alpha(val_from)
    timer = utils_timer.default.add(duration, True)
    timer.tick += lambda sender: \
        to_alpha(surface, val_to, timer)
    timer.elapsed += lambda sender, callback_bound=callback: \
        _cleanup_and_call(sender, callback, callback_delay)
    return timer

def fadein(surface, duration, callback, callback_delay = None):
    return fromto_alpha(surface, duration, 0, 255, callback, callback_delay)

def fadeout(surface, duration, callback, callback_delay = None):
    return fromto_alpha(surface, duration, 255, 0, callback, callback_delay)

def entity_to_alpha(entity, target_alpha, timer):
    to_alpha(entity.get_surface(), target_alpha, timer)

def entity_fromto_alpha(entity, duration, val_from, val_to, callback, callback_delay = None):
    return fromto_alpha(entity.get_surface(), duration, val_from, val_to, callback, callback_delay)

def entity_fadein(entity, duration, callback, callback_delay = None):
    return fromto_alpha(entity.get_surface(), duration, 0, 255, callback, callback_delay)

def entity_fadeout(entity, duration, callback, callback_delay = None):
    return fromto_alpha(entity.get_surface(), duration, 255, 0, callback, callback_delay)
