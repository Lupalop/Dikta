from engine import *
from engine.entities import *

import pygame

def load_area_image(scene_id, image_name):
    scene_dir = "area" + str(scene_id)
    return content.load_image(image_name, scene_dir)

def get_default_button():
    return _button_default_tpl

def get_fonts():
    return _fonts

def get_font(font_name):
    return _fonts[font_name]

_font_default = "franklingothicmediumcond"

_fonts = {
    "sm": content.load_font(_font_default, 12),
    "md": content.load_font(_font_default, 20)
}

_button_default_states = {
    "normal": content.load_image("btn_sm_normal.png"),
    "hover": content.load_image("btn_sm_hover.png"),
    "active": content.load_image("btn_sm_active.png")
}

_button_default_tpl = Button(
    _button_default_states, "", _fonts["md"], pygame.Color("white"), (0, 0))
