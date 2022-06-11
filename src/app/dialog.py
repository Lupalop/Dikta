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
RECT_POPUP = pygame.Rect(0, 0, 380, 40)

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
    def __init__(self, emitter, position, text_key, name, text, portrait_id = None, flags = DialogFlags.NORMAL, callback = None):
        super().__init__(
            emitter.owner,
            position,
            RECT_DIALOG.size,
            pygame.Surface(RECT_DIALOG.size, pygame.SRCALPHA, 32)
        )

        self.emitter = emitter
        self.text_key = text_key
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
            if self.is_hovered and self.flags & DialogFlags.CLOSEABLE:
                utils.set_cursor("select")
        self.label_speech.completed += _update_cursor
        # Draw portrait to entity surface
        if self.portrait:
            self.portrait.draw(self._surface)

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
        if not (self.flags & DialogFlags.CLOSEABLE):
            pass
        elif state == ClickState.NORMAL:
            utils.reset_cursor()
        elif state == ClickState.HOVER:
            if self.label_speech.is_completed:
                utils.set_cursor("select")
            else:
                utils.set_cursor("work")
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
        if self.label_speech.is_completed and \
           (self.flags & DialogFlags.CLOSEABLE):
            if self.callback:
                self.callback()
            utils.reset_cursor()
            self.emitter.set_viewed(self.text_key)
            self.emitter.next()
        elif self.flags & DialogFlags.SKIPPABLE:
            self.label_speech.skip()

    # XXX The following overrides the intersection check to always return true,
    # so as to cover the entire screen. This isn't ideal, but it is what it is.
    def intersects(self, point, use_rect = False):
        return True

class Popup(ClickableEntity):
    def __init__(self, emitter, position, item_name):
        super().__init__(
            emitter.owner,
            position,
            RECT_POPUP.size,
            pygame.Surface(RECT_POPUP.size, pygame.SRCALPHA, 32)
        )

        self.item_name = item_name
        self.emitter = emitter

        # Draw boxes to entity surface
        self.box_base = utils.load_ui_image("popup-box")
        self._surface.blit(self.box_base, RECT_POPUP)
        # Initialize speech text and its position
        text = "Item found: {}".format(item_name)
        self.label_item = SequenceLabel(self.owner, text, utils.get_font(24), pygame.Color("white"))
        label_item_pos = (
            position[0] + 55,
            position[1] + (RECT_POPUP.height / 2) - (self.label_item.get_rect().height / 2)
        )
        self.label_item.set_position(label_item_pos)
        def _hide_popup(sender):
            self.owner.animator.fadeout(
                self.label_item,
                250,
                lambda: None
            )
            self.owner.animator.fadeout(
                self,
                250,
                lambda: self.next_or_skip()
            )
        def _delay(sender):
            timer = self.owner.timers.add(1500, True)
            timer.elapsed += _hide_popup
        self.label_item.completed += _delay

    def set_position(self, position):
        raise("Changing the position of a dialog is not allowed.")

    def set_rect(self, rect):
        raise("Changing the rectangle of a dialog is not allowed.")

    def set_size(self, size):
        raise("Changing the size of a dialog is not allowed.")

    def set_surface(self, texture):
        raise("Changing the surface of a dialog is not allowed.")

    # Event handlers
    def draw(self, layer):
        super().draw(layer)
        self.label_item.draw(layer)

    def update(self, game, events):
        super().update(game, events)
        self.label_item.update(game, events)

    def next_or_skip(self):
        if self.label_item.is_completed:
            utils.reset_cursor()
            self.emitter.next_popup()
            return
        self.label_item.skip()

class DialogEmitter():
    def __init__(self, owner, default_side):
        self.owner = owner
        self.default_side = default_side
        self.queue = Queue()
        self.popup_queue = Queue()
        self.current_dialog = None
        self.current_popup = None
        self.current_chooser = None

    def next(self):
        if self.queue.empty():
            self.current_dialog = None
        else:
            self.current_dialog = self.queue.get()

    def next_popup(self):
        if self.popup_queue.empty():
            self.current_popup = None
        else:
            self.current_popup = self.popup_queue.get()

    def clear_choiceset(self, sender):
        if sender is not self.current_chooser:
            print("this mission's choice set was cleared by something else")
        self.current_chooser = None

    def update(self, game, events):
        if self.current_dialog:
            self.current_dialog.update(game, events)
            for event in events:
                if event.type == pygame.KEYUP and \
                   (event.key == pygame.K_KP_ENTER or \
                    event.key == pygame.K_RETURN or \
                    event.key == pygame.K_SPACE):
                    self.current_dialog.next_or_skip()
                    break
        if self.current_popup:
            self.current_popup.update(game, events)
        if self.current_chooser:
            self.current_chooser.update(game, events)

    def draw(self, layer):
        if self.current_dialog:
            self.current_dialog.draw(layer)
        if self.current_popup:
            self.current_popup.draw(layer)
        if self.current_chooser:
            self.current_chooser.draw(layer)

    def get_all_viewed(self):
        return prefs.savedgame.get(self.owner.dialog_key, [])

    def set_viewed(self, text_key):
        all_viewed = self.get_all_viewed()
        if text_key in all_viewed:
            return False
        all_viewed.append(text_key)
        prefs.savedgame.set(self.owner.dialog_key, all_viewed)
        return True

    def get_viewed(self, text_key):
        all_viewed = self.get_all_viewed()
        return (text_key in all_viewed)

    def compute_position(self, target_rect, side):
        position = (0, 0)

        dialog_centerx = (game.layer_size[0] / 2) - (target_rect.width / 2)
        dialog_centery = (game.layer_size[1] / 2) - (target_rect.height / 2)
        dialog_leftx = 64
        dialog_topy = 25
        dialog_rightx = game.layer_size[0] - target_rect.width - dialog_leftx
        dialog_bottomy = game.layer_size[1] - dialog_topy - target_rect.height

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

        return position

    # Add dialogue with all features
    def add_custom(self, text_key, name, text, portrait_id = None, side = None, flags = DialogFlags.NORMAL, callback = None):
        if not side:
            side = self.default_side
        position = self.compute_position(RECT_DIALOG, side)
        dialog = Dialog(self, position, text_key, name, text, portrait_id, flags, callback)
        self.queue.put(dialog)
        if not self.current_dialog:
            self.next()
        utils.reset_cursor()
        return dialog

    # Add dialogue with all features except with custom text/name
    def add(self, character_id, text_id, portrait_id = None, side = None, flags = DialogFlags.NORMAL, callback = None, repeat = True):
        text_id_final = text_id
        # Choose a random text ID if we've received a list
        if isinstance(text_id, list):
            text_id_final = random.choice(text_id)
        string = self.owner.get_string(character_id, text_id_final)
        is_viewed = self.get_viewed(string[2])
        if not repeat and is_viewed:
            return
        return self.add_custom(
            string[2],
            string[0],
            string[1],
            portrait_id,
            side,
            flags,
            callback
        )

    def add_popup(self, item_id, side = DialogSide.BOTTOM_LEFT):
        item_name = utils.get_item_string(item_id)
        position = self.compute_position(RECT_POPUP, side)
        popup = Popup(self, position, item_name)
        self.popup_queue.put(popup)
        if not self.current_popup:
            self.next_popup()
        return popup
