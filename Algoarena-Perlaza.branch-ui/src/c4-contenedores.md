# Diagrama C4 — Nivel 2: Contenedores

Muestra los bloques tecnológicos principales de AlgoArena y cómo se comunican entre sí.

```mermaid
C4Container
    title AlgoArena — Diagrama de Contenedores (C4 Nivel 2)

    Person(estudiante, "Estudiante")
    Person(admin, "Administrador")

    System_Boundary(algoarena, "AlgoArena") {
        Container(frontend, "Web Browser / Cliente", "React / HTML", "Interfaz de usuario. Permite registrarse, consultar problemas y enviar soluciones.")
        Container(api, "API Flask", "Flask 3.x + Python 3.12", "Lógica de negocio. Expone endpoints REST y coordina los demás servicios.")
        Container(auth, "Servicio de Autenticación", "Flask-JWT-Extended 4.x", "Emite y valida tokens JWT para controlar el acceso.")
        ContainerDb(db, "Base de Datos", "PostgreSQL 16", "Almacena usuarios, problemas, casos de prueba, envíos y progreso.")
    }

    System_Ext(judge0, "Servicio Juez", "Judge0 CE — Ejecuta código en entorno aislado.")

    Rel(estudiante, frontend, "Usa", "HTTPS")
    Rel(admin, frontend, "Administra", "HTTPS")
    Rel(frontend, api, "Peticiones REST", "HTTP/JSON")
    Rel(api, auth, "Valida token JWT", "Interno")
    Rel(api, db, "Lee y escribe datos", "SQLAlchemy / SQL")
    Rel(api, judge0, "Envía código + casos de prueba", "HTTP/REST")
    Rel(judge0, api, "Retorna resultado JSON", "HTTP/REST")
```

## Descripción de Contenedores

| Contenedor | Tecnología | Responsabilidad |
|---|---|---|
| Web Browser / Cliente | React / HTML | Interfaz de usuario |
| API Flask | Flask 3.x + Python 3.12 | Lógica de negocio y endpoints REST |
| Servicio de Autenticación | Flask-JWT-Extended | Emisión y validación de tokens JWT |
| Servicio Juez | Judge0 CE | Ejecución de código en entorno aislado |
| Base de Datos | PostgreSQL 16 | Persistencia de todos los datos del sistema |
