from engine import *
from engine.entities import *

import pygame

# Utility functions for retrieving images from the assets folder
def load_png_image(image_name, *subdirectories):
    return content.load_image(image_name + ".png", *subdirectories)

def load_em_image(episode_id, mission_id, image_name):
    scene_dir = "e{}m{}".format(episode_id, mission_id)
    return load_png_image(image_name, scene_dir)

def load_mm_image(image_name):
    return load_png_image(image_name, "mainmenu")

def load_ui_image(image_name):
    return load_png_image(image_name, "ui")

def load_ca_image(image_name):
    return load_png_image(image_name, "ca")

strings = content.load_json_asset("strings")

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
    None,
    button_default_states,
    Label(None, "",
          get_font(20),
          pygame.Color("white")),
    (0, 0))

def load_cursor(cursor_name):
    return load_png_image(cursor_name, "cursors")

cursors = {
    "default": load_cursor("cursor_default"),
    "select": load_cursor("cursor_select"),
    "zoomin": load_cursor("cursor_zomming"),
    "zoomout": load_cursor("cursor_zoomout"),
    "grab": load_cursor("cursor_grab"),
    "grabbing": load_cursor("cursor_grabbing"),
    "unavailable": load_cursor("cursor_unavailable"),
    "work": load_cursor("cursor_work1"),
}

# PyGame's color cursors don't scale properly. Instead, we draw our own cursor
# via an overlay, which then references this module's current cursor variable.
cursor_current = None
def set_cursor(cursor_name):
    global cursor_current
    cursor_current = cursors[cursor_name]

def reset_cursor():
    set_cursor("default")

# The following disables hardware cursors.
pygame.mouse.set_visible(False)
