# app/models.py

from . import db
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enable_scraping = db.Column(db.Boolean, nullable=False)
    current_status = db.Column(db.String, nullable=False)
    valid_date = db.Column(db.String, nullable=False)
    bottom_text = db.Column(db.String, nullable=True)

    # Relationships
    css_vars_id = db.Column(db.Integer, db.ForeignKey('css_vars.id'))
    css_vars = relationship("CSSVars", back_populates="config")

    times_id = db.Column(db.Integer, db.ForeignKey('times.id'))
    times = relationship("Times", back_populates="config")

    scrapper_config_id = db.Column(db.Integer, db.ForeignKey('scrapper_config.id'))
    scrapper_config = relationship("ScrapperConfig", back_populates="config")

    shutdown_id = db.Column(db.Integer, db.ForeignKey('shutdown.id'))
    shutdown = relationship("Shutdown", back_populates="config")


class CSSVars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header_bg_color = db.Column(db.String, nullable=False)
    table_text_color = db.Column(db.String, nullable=False)
    table_bg_color = db.Column(db.String, nullable=False)
    table_border_color = db.Column(db.String, nullable=False)
    animation_speed = db.Column(db.String, nullable=False)
    table_font_size = db.Column(db.String, nullable=False)
    table_border_thickness = db.Column(db.String, nullable=False)
    table_text = db.Column(db.String, nullable=False)
    word_font_size = db.Column(db.String, nullable=False)
    word_color = db.Column(db.String, nullable=False)
    shadow = db.Column(db.String, nullable=False)
    word_border_color = db.Column(db.String, nullable=False)
    table_header_text_color = db.Column(db.String, nullable=False)

    config = relationship("Config", back_populates="css_vars")


class Times(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    schedule = db.Column(JSON, nullable=False)  # Storing as JSON for simplicity

    config = relationship("Config", back_populates="times")


class Schedule(db.Model):  # If you need more normalization
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    time_slot_1 = db.Column(db.String, nullable=False)
    time_slot_2 = db.Column(db.String, nullable=True)


class ScrapperConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    frame_id = db.Column(db.String, nullable=False)
    refresh_time = db.Column(db.Integer, nullable=False)
    valid_date = db.Column(db.String, nullable=True)

    config = relationship("Config", back_populates="scrapper_config")

class Shutdown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_spar = db.Column(db.Boolean, nullable=False)
    start = db.Column(db.String, nullable=False)
    end = db.Column(db.String, nullable=False)

    config = relationship("Config", back_populates="shutdown")





