import json
import re
from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory

from app.db import get_db


main = Blueprint("main", __name__)
VALID_LANGUAGES = {"python", "java", "cpp"}
BASE_DIR = Path(__file__).resolve().parents[2]


@main.route("/", methods=["GET"])
def home():
    return send_from_directory(BASE_DIR, "index.html")


@main.route("/health", methods=["GET"])
def health():
    return jsonify({
        "app": "AlgoArena",
        "status": "ok",
        "version": "1.0.0",
        "features": [
            "autenticacion",
            "problemas_filtrables",
            "datos_de_prueba",
            "validacion_de_soluciones",
            "multiples_lenguajes",
            "auditoria",
            "gestion_admin",
        ],
    })


def row_to_problem(row, include_tests=False):
    problem = {
        "id": row["id"],
        "titulo": row["titulo"],
        "descripcion": row["descripcion"],
        "dificultad": row["dificultad"],
        "categoria": row["categoria"],
        "plantillas": {
            "python": row["plantilla_python"] or "",
            "java": row["plantilla_java"] or "",
            "cpp": row["plantilla_cpp"] or "",
        },
    }
    if include_tests:
        problem["test_cases"] = json.loads(row["test_cases"] or "[]")
    return problem


def log_event(cursor, usuario_id, username, tipo_evento, detalle=""):
    cursor.execute(
        """
        INSERT INTO eventos (usuario_id, username, tipo_evento, detalle)
        VALUES (?, ?, ?, ?)
        """,
        (usuario_id, username, tipo_evento, detalle),
    )


def get_user(cursor, usuario_id):
    if not usuario_id:
        return None
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    return cursor.fetchone()


def require_admin(cursor, usuario_id):
    user = get_user(cursor, usuario_id)
    return user if user and user["rol"] == "admin" else None


@main.route("/problemas", methods=["GET"])
def listar_problemas():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problemas ORDER BY id")
    problems = [row_to_problem(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(problems)


@main.route("/problemas/<int:problema_id>", methods=["GET"])
def detalle_problema(problema_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problemas WHERE id = ?", (problema_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Problema no encontrado"}), 404
    return jsonify(row_to_problem(row, include_tests=True))


@main.route("/problemas", methods=["POST"])
def crear_problema():
    data = request.get_json() or {}
    usuario_id = data.get("usuario_id")

    conn = get_db()
    cursor = conn.cursor()
    admin = require_admin(cursor, usuario_id)
    if not admin:
        conn.close()
        return jsonify({"error": "Solo un administrador puede crear problemas"}), 403

    required = ("titulo", "descripcion", "dificultad", "categoria", "test_cases")
    if any(not data.get(field) for field in required):
        conn.close()
        return jsonify({"error": "Faltan campos requeridos"}), 400

    test_cases = data.get("test_cases")
    if not isinstance(test_cases, list) or not test_cases:
        conn.close()
        return jsonify({"error": "Debes registrar al menos un dato de prueba"}), 400

    normalized_cases = []
    for index, case in enumerate(test_cases, start=1):
        entrada = str(case.get("input", "")).strip()
        salida = str(case.get("output", "")).strip()
        if not entrada or not salida:
            conn.close()
            return jsonify({"error": "Cada caso debe tener entrada y salida esperada"}), 400
        normalized_cases.append({
            "id": case.get("id") or f"TC-{index:02d}",
            "descripcion": case.get("descripcion") or "Caso publico",
            "input": entrada,
            "output": salida,
        })

    cursor.execute(
        """
        INSERT INTO problemas (
            titulo, descripcion, dificultad, categoria, test_cases,
            plantilla_python, plantilla_java, plantilla_cpp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["titulo"].strip(),
            data["descripcion"].strip(),
            data["dificultad"],
            data["categoria"].strip(),
            json.dumps(normalized_cases, ensure_ascii=True),
            data.get("plantilla_python", ""),
            data.get("plantilla_java", ""),
            data.get("plantilla_cpp", ""),
        ),
    )
    problem_id = cursor.lastrowid
    log_event(cursor, admin["id"], admin["username"], "creacion_problema", f"Problema {problem_id}")
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Problema creado", "id": problem_id})


@main.route("/registro", methods=["POST"])
def registro():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Usuario y contrasena son obligatorios"}), 400

    rol = "admin" if username.lower() == "admin" else "estudiante"
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (username, password, rol, correctos, incorrectos)
            VALUES (?, ?, ?, 0, 0)
            """,
            (username, password, rol),
        )
        user_id = cursor.lastrowid
        log_event(cursor, user_id, username, "registro", f"Rol {rol}")
        conn.commit()
        return jsonify({"mensaje": "Usuario creado", "user_id": user_id, "rol": rol})
    except Exception:
        return jsonify({"error": "Usuario ya existe"}), 409
    finally:
        conn.close()


@main.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (username, password),
    )
    user = cursor.fetchone()

    if user:
        log_event(cursor, user["id"], user["username"], "login", "Inicio de sesion exitoso")
        conn.commit()
        response = {
            "mensaje": "Login exitoso",
            "user_id": user["id"],
            "username": user["username"],
            "rol": user["rol"],
            "stats": {
                "correctos": user["correctos"],
                "incorrectos": user["incorrectos"],
            },
        }
        conn.close()
        return jsonify(response)

    conn.close()
    return jsonify({"error": "Credenciales incorrectas"}), 401


