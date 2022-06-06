from engine import Entity

class Image(Entity):
    def __init__(self, owner, surface, position_or_rect = (0, 0), size = None):
        super().__init__(owner, position_or_rect, size, surface)
