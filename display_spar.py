import time
import os
from lib.ConfigManager import ConfigManager

def manage_display(config_manager):
    while True:  # Run indefinitely
        config_data = config_manager.load()  # Load the configuration regularly

        display_start_time = config_data["shutdown"].get("start", "00:00")
        display_end_time = config_data["shutdown"].get("end", "23:59")

        # If display_spar is True, apply the logic
        if config_data["shutdown"].get("display_spar", False):
            current_time = time.strftime("%H:%M")

            if display_start_time <= current_time <= display_end_time:
                os.system("vcgencmd display_power 0")
            else:
                os.system("vcgencmd display_power 1")

        # Sleep for 60 seconds before the next loop iteration
        time.sleep(60)

if __name__ == "__main__":
    config_manager = ConfigManager("config.json")
    manage_display(config_manager)