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

def load_ui_image(image_name):
    return content.load_image(image_name + EXT_PNG, "ui")

def load_ca_image(image_name):
    return content.load_image(image_name + EXT_PNG, "ca")

strings = content.load_json("strings")

def get_ep_string(episode_id, mission_id, character_id, text_id):
    episode_key = "e{}".format(episode_id)
    mission_key = "m{}".format(mission_id)
    text_key = "{}_{}".format(character_id, text_id)
    try:
        return (
            strings["characters"][character_id],
            strings[episode_key][mission_key][text_key]["text"]
        )
    except KeyError:
        return (
            "XXXmissing: [{}]".format(character_id),
            "XXXmissing: [{}][{}][{}]".format(episode_key, mission_key, text_key)
        )

def get_item_string(item_name):
    return strings["items"][item_name]

font_default = "franklingothicmediumcond"

fonts = {}

def get_font(size):
    key = "{}_{}".format(font_default, size)
    if key not in fonts:
        fonts[key] = content.load_font(font_default, size)
    return fonts[key]

button_default_states = {
    "normal": load_ui_image("btn_sm_normal"),
    "hover": load_ui_image("btn_sm_hover"),
    "active": load_ui_image("btn_sm_active")
}

button_default = Button(
    button_default_states,
    Label("",
          get_font(20),
          pygame.Color("white")),
    (0, 0))
