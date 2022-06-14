from engine import *
from app import utils, scene_list
from app.entities import *

import pygame

class CreditsScene(Scene):
    def __init__(self):
        super().__init__("Credits")

    def load_content(self):
        utils.set_music("main_menu", 0.5)

        self._labels = []
        data = content.read_all_lines("credits.txt")
        self.scroll_height = game.layer_size[1]
        self.scroll_pos = game.layer_size[1]
        for line in data:
            font = utils.get_font(24)
            if line.startswith("+"):
                font = utils.get_font(30)
                font.strong = True
                line = line[1:]
            if line.startswith("-"):
                font = utils.get_font(26)
                font.strong = True
                line = line[1:]
                
            line_label = Label(
                self,
                line,
                font,
                pygame.Color("white"),
                ignore_newline = True)
            line_label.set_position((
                (game.layer_size[0] / 2) - (line_label.get_size()[0] / 2),
                self.scroll_height
            ))
            self.scroll_height += line_label.get_rect().height + (font.get_sized_height() / 2)
            self._labels.append(line_label)

        def _animate(entity, position, reset_position = True):
            if reset_position:
                entity.set_position(position)
            self.animator.to_position(
                entity,
                500 * len(data),
                [
                    None,
                    -self.scroll_height
                ],
                True,
                lambda label_bound=entity, initial_bound=position: \
                    _animate(label_bound, initial_bound)
            )

        for label in self._labels:
            initial = label.get_position()
            _animate(label, initial, False)

        btn_exit = KeyedButton(self, (64, 64), "Back", pygame.K_x, "X")
        btn_exit.click += self._to_main_menu

        self.entities = {
            "btn_exit": btn_exit,
        }

    def update(self, game, events):
        super().update(game, events)
        return
        for label in self._labels:
            label.set_position((
                label.get_position()[0],
                label.get_position()[1] - 1
            ))

    def draw(self, layer):
        super().draw(layer)
        for label in self._labels:
            label.draw(layer)

    def _to_main_menu(self, sender, button):
        game.scenes.set_scene("main_menu")

scene_list.all["credits"] = CreditsScene()
