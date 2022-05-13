from engine import *

def load_area_image(scene_id, image_name):
    scene_dir = "area" + str(scene_id)
    return content.load_image(image_name, scene_dir)
