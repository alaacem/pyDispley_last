import time
import subprocess
import threading
from lib.TableScraper import TableScraper
from lib.ConfigManager import ConfigManager
import os




def scrap():
    config_manager = ConfigManager("config.json")
    config_data = config_manager.load()
    scrapper_config = config_data['scrapper_config']
    refresh_time = config_data.get('refresh_time', 60)

    while config_data.get('enable_scraping', False):
        scraper = TableScraper(scrapper_config)
        test_week = scraper.fetch_data_by_frame_id()

        if test_week:
            config_data['times'] = test_week
            config_manager.save(config_data)

        time.sleep(refresh_time)

def manage_display(config_data):
    display_start_time = config_data["shutdown"].get("start", "00:00")
    display_end_time = config_data["shutdown"].get("end", "23:59")
    while config_data["shutdown"].get("display_spar", False):
        current_time = time.strftime("%H:%M")

        if display_start_time <= current_time <= display_end_time:
            os.system("vcgencmd display_power 0")
        else:
            os.system("vcgencmd display_power 1")

        time.sleep(60)

def main():

    subprocess.Popen(["python", "anzeige_flask.py"])

    config_manager = ConfigManager("config.json")
    config_data = config_manager.load()

    # Starting Threads
    scraping_thread = threading.Thread(target=scrap)
    display_thread = threading.Thread(target=manage_display, args=(config_data,))


    # Starting browser
    browser = subprocess.Popen(["chromium-browser", "--kiosk", "--app=http://127.0.0.1:4000/", "--disable-overlay-scrollbar"])

    scraping_thread.start()
    display_thread.start()

    # Wait for threads to complete execution
    scraping_thread.join()
    display_thread.join()

    # Close browser when exiting
    browser.terminate()

if __name__ == "__main__":
    main()
