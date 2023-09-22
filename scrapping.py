import time
from lib.TableScraper import TableScraper
from lib.ConfigManager import ConfigManager

if __name__=='__main__':
    config_manager = ConfigManager("config.json")
    config_data = config_manager.load()
    scrapper_config = config_data['scrapper_config']

    enable_scraping = config_data.get('enable_scraping')
    scraper = TableScraper(scrapper_config)

    while True:
        config_data = config_manager.load()
        enable_scraping = config_data.get('enable_scraping')

        if enable_scraping:

            test_week = scraper.fetch_data_by_frame_id()
            if test_week:
                config_data['times'] = test_week
                config_manager.save(config_data)
            print("refresh_time")
            refresh_time = int(scrapper_config.get('refresh_time',0)) if scrapper_config.get('refresh_time') else 1000  # Convert to integer
            time.sleep(refresh_time)  # Pause the execution for "refresh_time" seconds
        else:
            break
