from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from engine import game, ClickableEntity, prefs

from app import utils
from app.entities import Label, SequenceLabel, Image

import pygame
import random
from queue import Queue
from enum import IntEnum, IntFlag

RECT_NAME = pygame.Rect(0, 0, 155, 38)
RECT_BASE = pygame.Rect(0, RECT_NAME.height, 765, 90)
RECT_SPEECH = pygame.Rect(20, RECT_NAME.height, RECT_BASE.width - 140, RECT_BASE.height)
RECT_DIALOG = pygame.Rect(0, 0, RECT_BASE.width, RECT_NAME.height + RECT_BASE.height)
RECT_PORTRAIT = pygame.Rect(RECT_DIALOG.x, RECT_DIALOG.y, RECT_DIALOG.height, RECT_DIALOG.height)
RECT_NAME_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_NAME.y, RECT_NAME.width, RECT_NAME.height)
RECT_SPEECH_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_SPEECH.y, RECT_SPEECH.width, RECT_SPEECH.height)

class DialogSide(IntEnum):
    TOP = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    MIDDLE_LEFT = 4
    MIDDLE = 5
    MIDDLE_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM = 8
    BOTTOM_RIGHT = 9

class DialogFlags(IntFlag):
    CLOSEABLE = 1
    SKIPPABLE = 2
    NORMAL = 3

class Dialog(ClickableEntity):
    def __init__(self, emitter, position, dialog_key, name, text, portrait_id = None, flags = DialogFlags.NORMAL, callback = None):
        super().__init__(
            emitter.owner,
            position,
            RECT_DIALOG.size,
            pygame.Surface(RECT_DIALOG.size, pygame.SRCALPHA, 32)
        )

        self.emitter = emitter
        self.dialog_key = dialog_key
        self.callback = callback
        self.flags = flags

        rect_speech_final = RECT_SPEECH
        rect_name_final = RECT_NAME
        # Determine if we have a portrait and adjust position accordingly
        self.portrait = None
        if portrait_id:
            self.portrait = Image(self.owner, utils.load_ca_image(portrait_id), RECT_PORTRAIT)
            rect_speech_final = RECT_SPEECH_WP
            rect_name_final = RECT_NAME_WP
        # Draw boxes to entity surface
        self.box_name = utils.load_ui_image("dialog-box-nametag")
        self._surface.blit(self.box_name, rect_name_final)
        self.box_base = utils.load_ui_image("dialog-box-main")
        self._surface.blit(self.box_base, RECT_BASE)
        # Initialize name tag and its position
        self.label_name = Label(self.owner, name, utils.get_font(28), pygame.Color("white"))
        label_name_pos = (
            position[0] + rect_name_final.x + (rect_name_final.width / 2) - self.label_name.get_rect().width / 2,
            position[1] + rect_name_final.y + (rect_name_final.height / 2) - self.label_name.get_rect().height / 2
        )
        self.label_name.set_position(label_name_pos)
        # Initialize speech text and its position
        self.label_speech = SequenceLabel(self.owner, text, utils.get_font(24), pygame.Color("white"))
        label_speech_pos = (
            position[0] + rect_speech_final.x,
            position[1] + rect_speech_final.y + (rect_speech_final.height / 2) - self.label_speech.get_rect().height / 2
        )
        self.label_speech.set_position(label_speech_pos)
        def _update_cursor(sender):
            if self.is_hovered:
                utils.set_cursor("select")
        self.label_speech.completed += _update_cursor
        # Draw portrait to entity surface
        if self.portrait:
            self.portrait.draw(self._surface)

    @classmethod
    def from_entity(cls, entity, name, text):
        entity_copy = cls(name,
                          text,
                          entity.get_position())
        return entity_copy

    def set_position(self, position):
        raise("Changing the position of a dialog is not allowed.")

    def set_rect(self, rect):
        raise("Changing the rectangle of a dialog is not allowed.")

    def set_size(self, size):
        raise("Changing the size of a dialog is not allowed.")

    def set_surface(self, texture):
        raise("Changing the surface of a dialog is not allowed.")

    # Event handlers
    def _on_state_changed(self, state):
        if state == ClickState.HOVER:
            if self.label_speech.is_completed:
                utils.set_cursor("select")
            else:
                utils.set_cursor("work")
        elif state == ClickState.NORMAL:
            utils.reset_cursor()
        super()._on_state_changed(state)

    def _on_click(self, button):
        self.next_or_skip()
        super()._on_click(button)

    def draw(self, layer):
        super().draw(layer)
        self.label_speech.draw(layer)
        self.label_name.draw(layer)

    def update(self, game, events):
        super().update(game, events)
        self.label_speech.update(game, events)
        self.label_name.update(game, events)

    def next_or_skip(self):
        if self.label_speech.is_completed and self.flags & DialogFlags.CLOSEABLE:
            utils.reset_cursor()
            prefs.savedgame.set(self.dialog_key, True)
            self.emitter.next()
            return
        if self.flags & DialogFlags.SKIPPABLE:
            self.label_speech.skip()

