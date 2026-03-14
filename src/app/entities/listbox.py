from engine import Entity
from engine.enums import MouseButton
from engine.event_handler import EventHandler
from app import utils
from app.entities import Image, Label, ListItem

import pygame

LISTBOX_MAIN_RECT = pygame.Rect(0, 0, 400, 500)
LISTBOX_TITLE_RECT = pygame.Rect(0, 0, LISTBOX_MAIN_RECT.width, 84)

class ListBox(Entity):
    """
    The data parameter accepts a list with the following format:
    data = [
        {
            "text": "Pen",
            "value": "pen"
        },
        {
            "text": "Press Card",
            "value": "press-card"
        },
    ]
    After a list item is selected, the sender and the attached item's data is
    passed to subscribers of the `selected` event.
    """
    def __init__(self, owner, position, title, dataset, hide_on_select = False, show_disabled = False, strike_disabled = False):
        surface = pygame.Surface(LISTBOX_MAIN_RECT.size, pygame.SRCALPHA, 32)
        super().__init__(owner, position, LISTBOX_MAIN_RECT.size, surface, False)
        self.hide_on_select = hide_on_select
        self.show_disabled = show_disabled
        self.strike_disabled = strike_disabled
        self.is_hiding = False
        self.is_hidden = False
        self.dataset = dataset
        if not dataset:
            self.dataset = [{
                "text": "Empty",
                "value": None
            }]
        self.title = title
        self.selected = EventHandler()
        self.marked = EventHandler()
        self.hidden = EventHandler()
        self.cancelled = EventHandler()
        self.listitems = []
        self.index = 0
        # Set-up base UI elements.
        base_bg = Image(self.owner, utils.load_ui_image("note-bg"))
        base_title = Label(
            self, title, utils.get_comic_font(32), pygame.Color("black"),
        )
        base_title.set_position((
            (LISTBOX_TITLE_RECT.width / 2) - (base_title.get_rect().width / 2),
            (LISTBOX_TITLE_RECT.height / 2) - (base_title.get_rect().height / 2)
        ))
        base_bg.draw(surface)
        base_title.draw(surface)
        # Enumerate through the given data set and create list items.
        currenty = LISTBOX_TITLE_RECT.height
        for i in enumerate(self.dataset):
            listitem = ListItem(
                owner,
                (position[0], position[1] + currenty),
                i[1],
                strike_disabled=self.strike_disabled
            )
            # Update y-coordinate of the next list item.
            currenty += listitem.get_rect().height
            # Set the list item's actions.
            listitem.leftclick += lambda sender, i_bound=i: \
                self._on_selected(sender, i_bound)
            # Keep track and store the created list item.
            self.listitems.append(listitem)
        # Set the active list item now.
        initial_index = self._get_next_enabled_index(0)
        if initial_index is None:
            initial_index = 0
        self._mark_listitems(initial_index)

    @classmethod
    def from_entity(cls, owner, entity):
        entity_copy = cls(
            owner,
            entity.get_position(),
            entity.title,
            entity.dataset,
            entity.hide_on_select,
            entity.show_disabled,
            entity.strike_disabled
        )
        return entity_copy

    def _is_item_disabled(self, index):
        return self.listitems[index].data.get("disabled", False)

    def _get_next_enabled_index(self, start, step=1):
        index = start
        while index >= 0 and index < len(self.listitems):
            if not self._is_item_disabled(index):
                return index
            index += step
        return None

    def _mark_listitems(self, index):
        self.index = index

        target = self.listitems[index]
        for item in self.listitems:
            is_target = (item is target)
            item.set_is_selected(is_target)
            if is_target:
                self._on_marked(item.data)

    # Event handlers
    def _on_marked(self, value):
        self.marked(self, value)

    def _on_hidden(self):
        self.is_hiding = False
        self.is_hidden = True
        self.hidden(self)

    def _on_cancelled(self):
        self.cancelled(self)
        self._close_anim()

    def _close_anim(self, on_complete=None):
        self.is_hiding = True
        utils.reset_cursor()

        for item in self.listitems:
            item._close_anim()
            self.owner.animator.to_alpha(
                item,
                250,
                0
            )
        self.owner.animator.to_alpha(
            self,
            250,
            0,
            on_complete or self._on_hidden
        )

    def _on_selected(self, sender, value):
        if value[1].get("disabled", False):
            return
        # Send only the attached item data to subscribers.
        self.selected(self, value[1])
        # Mark the selected list item.
        self._mark_listitems(value[0])

        # Update state and fade out everything if necessary.
        if self.hide_on_select:
            self._close_anim()

    def _handle_keys(self, key):
        is_enter = (key == pygame.K_KP_ENTER or \
                    key == pygame.K_RETURN or \
                    key == pygame.K_SPACE)
        is_up = (key == pygame.K_UP)
        is_down = (key == pygame.K_DOWN)

        if is_enter:
            if not self._is_item_disabled(self.index):
                self.listitems[self.index]._on_click(MouseButton.LEFT)
        elif is_up and self.index > 0:
            target = self._get_next_enabled_index(self.index - 1, -1)
            if target is not None:
                self._mark_listitems(target)
        elif is_down and self.index < (len(self.listitems) - 1):
            target = self._get_next_enabled_index(self.index + 1, 1)
            if target is not None:
                self._mark_listitems(target)

    def update(self, game, events):
        # Stop updating the listbox if we're hiding.
        if self.is_hiding or self.is_hidden:
            return

        super().update(game, events)
        for item in self.listitems:
            if item.data.get("disabled", False):
                continue
            item.update(game, events)
        # We always steal keyboard events.
        for event in events:
            if event.type == pygame.KEYUP:
                self._handle_keys(event.key)
                break

    def draw(self, layer):
        # There's no use of drawing a hidden entity.
        if self.is_hidden:
            return
        super().draw(layer)
        for item in self.listitems:
            if item.data.get("disabled", False) and not self.show_disabled:
                continue
            item.draw(layer)
