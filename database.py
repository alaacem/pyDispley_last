from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def get_data():
    css_vars = query_db('SELECT * FROM css_vars')
    times = query_db('SELECT * FROM times')
    statuses = query_db('SELECT * FROM status')  # changed 'status' to 'statuses'
    scrapper_config = query_db('SELECT * FROM scrapper_config')
    # Convert the data to a dictionary, or however you need to format it
    data = {
        'css_vars': {row[0]: row[1] for row in css_vars},
        'times': {row[0]: [row[1], row[2]] for row in times},
        'statuses': {row[0]: {'color': row[1]} for row in statuses},  # changed 'status' to 'statuses'
        'scrapper_config': scrapper_config[0] if scrapper_config else None,
    }
    return data

@app.route('/settings', methods=['POST'])
def update_settings():
    data = request.form.to_dict()
    # TODO: Update your database with the new settings
    return jsonify({'message': 'Settings updated successfully'})

@app.route('/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    # TODO: Update your database with the new status
    return jsonify({'message': 'Status updated successfully'})

@app.route('/')
def index():
    data = get_data()
    return render_template_string(open('/home/hiwiadmin/pyDisplay/templates/settings.html').read(), **data)

if __name__ == '__main__':
    app.run(debug=True)
