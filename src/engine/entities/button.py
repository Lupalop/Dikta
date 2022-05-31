from engine.entities import Entity, Image, Label
from engine.enums import MouseButton, ButtonState

import pygame

class Button(Entity):
    def __init__(self, button_states, text, font, color, position_or_rect, size = None):
        super().__init__(position_or_rect, size)

        if not "normal" in button_states:
            raise ValueError("A 'normal' state should be present in the specified button states.")

        self._button_states = button_states

        self._images = {}
        for key in button_states:
            surface = button_states[key]
            image = Image(surface, position_or_rect, size)
            image.set_position(self.get_position())
            if self.get_size() != (0, 0):
                image.set_size(self.get_size())
            self._images[key] = image

        if not "hover" in button_states:
            self._images["hover"] = self._images["normal"]

        if not "active" in button_states:
            self._images["active"] = self._images["normal"]

        self._current_image = self._images["normal"]

        if self.get_size() == (0, 0):
            self._rect.size = self._current_image.get_size()

        self._label = Label(text, font, color, (0, 0))
        self._update_child_label()
        self.state = ButtonState.NORMAL

    @classmethod
    def from_entity(cls, entity):
        return self.from_button(entity, entity._label.get_text())
    @classmethod
    def from_button(cls, entity, text, copy_handlers = False):
        copiedEntity = cls(entity._button_states,
                           text,
                           entity._label.get_font(),
                           entity._label.get_color(),
                           entity._rect)
        if copy_handlers:
            copiedEntity.on_left_click = entity.on_left_click
            copiedEntity.on_middle_click = entity.on_middle_click
            copiedEntity.on_right_click = entity.on_right_click
        return copiedEntity

    def get_surface(self):
        return self._current_image.get_surface()

    def set_surface(self, surface):
        print("Changing the surface of a Button entity is not allowed.")

    def get_mask(self):
        return self._current_image.get_mask()

    def intersects_rect(self, point):
        return self._current_image.intersects_rect(point)

    def intersects_mask(self, point):
        return self._current_image.intersects_mask(point)

    # Overridden base entity setter functions

    def _update_child_images(self, is_position_only = False):
        if is_position_only:
            for image in self._images.values():
                image.set_position(self.get_position())
            return

        for image in self._images.values():
            image.set_size(self.get_size())
            image.set_position(self.get_position())

    def _update_child_label(self):
        if not self._label:
            return
        label_pos = (self._current_image.get_rect().centerx - (self._label.get_rect().width / 2),
                     self._current_image.get_rect().centery - (self._label.get_rect().height / 2))
        self._label.set_position(label_pos)

    def set_size(self, size):
        super().set_size(size)
        self._update_child_images()
        self._update_child_label()

    def set_rect(self, rect):
        super().set_rect(rect)
        self._update_child_images()
        self._update_child_label()

    def set_position(self, position):
        super().set_position(position)
        self._update_child_images(True)
        self._update_child_label()

    # Label
    def get_text(self):
        return self._label.get_text()

    def set_text(self, text):
        self._label.set_text(text)

    def get_font(self):
        return self._label.get_font()

    def set_font(self, font):
        self._label.set_font(font)

    def get_color(self):
        return self._label.get_color()

    def set_color(self, color):
        self._label.set_color(color)

    # Event handlers

    def on_left_click(self):
        pass

    def on_middle_click(self):
        pass

    def on_right_click(self):
        pass

    def update(self, game, events):
        is_mb_down = False
        is_mb_up = False
        button = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mb_down = True
                button = event.button
            if event.type == pygame.MOUSEBUTTONUP:
                is_mb_up = True
                button = event.button

        is_hovered = self.intersects_mask(game.get_mouse_pos())

        if self.state == ButtonState.ACTIVE:
            if is_mb_up:
                self.state = ButtonState.RELEASED
                # Execute click handlers only if the mouse button was
                # released while hovering on this button.
                if is_hovered:
                    if button == MouseButton.LEFT:
                        self.on_left_click()
                    elif button == MouseButton.MIDDLE:
                        self.on_middle_click()
                    elif button == MouseButton.RIGHT:
                        self.on_right_click()
            else:
                return

        if is_hovered:
            if self.state != ButtonState.HOVER:
                self.state = ButtonState.HOVER
                self._current_image = self._images["hover"]
            elif is_mb_down:
                self.state = ButtonState.ACTIVE
                self._current_image = self._images["active"]
        elif self.state != ButtonState.NORMAL:
            self.state = ButtonState.NORMAL
            self._current_image = self._images["normal"]

    def draw(self, layer):
        self._current_image.draw(layer)
        self._label.draw(layer)
