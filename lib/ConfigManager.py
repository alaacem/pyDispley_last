from flask import Flask
from models import db, Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class ConfigManager:
    def __init__(self):
        with app.app_context():
            db.create_all()

    def load(self):
        with app.app_context():
            configs = Config.query.all()
            return {config.key: config.value for config in configs}

    def save(self, config_data):
        with app.app_context():
            for key, value in config_data.items():
                config = Config.query.filter_by(key=key).first()
                if not config:
                    new_config = Config(key=key, value=value)
                    db.session.add(new_config)
                else:
                    config.value = value
            db.session.commit()
