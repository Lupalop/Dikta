from engine import ClickableEntity, Entity
from engine.enums import MouseButton, ClickState
from engine.event_handler import EventHandler
from app import utils
from app.entities import Image, Label, ChoiceButton

import pygame

CHOICE_DISTANCE = 25

class ChoiceSet(Entity):
    """
    The items parameter accepts a list with the following format:
    items = [
        "Luneta", "Congress", "Home"
    ]
    After a choice is selected, the sender and the attached item's *one-based*
    index and value is passed to subscribers of the `selected` event.
    """
    def __init__(self, owner, position, items, hide_on_select = False, handle_keys = True, distance = CHOICE_DISTANCE):
        super().__init__(owner, position, None)
        self.hide_on_select = hide_on_select
        self.handle_keys = handle_keys
        self.distance = distance
        self.is_hiding = False
        self.selected = EventHandler()
        self.hidden = EventHandler()
        self._items = items
        self._choices = []
        # Create rectangle for computations.
        rect_final = pygame.Rect(0, 0, 0, 0)
        # Create this choice set's child choices.
        for i in enumerate(self._items):
            i_adjusted = (i[0] + 1, i[1])
            choice = None
            choice_position = (position[0], position[1] + rect_final.height)
            if isinstance(i[1], pygame.Surface):
                choice = ChoiceButton(
                    owner,
                    choice_position,
                    i_adjusted[0],
                    surface = i_adjusted[1]
                )
            else:
                choice = ChoiceButton(
                    owner,
                    choice_position,
                    i_adjusted[0],
                    i_adjusted[1]
                )
            # Add this child choice's height and determine whether to change
            # the choice set's width to the child choice's width.
            rect_final.height += choice.get_rect().height
            if i[0] < len(self._items) - 1:
                rect_final.height += self.distance
            choice_width = choice.get_rect().width
            if choice_width > rect_final.width:
                rect_final.width = choice_width
            # Set the child choice's actions.
            choice.state_changed += self._choice_on_state_changed
            choice.click += lambda sender, button, i_bound=i_adjusted: self._on_selected(i_bound, sender)
            # Include the created choice in the list of child choices.
            self._choices.append(choice)
        # Update the choice set's dimensions.
        self.get_rect().size = rect_final.size

    @classmethod
    def from_entity(cls, owner, entity):
        entity_copy = cls(
            owner,
            entity.get_position(),
            entity._items,
            entity.hide_on_select,
            entity.handle_keys,
            entity.distance
        )
        return entity_copy

    def _on_entity_dirty(self, resize):
        # Create rectangle for computations.
        rect_final = pygame.Rect(0, 0, 0, 0)
        position = self.get_position()
        # Create this choice set's child choices.
        for i in enumerate(self._choices):
            choice = i[1]
            choice.set_position((
                position[0],
                position[1] + rect_final.height
            ))
            # Add this child choice's height and determine whether to change
            # the choice set's width to the child choice's width.
            rect_final.height += choice.get_rect().height
            if i[0] < len(self._items) - 1:
                rect_final.height += self.distance
            choice_width = choice.get_rect().width
            if choice_width > rect_final.width:
                rect_final.width = choice_width
        # Update the choice set's dimensions.
        self.get_rect().size = rect_final.size
        
        self.entity_dirty(self, resize)

    # Event handlers
    def _on_hidden(self, is_target):
        if not is_target:
            return
        self.hidden(self)

    def _choice_on_state_changed(self, sender, state):
        if self.is_hiding:
            return
        # Close any active animations and emphasize the current choice.
        sender._close_anim()
        sender._anim = self.owner.animator.to_alpha(
            sender, 250, 255)
        # De-emphasize the other choices if we're highlighting the current
        # choice. Otherwise, all choices should be of the same opacity.
        target_opacity = 100
        if state == ClickState.NORMAL:
            target_opacity = 255
        # Initialize animators on the remaining choices.
        for choice in self._choices:
            if choice is sender:
                continue
            if choice._anim:
                choice._anim.close()
            choice._anim = self.owner.animator.to_alpha(
                choice, 250, target_opacity)

    def _on_selected(self, value, target_choice):
        self.selected(self, value)
        if not self.hide_on_select:
            return

        self.is_hiding = True
        for choice in self._choices:
            choice._close_anim()
            delay = 0
            is_target = (choice == target_choice)
            if is_target:
                delay = 750
            delay_timer = self.owner.timers.add(delay, True)
            delay_timer.elapsed += lambda \
                sender, choice_bound=choice, is_target_bound=is_target: \
                self.owner.animator.to_alpha(
                    choice_bound,
                    250,
                    0,
                    lambda: self._on_hidden(is_target_bound)
                )

    def _keytochoice(self, character):
        if not character.isnumeric():
            return
        # Get the integer representation of the character and select its
        # matching choice by triggering a left mouse click. This does
        # not handle numbers greater than or equal to 10.
        target = int(character)
        for i in enumerate(self._choices):
            choice = i[1]
            if target == choice.number:
                choice._on_click(MouseButton.LEFT)
                break

    def update(self, game, events):
        # Stop updating the choices if we're hiding.
        if self.is_hiding:
            return
        super().update(game, events)
        for choice in self._choices:
            choice.update(game, events)
        # Process keyboard events only if we're allowed to.
        if self.handle_keys:
            for event in events:
                if event.type == pygame.KEYUP:
                    self._keytochoice(event.unicode)
                    break

    def draw(self, layer):
        super().draw(layer)
        for choice in self._choices:
            choice.draw(layer)
