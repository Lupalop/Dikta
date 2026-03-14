from engine import game, ClickableEntity
from app import defaults, scene_list, utils
from app.entities import ChoiceSet, KeyedButton, ListBox, Image
from app.mission import Mission
from app.dialog import DialogSide

import pygame
from typing import Any, cast

CHOICE_KEYS = {
    1: "fact",
    2: "doubt",
    3: "accuse",
}

QUESTION_RESULT_CORRECT = "correct"
QUESTION_RESULT_WRONG = "wrong"

class InterrogationBase(Mission):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, side)
        self.tree_name = tree_name
        self._tree_cache = None
        self._btn_clues = None
        
        # Switches
        self.SW_TALK1 = "e{}m{}_talk1".format(episode_id, mission_id)
        self.SW_QUESTIONS = "e{}m{}_fda_questions".format(episode_id, mission_id)
        self.SW_QUESTION_CURRENT = "e{}m{}_fda_question_id".format(episode_id, mission_id)
        self.SW_FDA_CHOICE = "e{}m{}_fda_choice".format(episode_id, mission_id)
        self.SW_PRESENTED_CLUE = "e{}m{}_presented_clue".format(episode_id, mission_id)
        self.SW_RETURN_TO_CHOICES = "e{}m{}_fda_return_to_choices".format(episode_id, mission_id)
        self.SW_CORRECT_COUNT = "e{}m{}_fda_correct_count".format(episode_id, mission_id)
        self.SW_RESULT_PENDING = "e{}m{}_fda_result_pending".format(episode_id, mission_id)

    def _get_total_questions_count(self):
        tree = self._load_tree()
        questions = tree.get("questions") if isinstance(tree, dict) else None
        if isinstance(questions, list):
            return len(questions)

        loaded = self.find_switch(self.SW_QUESTIONS)
        if isinstance(loaded, list):
            return len(loaded)
        return 0

    def _render_question_text(self, item):
        text_base = item.get("text_base", item.get("text", ""))
        item["text_base"] = text_base

        status_icon = None
        if item.get("locked", False):
            status_icon = "lock"
        elif item.get("result") == QUESTION_RESULT_CORRECT:
            status_icon = "correct"
        elif item.get("result") == QUESTION_RESULT_WRONG:
            status_icon = "wrong"

        item["status_icon"] = status_icon
        item["text"] = text_base

    def _set_question_result(self, question_value, result):
        questions = self.find_switch(self.SW_QUESTIONS)
        if not isinstance(questions, list):
            return False

        for item in questions:
            if item.get("value") != question_value:
                continue

            item["locked"] = False
            item["disabled"] = True
            item["result"] = result
            self._render_question_text(item)
            self.set_switch(self.SW_QUESTIONS, questions)
            return True

        return False

    def _get_callbacks(self):
        return {}

    def _load_tree(self):
        if self._tree_cache is None:
            self._tree_cache = utils.load_json_asset(self.tree_name)
        return self._tree_cache

    def _build_review_clues_button(self, pos=(64, 64)):
        btn_clues = KeyedButton(self, pos, "Review clues", pygame.K_F12, "TAB")
        btn_clues.leftclick += lambda sender=None: getattr(scene_list.all["ig_clues"], "toggle_visibility", lambda: None)()
        return btn_clues

    def _set_review_clues_button_visible(self, visible):
        if not visible:
            self._btn_clues = None
            return
        if self._btn_clues:
            return
        self._btn_clues = self._build_review_clues_button((64, 64))

    def update(self, game, events):
        super().update(game, events)
        if self._btn_clues:
            self._btn_clues.update(game, events)
            self._call_captured()

    def draw(self, layer):
        super().draw(layer)
        if self._btn_clues:
            self._btn_clues.draw(layer)

    def _emit_node(self, node, callbacks, repeat_override=None):
        cb_name = node.get("callback")
        cb = callbacks.get(cb_name) if cb_name else None
        clue_id = node.get("grants_clue")
        if clue_id:
            original_cb = cb
            def _grant_and_cb(clue=clue_id, next_cb=original_cb):
                self.add_clue(clue)
                if next_cb:
                    next_cb()
            cb = _grant_and_cb
        self.emitter.add(
            node["character"], node["text_id"],
            callback=cb,
            repeat=(node.get("repeat", True) if repeat_override is None else repeat_override)
        )

    def _run_dialog_tree(self, branch, callbacks):
        tree = self._load_tree()
        
        # If intro branch
        if branch not in tree:
            return

        # Check for first talk
        talk1 = self.find_switch(self.SW_TALK1)
        if not talk1 and "intro" in tree[branch]:
            for node in tree[branch]["intro"]:
                self._emit_node(node, callbacks)
            return
            
        return self._run_question_tree(branch, callbacks)

    def _run_question_tree(self, branch, callbacks):
        tree = self._load_tree()
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        if q is None:
            return
        
        choice = self.find_switch(self.SW_FDA_CHOICE)
        q_data = tree[branch]["questions"][q]
        replay_initial = (choice is None)
        for node in q_data["initial"]:
            # Replay initial nodes only when the question has no selected FDA
            # choice yet (save-load recovery path).
            self._emit_node(node, callbacks, repeat_override=(True if replay_initial else None))

        choice_key = CHOICE_KEYS.get(choice) if isinstance(choice, int) else None
        choice_data = q_data["choices"].get(choice_key) if choice_key else None
        if not choice_data:
            return

        if choice_key != "accuse":
            nodes = choice_data.get("nodes", [])
        else:
            responses = choice_data.get("clue_responses")
            if not responses:
                # Simple accusation with no clue selection logic on this side.
                nodes = choice_data.get("nodes", [])
            else:
                # We haven't picked a clue yet, but we are in Dan's scene.
                # This shouldn't happen unless we're waiting for Joe.
                presented = self.find_switch(self.SW_PRESENTED_CLUE)
                if isinstance(presented, dict):
                    presented = presented.get("id")
                if presented is None:
                    return
                try:
                    nodes = responses.get(presented, responses.get("else", []))
                except TypeError:
                    nodes = responses.get("else", [])

        for node in nodes:
            self._emit_node(node, callbacks, repeat_override=True)

    def _show_result_and_switch(self, next_scene):
        if self.find_switch(self.SW_RESULT_PENDING):
            return

        total = self._get_total_questions_count()

        correct = self.find_switch(self.SW_CORRECT_COUNT)
        if not isinstance(correct, int):
            correct = 0

        # Guard against stale values from previous runs.
        if correct > total:
            correct = total

        if total <= 0:
            verdict = "No questions answered"
        else:
            ratio = correct / total
            if ratio >= 0.9:
                verdict = "Solid read on the witness"
            elif ratio >= 0.6:
                verdict = "Good read, some loose ends"
            else:
                verdict = "Weak read, revisit testimony"

        self.set_switch(self.SW_RESULT_PENDING, True)

        outro_characters = [c for c in self._get_outro_characters() if c]
        pending = 2 if outro_characters else 1

        def _finish_part():
            nonlocal pending
            pending -= 1
            if pending > 0:
                return
            self.set_switch(self.SW_RESULT_PENDING, False)
            game.scenes.set_scene(next_scene)

        if outro_characters:
            self._switch_speaker_visual(outro_characters[0])
            for i, character in enumerate(outro_characters):
                next_character = outro_characters[i + 1] if i + 1 < len(outro_characters) else None
                callback = (lambda ch=next_character: self._switch_speaker_visual(ch)) if next_character else _finish_part
                self.emitter.add(character, "outro_result", callback=callback)

        self.emitter.add_note(
            "Questions: {}/{} Correct | {}".format(correct, total, verdict),
            duration_ms=3200,
            callback=_finish_part
        )

    def _get_outro_characters(self):
        return []

    def _switch_speaker_visual(self, character, callback=None):
        self._apply_outro_cutout(character)
        if callback:
            callback()

    def _get_outro_visual(self, character) -> dict[str, Any] | None:
        return None

    def _apply_outro_cutout(self, character):
        visual = self._get_outro_visual(character)
        if not visual or not isinstance(self.entities, dict):
            return

        background_id = visual.get("background")
        if background_id:
            self.background.set_surface(self.get_image(background_id))

        # Keep only speaker-dependent visuals in sync for the outro sequence.
        self.entities.pop("prop_people", None)

        for key in [k for k in self.entities.keys() if isinstance(k, str) and k.startswith("ca_")]:
            self.entities.pop(key, None)

        prop_id = visual.get("prop")
        prop_pos = visual.get("prop_pos")
        if prop_id and prop_pos:
            self.entities["prop_people"] = Image(self, self.get_image(prop_id), prop_pos)

        cutout_id = visual.get("cutout")
        cutout_pos = visual.get("cutout_pos")
        if cutout_id and cutout_pos:
            self.entities["ca_{}".format(character)] = Image(self, utils.load_ca_image(cutout_id), cutout_pos)

