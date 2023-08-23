import json

class ConfigManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def update_value(self, key, value):
        data = self.load()
        if key not in data:
            return None
        data[key] = value
        self.save(data)
    def has_changes(self, other_config):
        current_config = self.load()
        return current_config != other_config
    def save_if_changed(config_manager, new_config):
        """Save the config only if there are changes."""
        current_config = config_manager.load()
        if current_config != new_config:
            config_manager.save(new_config)