@main.route("/historial", methods=["GET"])
def historial():
    usuario_id = request.args.get("usuario_id")
    tipo = request.args.get("tipo", "")
    username = request.args.get("username", "")

    conn = get_db()
    cursor = conn.cursor()
    admin = require_admin(cursor, usuario_id)
    if not admin:
        conn.close()
        return jsonify({"error": "Solo un administrador puede consultar el historial"}), 403

    query = "SELECT * FROM eventos WHERE 1=1"
    params = []
    if tipo:
        query += " AND tipo_evento = ?"
        params.append(tipo)
    if username:
        query += " AND username LIKE ?"
        params.append(f"%{username}%")
    query += " ORDER BY fecha DESC LIMIT 100"

    cursor.execute(query, params)
    eventos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(eventos)


@main.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json() or {}
    problema_id = data.get("problema_id")
    codigo = data.get("codigo") or data.get("respuesta") or ""
    lenguaje = (data.get("lenguaje") or "python").lower()
    usuario_id = data.get("usuario_id")

    if lenguaje not in VALID_LANGUAGES:
        return jsonify({"error": "Lenguaje no soportado"}), 400

    conn = get_db()
    cursor = conn.cursor()
    user = get_user(cursor, usuario_id)

    cursor.execute("SELECT * FROM problemas WHERE id = ?", (problema_id,))
    problema = cursor.fetchone()
    if not problema:
        conn.close()
        return jsonify({"error": "Problema no encontrado"}), 404

    test_cases = json.loads(problema["test_cases"] or "[]")
    validation = validar_codigo(codigo, lenguaje)
    if validation:
        if user:
            log_event(cursor, user["id"], user["username"], "envio_error_compilacion", validation)
            conn.commit()
        conn.close()
        return jsonify({
            "resultado": "Error de compilacion",
            "correcto": False,
            "tipo_error": "compilacion",
            "mensaje": validation,
            "casos": [],
        })

    casos = []
    passed = 0
    for case in test_cases:
        salida_usuario = evaluar_respuesta(codigo, case["input"], problema["titulo"])
        ok = str(salida_usuario).strip().lower() == str(case["output"]).strip().lower()
        if ok:
            passed += 1
        casos.append({
            "id": case.get("id", ""),
            "descripcion": case.get("descripcion", ""),
            "entrada": case["input"],
            "esperado": case["output"],
            "obtenido": salida_usuario,
            "estado": "Aprobado" if ok else "Fallo",
        })

    correcto = passed == len(test_cases)
    if user:
        if correcto:
            cursor.execute("UPDATE usuarios SET correctos = correctos + 1 WHERE id = ?", (user["id"],))
        else:
            cursor.execute("UPDATE usuarios SET incorrectos = incorrectos + 1 WHERE id = ?", (user["id"],))
        log_event(
            cursor,
            user["id"],
            user["username"],
            "envio_solucion",
            f"Problema {problema_id} en {lenguaje}: {passed}/{len(test_cases)}",
        )
        conn.commit()

    stats = {"correctos": 0, "incorrectos": 0}
    if user:
        cursor.execute("SELECT correctos, incorrectos FROM usuarios WHERE id = ?", (user["id"],))
        stats = dict(cursor.fetchone())

    conn.close()
    return jsonify({
        "resultado": "Correcto" if correcto else "Incorrecto",
        "correcto": correcto,
        "lenguaje": lenguaje,
        "casos": casos,
        "stats": stats,
    })


def validar_codigo(codigo, lenguaje):
    text = codigo.strip()
    if not text:
        return "El editor esta vacio."
    lowered = text.lower()
    if "syntaxerror" in lowered or "compilationerror" in lowered:
        return "Se detecto un error de sintaxis en la solucion."
    if lenguaje == "python" and text.count("(") != text.count(")"):
        return "Parentesis incompletos en codigo Python."
    if lenguaje in {"java", "cpp"} and "{" in text and text.count("{") != text.count("}"):
        return "Llaves incompletas en el codigo."
    return None


def evaluar_respuesta(codigo, entrada, titulo):
    try:
        nums = list(map(int, entrada.split()))
    except ValueError:
        nums = []

    title = titulo.lower()
    code = codigo.lower()

    # Motor controlado para la demo: valida patrones de solucion sin ejecutar codigo arbitrario.
    if "suma" in title and ("sum" in code or "+" in code or "suma" in code):
        return sum(nums)
    if "multiplicacion" in title and ("*" in code or "multip" in code):
        result = 1
        for n in nums:
            result *= n
        return result
    if "par" in title and ("%" in code or "mod" in code or "par" in code):
        return "true" if nums and nums[0] % 2 == 0 else "false"
    if "mayor" in title and ("max" in code or "mayor" in code):
        return max(nums)
    if "lista" in title and "suma" in title and ("sum" in code or "+" in code):
        return sum(nums)
    if "contar" in title and ("len" in code or "length" in code or "count" in code):
        return len(nums)
    if "invertir" in title and ("[::-1]" in code or "reverse" in code or "invert" in code):
        return entrada[::-1]
    if "palindromo" in normalize(title) and ("[::-1]" in code or "reverse" in code or "pal" in code):
        return "true" if entrada == entrada[::-1] else "false"
    if "factorial" in title and ("for" in code or "while" in code or "factorial" in code):
        result = 1
        for i in range(1, nums[0] + 1):
            result *= i
        return result
    if "fibonacci" in title and ("fib" in code or "for" in code or "while" in code):
        a, b = 0, 1
        for _ in range(nums[0]):
            a, b = b, a + b
        return a
    if "maximo" in normalize(title) and ("max" in code or "mayor" in code):
        return max(nums)
    if "ordenar" in title and ("sort" in code or "sorted" in code or "orden" in code):
        return " ".join(map(str, sorted(nums)))

    direct_answer = extract_direct_answer(codigo)
    if direct_answer is not None:
        return direct_answer
    return "No coincide con la solucion esperada"


def normalize(text):
    return (
        text.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )


def extract_direct_answer(codigo):
    match = re.search(r"respuesta\s*:\s*(.+)", codigo, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
