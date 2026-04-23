# comentario de prueba para code review
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "AlgoArena funcionando "}
