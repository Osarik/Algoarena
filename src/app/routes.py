from flask import Blueprint, request, jsonify
from app.db import get_db
import json

main = Blueprint("main", __name__)

# =========================
# 🔥 OBTENER PROBLEMAS
# =========================
@main.route("/problemas", methods=["GET"])
def problemas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM problemas")
    problemas = cursor.fetchall()

    resultado = []
    for p in problemas:
        resultado.append({
            "id": p["id"],
            "titulo": p["titulo"],
            "descripcion": p["descripcion"],
            "dificultad": p["dificultad"],
            "categoria": p["categoria"]
        })

    return jsonify(resultado)


# =========================
# 🔥 REGISTRO
# =========================
@main.route("/registro", methods=["POST"])
def registro():
    data = request.get_json()
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
        return jsonify({"mensaje": "Usuario creado"})
    except:
        return jsonify({"error": "Usuario ya existe"})


# =========================
# 🔥 LOGIN
# =========================
@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()
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
        return jsonify({
            "mensaje": "Login exitoso",
            "user_id": user["id"]
        })
    else:
        return jsonify({"error": "Credenciales incorrectas"})


# =========================
# 🔥 ENVIAR SOLUCIÓN (PRO)
# =========================
@main.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()

    problema_id = data.get("problema_id")
    respuesta_usuario = data.get("respuesta")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM problemas WHERE id = ?", (problema_id,))
    problema = cursor.fetchone()

    if not problema:
        return jsonify({"error": "Problema no encontrado"})

    test_cases = json.loads(problema["test_cases"])

    passed = 0
    total = len(test_cases)
    detalles = []

    for case in test_cases:
        entrada = case["input"]
        salida_esperada = case["output"]

        salida_usuario = evaluar_respuesta(
            respuesta_usuario,
            entrada,
            problema["titulo"]
        )

        correcto = str(salida_usuario) == str(salida_esperada)

        if correcto:
            passed += 1

        detalles.append({
            "input": entrada,
            "esperado": salida_esperada,
            "obtenido": salida_usuario,
            "correcto": correcto
        })

    return jsonify({
        "resultado": f"{passed}/{total} casos correctos",
        "correcto": passed == total,
        "detalles": detalles
    })


# =========================
# 🔥 MOTOR DE EVALUACIÓN
# =========================
def evaluar_respuesta(respuesta, entrada, titulo):
    try:
        nums = list(map(int, entrada.split()))

        # 🔥 LÓGICA SEGÚN PROBLEMA
        if "Suma" in titulo:
            return sum(nums)

        if "Multiplicación" in titulo:
            r = 1
            for n in nums:
                r *= n
            return r

        if "par" in titulo.lower():
            return "true" if nums[0] % 2 == 0 else "false"

        if "Mayor" in titulo:
            return max(nums)

        if "Suma de lista" in titulo:
            return sum(nums)

        if "Contar" in titulo:
            return len(nums)

        if "Invertir" in titulo:
            return entrada[::-1]

        if "Palíndromo" in titulo:
            return "true" if entrada == entrada[::-1] else "false"

        if "Factorial" in titulo:
            n = nums[0]
            r = 1
            for i in range(1, n + 1):
                r *= i
            return r

        if "Fibonacci" in titulo:
            n = nums[0]
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        if "Máximo" in titulo:
            return max(nums)

        if "Ordenar" in titulo:
            return " ".join(map(str, sorted(nums)))

        return "error"

    except:
        return "error"