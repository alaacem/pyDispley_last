from lib.ConfigManager import ConfigManager
from lib.FileManager import FileManager
from lib.FixedSizeRotatingFileHandler import FixedSizeRotatingFileHandler
from lib.TableScraper import TableScraper

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import time
import re
import logging
from werkzeug.exceptions import BadRequestKeyError
from threading import Lock



app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# 250 MB
MAX_LOG_SIZE_FLASK = 250 * 1024 * 1024
MAX_LOG_SIZE = 250 * 1024 * 1024


app_logger = logging.getLogger("app_log")
app_logger.setLevel(logging.DEBUG)
fh = FixedSizeRotatingFileHandler("app_log.log", maxBytes=MAX_LOG_SIZE)  # 5KB
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
app_logger.addHandler(fh)


# werkzeug_logger = logging.getLogger("werkzeug")
# werkzeug_logger.setLevel(logging.DEBUG)
# werkzeug_logger_fh = FixedSizeRotatingFileHandler("flask_log.log", maxBytes=MAX_LOG_SIZE_FLASK)  # 5KB
# werkzeug_logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# werkzeug_logger_fh.setFormatter(werkzeug_logger_formatter )
# werkzeug_logger.addHandler(werkzeug_logger_fh)
# werkzeug_logger.propagate = False



def update_current_status(new_status):
    config = config_manager.load()
    if new_status in config['status']:
        config['current_status'] = new_status
        for property_name, property_value in config['status'][new_status].items():
            config['css_vars'][property_name] = property_value
        #    print(property_name,config['css_vars'][property_name],property_value,"\n",config)
        config_manager.save(config)
        update_css_file_from_config()
        #print(f"New Config: {config}")
        return True
    else:
        return False


def update_css_file_from_config():
    config = config_manager.load()
    css_vars = config['css_vars']


    # Read the file using FileManager
    css_content = file_manager.read_file()

    for var, value in css_vars.items():
        pattern = f'--{var}:\s*[^;]*;'
        if re.search(pattern, css_content):
            css_content = re.sub(pattern, f'--{var}: {value};', css_content)
        else:
            css_content = css_content.replace(':root {', f':root {{\n  --{var}: {value};')

    # Write the updated content using FileManager
    if css_content:
        file_manager.write_file(css_content)


def load_css_vars():
    css_content = file_manager.read_file()


    # Extract the content of the :root selector
    root_content_match = re.search(r':root\s*{\s*([^}]+)\s*}', css_content)
    if not root_content_match:
        return {}

    root_content = root_content_match.group(1)

    # Extract all --variable: value; pairs from the :root content
    variables = re.findall(r'--(.*?):\s?(.*?);', root_content)

    return {var_name: value for var_name, value in variables}

def update_times_in_config():
    """Update the opening times in the config."""
    config = config_manager.load()
    times = config['times']

    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]

    config_manager.save_if_changed(config)

def load_css_vars_from_config():
    return config_manager.load()['css_vars']
def load_status_word_from_config():
    return config_manager.load()['current_status']
def load_times_from_config():
    return config_manager.load()['times']


def update_config_from_post_request():
    config = config_manager.load()

    # Update CSS variables
    css_vars_from_file = load_css_vars()
    new_css_vars = {key: request.form.get(key, default='') for key in css_vars_from_file.keys()}
    config['css_vars'] = {**config.get('css_vars', {}), **new_css_vars}

    # Update times
    times = config['times']['schedule']
    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]
        config['times']['schedule'] = times

    # Update statuses
    for status_key in config['status'].keys():
        for property_name in config['status'][status_key].keys():
            input_name = f"{status_key}_{property_name}"
            config['status'][status_key][property_name] = request.form.get(input_name, default='')
    #update Scrapper Config
    config['scrapper_config']['url']=request.form.get('url')
    config['enable_scraping']=request.form.get('enable_scraping') == 'on'
    config['scrapper_config']['frame_id']= request.form.get('frame_id')
    config['scrapper_config']['refresh_time'] = request.form.get('refresh_time')
    config['scrapper_config']['valid_date']= request.form.get('valid_date')
    #update_bottom_text
    config['bottom_text']= request.form.get('bottom_text',"Außerhalb die Öffnungszeiten : <a href="">help@hs-kl.de</a>")


    config_manager.save(config)