class InterrogationConversation(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, questions_scene, next_scene, interrogator_branch, respondent_branch, side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.questions_scene = questions_scene
        self.next_scene = next_scene
        self.interrogator_branch = interrogator_branch
        self.respondent_branch = respondent_branch
        self.SW_ACTIVE_BRANCH = "e{}m{}_fda_active_branch".format(episode_id, mission_id)
        self._pending_return_to_questions = False

    def load_content(self):
        super().load_content()
        self._pending_return_to_questions = False

        # Match original split-scene behavior: every entry from question select
        # starts on the interrogator side.
        active_branch = self.interrogator_branch
        self.set_switch(self.SW_ACTIVE_BRANCH, active_branch)

        self._apply_outro_cutout(active_branch)
        self._run_dialog_tree(active_branch, self._get_callbacks())

        # Save-load fallback: if all repeat=false nodes were already viewed,
        # the emitter can end up with no dialog and no selector.
        if not self.emitter.current_dialog and not self.emitter.current_selector:
            self._pending_return_to_questions = True

    def _resolve_generic_vox(self, character_id, text_key):
        if character_id == self.interrogator_branch:
            options = ["joe_generic1", "joe_generic2"]
        elif character_id == self.respondent_branch:
            options = ["respondent_generic1", "respondent_generic2", "respondent_generic3"]
        else:
            return None

        available = [key for key in options if utils.load_vox(key)]
        if not available:
            return None

        # Keep fallback selection deterministic per text key.
        stable_index = sum(ord(ch) for ch in text_key) % len(available)
        return available[stable_index]

    def get_string(self, character_id, text_id):
        name, text, text_key, vox_key = super().get_string(character_id, text_id)

        # Prefer authored VOX line when available.
        if utils.load_vox(vox_key):
            return (name, text, text_key, vox_key)

        generic_vox = self._resolve_generic_vox(character_id, text_key)
        if generic_vox:
            return (name, text, text_key, generic_vox)

        return (name, text, text_key, vox_key)

    def _get_callbacks(self):
        def finish_question():
            q = self.find_switch(self.SW_QUESTION_CURRENT)
            self._set_question_result(q, QUESTION_RESULT_WRONG)
            self._to_questions()

        def backoff_to_choices():
            self.set_switch(self.SW_FDA_CHOICE, None)
            self.set_switch(self.SW_PRESENTED_CLUE, None)
            self._show_fda()

        callbacks = super()._get_callbacks()
        callbacks.update({
            "to_interrogator": lambda: self._switch_branch_and_run(self.interrogator_branch),
            "to_respondent": lambda: self._switch_branch_and_run(self.respondent_branch),
            "to_questions": self._to_questions,
            "show_fda": self._show_fda,
            "backoff_to_choices": backoff_to_choices,
            "finish_question": finish_question,
            "mark_correct": self._mark_correct,
            "accuse": self._accuse,
        })
        return callbacks

    def update(self, game, events):
        super().update(game, events)

        if self._pending_return_to_questions:
            self._pending_return_to_questions = False
            self._to_questions()
            return

        selector = self.emitter.current_selector
        if not isinstance(selector, ListBox):
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
                selector._on_cancelled()
                break

    def _fade_switch_visual(self, character, callback=None):
        duration_ms = 180
        overlay_key = "_vn_visual_fade"

        if not isinstance(self.entities, dict):
            self._apply_outro_cutout(character)
            if callback:
                callback()
            return

        # Guard against overlapping transitions.
        if self.entities.get(overlay_key):
            self._apply_outro_cutout(character)
            if callback:
                callback()
            return

        overlay = ClickableEntity(
            self,
            (0, 0),
            game.layer_size,
            pygame.Surface(game.layer_size, pygame.SRCALPHA, 32)
        )
        overlay_surface = overlay.get_surface()
        if overlay_surface:
            overlay_surface.fill((0, 0, 0))
            overlay_surface.set_alpha(0)
        self.entities[overlay_key] = overlay

        def _on_fadein_done(sender = None):
            self._apply_outro_cutout(character)

            def _on_fadeout_done(fade_sender = None):
                self.entities.pop(overlay_key, None)
                if callback:
                    callback()

            self.animator.fadeout(overlay, duration_ms, callback=_on_fadeout_done)

        self.animator.fadein(overlay, duration_ms, callback=_on_fadein_done)

    def _switch_branch_and_run(self, branch):
        if branch not in (self.interrogator_branch, self.respondent_branch):
            return

        current_branch = self.find_switch(self.SW_ACTIVE_BRANCH)
        self.set_switch(self.SW_ACTIVE_BRANCH, branch)

        def run_branch():
            if branch == self.respondent_branch and self.find_switch(self.SW_RETURN_TO_CHOICES):
                self.clear_switch(self.SW_RETURN_TO_CHOICES)
                self._show_fda()
                return
            self._set_review_clues_button_visible(False)
            self._run_dialog_tree(branch, self._get_callbacks())

        if current_branch == branch:
            run_branch()
            return

        self._fade_switch_visual(branch, callback=run_branch)

    def _switch_speaker_visual(self, character, callback=None):
        self._fade_switch_visual(character, callback=callback)

    def _to_questions(self):
        questions = self.find_switch(self.SW_QUESTIONS)
        has_remaining = bool(questions) and any(not item.get("disabled", False) for item in questions)

        if not questions or has_remaining:
            game.scenes.set_scene(self.questions_scene)
        else:
            self._show_result_and_switch(self.next_scene)

    def _mark_correct(self):
        current_correct = self.find_switch(self.SW_CORRECT_COUNT)
        if not isinstance(current_correct, int):
            current_correct = 0

        q = self.find_switch(self.SW_QUESTION_CURRENT)
        if self._set_question_result(q, QUESTION_RESULT_CORRECT):
            self.set_switch(self.SW_CORRECT_COUNT, current_correct + 1)
        self._to_questions()

    def _show_fda(self):
        if self.find_switch(self.SW_FDA_CHOICE) is not None:
            return

        if self.emitter.current_selector:
            return

        choiceset = ChoiceSet.from_entity(self, defaults.FDA_CHOICESET)
        choiceset.selected += self._handle_choice
        choiceset.hidden += self.emitter.clear_choiceset
        self.emitter.current_selector = choiceset
        self._set_review_clues_button_visible(True)

    def _accuse(self):
        items = self.emitter.add_clues_selector()

        def _on_clue_selected(sender, data):
            clue_id = data.get("id")
            self.set_switch(self.SW_PRESENTED_CLUE, clue_id)
            self._switch_branch_and_run(self.respondent_branch)

        def _on_clue_cancelled(sender):
            self.set_switch(self.SW_FDA_CHOICE, None)
            self.set_switch(self.SW_PRESENTED_CLUE, None)
            self.set_switch(self.SW_RETURN_TO_CHOICES, True)

            def _after_selector_hidden(hidden_sender):
                self.emitter.add(
                    self.interrogator_branch,
                    "accuse_backdown",
                    callback=lambda: self._switch_branch_and_run(self.respondent_branch)
                )

            items.hidden += _after_selector_hidden

        items.selected += _on_clue_selected
        items.cancelled += _on_clue_cancelled

    def _handle_choice(self, sender, value):
        i = value[0]
        self.set_switch(self.SW_FDA_CHOICE, i)
        self.set_switch(self.SW_PRESENTED_CLUE, None)
        self._set_review_clues_button_visible(False)
        choice_key = CHOICE_KEYS.get(i) if isinstance(i, int) else None

        if choice_key in ("fact", "doubt", "accuse"):
            sender.hidden += lambda hidden_sender: self._switch_branch_and_run(self.interrogator_branch)
            return

        self._run_question_tree(self.respondent_branch, self._get_callbacks())

        tree = self._load_tree()
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        q_data = tree[self.respondent_branch]["questions"][q]

        choice_data = q_data["choices"].get(choice_key, {})
        if choice_data.get("nodes") or choice_data.get("clue_responses"):
            return

        is_correct = choice_data.get("correct", False)

        def _to_scene(hidden_sender):
            if is_correct:
                self._mark_correct()
            else:
                self._switch_branch_and_run(self.interrogator_branch)

        sender.hidden += _to_scene

    def _get_outro_characters(self):
        speakers = []
        if self.respondent_branch:
            speakers.append(self.respondent_branch)
        if self.interrogator_branch and self.interrogator_branch not in speakers:
            speakers.append(self.interrogator_branch)
        return speakers

class InterrogationMenu(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, interrogator_scene, title="QUESTIONS", pos=(312, 192), side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.interrogator_scene = interrogator_scene
        self.menu_title = title
        self.menu_pos = pos

    def load_content(self):
        super().load_content()
        self._load_questions()
        listbox = ListBox(
            self,
            self.menu_pos,
            self.menu_title,
            self.questions,
            show_disabled=True,
            strike_disabled=True
        )
        listbox.selected += self._listbox_on_selected
        self.set_switch(self.SW_TALK1, True)
        self.entities["listbox"] = listbox

    def _load_questions(self):
        saved_questions = self.find_switch(self.SW_QUESTIONS)
        if not isinstance(saved_questions, list):
            saved_questions = []

        saved_by_value = {
            item.get("value"): item
            for item in saved_questions
            if isinstance(item, dict)
        }

        clues = self.get_clues()
        tree_questions = self._load_tree().get("questions", [])
        if not isinstance(tree_questions, list):
            tree_questions = []
        normalized_questions = []

        for base_item in tree_questions:
            if not isinstance(base_item, dict):
                continue

            item = cast(dict[str, Any], dict(base_item))
            item["text_base"] = item.get("text", "")
            value = item.get("value")
            saved = saved_by_value.get(value)
            if not isinstance(saved, dict):
                saved = {}

            is_locked = item.get("requires_clue") is not None and item.get("requires_clue") not in clues

            item["locked"] = is_locked
            item["result"] = saved.get("result")

            if is_locked:
                item["disabled"] = True
            else:
                item["disabled"] = bool(saved.get("disabled", False))

            if isinstance(saved.get("text_base"), str):
                item["text_base"] = saved.get("text_base")

            self._render_question_text(item)
            normalized_questions.append(item)

        self.questions = normalized_questions
        self.set_switch(self.SW_QUESTIONS, self.questions)

        if not saved_questions:
            self.set_switch(self.SW_CORRECT_COUNT, 0)
            self.set_switch(self.SW_RESULT_PENDING, False)

    def _listbox_on_selected(self, sender, data):
        self.set_switch(self.SW_QUESTION_CURRENT, data["value"])
        self.set_switch(self.SW_FDA_CHOICE, None)
        self.set_switch(self.SW_PRESENTED_CLUE, None)
        game.scenes.set_scene(self.interrogator_scene)
