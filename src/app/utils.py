from engine import *
from engine.entities import *

import pygame

EXT_PNG = ".png"

# Utility functions for retrieving images from the assets folder
def load_em_image(episode_id, mission_id, image_name):
    scene_dir = "e{}m{}".format(episode_id, mission_id)
    return content.load_image(image_name + EXT_PNG, scene_dir)

def load_mm_image(image_name):
    return content.load_image(image_name + EXT_PNG, "mainmenu")

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
    Label("",
          fonts["md"],
          pygame.Color("white")),
    (0, 0))
