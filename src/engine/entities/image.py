from engine.entities import Entity

class Image(Entity):
    def __init__(self, surface, position_or_rect, size = None):
        super().__init__(position_or_rect, size, surface)
