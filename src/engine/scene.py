class Scene:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.entities = {}
        print("Initialized: Scene - {}".format(name))

    def update(self, events):
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.update()

    def draw(self, layer):
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.draw(layer)

    def load_content(self):
        pass

    def dispose(self):
        self.entities = None
