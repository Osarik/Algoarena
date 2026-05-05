import sqlite3
import json

def get_db():
    conn = sqlite3.connect("algoarena.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 🔥 TABLA USUARIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        correctos INTEGER DEFAULT 0,
        incorrectos INTEGER DEFAULT 0
        
        
    )
    """)

    # 🔥 TABLA PROBLEMAS (MEJORADA)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        dificultad TEXT,
        categoria TEXT,
        test_cases TEXT
    )
    """)

    # 🔥 LIMPIAR (para evitar duplicados al reiniciar)
    cursor.execute("DELETE FROM problemas")

    # 🔥 LISTA DE PROBLEMAS (12 EJERCICIOS)
    problemas = [
        {
            "titulo": "Suma de dos números",
            "descripcion": "Recibe dos números separados por espacio",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"input": "2 2", "output": "4"},
                {"input": "3 5", "output": "8"}
            ]
        },
        {
            "titulo": "Multiplicación",
            "descripcion": "Multiplica dos números",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"input": "2 3", "output": "6"},
                {"input": "4 5", "output": "20"}
            ]
        },
        {
            "titulo": "Número par",
            "descripcion": "Determina si un número es par",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"input": "2", "output": "true"},
                {"input": "3", "output": "false"}
            ]
        },
        {
            "titulo": "Mayor de dos números",
            "descripcion": "Retorna el mayor de dos números",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"input": "5 8", "output": "8"},
                {"input": "10 2", "output": "10"}
            ]
        },
        {
            "titulo": "Suma de lista",
            "descripcion": "Suma una lista de números",
            "dificultad": "medio",
            "categoria": "estructuras",
            "test_cases": [
                {"input": "1 2 3", "output": "6"},
                {"input": "4 5 6", "output": "15"}
            ]
        },
        {
            "titulo": "Contar elementos",
            "descripcion": "Cuenta cuántos elementos hay",
            "dificultad": "medio",
            "categoria": "estructuras",
            "test_cases": [
                {"input": "1 2 3", "output": "3"},
                {"input": "5 6", "output": "2"}
            ]
        },
        {
            "titulo": "Invertir string",
            "descripcion": "Invierte un texto",
            "dificultad": "medio",
            "categoria": "algoritmos",
            "test_cases": [
                {"input": "hola", "output": "aloh"},
                {"input": "abc", "output": "cba"}
            ]
        },
        {
            "titulo": "Palíndromo",
            "descripcion": "Verifica si es palíndromo",
            "dificultad": "medio",
            "categoria": "algoritmos",
            "test_cases": [
                {"input": "ana", "output": "true"},
                {"input": "hola", "output": "false"}
            ]
        },
        {
            "titulo": "Factorial",
            "descripcion": "Calcula factorial",
            "dificultad": "dificil",
            "categoria": "matematica",
            "test_cases": [
                {"input": "3", "output": "6"},
                {"input": "5", "output": "120"}
            ]
        },
        {
            "titulo": "Fibonacci",
            "descripcion": "Devuelve n de Fibonacci",
            "dificultad": "dificil",
            "categoria": "algoritmos",
            "test_cases": [
                {"input": "5", "output": "5"},
                {"input": "6", "output": "8"}
            ]
        },
        {
            "titulo": "Máximo en lista",
            "descripcion": "Encuentra el mayor número",
            "dificultad": "medio",
            "categoria": "estructuras",
            "test_cases": [
                {"input": "1 9 3", "output": "9"},
                {"input": "5 2 7", "output": "7"}
            ]
        },
        {
            "titulo": "Ordenar lista",
            "descripcion": "Ordena números",
            "dificultad": "dificil",
            "categoria": "algoritmos",
            "test_cases": [
                {"input": "3 1 2", "output": "1 2 3"},
                {"input": "5 4 6", "output": "4 5 6"}
            ]
        }
    ]

    # 🔥 INSERTAR PROBLEMAS
    for p in problemas:
        cursor.execute("""
        INSERT INTO problemas (titulo, descripcion, dificultad, categoria, test_cases)
        VALUES (?, ?, ?, ?, ?)
        """, (
            p["titulo"],
            p["descripcion"],
            p["dificultad"],
            p["categoria"],
            json.dumps(p["test_cases"])
        ))

    conn.commit()
    conn.close()