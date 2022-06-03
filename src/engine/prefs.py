from engine import content

PREF_FILENAME = "prefs"

class PreferencesManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all = {}

    def load(self):
        try:
            self.all = content.load_json(self.file_name)
        except:
            print("Failed to load preferences file")
            self.all = {}

    def save(self):
        content.save_json(self.file_name, self.all)
        print("Saving preferences file")

    def get(self, name, default_value = None):
        value = default_value

        try:
            value = self.all[name]
        except:
            print(self.all)
            if not default_value:
                raise("unexpected preference name")
            self.all[name] = default_value
            return default_value

        return value

    def set(self, name, value):
        self.all[name] = value

default = PreferencesManager(PREF_FILENAME)