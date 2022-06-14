from engine import *

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

def load_clue_image(image_name):
    return load_png_image(image_name, "items")

def load_vox(file_name):
    file_name = file_name + ".mp3"
    sound = content.load_sound(file_name, "vox")
    return sound

strings = content.load_json_asset("strings")

def get_ep_string(episode_id, mission_id, character_id, text_id):
    episode_key = "e{}".format(episode_id)
    mission_key = "m{}".format(mission_id)
    text_key = "{}_{}".format(character_id, text_id)
    vox_key = "{}{}_{}".format(episode_key, mission_key, text_key)
    
    nametag_string = ""
    try:
        nametag_string = strings["characters"][character_id]
    except KeyError:
        nametag_string = "XXXmissing: [{}]".format(character_id)

    text_string = ""
    try:
        text_string = strings[episode_key][mission_key][text_key]["text"]
    except KeyError:
        text_string = "XXXmissing: [{}][{}][{}]".format(episode_key, mission_key, text_key)

    return (nametag_string, text_string, text_key, vox_key)

FONT_DEFAULT = "franklingothicmediumcond"
FONT_COMIC = "badcomic_italic"
FONT_EXT_TTF = ".ttf"

fonts = {}

def get_font(size):
    key = "{}_{}".format(FONT_DEFAULT, size)
    if key not in fonts:
        fonts[key] = content.load_font(FONT_DEFAULT, size)
    return fonts[key]

def get_comic_font(size):
    key = "{}_{}".format(FONT_COMIC, size)
    if key not in fonts:
        fonts[key] = content.load_font(FONT_COMIC + FONT_EXT_TTF, size, False)
    return fonts[key]

def load_cursor(cursor_name):
    return load_png_image(cursor_name, "cursors")

cursors = {
    "none": None,
    "default": load_cursor("cursor_default"),
    "select": load_cursor("cursor_select"),
    "zoomin": load_cursor("cursor_zomming"),
    "zoomout": load_cursor("cursor_zoomout"),
    "grab": load_cursor("cursor_grab"),
    "grabbing": load_cursor("cursor_grabbing"),
    "unavailable": load_cursor("cursor_unavailable"),
    "work": load_cursor("cursor_work1"),
}

# Inventory and Clues

def get_clues_key(episode_id):
    return "clues.ep{}".format(episode_id)

def get_clue_data(clue_id):
    return strings["clues"][clue_id]

def create_listitem_data(text, id, value):
    data = {
        "text": text,
        "id": id,
        "value": value
    }
    return data

# BGM/SFX
def get_music():
    return content.music_current

def set_music(file_name, volume = 1.0):
    is_loaded = content.load_music(file_name + ".mp3")
    if is_loaded:
        pygame.mixer.music.play(loops=-1, fade_ms=500)
        pygame.mixer.music.set_volume(volume)

def play_sfx(file_name, volume = 1.0):
    file_name = file_name + ".mp3"
    sound = content.load_sound(file_name, "sfx")
    sound.set_volume(volume)
    sound.play()
    return sound

# PyGame's color cursors don't scale properly. Instead, we draw our own cursor
# via an overlay, which then references this module's current cursor variable.
cursor_current = None
cursor_locked = False
def set_cursor(cursor_name):
    global cursor_current
    global cursor_locked
    if cursor_locked:
        return
    cursor_current = cursors[cursor_name]

def reset_cursor():
    global cursor_locked
    cursor_locked = False
    set_cursor("default")

def hide_cursor():
    global cursor_locked
    set_cursor("none")
    cursor_locked = True

# The following disables hardware cursors.
pygame.mouse.set_visible(False)
