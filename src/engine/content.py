import os
import pygame
import pygame.freetype

font_cache = {}
image_cache = {}

pygame.freetype.init()

def load_image(image_name, *subdirectories):
    image_path = os.path.join("app", "assets", *subdirectories, image_name);
    asset = None
    if image_path in image_cache:
        asset = image_cache[image_path]
    else:
        asset = pygame.image.load(image_path).convert_alpha()
        image_cache[image_path] = asset
    return asset

def load_font(font_name_or_file, font_size, is_system = True):
    font_name = font_name_or_file
    if not is_system:
        font_name = os.path.basename(
            os.path.splitext(font_name_or_file)[0])
    if font_name in font_cache:
        font_targets = font_cache[font_name]
        if font_size in font_targets:
            return font_targets[font_size]
        else:
            current_font = load_new_font(
                font_name_or_file, font_size, is_system)
            font_targets[font_size] = current_font
            return current_font
    else:
        current_font = load_new_font(
            font_name_or_file, font_size, is_system)
        font_targets = {}
        font_targets[font_size] = current_font
        font_cache[font_name] = font_targets
        return current_font

def load_new_font(font_name_or_file, font_size, is_system = True):
    if is_system:
        return pygame.freetype.SysFont(font_name_or_file, font_size)
    return pygame.freetype.Font(font_name_or_file, font_size)
