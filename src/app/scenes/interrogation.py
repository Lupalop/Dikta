from engine import game
from app import defaults, scene_list, utils
from app.entities import ChoiceSet, KeyedButton, ListBox
from app.mission import Mission
from app.dialog import DialogSide

import pygame

def _toggle_clues(sender):
    scene_list.all["ig_clues"].toggle_visibility()

class InterrogationBase(Mission):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, side)
        self.tree_name = tree_name
        self._tree_cache = None
        
        # Switches
        self.SW_TALK1 = "e{}m{}_talk1".format(episode_id, mission_id)
        self.SW_QUESTIONS = "e{}m{}_fda_questions".format(episode_id, mission_id)
        self.SW_QUESTION_CURRENT = "e{}m{}_fda_question_id".format(episode_id, mission_id)
        self.SW_FDA_CHOICE = "e{}m{}_fda_choice".format(episode_id, mission_id)
        self.SW_PRESENTED_CLUE = "e{}m{}_presented_clue".format(episode_id, mission_id)
        self.SW_RETURN_TO_CHOICES = "e{}m{}_fda_return_to_choices".format(episode_id, mission_id)

    def _get_callbacks(self):
        # Base callbacks available to all interrogation scenes
        return {
            "to_interrogator": self._to_interrogator,
            "to_respondent": self._to_respondent,
            "to_questions": self._to_questions,
            "show_fda": self._show_fda,
            "backoff_to_choices": self._backoff_to_choices,
            "finish_question": self._finish_question,
            "mark_correct": self._mark_correct,
            "accuse": self._accuse,
        }

    def _load_tree(self):
        if self._tree_cache is None:
            self._tree_cache = utils.load_json_asset(self.tree_name)
        return self._tree_cache

    def _emit_node(self, node, callbacks):
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
            repeat=node.get("repeat", True)
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
        
        for node in q_data["initial"]:
            self._emit_node(node, callbacks)
            
        choice_key = {1: "fact", 2: "doubt", 3: "accuse"}.get(choice) if isinstance(choice, int) else None
        if choice_key and choice_key in q_data["choices"]:
            choice_data = q_data["choices"][choice_key]
            
            # Handle clue-specific responses for accusations
            if choice_key == "accuse":
                presented = self.find_switch(self.SW_PRESENTED_CLUE)
                if "clue_responses" in choice_data:
                    if presented is None:
                        # We haven't picked a clue yet, but we are in Dan's scene.
                        # This shouldn't happen unless we're waiting for Joe.
                        return
                        
                    responses = choice_data["clue_responses"]
                    nodes = responses.get(presented) if presented in responses else responses.get("else", [])
                    for node in nodes:
                        self._emit_node(node, callbacks)
                else:
                    # Simple accusation with no clue selection logic on this side
                    for node in choice_data.get("nodes", []):
                        self._emit_node(node, callbacks)
            else:
                for node in choice_data.get("nodes", []):
                    self._emit_node(node, callbacks)

    def _to_interrogator(self):
        # To be implemented by subclasses if needed
        pass

    def _to_respondent(self):
        # To be implemented by subclasses if needed
        pass

    def _to_questions(self):
        # To be implemented by subclasses if needed
        pass

    def _show_fda(self):
        # To be implemented by subclasses if needed
        pass

    def _backoff_to_choices(self):
        # To be implemented by subclasses if needed
        pass

    def _accuse(self):
        # To be implemented by subclasses if needed
        pass

    def _disable_current_question(self):
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        questions = self.find_switch(self.SW_QUESTIONS)
        if not questions:
            return False
        for item in questions:
            if item["value"] == q:
                item["disabled"] = True
                self.set_switch(self.SW_QUESTIONS, questions)
                return True
        return False

    def _finish_question(self):
        self._disable_current_question()
        self._to_questions()

    def _mark_correct(self):
        if not self._disable_current_question():
            self._to_questions()
            return
        self._to_questions()


class InterrogationInterrogator(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, respondent_scene, questions_scene, next_scene, side=DialogSide.BOTTOM):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.respondent_scene = respondent_scene
        self.questions_scene = questions_scene
        self.next_scene = next_scene
        self.interrogator_branch = None # Set by subclass

    def load_content(self):
        super().load_content()
        self._run_dialog_tree(self.interrogator_branch, self._get_callbacks())

    def _to_respondent(self):
        game.scenes.set_scene(self.respondent_scene)

    def _to_questions(self):
        questions = self.find_switch(self.SW_QUESTIONS)
        has_remaining = False
        if questions:
            for item in questions:
                if not item.get("disabled", False):
                    has_remaining = True
                    break

        if not questions or has_remaining:
            game.scenes.set_scene(self.questions_scene)
        else:
            game.scenes.set_scene(self.next_scene)

    def _get_backdown_text_id(self):
        return "accuse_backdown"

    def _accuse(self):
        items = self.emitter.add_clues_selector()
        def _on_clue_selected(sender, data):
            self.set_switch(self.SW_PRESENTED_CLUE, data["value"])
            self._to_respondent()
            
        def _on_clue_cancelled(sender):
            self.set_switch(self.SW_PRESENTED_CLUE, None)
            self.set_switch(self.SW_FDA_CHOICE, None)
            self.set_switch(self.SW_RETURN_TO_CHOICES, True)

            def _after_selector_hidden(hidden_sender):
                self.emitter.add(
                    self.interrogator_branch,
                    self._get_backdown_text_id(),
                    callback=self._to_respondent
                )

            items.hidden += _after_selector_hidden
            
        items.selected += _on_clue_selected
        items.cancelled += _on_clue_cancelled

