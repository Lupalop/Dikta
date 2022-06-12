from app.entities import *
from app import utils

import pygame

button_default_states = {
    "normal": utils.load_ui_image("btn_sm_normal"),
    "hover": utils.load_ui_image("btn_sm_hover"),
    "active": utils.load_ui_image("btn_sm_active")
}

button_default = Button(
    None,
    button_default_states,
    Label(None, "",
          utils.get_font(20),
          pygame.Color("white")),
    (0, 0)
)

hand_right = Image(
    None,
    utils.load_ca_image("joe-hand"),
    (512, 160)
)

hand_left = Image(
    None,
    utils.load_ca_image("joe-hand-left"),
    (0, 154)
)

FDA_CHOICESET = ChoiceSet(
    None,
    (60, 140),
    [
        utils.load_ui_image("fda-fact"),
        utils.load_ui_image("fda-doubt"),
        utils.load_ui_image("fda-accuse")
    ],
    True,
    True,
    0
)
