from engine import ClickableEntity, Entity
from engine.enums import MouseButton, ClickState
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
    def __init__(self, owner, position, title, dataset, hide_on_select = False):
        surface = pygame.Surface(LISTBOX_MAIN_RECT.size, pygame.SRCALPHA, 32)
        super().__init__(owner, position, LISTBOX_MAIN_RECT.size, surface, False)
        self.hide_on_select = hide_on_select
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
        self.hidden = EventHandler()
        self.listitems = []
        # Set-up base UI elements.
        base_bg = Image(self, utils.load_ui_image("note-bg"))
        base_title = Label(
            self, "ITEMS", utils.get_comic_font(32), pygame.Color("black"),
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
                i[1]
            )
            # Update y-coordinate of the next list item.
            currenty += listitem.get_rect().height
            # Set the list item's actions.
            listitem.leftclick += lambda sender, i_bound=i: \
                self._on_selected(sender, i_bound)
            # Keep track and store the created list item.
            self.listitems.append(listitem)
        # Set the active list item now.
        self.index = 0
        self._mark_listitems(self.index)

    @classmethod
    def from_entity(cls, owner, entity):
        entity_copy = cls(
            owner,
            entity.get_position(),
            entity.title,
            entity.dataset,
            entity.hide_on_select
        )
        return entity_copy

    def _mark_listitems(self, index):
        self.index = index

        target = self.listitems[index]
        for item in self.listitems:
            item.set_is_selected(item is target)

    # Event handlers
    def _on_hidden(self):
        self.is_hiding = False
        self.is_hidden = True
        self.hidden(self)

    def _on_selected(self, sender, value):
        # Send only the attached item data to subscribers.
        self.selected(self, value[1])
        # Mark the selected list item.
        self._mark_listitems(value[0])

        # Update state and fade out everything if necessary.
        if self.hide_on_select:
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
                self._on_hidden
            )

    def _handle_keys(self, key):
        is_enter = (key == pygame.K_KP_ENTER or \
                    key == pygame.K_RETURN or \
                    key == pygame.K_SPACE)
        is_up = (key == pygame.K_UP)
        is_down = (key == pygame.K_DOWN)

        if is_enter:
            self.listitems[self.index]._on_click(MouseButton.LEFT)
        elif is_up and self.index > 0:
            self._mark_listitems(self.index - 1)
        elif is_down and self.index < (len(self.listitems) - 1):
            self._mark_listitems(self.index + 1)

    def update(self, game, events):
        # Stop updating the listbox if we're hiding.
        if self.is_hiding or self.is_hidden:
            return

        super().update(game, events)
        for item in self.listitems:
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
            item.draw(layer)
