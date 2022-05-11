import os
import pygame

class ContentManager:
    @staticmethod
    def load_asset(aAssetName):
        asset_path = os.path.join("assets", aAssetName);
        return pygame.image.load(asset_path)
    @staticmethod
    def load_scene_asset(aSceneId, aAssetName):
        scene_dir = "scene" + str(aSceneId) + "/"
        asset_path = os.path.join("assets", scene_dir, aAssetName);
        return pygame.image.load(asset_path)    
