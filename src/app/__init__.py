from flask import Flask
from flask_cors import CORS
from app.routes import main
from app.db import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 🔥 IMPORTANTE (esto crea la BD)
    init_db()

    app.register_blueprint(main)

    return app