from engine.enums import ClickState
from engine import game, ClickableEntity, prefs

from app import utils
from app.entities import Label, SequenceLabel, Image, ChoiceSet, ListBox
from app.entities.listbox import LISTBOX_MAIN_RECT as RECT_LISTBOX

import pygame
import random
from enum import IntEnum, IntFlag

RECT_NAME = pygame.Rect(0, 0, 155, 38)
RECT_BASE = pygame.Rect(0, RECT_NAME.height, 765, 90)
RECT_SPEECH = pygame.Rect(20, RECT_NAME.height, RECT_BASE.width - 140, RECT_BASE.height)
RECT_DIALOG = pygame.Rect(0, 0, RECT_BASE.width, RECT_NAME.height + RECT_BASE.height)
RECT_PORTRAIT = pygame.Rect(RECT_DIALOG.x, RECT_DIALOG.y, RECT_DIALOG.height, RECT_DIALOG.height)
RECT_NAME_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_NAME.y, RECT_NAME.width, RECT_NAME.height)
RECT_SPEECH_WP = pygame.Rect(RECT_PORTRAIT.width, RECT_SPEECH.y, RECT_SPEECH.width, RECT_SPEECH.height)
RECT_SIDENOTE = pygame.Rect(0, 0, 340, 72)

TITLE_CLUES = "CLUES"

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
    def __init__(self, emitter, position, text_key, name, text, portrait_id = None, vox_key = None, flags = DialogFlags.NORMAL, callback = None):
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

        # Speech
        self._played = False
        self._vox_key = vox_key
        self._vox = utils.load_vox(self._vox_key) if self._vox_key else None

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
        if self._surface and self.box_name:
            self._surface.blit(self.box_name, rect_name_final)
        self.box_base = utils.load_ui_image("dialog-box-main")
        if self._surface and self.box_base:
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
        raise Exception("Changing the position of a dialog is not allowed.")

    def set_rect(self, rect, resize = True):
        raise Exception("Changing the rectangle of a dialog is not allowed.")

    def set_size(self, size, resize = True):
        raise Exception("Changing the size of a dialog is not allowed.")

    def set_surface(self, surface, resize = True):
        raise Exception("Changing the surface of a dialog is not allowed.")

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
        if self._vox and not self._played:
            self._vox.play()
            self._played = True

    def _can_skip(self):
        return prefs.default.get("game.dialog.can_skip", True)

    def next_or_skip(self):
        if self.label_speech.is_completed and \
           (self.flags & DialogFlags.CLOSEABLE):
            if self.callback:
                self.callback()
            if self._played and self._vox:
                self._vox.stop()
            utils.reset_cursor()
            self.emitter.set_viewed(self.text_key)
            self.emitter.next()
        elif self._can_skip() and \
             (self.flags & DialogFlags.SKIPPABLE):
            self.label_speech.skip()

    # XXX The following overrides the intersection check to always return true,
    # so as to cover the entire screen. This isn't ideal, but it is what it is.
    def intersects(self, point, use_rect = False):
        return True

