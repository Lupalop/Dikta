# This module provides a Python equivalent for C#'s event handlers.
class EventHandler:
    def __init__(self):
        self.handlers = set()
        self._pending_adds = set()
        self._pending_removes = set()

    def __iadd__(self, handler):
        self._pending_adds.add(handler)
        return self

    def __isub__(self, handler):
        self._pending_removes.add(handler)
        return self

    def __call__(self, *args, **kargs):
        for handler_to_add in self._pending_adds:
            self.handlers.add(handler_to_add)
        self._pending_adds.clear()
        for handler_to_remove in self._pending_removes:
            self.handlers.remove(handler_to_remove)
        self._pending_removes.clear()
        for handler in self.handlers:
            handler(*args, **kargs)

    def __len__(self):
        return len(self.handlers)

    def clear(self):
        self.handlers.clear()
