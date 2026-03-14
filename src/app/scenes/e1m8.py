from engine import game, ClickableEntity
from app import scene_list, utils
from app.entities import Label, ChoiceSet, KeyedButton
from app.dialog import DialogSide
from app.mission import Mission

import pygame


class E1M8Scene(Mission):
    SW_REPORT_INDEX = "e1_report_index"
    SW_REPORT_SCORE = "e1_report_score"
    SW_REPORT_DONE = "e1_report_done"

    def __init__(self):
        super().__init__(1, 8, "", "Report Writing")
        self.report_entries = []

    def _get_report_entries(self):
        report_data = utils.strings.get("report", {})
        entries = report_data.get("e1", [])
        if not isinstance(entries, list):
            return []
        return entries

    def _get_report_index(self):
        index = self.find_switch(self.SW_REPORT_INDEX)
        if not isinstance(index, int):
            index = 0
        return index

    def _get_report_score(self):
        score = self.find_switch(self.SW_REPORT_SCORE)
        if not isinstance(score, int):
            score = 0
        return score

    def _set_report_state(self, index=None, score=None):
        if index is not None:
            self.set_switch(self.SW_REPORT_INDEX, index)
        if score is not None:
            self.set_switch(self.SW_REPORT_SCORE, score)

    def _to_ep2(self, sender=None, button=None):
        game.scenes.set_scene("e1mend")

    def _create_screen_overlay(self):
        overlay = ClickableEntity(
            self,
            (0, 0),
            game.layer_size,
            pygame.Surface(game.layer_size, pygame.SRCALPHA, 32),
            False,
        )
        surface = overlay.get_surface()
        if surface:
            surface.fill((0, 0, 0, 165))
        return overlay

    def _finish_report(self):
        self.emitter.current_selector = None

        total = len(self.report_entries)
        score = self._get_report_score()
        if score > total:
            score = total

        self.set_switch(self.SW_REPORT_DONE, True)

        verdict = "Solid reporting"
        if total > 0:
            ratio = score / total
            if ratio < 0.6:
                verdict = "Needs stronger notes"
            elif ratio < 0.9:
                verdict = "Good draft, some misses"

        summary = "Report complete: {}/{} | {}".format(score, total, verdict)
        self.emitter.add_note(
            "{}/{} correct | {}".format(score, total, verdict),
            duration_ms=4200,
            title="Summary"
        )

        label_done = Label(
            self,
            "Draft complete.",
            utils.get_font(48),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_done.set_position((
            (game.layer_size[0] / 2) - (label_done.get_rect().width / 2),
            235,
        ))

        label_summary = Label(
            self,
            summary,
            utils.get_font(30),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_summary.set_position((
            (game.layer_size[0] / 2) - (label_summary.get_rect().width / 2),
            320,
        ))

        btn_continue = KeyedButton(self, (555, 630), "Continue", pygame.K_x, "X")
        btn_continue.click += self._to_ep2

        self.entities = {
            "overlay": self._create_screen_overlay(),
            "label_done": label_done,
            "label_summary": label_summary,
            "btn_continue": btn_continue,
        }

    def _on_answer_selected(self, sender, value):
        index = self._get_report_index()
        if index < 0 or index >= len(self.report_entries):
            self._finish_report()
            return

        selected = -1
        if isinstance(value, tuple) and len(value) > 0:
            try:
                selected = int(value[0]) - 1
            except (TypeError, ValueError):
                selected = -1

        entry = self.report_entries[index]
        correct_answer = entry.get("answer")

        score = self._get_report_score()
        if selected == correct_answer:
            score += 1
            self.emitter.add_note(
                "Detail marked correct.",
                side=DialogSide.BOTTOM_RIGHT,
                duration_ms=1800,
                title="Draft"
            )
        else:
            self.emitter.add_note(
                "Detail marked incorrect.",
                side=DialogSide.BOTTOM_RIGHT,
                duration_ms=1800,
                title="Draft"
            )

        self._set_report_state(index=index + 1, score=score)
        self._render_current_prompt()

    def _render_current_prompt(self):
        self.emitter.current_selector = None

        index = self._get_report_index()
        total = len(self.report_entries)
        if index >= total:
            self._finish_report()
            return

        entry = self.report_entries[index]
        title = entry.get("title", "Untitled")
        description = entry.get("description", "")
        choices = entry.get("choices", [])
        if not isinstance(choices, list):
            choices = []

        choice_items = [str(text) for text in choices]
        if not choice_items:
            choice_items = ["No options"]

        label_header = Label(
            self,
            "REPORT WRITING",
            utils.get_font(40),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_header.set_position((
            (game.layer_size[0] / 2) - (label_header.get_rect().width / 2),
            72,
        ))

        label_progress = Label(
            self,
            "Prompt {}/{}".format(index + 1, total),
            utils.get_font(28),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_progress.set_position((
            (game.layer_size[0] / 2) - (label_progress.get_rect().width / 2),
            122,
        ))

        label_title = Label(
            self,
            str(title),
            utils.get_font(30),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_title.set_position((220, 200))

        label_description = Label(
            self,
            str(description),
            utils.get_font(21),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )
        label_description.set_position((220, 250))

        label_select = Label(
            self,
            "SELECT DETAIL",
            utils.get_font(30),
            pygame.Color("white"),
            outline_color=(0, 0, 0),
            outline_width=2,
        )

        selector = ChoiceSet(
            self,
            (0, 0),
            choice_items,
            hide_on_select=False,
            handle_keys=True,
        )
        selector.set_position((
            (game.layer_size[0] / 2) - (selector.get_rect().width / 2),
            505,
        ))
        label_select.set_position((
            (game.layer_size[0] / 2) - (label_select.get_rect().width / 2),
            445,
        ))

        selector.selected += self._on_answer_selected
        self.emitter.current_selector = selector

        self.entities = {
            "overlay": self._create_screen_overlay(),
            "label_header": label_header,
            "label_progress": label_progress,
            "label_title": label_title,
            "label_description": label_description,
            "label_select": label_select,
        }

    def load_content(self):
        super().load_content()

        if self.find_switch(self.SW_REPORT_DONE):
            game.scenes.set_scene("e1mend")
            return

        self.background.set_surface(utils.load_em_image(1, 1, "bg-main"))

        self.report_entries = self._get_report_entries()
        if not self.report_entries:
            self.emitter.add_note(
                "Report metadata missing; skipping.",
                duration_ms=1200,
                callback=lambda: game.scenes.set_scene("e1mend"),
            )
            return

        if not isinstance(self.find_switch(self.SW_REPORT_INDEX), int):
            self.set_switch(self.SW_REPORT_INDEX, 0)
        if not isinstance(self.find_switch(self.SW_REPORT_SCORE), int):
            self.set_switch(self.SW_REPORT_SCORE, 0)

        self._render_current_prompt()


scene_list.add_mission(E1M8Scene())
