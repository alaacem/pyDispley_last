from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import re
import logging
from werkzeug.exceptions import BadRequestKeyError
from lib.Config_Manger import ConfigManager


class FixedSizeRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a+', maxBytes=0, encoding=None, delay=0):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:  # Are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, os.SEEK_END)  # Go to the end of the file
            if self.stream.tell() + len(msg) > self.maxBytes:
                # Figure out how much we need to trim from the start
                trim_length = len(msg)
                self.stream.seek(0)  # Go to the start
                self.stream.read(trim_length)  # "read out" the part we want to trim
                remaining_log = self.stream.read()  # save the remaining log content
                self.stream.seek(0)
                self.stream.truncate()  # empty the file
                self.stream.write(remaining_log)
            self.stream.write(msg)
            self.stream.flush()
        else:
            logging.FileHandler.emit(self, record)

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# 250 MB
MAX_LOG_SIZE_FLASK = 250 * 1024 * 1024
MAX_LOG_SIZE = 250 * 1024 * 1024 #250mb


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

json_file_path = "config.json"
config_manager = ConfigManager(json_file_path)


def update_css_file_from_config():
    config = config_manager.load()
    css_vars=config['css_vars']
    with open("static/Home.css", "r") as file:
        css_content = file.read()

    for var, value in css_vars.items():
        pattern = f'--{var}:\s*[^;]*;'
        if re.search(pattern, css_content):
            css_content = re.sub(pattern, f'--{var}: {value};', css_content)

        else:
            css_content = css_content.replace(':root {', f':root {{\n  --{var}: {value};')
            print(var)

    with open("static/Home.css", "w") as file:
        file.write(css_content)

def load_css_vars():
    with open("static/Home.css", "r") as file:
        css_content = file.read()

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

@app.errorhandler(BadRequestKeyError)
def handle_bad_request(e):
    return f'bad request!:{e}', 400


@app.route('/update-css-vars', methods=['POST'])
def update_css_vars():
    received_data = request.json
    received_css_vars = received_data['cssVars']
    received_status_word = received_data['currentStatusWord']
    received_times = received_data['times']

    config_css_vars = load_css_vars_from_config()
    config_status_word = load_status_word_from_config()
    config_times = load_times_from_config()

    # Check if specific CSS variables have changed
    word_color_changed = received_css_vars['word-color'] != config_css_vars['word-color']
    shadow_changed = received_css_vars['shadow'] != config_css_vars['shadow']
    print(received_css_vars['word-color'],config_css_vars['word-color'])
    # Check if the status word or times have changed
    status_word_changed = received_status_word != config_status_word
    times_changed = received_times != config_times
    print(word_color_changed,shadow_changed,status_word_changed,times_changed)
    # Determine if any changes occurred
    if word_color_changed or shadow_changed or status_word_changed or times_changed:
        global prev_css_vars, prev_status_word, prev_times
        prev_css_vars = received_css_vars
        prev_status_word = received_status_word
        prev_times = received_times
        update_css_file_from_config()

        return {"refresh": True}

    return {"refresh": False}


@app.route('/', methods=['GET'])
def configure_times_get():
    config = config_manager.load()
    times = config['times']
    current_status_word=config['current_status']
    return render_template(r'index1_new.html', times=times, current_status_word=current_status_word)

@app.route('/', methods=['POST'])
def configure_times_post():

    config = config_manager.load()
    times = config['times']
    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]

    config['times'] = times
    config_manager.save_if_changed(config)
    return redirect(url_for('configure_times_get'))


@app.route('/update-times', methods=['POST'])
def update_times():
    config = config_manager.load()
    times = config['times']
    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]

    config['times'] = times
    config_manager.save_if_changed(config)

    return redirect(url_for('settings'))


@app.route('/settings', methods=['GET'])
def settings_get():
    config = config_manager.load()
    times = config['times']
    css_vars = load_css_vars()
    return render_template('settings.html', css_vars=css_vars, times=times)


@app.route('/settings', methods=['POST'])
def settings_post():
    config = config_manager.load()
    css_vars_from_file = load_css_vars()

    new_css_vars = {key: request.form.get(key, default='') for key in css_vars_from_file.keys()}
    config['css_vars'] = {**config.get('css_vars', {}), **new_css_vars}
    times = config['times']

    for day in times.keys():
        morning_time = request.form.get(f'{day}_morning')
        afternoon_time = request.form.get(f'{day}_afternoon')
        times[day] = [morning_time, afternoon_time]
    config['times']=times
    config_manager.save(config)

    update_css_file_from_config()

    return redirect(url_for('settings_get'))

@app.route('/css/<filename>')
def serve_css(filename):
    return send_from_directory("static", filename)  # Adjusted directory


if __name__ == "__main__":
    prev_file_timestamp = None
    app.run(debug=True, threaded=True)
