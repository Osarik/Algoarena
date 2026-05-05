import sqlite3

def get_db():
    conn = sqlite3.connect("algoarena.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 🧠 TABLA PROBLEMAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problemas (
        id INTEGER PRIMARY KEY,
        titulo TEXT,
        descripcion TEXT,
        respuesta TEXT,
        dificultad TEXT,
        categoria TEXT
    )
    """)

    # 👤 TABLA USUARIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # 📊 TABLA ENVIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS envios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        problema_id INTEGER,
        resultado TEXT
    )
    """)

    # 🔥 INSERTAR PROBLEMAS SI NO EXISTEN
    cursor.execute("SELECT COUNT(*) FROM problemas")
    if cursor.fetchone()[0] == 0:
        problemas = [
            (1, "Suma", "2+2", "4", "facil", "matematica"),
            (2, "Multiplicación", "2*3", "6", "facil", "matematica"),
            (3, "Resta", "5-3", "2", "facil", "matematica"),
            (4, "División", "10/2", "5", "facil", "matematica"),
            (5, "Par o impar", "4 es par?", "true", "facil", "logica"),
            (6, "Mayor número", "max(3,7)", "7", "medio", "algoritmos"),
            (7, "Invertir lista", "[1,2,3]", "[3,2,1]", "medio", "estructuras"),
            (8, "Contar letras", "hola", "4", "medio", "strings"),
            (9, "Factorial", "5!", "120", "medio", "matematica"),
            (10, "Fibonacci", "fib(6)", "8", "dificil", "algoritmos"),
            (11, "Palíndromo", "oso", "true", "dificil", "strings"),
            (12, "Ordenar lista", "[3,1,2]", "[1,2,3]", "dificil", "estructuras")
        ]

        cursor.executemany("""
        INSERT INTO problemas VALUES (?, ?, ?, ?, ?, ?)
        """, problemas)

    conn.commit()
    conn.close()