class DialogEmitter():
    def __init__(self, owner, default_side):
        self.owner = owner
        self.default_side = default_side
        self.queue = []
        self.popup_queue = []
        self.current_dialog = None
        self.current_popup = None
        self.current_selector = None
        self.current_popup_image = None

    def next(self):
        if not self.queue:
            self.current_dialog = None
        else:
            self.current_dialog = self.queue.pop(0)

    def next_popup(self):
        if not self.popup_queue:
            self.current_popup = None
        else:
            self.current_popup = self.popup_queue.pop(0)
            if getattr(self.current_popup, "play_sfx", True):
                utils.play_sfx("clue", 0.5)

    def next_popup_image(self):
        self.current_popup_image = None

    def clear_choiceset(self, sender):
        if sender is not self.current_selector:
            print("this mission's choice set was cleared by something else")
        self.current_selector = None

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
        if self.current_selector:
            self.current_selector.update(game, events)
        if self.current_popup_image:
            self.current_popup_image.update(game, events)

    def draw(self, layer):
        if self.current_dialog:
            self.current_dialog.draw(layer)
        if self.current_popup:
            self.current_popup.draw(layer)
        if self.current_selector:
            self.current_selector.draw(layer)
        if self.current_popup_image:
            self.current_popup_image.draw(layer)

    def get_all_viewed(self):
        if not hasattr(self.owner, "dialog_key"):
            return []
        return prefs.savedgame.get(self.owner.dialog_key, [])

    def set_viewed(self, text_key):
        if not hasattr(self.owner, "dialog_key"):
            return False
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
        dialog_topy = 64
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
            raise Exception("unexpected dialog side")

        return position

    # Add dialogue with all features
    def add_custom(self, text_key, name, text, portrait_id = None, vox_key = None, side = None, flags = DialogFlags.NORMAL, callback = None):
        if not side:
            side = self.default_side
        position = self.compute_position(RECT_DIALOG, side)
        dialog = Dialog(self, position, text_key, name, text, portrait_id, vox_key, flags, callback)
        self.queue.append(dialog)
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
            string[3],
            side,
            flags,
            callback
        )

    def add_popup(self, clue_id, side = DialogSide.TOP_RIGHT):
        clue_name = utils.get_clue_data(clue_id)["name"]
        position = self.compute_position(RECT_SIDENOTE, side)
        popup = SideNote(self, position, "NEW CLUE: {}".format(clue_name), icon_type="clue")
        popup.play_sfx = True
        self.popup_queue.append(popup)
        if not self.current_popup:
            self.next_popup()
        return popup

    def add_note(self, text, side = DialogSide.TOP_RIGHT, callback = None, duration_ms = 2800):
        position = self.compute_position(RECT_SIDENOTE, side)
        popup = SideNote(self, position, text, callback=callback, duration_ms=duration_ms)
        self.popup_queue.append(popup)
        if not self.current_popup:
            self.next_popup()
        return popup

    def add_popup_image(self, surface, side = DialogSide.BOTTOM_RIGHT):
        image = Image(self.owner, surface, (0, 0))
        position = self.compute_position(image.get_rect(), side)
        image.set_position(position)
        self.current_popup_image = image
        return image

    def add_choiceset(self, choices, side = DialogSide.TOP_LEFT, hide_on_select = True):
        choiceset = ChoiceSet(self.owner, (0, 0), choices, hide_on_select, True)
        position = self.compute_position(choiceset.get_rect(), side)
        choiceset.set_position(position)
        choiceset.hidden += self.clear_choiceset
        self.current_selector = choiceset
        return choiceset

    def add_clues_selector(self, side = DialogSide.TOP_LEFT):
        position = self.compute_position(RECT_LISTBOX, side)
        dataset = self.owner.get_clues_dataset()
        listbox = ListBox(self.owner, position, TITLE_CLUES, dataset, True)
        self.current_selector = listbox
        return listbox

