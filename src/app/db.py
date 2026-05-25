import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "instance" / "algoarena.db"


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row["name"] == column for row in cursor.fetchall())


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT DEFAULT 'estudiante',
        correctos INTEGER DEFAULT 0,
        incorrectos INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problemas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        dificultad TEXT NOT NULL,
        categoria TEXT NOT NULL,
        test_cases TEXT NOT NULL,
        plantilla_python TEXT DEFAULT '',
        plantilla_java TEXT DEFAULT '',
        plantilla_cpp TEXT DEFAULT ''
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        usuario_id INTEGER,
        username TEXT,
        tipo_evento TEXT NOT NULL,
        detalle TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)

    if not column_exists(cursor, "usuarios", "rol"):
        cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'estudiante'")
    for column in ("plantilla_python", "plantilla_java", "plantilla_cpp"):
        if not column_exists(cursor, "problemas", column):
            cursor.execute(f"ALTER TABLE problemas ADD COLUMN {column} TEXT DEFAULT ''")

    cursor.execute("SELECT COUNT(*) AS total FROM problemas")
    if cursor.fetchone()["total"] == 0:
        seed_problems(cursor)

    cursor.execute("SELECT id, titulo FROM problemas")
    for problem in cursor.fetchall():
        templates = build_templates(problem["titulo"])
        cursor.execute(
            """
            UPDATE problemas
            SET plantilla_python = COALESCE(NULLIF(plantilla_python, ''), ?),
                plantilla_java = COALESCE(NULLIF(plantilla_java, ''), ?),
                plantilla_cpp = COALESCE(NULLIF(plantilla_cpp, ''), ?)
            WHERE id = ?
            """,
            (templates["python"], templates["java"], templates["cpp"], problem["id"]),
        )

    cursor.execute("SELECT id FROM usuarios WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute(
            """
            INSERT INTO usuarios (username, password, rol, correctos, incorrectos)
            VALUES (?, ?, ?, 0, 0)
            """,
            ("admin", "admin123", "admin"),
        )

    conn.commit()
    conn.close()


def seed_problems(cursor):
    problemas = [
        {
            "titulo": "Suma de dos numeros",
            "descripcion": "Recibe dos numeros separados por espacio y retorna su suma.",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"id": "TC-01", "descripcion": "Numeros pequenos", "input": "2 2", "output": "4"},
                {"id": "TC-02", "descripcion": "Numeros positivos", "input": "3 5", "output": "8"},
            ],
        },
        {
            "titulo": "Numero par",
            "descripcion": "Determina si un numero entero es par. Retorna true o false.",
            "dificultad": "facil",
            "categoria": "matematica",
            "test_cases": [
                {"id": "TC-01", "descripcion": "Entrada par", "input": "2", "output": "true"},
                {"id": "TC-02", "descripcion": "Entrada impar", "input": "3", "output": "false"},
            ],
        },
        {
            "titulo": "Invertir string",
            "descripcion": "Recibe un texto y retorna el mismo texto invertido.",
            "dificultad": "medio",
            "categoria": "algoritmos",
            "test_cases": [
                {"id": "TC-01", "descripcion": "Palabra corta", "input": "hola", "output": "aloh"},
                {"id": "TC-02", "descripcion": "Tres caracteres", "input": "abc", "output": "cba"},
            ],
        },
        {
            "titulo": "Factorial",
            "descripcion": "Calcula el factorial de un numero entero no negativo.",
            "dificultad": "dificil",
            "categoria": "matematica",
            "test_cases": [
                {"id": "TC-01", "descripcion": "Factorial de 3", "input": "3", "output": "6"},
                {"id": "TC-02", "descripcion": "Factorial de 5", "input": "5", "output": "120"},
            ],
        },
        {
            "titulo": "Ordenar lista",
            "descripcion": "Ordena una lista de numeros de menor a mayor.",
            "dificultad": "dificil",
            "categoria": "estructuras",
            "test_cases": [
                {"id": "TC-01", "descripcion": "Lista desordenada", "input": "3 1 2", "output": "1 2 3"},
                {"id": "TC-02", "descripcion": "Otra lista", "input": "5 4 6", "output": "4 5 6"},
            ],
        },
    ]

    for problem in problemas:
        templates = build_templates(problem["titulo"])
        cursor.execute(
            """
            INSERT INTO problemas (
                titulo, descripcion, dificultad, categoria, test_cases,
                plantilla_python, plantilla_java, plantilla_cpp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                problem["titulo"],
                problem["descripcion"],
                problem["dificultad"],
                problem["categoria"],
                json.dumps(problem["test_cases"], ensure_ascii=True),
                templates["python"],
                templates["java"],
                templates["cpp"],
            ),
        )


def build_templates(titulo):
    slug = titulo.lower().replace(" ", "_")
    return {
        "python": f"def resolver(entrada):\n    # Implementa {titulo}\n    return None\n\nprint(resolver(input()))",
        "java": f"// Implementa {titulo}\nclass Main {{\n    public static void main(String[] args) {{\n        // leer entrada y mostrar salida\n    }}\n}}",
        "cpp": f"#include <iostream>\nusing namespace std;\n\nint main() {{\n    // Implementa {slug}\n    return 0;\n}}",
    }
