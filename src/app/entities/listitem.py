from engine import ClickableEntity
from engine.enums import ClickState
from app import utils
from app.entities import Label

import pygame

COLOR_ACTIVE = pygame.Color("red")
COLOR_NORMAL = pygame.Color("black")
COLOR_DISABLED = pygame.Color(80, 80, 80)
LABEL_DISTANCE = 16
LISTITEM_RECT = pygame.Rect(0, 0, 400, 32)
LISTITEM_RECT_INF = LISTITEM_RECT.inflate(0, 8)
FONT_HEIGHT = 28
ALPHA_NORMAL = 100
ALPHA_DISABLED = 45
ALPHA_ACTIVE = 255

class ListItem(ClickableEntity):
    def __init__(self, owner, position, data, strike_disabled = False):
        super().__init__(owner, position, LISTITEM_RECT.size, None, tor = False, hit_rect = True)
        self.data = data
        self.strike_disabled = strike_disabled
        self._is_selected = False
        self._anim = None
        self._redraw_surface()

    def _redraw_surface(self):
        color = COLOR_NORMAL
        alpha = ALPHA_NORMAL
        is_disabled = self.data.get("disabled", False)
        if self.is_selected():
            color = COLOR_ACTIVE
            alpha = ALPHA_ACTIVE
        elif is_disabled:
            color = COLOR_DISABLED
            alpha = ALPHA_DISABLED

        status_icon = self.data.get("status_icon")
        surface = pygame.Surface(LISTITEM_RECT_INF.size, pygame.SRCALPHA, 32)
        surface.set_alpha(alpha)
        text_final = self.data["text"]
        self.label_item = Label(
            self.owner, text_final, utils.get_comic_font(FONT_HEIGHT), color)
        self.label_item.set_position((
            38,
            LISTITEM_RECT.height - (FONT_HEIGHT - 7)
        ))
        # pygame.draw.rect(surface, (255, 32, 5, 200), LISTITEM_RECT, 0)
        self._draw_left_marker(surface, status_icon, color)
        self.label_item.draw(surface)

        if is_disabled and self.strike_disabled:
            label_rect = self.label_item.get_rect()
            strike_y = self.label_item.get_position()[1] + (label_rect.height // 2)
            strike_start = (self.label_item.get_position()[0], strike_y)
            strike_end = (self.label_item.get_position()[0] + label_rect.width, strike_y)
            pygame.draw.line(surface, color, strike_start, strike_end, 2)
        self.set_surface(surface)

    def _draw_left_marker(self, surface, status_icon, color):
        cx = 18
        cy = LISTITEM_RECT.height - 11

        if status_icon is None:
            pygame.draw.circle(surface, color, (cx, cy), 5)
            return

        if status_icon == "correct":
            pygame.draw.line(surface, color, (cx - 6, cy), (cx - 1, cy + 5), 4)
            pygame.draw.line(surface, color, (cx - 1, cy + 5), (cx + 7, cy - 6), 4)
            return

        if status_icon == "wrong":
            pygame.draw.line(surface, color, (cx - 6, cy - 5), (cx + 6, cy + 5), 4)
            pygame.draw.line(surface, color, (cx + 6, cy - 5), (cx - 6, cy + 5), 4)
            return

        if status_icon == "lock":
            lock_cy = cy - 1
            body = pygame.Rect(cx - 6, lock_cy - 1, 12, 9)
            pygame.draw.rect(surface, color, body, 2, border_radius=2)
            shackle_rect = pygame.Rect(cx - 5, lock_cy - 9, 10, 9)
            pygame.draw.arc(surface, color, shackle_rect, 3.14, 0.0, 2)
            pygame.draw.circle(surface, color, (cx, lock_cy + 2), 2)

    def is_selected(self):
        return self._is_selected

    def set_is_selected(self, value):
        if value and self.data.get("disabled", False):
            value = False
        self._is_selected = value
        self._redraw_surface()

    @classmethod
    def from_entity(cls, owner, entity, copy_handlers = False):
        entity_copy = cls(owner, entity.get_position(), entity.data, entity.strike_disabled)
        return entity_copy

    def _close_anim(self):
        if self._anim:
            self._anim.close()
            self._anim = None

    # Event handlers
    def _on_click(self, button):
        super()._on_click(button)
        utils.play_sfx("click")

    def _on_state_changed(self, state):
        self._close_anim()

        if state == ClickState.NORMAL:
            normal_alpha = ALPHA_NORMAL
            if self.is_selected():
                normal_alpha = ALPHA_ACTIVE

            self._anim = self.owner.animator.to_alpha(
                self, 250, normal_alpha)
            utils.reset_cursor()
        elif state == ClickState.HOVER or \
             state == ClickState.ACTIVE:
            self._anim = self.owner.animator.to_alpha(
                self, 250, 255)
            utils.set_cursor("select")
        elif state == ClickState.RELEASED:
            pass
        else:
            raise ValueError("unexpected button state")
        super()._on_state_changed(state)
