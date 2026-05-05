from flask import Blueprint, request
from app.db import get_db

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return {"message": "AlgoArena funcionando"}

# 📚 OBTENER PROBLEMAS
@main.route("/problemas")
def problemas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problemas")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


# 📤 ENVIAR RESPUESTA + GUARDAR
@main.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()

    problema_id = data.get("problema_id")
    respuesta = data.get("respuesta")
    usuario_id = data.get("usuario_id")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT respuesta FROM problemas WHERE id = ?", (problema_id,))
    row = cursor.fetchone()

    if not row:
        return {"error": "Problema no encontrado"}, 404

    resultado = "Correcto" if respuesta == row["respuesta"] else "Incorrecto"

    # 🔥 guardar intento
    cursor.execute("""
        INSERT INTO envios (usuario_id, problema_id, resultado)
        VALUES (?, ?, ?)
    """, (usuario_id, problema_id, resultado))

    conn.commit()

    return {"resultado": resultado}


# 🔐 REGISTRO
@main.route("/registro", methods=["POST"])
def registro():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return {"mensaje": "Usuario creado"}
    except:
        return {"error": "Usuario ya existe"}, 400


# 🔐 LOGIN
@main.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        return {"mensaje": "Login exitoso", "user_id": user["id"]}
    else:
        return {"error": "Credenciales incorrectas"}, 401