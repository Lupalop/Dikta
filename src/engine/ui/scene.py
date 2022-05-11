class Scene:
    def __init__(self, name):
        self.name = name
        self.enabled = True
        self.entities = {}
        print("Initialized: Scene - {}".format(name))

    def update(self):
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.update()

    def draw(self, window):
        for entityName in self.entities:
            entity = self.entities[entityName]
            entity.draw(window)

    def load_content(self):
        pass

    def dispose(self):
        self.entities = None
