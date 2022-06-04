from engine import content

PF_DEFAULT = "prefs"
PF_SAVEDGAME = "savedgame"

class PreferencesManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all = {}

    def load(self):
        try:
            self.all = content.load_json(self.file_name)
            print("Loading preferences file: {}".format(self.file_name))
        except:
            print("Failed to load preferences file: {}".format(self.file_name))
            self.all = {}

    def save(self):
        content.save_json(self.file_name, self.all)
        print("Saving preferences file: {}".format(self.file_name))

    def get(self, name, default_value = None):
        value = default_value

        try:
            value = self.all[name]
        except:
            if default_value is None:
                raise("unexpected preference name")
            self.all[name] = default_value
            return default_value

        return value

    def set(self, name, value):
        self.all[name] = value

default = PreferencesManager(PF_DEFAULT)
savedgame = PreferencesManager(PF_SAVEDGAME)