def update_config_from_status_change(new_status):
    config = config_manager.load()

    if new_status in config['status']:
        config['current_status'] = new_status
        for property_name, property_value in config['status'][new_status].items():
            config['css_vars'][property_name] = property_value
        config_manager.save(config)
        update_css_file_from_config()
        return True
    else:
        return False

@app.errorhandler(BadRequestKeyError)
def handle_bad_request(e):
    return f'bad request!:{e}', 400
@app.route('/update-css-vars', methods=['POST'])
def update_css_vars():
    received_data = request.json
    #print(received_data)
    received_css_vars = received_data.get('cssVars', {})
    received_status_word = received_data.get('currentStatusWord', "")
    received_times = received_data.get('times', {})
    received_bottom_text = received_data.get('bottom_text', "")

    config_data = config_manager.load()
    config_css_vars = config_data['css_vars']
    config_status_word = config_data['current_status']
    config_times = config_data['times']['schedule']
    bottom_text=config_data['bottom_text']
    # Determine if any CSS variables changed
    css_vars_changed = any(received_css_vars[key] != config_css_vars.get(key) for key in received_css_vars)

    # Check if the status word has changed
    status_word_changed = received_status_word != config_status_word

    # Check if times have changed
    times_changed = received_times != config_times
    #Check if bottom_text changed
    bottom_text_changed = bottom_text != received_bottom_text
    # Determine if any changes occurred
    if css_vars_changed or status_word_changed or times_changed or bottom_text_changed:
        global prev_css_vars, prev_status_word, prev_times
        prev_css_vars = received_css_vars
        prev_status_word = received_status_word
        prev_times = received_times
        update_css_file_from_config()
      #  print(css_vars_changed,status_word_changed,times_changed,bottom_text_changed)
      #  print(received_bottom_text,"sda",bottom_text)
        return {"refresh": True}

    return {"refresh": False}

@app.route('/', methods=['GET'])
def configure_times_get():
    config = config_manager.load()
    times = config['times']
    bottom_text=config['bottom_text']
    current_status_word=config['current_status']
    von=config['times']['start_date']
    bis=config['times']['end_date']

    return render_template(r'index1_new.html', times=times['schedule'], current_status_word=current_status_word,von=von,bis=bis,bottom_text=bottom_text)

@app.route('/', methods=['POST'])
def configure_times_post():

    config = config_manager.load()
    times = config['times']['schedule']
    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]

    config['times']['schedule']= times
    config_manager.save_if_changed(config)
    return redirect(url_for('configure_times_get'))


@app.route('/settings', methods=['GET'])
def settings_get():
    config = config_manager.load()
    times = config['times']['schedule']
    enable_scraping=config['enable_scraping']
    css_vars = load_css_vars()
    scrapper_config=config['scrapper_config']
    bottom_text=config["bottom_text"]
    return render_template('settings.html', css_vars=css_vars, times=times, statuses=config['status'],enable_scraping=enable_scraping,scrapper_config=scrapper_config,bottom_text=bottom_text)

@app.route('/settings', methods=['POST'])
def settings_post():

    update_config_from_post_request()
    update_css_file_from_config()  # Update the CSS file based on the new config
    return redirect(url_for('settings_get'))

@app.route('/update-status', methods=['POST'])
def update_status():
    received_data = request.json
    new_status = received_data['current_status']
    if update_config_from_status_change(new_status):
        return {"message": "Status updated successfully"}
    else:
        return {"message": "Invalid status"}, 400



@app.route('/css/<filename>')
def serve_css(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    json_file_path = "config.json"

    config_manager = ConfigManager(json_file_path)
    file_manager = FileManager("static/Home.css")
    app.run(host='0.0.0.0', port=4000,debug=True, threaded=True,use_reloader=False)