class InterrogationRespondent(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, interrogator_scene, questions_scene, next_scene, side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.interrogator_scene = interrogator_scene
        self.questions_scene = questions_scene
        self.next_scene = next_scene
        self.respondent_branch = None # Set by subclass

    def load_content(self):
        super().load_content()
        if self.find_switch(self.SW_RETURN_TO_CHOICES):
            self.clear_switch(self.SW_RETURN_TO_CHOICES)
            retry_timer = self.timers.add(0, True)
            retry_timer.elapsed += lambda sender: self._show_fda()
            return
        self._run_dialog_tree(self.respondent_branch, self._get_callbacks())

    def _to_interrogator(self):
        game.scenes.set_scene(self.interrogator_scene)

    def _to_questions(self):
        questions = self.find_switch(self.SW_QUESTIONS)
        has_remaining = False
        if questions:
            for item in questions:
                if not item.get("disabled", False):
                    has_remaining = True
                    break
        
        if not questions or has_remaining:
            game.scenes.set_scene(self.questions_scene)
        else:
            game.scenes.set_scene(self.next_scene)

    def _show_fda(self):
        if self.find_switch(self.SW_FDA_CHOICE) is not None:
            # We already made a choice, don't show the menu again.
            return

        choiceset = ChoiceSet.from_entity(self, defaults.FDA_CHOICESET)
        choiceset.selected += self._handle_choice
        self.entities["fda"] = choiceset
        btn_clues = KeyedButton(self, (64, 64), "Review clues", pygame.K_F12, "TAB")
        btn_clues.leftclick += _toggle_clues
        self.entities["btn_clues"] = btn_clues

    def _backoff_to_choices(self):
        self.set_switch(self.SW_FDA_CHOICE, None)
        self.set_switch(self.SW_PRESENTED_CLUE, None)
        self._show_fda()

    def _handle_choice(self, sender, value):
        i = value[0]
        self.set_switch(self.SW_FDA_CHOICE, i)
        self.set_switch(self.SW_PRESENTED_CLUE, None) # Clear any previous cancelled state
        choice_key = {1: "fact", 2: "doubt", 3: "accuse"}.get(i)

        if choice_key == "accuse":
            self.entities["fda"].hidden += lambda sender: self._to_interrogator()
            return
        
        # Trigger the response dialogue nodes.
        # This will emit the nodes for the chosen branch (Fact/Doubt/Accuse).
        self._run_question_tree(self.respondent_branch, self._get_callbacks())
        
        tree = self._load_tree()
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        q_data = tree[self.respondent_branch]["questions"][q]
        
        # If there are no nodes to play, we need to transition immediately via the hide callback.
        # But if there ARE nodes, they should handle the transition via their own callbacks.
        choice_data = q_data["choices"].get(choice_key, {})
        if not choice_data.get("nodes") and not choice_data.get("clue_responses"):
            is_correct = choice_data.get("correct", False)
            def _to_scene(sender):
                if is_correct:
                    self._mark_correct()
                else:
                    self._to_interrogator()
            self.entities["fda"].hidden += _to_scene


class InterrogationMenu(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, interrogator_scene, title="QUESTIONS", pos=(312, 192), side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.interrogator_scene = interrogator_scene
        self.menu_title = title
        self.menu_pos = pos

    def load_content(self):
        super().load_content()
        self._load_questions()
        listbox = ListBox(self, self.menu_pos, self.menu_title, self.questions)
        listbox.selected += self._listbox_on_selected
        self.set_switch(self.SW_TALK1, True)
        self.entities["listbox"] = listbox

    def _load_questions(self):
        self.questions = self.find_switch(self.SW_QUESTIONS)
        if not self.questions:
            clues = self.get_clues()
            self.questions = [
                q for q in self._load_tree()["questions"]
                if q.get("requires_clue") is None or q["requires_clue"] in clues
            ]
            self.set_switch(self.SW_QUESTIONS, self.questions)

    def _listbox_on_selected(self, sender, data):
        self.set_switch(self.SW_QUESTION_CURRENT, data["value"])
        self.set_switch(self.SW_FDA_CHOICE, None)
        self.set_switch(self.SW_PRESENTED_CLUE, None)
        game.scenes.set_scene(self.interrogator_scene)
