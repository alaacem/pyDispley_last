from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from lib.ConfigManager import ConfigManager
from lib.ReloadMenger import ReloadMenger

settings_bp = Blueprint('settings', __name__, template_folder='templates')

reload_bool=ReloadMenger("settings_json/reload.txt")

#css_config_manager = ConfigManager("css.json")
css_config = ConfigManager("settings_json/css.json")
display_spar_config = ConfigManager("settings_json/display_spar.json")
scrapping_config = ConfigManager("settings_json/scrapping_config.json")
status_config = ConfigManager("settings_json/status.json")
woche_config = ConfigManager("settings_json/woche.json")

@settings_bp.route('/', methods=['GET'])
def settings_get():
    css_config_data = css_config.load()
    display_spar_config_data = display_spar_config.load()
    scrapping_config_data = scrapping_config.load()
    status_config_data=status_config.load()
    woche_config_data=woche_config.load()
    #print(woche_config_data)
    return render_template('settings.html'
                           , css_config=css_config_data
                           ,times=woche_config_data['schedule']
                           ,start_date=woche_config_data['start_date']
                           ,end_date=woche_config_data['end_date'],
                           statuses=status_config_data,
                           scrappping=scrapping_config_data,
                           display_spar_config_data=display_spar_config_data
                           )

@settings_bp.route('/', methods=['POST'])
def settings_post():
    return redirect(url_for('settings.settings_get'))

@settings_bp.route('/update-css-settings', methods=['POST'])
def update_css_settings():
    css_config_data = css_config.load()
    received_data = request.form.to_dict()

    changes = []
    for key, new_value in received_data.items():
        if key in css_config_data and css_config_data[key] != new_value:
            old_value = css_config_data[key]
            css_config_data[key] = new_value
            changes.append(f"{key}: '{old_value}' -> '{new_value}'")

    css_config.save(css_config_data)

    if changes:
        changes_summary = ', '.join(changes)
        message = f"CSS settings updated successfully. Changes: {changes_summary}"
    else:
        message = "No changes were made to the CSS settings."

    return jsonify(message=message)
@settings_bp.route('/update-times-woche', methods=['POST'])
def update_time_settings():
    woche_config_data = woche_config.load()
    received_data = request.form.to_dict()

    changes = []

    # Handle start_date and end_date
    for date_key in ['start_date', 'end_date']:
        if date_key in received_data:
            new_value = received_data[date_key]
            old_value = woche_config_data[date_key]
            if old_value != new_value:
                woche_config_data[date_key] = new_value
                changes.append(f"{date_key}: '{old_value}' -> '{new_value}'")

    # Handle schedule
    for day in woche_config_data['schedule']:
        morning_key = f'{day}_morning'
        afternoon_key = f'{day}_afternoon'
        if morning_key in received_data or afternoon_key in received_data:
            old_morning, old_afternoon = woche_config_data['schedule'][day]
            new_morning = received_data.get(morning_key, old_morning)
            new_afternoon = received_data.get(afternoon_key, old_afternoon)
            woche_config_data['schedule'][day] = [new_morning, new_afternoon]
            if old_morning != new_morning or old_afternoon != new_afternoon:
                changes.append(f"{day}: '{old_morning}, {old_afternoon}' -> '{new_morning}, {new_afternoon}'")

    # Save changes if any
    if changes:
        woche_config.save(woche_config_data)
        changes_summary = ', '.join(changes)
        message = f"Time settings updated successfully. Changes: {changes_summary}"
    else:
        message = "No changes were made to the time settings."

    return jsonify(message=message)


@settings_bp.route('/update-status', methods=['POST'])
def update_status():
    status_config_data = status_config.load()
    received_data = request.form.to_dict()

    changes = []
    for key, new_value in received_data.items():
        status, property_name = key.split('_', 1)
        if status in status_config_data and property_name in status_config_data[status]:
            old_value = status_config_data[status][property_name]
            if old_value != new_value:
                status_config_data[status][property_name] = new_value
                changes.append(f"{status} {property_name}: '{old_value}' -> '{new_value}'")

    status_config.save(status_config_data)

    if changes:
        changes_summary = ', '.join(changes)
        message = f"Status settings updated successfully. Changes: {changes_summary}"
    else:
        message = "No changes were made to the status settings."

    return jsonify(message=message)


@settings_bp.route('/update-scrapping-config', methods=['POST'])
def update_scrapping_settings():
    scrapping_config_data = scrapping_config.load()
    received_data = request.form.to_dict()

    changes = []
    for key, new_value in received_data.items():
        if key in scrapping_config_data and scrapping_config_data[key] != new_value:
            old_value = scrapping_config_data[key]
            scrapping_config_data[key] = new_value
            changes.append(f"{key}: '{old_value}' -> '{new_value}'")

    scrapping_config.save(scrapping_config_data)

    if changes:
        changes_summary = ', '.join(changes)
        message = f"CSS settings updated successfully. Changes: {changes_summary}"
    else:
        message = "No changes were made to the CSS settings."

    return jsonify(message=message)

@settings_bp.route('/update-display-spar', methods=['POST'])
def update_display_spar():
    display_spar_config_data = display_spar_config.load()
    received_data = request.form.to_dict()

    changes = []
    for key, new_value in received_data.items():
        if key in display_spar_config_data:
            old_value = display_spar_config_data[key]
            new_value_converted = new_value.lower() == 'true' if key == 'display_spar' else new_value
            display_spar_config_data[key] = new_value_converted
            changes.append(f"{key}: '{old_value}' -> '{new_value_converted}'")

    display_spar_config.save(display_spar_config_data)

    if changes:
        changes_summary = ', '.join(changes)
        message = f"Display Spar settings updated successfully. Changes: {changes_summary}"

    else:
        message = "No changes were made to Display Spar settings."

    return jsonify(message=message)