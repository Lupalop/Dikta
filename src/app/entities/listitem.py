from engine import ClickableEntity
from engine.enums import MouseButton, ClickState
from app import utils
from app.entities import Image, Label

import pygame

COLOR_ACTIVE = pygame.Color("red")
COLOR_NORMAL = pygame.Color("black")
CHAR_BULLET = "•"
LABEL_DISTANCE = 16
LISTITEM_RECT = pygame.Rect(0, 0, 400, 32)
LISTITEM_RECT_INF = LISTITEM_RECT.inflate(0, 8)
FONT_HEIGHT = 28
ALPHA_NORMAL = 100
ALPHA_ACTIVE = 255

class ListItem(ClickableEntity):
    def __init__(self, owner, position, data):
        super().__init__(owner, position, LISTITEM_RECT.size, None, tor = False, hit_rect = True)
        self.data = data
        self._is_selected = False
        self._anim = None
        self._redraw_surface()

    def _redraw_surface(self):
        color = COLOR_NORMAL
        alpha = ALPHA_NORMAL
        if self.is_selected():
            color = COLOR_ACTIVE
            alpha = ALPHA_ACTIVE
        surface = pygame.Surface(LISTITEM_RECT_INF.size, pygame.SRCALPHA, 32)
        surface.set_alpha(alpha)
        text_final = "{}  {}".format(CHAR_BULLET, self.data["text"])
        self.label_item = Label(
            self.owner, text_final, utils.get_comic_font(FONT_HEIGHT), color)
        self.label_item.set_position((
            25,
            LISTITEM_RECT.height - (FONT_HEIGHT - 8)
        ))
        # pygame.draw.rect(surface, (255, 32, 5, 200), LISTITEM_RECT, 0)
        self.label_item.draw(surface)
        self.set_surface(surface)

    def is_selected(self):
        return self._is_selected

    def set_is_selected(self, value):
        self._is_selected = value
        self._redraw_surface()

    @classmethod
    def from_entity(cls, owner, entity):
        entity_copy = cls(owner, entity.get_surface(), entity._rect)
        return entity_copy

    def _close_anim(self):
        if self._anim:
            self._anim.close()
            self._anim = None

    # Event handlers
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