class SideNote(ClickableEntity):
    def __init__(self, emitter, position, text, callback = None, duration_ms = 2800, icon_type = "note"):
        super().__init__(
            emitter.owner,
            position,
            RECT_SIDENOTE.size,
            pygame.Surface(RECT_SIDENOTE.size, pygame.SRCALPHA, 32)
        )

        self.emitter = emitter
        self.callback = callback
        self.play_sfx = False
        self._duration_ms = duration_ms
        self._fade_in_ms = 320
        self._fade_out_ms = 420
        self._finished = False
        self._detail_shadow = None
        self._detail_shadow_soft = None
        self._detail_label = None
        self._panel = None
        self._panel_rect = pygame.Rect(0, 0, 0, 0)

        title = "QUESTIONS"
        subtitle = text
        detail = None
        if isinstance(text, str) and ":" in text:
            parts = text.split(":", 1)
            title = parts[0].strip().upper()
            subtitle = parts[1].strip().replace("correct", "Correct")
        if isinstance(subtitle, str) and "|" in subtitle:
            details = subtitle.split("|", 1)
            subtitle = details[0].strip()
            detail = details[1].strip()

        # Layered shadows provide a stronger soft blur behind text.
        self._title_shadow = Label(self.owner, title, utils.get_font(24), pygame.Color(0, 0, 0, 215))
        self._title_shadow_soft = Label(self.owner, title, utils.get_font(24), pygame.Color(0, 0, 0, 120))
        self._title_label = Label(self.owner, title, utils.get_font(24), pygame.Color("white"))
        self._subtitle_shadow = Label(self.owner, subtitle, utils.get_comic_font(20), pygame.Color(0, 0, 0, 205), ignore_newline = True)
        self._subtitle_shadow_soft = Label(self.owner, subtitle, utils.get_comic_font(20), pygame.Color(0, 0, 0, 115), ignore_newline = True)
        self._subtitle_label = Label(self.owner, subtitle, utils.get_comic_font(20), pygame.Color(225, 225, 225), ignore_newline = True)
        if detail:
            self._detail_shadow = Label(self.owner, detail, utils.get_comic_font(16), pygame.Color(0, 0, 0, 190), ignore_newline = True)
            self._detail_shadow_soft = Label(self.owner, detail, utils.get_comic_font(16), pygame.Color(0, 0, 0, 100), ignore_newline = True)
            self._detail_label = Label(self.owner, detail, utils.get_comic_font(16), pygame.Color(210, 210, 210), ignore_newline = True)

        self._icon_type = icon_type
        self._icon = self._build_note_icon()
        self._icon_rect = pygame.Rect(0, 0, 0, 0)
        if self._icon:
            self._icon_rect = self._icon.get_rect()
            self._icon_rect.x = 8
            self._icon_rect.y = 8

        text_left = 36
        self._title_shadow.set_position((text_left + 1, 9))
        self._title_shadow_soft.set_position((text_left + 2, 10))
        self._title_label.set_position((text_left, 8))
        self._subtitle_shadow.set_position((text_left + 1, 39))
        self._subtitle_shadow_soft.set_position((text_left + 2, 40))
        self._subtitle_label.set_position((text_left, 38))
        if self._detail_shadow and self._detail_label:
            self._detail_shadow.set_position((text_left + 1, 57))
            if self._detail_shadow_soft:
                self._detail_shadow_soft.set_position((text_left + 2, 58))
            self._detail_label.set_position((text_left, 56))

        panel_width = text_left + self._title_label.get_rect().width + 16
        row_top = 8
        row_height = max(self._title_label.get_rect().height, self._icon_rect.height if self._icon else 0)
        panel_height = row_height - 4
        self._panel_rect = pygame.Rect(4, row_top, panel_width, panel_height)
        self._panel = self._build_gradient_panel(self._panel_rect.width, self._panel_rect.height)

        hold_ms = max(0, self._duration_ms - self._fade_in_ms - self._fade_out_ms)
        if self._surface:
            self._surface.set_alpha(0)
            self.owner.animator.fadein(
                self,
                self._fade_in_ms,
                callback=self._start_fadeout,
                callback_delay=hold_ms
            )
        else:
            self._on_done(None)

    def _build_gradient_panel(self, width, height):
        # Soft-edge blur: draw in a downscaled surface then smoothscale back up.
        # The 1-pixel transparent border in small space becomes ~6px soft edges.
        SCALE = 6
        pad = 1
        sw = max(pad * 2 + 1, width // SCALE + pad * 2)
        sh = max(pad * 2 + 1, height // SCALE + pad * 2)
        small = pygame.Surface((sw, sh), pygame.SRCALPHA, 32)
        pygame.draw.rect(small, (0, 0, 0, 220), (pad, pad, sw - pad * 2, sh - pad * 2))
        panel = pygame.transform.smoothscale(small, (width, height))
        return panel

    def _build_note_icon(self):
        if self._icon_type == "clue":
            return self._build_clue_icon()
        return self._build_result_icon()

    def _build_clue_icon(self):
        icon = pygame.Surface((24, 24), pygame.SRCALPHA, 32)
        col = pygame.Color(235, 235, 235)

        # Magnifying glass lens
        pygame.draw.circle(icon, col, (10, 9), 6, 2)
        # Handle
        pygame.draw.line(icon, col, (15, 14), (21, 21), 3)

        return icon

    def _build_result_icon(self):
        icon = pygame.Surface((24, 24), pygame.SRCALPHA, 32)

        # Outline speech bubble.
        bubble_rect = pygame.Rect(2, 2, 19, 15)
        pygame.draw.rect(icon, pygame.Color(235, 235, 235), bubble_rect, 2, border_radius=4)
        tail_points = [(9, 17), (11, 22), (14, 17)]
        pygame.draw.polygon(icon, pygame.Color(235, 235, 235), tail_points, 2)

        # Tiny check mark to suggest "correct" results.
        check_points = [(6, 10), (9, 13), (15, 7)]
        pygame.draw.lines(icon, pygame.Color(235, 235, 235), False, check_points, 2)

        return icon

    def _on_done(self, sender):
        if self._finished:
            return
        self._finished = True
        if self.callback:
            self.callback()
        self.emitter.next_popup()

    def _start_fadeout(self):
        self.owner.animator.fadeout(self, self._fade_out_ms, callback=lambda: self._on_done(None))

    def draw(self, layer):
        if not self._surface:
            return

        self._surface.fill((0, 0, 0, 0))
        if self._panel:
            self._surface.blit(self._panel, self._panel_rect.topleft)
        if self._icon:
            self._surface.blit(self._icon, self._icon_rect)
        self._title_shadow.draw(self._surface)
        self._title_shadow_soft.draw(self._surface)
        self._title_label.draw(self._surface)
        self._subtitle_shadow.draw(self._surface)
        self._subtitle_shadow_soft.draw(self._surface)
        self._subtitle_label.draw(self._surface)
        if self._detail_shadow and self._detail_label:
            self._detail_shadow.draw(self._surface)
            if self._detail_shadow_soft:
                self._detail_shadow_soft.draw(self._surface)
            self._detail_label.draw(self._surface)

        layer.blit(self._surface, self._rect)
