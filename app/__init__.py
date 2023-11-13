# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configurations should go here. As an example:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anzige_config.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
