from pathlib import Path

from flask import Flask
from flask_cors import CORS

from app.db import init_db
from app.routes import main


BASE_DIR = Path(__file__).resolve().parents[2]


def create_app():
    app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")
    CORS(app)

    init_db()
    app.register_blueprint(main)

    return app
