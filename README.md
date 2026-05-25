# AlgoArena

Plataforma academica inspirada en LeetCode para practicar retos de programacion, validar soluciones con datos de prueba y registrar actividad del sistema.

## Resumen

AlgoArena permite a estudiantes autenticarse, explorar problemas por dificultad, escribir una solucion en un editor, seleccionar lenguaje de programacion y ejecutar validaciones contra casos de prueba publicos. Tambien incluye una vista administrativa para crear problemas y consultar el historial de eventos.

## Funcionalidades

- Autenticacion de estudiantes y administrador.
- Catalogo de problemas con dificultad, categoria y descripcion.
- Filtros por dificultad.
- Datos de prueba publicos por problema.
- Editor de solucion con plantillas para Python, Java y C++.
- Validacion de resultados por caso de prueba.
- Registro de estadisticas de envios correctos e incorrectos.
- Auditoria de eventos: login, registro, envios y creacion de problemas.
- Gestion administrativa para agregar nuevos problemas.

## Stack

- Python
- Flask
- Flask-CORS
- SQLite
- HTML, CSS y JavaScript vanilla

## Estructura

```text
algoarena/
├── index.html              # Interfaz principal servida por Flask
├── instance/               # Base de datos SQLite local generada en runtime
├── src/
│   ├── run.py              # Punto de entrada del servidor
│   ├── requirements.txt    # Dependencias Python
│   └── app/
│       ├── __init__.py     # Fabrica de la app Flask
│       ├── db.py           # Esquema, migraciones simples y datos iniciales
│       └── routes.py       # API REST y pagina principal
└── docs/
    ├── README.md
    ├── API.md
    └── SUSTENTACION.md
```

## Instalacion

Desde PowerShell:

```powershell
cd "C:\Users\Juan Felipe Vergara\Desktop\algoarena"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r src\requirements.txt
python src\run.py
```

Abre la aplicacion en:

```text
http://127.0.0.1:5000/
```

## Credenciales de prueba

```text
Usuario: admin
Contrasena: admin123
Rol: admin
```

Tambien puedes registrar usuarios estudiantes desde la interfaz.

## Endpoints principales

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/` | Interfaz web principal |
| GET | `/health` | Estado general de la app |
| POST | `/registro` | Registro de usuario |
| POST | `/login` | Inicio de sesion |
| GET | `/problemas` | Lista de problemas |
| GET | `/problemas/<id>` | Detalle de un problema con datos de prueba |
| POST | `/problemas` | Crear problema como administrador |
| POST | `/enviar` | Validar solucion contra datos de prueba |
| GET | `/historial` | Consultar eventos como administrador |

## Nota tecnica sobre ejecucion de codigo

Por seguridad, el prototipo no ejecuta codigo arbitrario del usuario en el sistema operativo. El motor actual valida patrones de solucion y compara resultados contra datos de prueba controlados. Esta decision evita riesgos de ejecucion remota durante una entrega academica y mantiene el flujo funcional requerido por el proyecto.

## Estado de la entrega

El proyecto cubre los requerimientos de Corte Dos y agrega las funcionalidades base del Corte Tres: auditoria, multiples lenguajes seleccionables y creacion de problemas por administrador.
