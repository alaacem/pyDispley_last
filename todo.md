source /home/hiwiadmin/pyDisplay/myenv/bin/activate


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

- css wars , statu .....setting.py the existings file change
to - reload (reload true or false refrech)
reload must from update change
