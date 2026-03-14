from engine import game
from app import defaults, scene_list, utils
from app.entities import ChoiceSet, KeyedButton, Image, ListBox
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
        if branch not in tree: return

        # Check for first talk
        talk1 = self.find_switch(self.SW_TALK1)
        if not talk1 and "intro" in tree[branch]:
            for node in tree[branch]["intro"]:
                self._emit_node(node, callbacks)
            return

        # Check for question branch
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        if q is None: return
        
        choice = self.find_switch(self.SW_FDA_CHOICE)
        q_data = tree[branch]["questions"][q]
        
        for node in q_data["initial"]:
            self._emit_node(node, callbacks)
            
        choice_key = {1: "fact", 2: "doubt", 3: "accuse"}.get(choice)
        if choice_key and choice_key in q_data["choices"]:
            choice_data = q_data["choices"][choice_key]
            for node in choice_data["nodes"]:
                self._emit_node(node, callbacks)

class InterrogationInterrogator(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, respondent_scene, side=DialogSide.BOTTOM):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.respondent_scene = respondent_scene
        self.interrogator_branch = None # Set by subclass

    def load_content(self):
        super().load_content()
        callbacks = {
            "to_respondent": self._to_respondent,
            "to_dan": self._to_respondent, # Backward compatibility
            "accuse": self._accuse,
        }
        self._run_dialog_tree(self.interrogator_branch, callbacks)

    def _to_respondent(self):
        game.scenes.set_scene(self.respondent_scene)

    def _accuse(self):
        self.emitter.add_clues_selector()

class InterrogationRespondent(InterrogationBase):
    def __init__(self, episode_id, mission_id, child_id, desc, tree_name, interrogator_scene, questions_scene, next_scene, side=DialogSide.TOP):
        super().__init__(episode_id, mission_id, child_id, desc, tree_name, side)
        self.interrogator_scene = interrogator_scene
        self.questions_scene = questions_scene
        self.next_scene = next_scene
        self.respondent_branch = None # Set by subclass

    def load_content(self):
        super().load_content()
        callbacks = {
            "to_interrogator": self._to_interrogator,
            "to_joe": self._to_interrogator, # Backward compatibility
            "to_questions": self._to_questions,
            "show_fda": self._show_fda,
        }
        self._run_dialog_tree(self.respondent_branch, callbacks)

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
        choiceset = ChoiceSet.from_entity(self, defaults.FDA_CHOICESET)
        choiceset.selected += self._handle_choice
        self.entities["fda"] = choiceset
        btn_clues = KeyedButton(self, (64, 64), "Review clues", pygame.K_F12, "TAB")
        btn_clues.leftclick += _toggle_clues
        self.entities["btn_clues"] = btn_clues

    def _handle_choice(self, sender, value):
        i = value[0]
        self.set_switch(self.SW_FDA_CHOICE, i)
        
        tree = self._load_tree()
        q = self.find_switch(self.SW_QUESTION_CURRENT)
        q_data = tree[self.respondent_branch]["questions"][q]
        choice_key = {1: "fact", 2: "doubt", 3: "accuse"}.get(i)
        
        is_correct = False
        if choice_key and choice_key in q_data["choices"]:
            is_correct = q_data["choices"][choice_key].get("correct", False)

        def _to_scene(sender):
            if is_correct:
                questions = self.find_switch(self.SW_QUESTIONS)
                for item in questions:
                    if item["value"] == q:
                        item["disabled"] = True
                        break
                self.set_switch(self.SW_QUESTIONS, questions)
                self._to_questions()
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
        game.scenes.set_scene(self.interrogator_scene)
