# This module provides a Python equivalent for C#'s event handlers.
class EventHandler:
    def __init__(self):
        self.handlers = set()

    def __iadd__(self, handler):
        self.handlers.add(handler)
        return self

    def __isub__(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError
        return self

    def __call__(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def __len__(self):
        return len(self.handlers)
