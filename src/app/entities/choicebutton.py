from engine import ClickableEntity, Entity
from app import utils
from app.entities import Image, Label

import pygame

LABEL_DISTANCE = 16
SURFACE_NUMBER_BOX = utils.load_ui_image("btn-circle")
RECT_NUMBER_BOX = pygame.Rect(0, 0, 48, 48)

class ChoiceButton(ClickableEntity):
    def __init__(self, owner, position, number, label):
        self.text = label
        self.number = number

        self.number_box = Image(
            owner, SURFACE_NUMBER_BOX, RECT_NUMBER_BOX)
        self.number_label = Label(
            owner, str(number), utils.get_font(28), pygame.Color("white"))
        self.number_label.set_position((
            (RECT_NUMBER_BOX.width / 2) - (self.number_label.get_rect().width / 2),
            (RECT_NUMBER_BOX.height / 2) - (self.number_label.get_rect().height / 2)
        ))
        self.choice_label = Label(
            owner, label, utils.get_font(24), pygame.Color("white"), outline_color = (0, 0, 0, 200), outline_width=3)
        self.choice_label.set_position((
            RECT_NUMBER_BOX.width + LABEL_DISTANCE,
            (RECT_NUMBER_BOX.height / 2) - (self.number_label.get_rect().height / 2)
        ))
        rect_final = pygame.Rect(
            0,
            0,
            RECT_NUMBER_BOX.width + LABEL_DISTANCE + self.choice_label.get_rect().width,
            RECT_NUMBER_BOX.height
        )
        surface = pygame.Surface(rect_final.size, pygame.SRCALPHA, 32)
        self.number_box.draw(surface)
        self.number_label.draw(surface)
        self.choice_label.draw(surface)
        self._anim = None

        super().__init__(owner, position, None, surface, hit_rect = True)

    @classmethod
    def from_entity(cls, owner, entity):
        entity_copy = cls(owner, entity.get_surface(), entity._rect)
        return entity_copy

    # Event handlers
    def _on_state_changed(self, state):
        super()._on_state_changed(state)

    def _close_anim(self):
        if self._anim:
            self._anim.close()
            self._anim = None
