from engine.timer import TimerManager
from engine.animator import Animator

class Scene:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.entities = {}
        self.timers = TimerManager()
        self.animator = Animator(self.timers)
        print("Initialized: Scene - {}".format(name))

    def update(self, game, events):
        self.timers.update(game, events)
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.update(game, events)

    def draw(self, layer):
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.draw(layer)

    def load_content(self):
        pass

    def dispose(self):
        self.timers.clear()