class DialogEmitter():
    def __init__(self, owner, default_side):
        self.owner = owner
        self.default_side = default_side
        self.queue = Queue()
        self.current = None

    def next(self):
        if self.current and self.current.callback:
            self.current.callback()
        if self.queue.empty():
            self.current = None
        else:
            self.current = self.queue.get()

    def update(self, game, events):
        if self.current:
            self.current.update(game, events)
            for event in events:
                if event.type == pygame.KEYUP and \
                   (event.key == pygame.K_KP_ENTER or \
                    event.key == pygame.K_RETURN or \
                    event.key == pygame.K_SPACE):
                    self.current.next_or_skip()

    def draw(self, layer):
        if self.current:
            self.current.draw(layer)

    # Add dialogue with all features
    def add_custom(self, dialog_key, name, text, portrait_id = None, side = None, flags = DialogFlags.NORMAL, callback = None):
        if not side:
            side = self.default_side
        position = (0, 0)

        dialog_centerx = (game.layer_size[0] / 2) - (RECT_DIALOG.width / 2)
        dialog_centery = (game.layer_size[1] / 2) - (RECT_DIALOG.height / 2)
        dialog_leftx = 25
        dialog_topy = 25
        dialog_rightx = game.layer_size[0] - RECT_DIALOG.width - 25
        dialog_bottomy = game.layer_size[1] - 60 - RECT_DIALOG.height

        if side == DialogSide.TOP_LEFT:
            position = (dialog_leftx, dialog_topy)
        elif side == DialogSide.TOP:
            position = (dialog_centerx, dialog_topy)
        elif side == DialogSide.TOP_RIGHT:
            position = (dialog_rightx, dialog_topy)
        elif side == DialogSide.MIDDLE_LEFT:
            position = (dialog_leftx, dialog_centery)
        elif side == DialogSide.MIDDLE:
            position = (dialog_centerx, dialog_centery)
        elif side == DialogSide.MIDDLE_RIGHT:
            position = (dialog_rightx, dialog_centery)
        elif side == DialogSide.BOTTOM_LEFT:
            position = (dialog_leftx, dialog_bottomy)
        elif side == DialogSide.BOTTOM:
            position = (dialog_centerx, dialog_bottomy)
        elif side == DialogSide.BOTTOM_RIGHT:
            position = (dialog_rightx, dialog_bottomy)
        else:
            raise("unexpected dialog side")

        dialog = Dialog(self, position, dialog_key, name, text, portrait_id, flags, callback)
        self.queue.put(dialog)
        if not self.current:
            self.next()
        utils.reset_cursor()

    # Add dialogue with all features except with custom text/name
    def add(self, character_id, text_id, portrait_id = None, side = None, flags = DialogFlags.NORMAL, callback = None, repeat = True):
        text_id_final = text_id
        # Choose a random text ID if we've received a list
        if isinstance(text_id, list):
            text_id_final = random.choice(text_id)
        string = self.owner.get_string(character_id, text_id_final)
        dialog_key = utils.get_dialog_key(self.owner.mission_key, character_id, text_id_final)
        is_viewed = prefs.savedgame.get(dialog_key, False)
        if not repeat and is_viewed:
            return
        self.add_custom(
            dialog_key,
            string[0],
            string[1],
            portrait_id,
            side,
            flags,
            callback
        )
