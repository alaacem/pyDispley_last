import keyboard
import time
from lib.ConfigManager import ConfigManager

def update_status(config_manager, status):
    # load the current configuration
    config_data = config_manager.load()
    config_data["current_status"] = status
    config_manager.save(config_data)
    print(f"Status updated to {status}")

def update_config_from_status_change(config_manager,new_status):
    config = config_manager.load()

    if new_status in config['status']:
        config['current_status'] = new_status
        for property_name, property_value in config['status'][new_status].items():
            config['css_vars'][property_name] = property_value
        config_manager.save(config)
    print(f"Status updated to {new_status}")
def key_listener(config_manager):
    while True:
        if keyboard.is_pressed('1'):
            update_config_from_status_change(config_manager, "Geöffnet")
            while keyboard.is_pressed('1'):  # wait until key '1' is released
                pass

        if keyboard.is_pressed('2'):
            update_config_from_status_change(config_manager, "Geschlossen")
            while keyboard.is_pressed('2'):  # wait until key '2' is released
                pass

        if keyboard.is_pressed('3'):
            update_config_from_status_change(config_manager, "Gleich zurück")
            while keyboard.is_pressed('3'):  # wait until key '3' is released
                pass

        time.sleep(0.1)  # prevent the loop from running too fast

if __name__=="__main__":
    config_manager = ConfigManager("config.json")
    key_listener(config_manager)