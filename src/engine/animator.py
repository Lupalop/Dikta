import pygame

def to_alpha(surface, target_alpha, timer):
    alpha = surface.get_alpha()
    time_ratio = timer.get_elapsed() / timer.interval
    alpha += ((target_alpha - alpha) * time_ratio)
    surface.set_alpha(alpha)

def entity_to_alpha(entity, target_alpha, timer):
    to_alpha(entity.get_surface(), target_alpha, timer)
