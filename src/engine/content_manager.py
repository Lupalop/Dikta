import os
import pygame

font_cache = {}

class ContentManager:
    def __init__(self):
        pygame.font.init()
    @staticmethod
    def load_asset(aAssetName):
        asset_path = os.path.join("app/assets", aAssetName);
        return pygame.image.load(asset_path).convert_alpha()
    @staticmethod
    def load_scene_asset(aSceneId, aAssetName):
        scene_dir = "scene" + str(aSceneId) + "/"
        asset_path = os.path.join("app/assets", scene_dir, aAssetName);
        return pygame.image.load(asset_path).convert_alpha()
    @staticmethod
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
                current_font = ContentManager.load_new_font(
                    font_name_or_file, font_size, is_system)
                font_targets[font_size] = current_font
                return current_font
        else:
            current_font = ContentManager.load_new_font(
                font_name_or_file, font_size, is_system)
            font_targets = {}
            font_targets[font_size] = current_font
            font_cache[font_name] = font_targets
            return current_font
    @staticmethod
    def load_new_font(font_name_or_file, font_size, is_system = True):
        if is_system:
            return pygame.font.SysFont(font_name_or_file, font_size)
        return pygame.font.Font(font_name_or_file, font_size)
