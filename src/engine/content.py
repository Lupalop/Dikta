import os
import pygame
import pygame.freetype
import json

font_cache = {}
image_cache = {}
sound_cache = {}

pygame.mixer.init()
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
    font_path = os.path.join("app", "assets", "fonts", font_name_or_file);
    return pygame.freetype.Font(font_path, font_size)

def load_json(file_name, *subdirectories):
    file_name = file_name + ".json"
    file_path = os.path.join(*subdirectories, file_name);
    file = open(file_path, "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    return data

def save_json(file_name, data, *subdirectories):
    file_name = file_name + ".json"
    file_path = os.path.join(*subdirectories, file_name);
    file = open(file_path, "w", encoding="utf-8")
    json.dump(data, file)
    file.close()

def load_json_asset(file_name, *subdirectories):
    return load_json(file_name, "app", "assets", *subdirectories)

def save_json_asset(file_name, data, *subdirectories):
    save_json(file_name, data, "app", "assets", *subdirectories)

def load_sound(file_name, *subdirectories):
    if file_name in sound_cache:
        return sound_cache[file_name]
    file_path = os.path.join("app", "assets", *subdirectories, file_name)
    if not os.path.exists(file_path):
        return None
    sound = pygame.mixer.Sound(file_path)
    sound_cache[file_name] = sound
    return sound
