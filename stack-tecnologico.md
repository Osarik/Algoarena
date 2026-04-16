# Stack Tecnológico

Diagrama del stack completo de AlgoArena y las relaciones entre sus componentes.

```mermaid
graph TD
    subgraph Frontend
        A[React / HTML]
    end

    subgraph Backend["Backend — Python 3.12"]
        B[Flask 3.x\nAPI REST]
        C[Flask-JWT-Extended 4.x\nAutenticación]
        D[SQLAlchemy 2.x\nORM]
        E[Alembic 1.x\nMigraciones]
    end

    subgraph Persistencia
        F[(PostgreSQL 16)]
    end

    subgraph Externo
        G[Judge0 CE\nEjecución de Código]
    end

    A -->|HTTP/JSON| B
    B --> C
    B --> D
    D --> E
    D --> F
    B -->|HTTP/REST| G
```

## Tabla de Componentes

| Componente | Tecnología | Versión | Rol |
|---|---|---|---|
| Lenguaje | Python | 3.12 | Backend principal |
| Framework web | Flask | 3.x | API REST |
| ORM | SQLAlchemy | 2.x | Abstracción de BD |
| Migraciones | Alembic | 1.x | Versionado de esquema |
| Base de datos | PostgreSQL | 16 | Persistencia |
| Autenticación | Flask-JWT-Extended | 4.x | Tokens JWT |
| Juez de código | Judge0 CE | — | Ejecución y evaluación |
