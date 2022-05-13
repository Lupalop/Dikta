from engine import *
from engine.entities import *

import pygame

def load_area_image(scene_id, image_name):
    scene_dir = "area" + str(scene_id)
    return content.load_image(image_name, scene_dir)

font_default = "franklingothicmediumcond"

fonts = {
    "sm": content.load_font(font_default, 12),
    "md": content.load_font(font_default, 20)
}

button_default_states = {
    "normal": content.load_image("btn_sm_normal.png"),
    "hover": content.load_image("btn_sm_hover.png"),
    "active": content.load_image("btn_sm_active.png")
}

button_default = Button(
    button_default_states,
    "",
    fonts["md"],
    pygame.Color("white"),
    (0, 0))
