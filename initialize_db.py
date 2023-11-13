import json
import sqlite3

with open('config.json', 'r') as file:
    json_data = json.load(file)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create tables
c.execute('''
          CREATE TABLE css_vars (
              property TEXT,
              value TEXT
          )
          ''')

c.execute('''
          CREATE TABLE times (
              day TEXT,
              opening_hours TEXT,
              additional_info TEXT
          )
          ''')

c.execute('''
          CREATE TABLE status (
              status TEXT,
              color TEXT
          )
          ''')

c.execute('''
          CREATE TABLE scrapper_config (
              url TEXT,
              frame_id TEXT,
              refresh_time INTEGER,
              valid_date TEXT
          )
          ''')

# Insert data
for property, value in json_data['css_vars'].items():
    c.execute("INSERT INTO css_vars VALUES (?, ?)", (property, value))

for day, info in json_data['times']['schedule'].items():
    opening_hours, additional_info = info
    c.execute("INSERT INTO times VALUES (?, ?, ?)", (day, opening_hours, additional_info))

for status, color_info in json_data['status'].items():
    color = color_info['word-color']
    c.execute("INSERT INTO status VALUES (?, ?)", (status, color))

scrapper = json_data['scrapper_config']
c.execute("INSERT INTO scrapper_config VALUES (?, ?, ?, ?)",
          (scrapper['url'], scrapper['frame_id'], scrapper['refresh_time'], scrapper['valid_date']))

# Commit the changes and close the connection
conn.commit()
conn.close()
