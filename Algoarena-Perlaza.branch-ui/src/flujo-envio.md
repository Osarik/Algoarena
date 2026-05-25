# Diagrama de Flujo — Envío de Código

Flujo completo de la operación de envío de solución desde el cliente hasta el veredicto final.

```mermaid
sequenceDiagram
    actor Usuario
    participant Frontend
    participant API as API Flask
    participant Auth as Servicio Auth
    participant DB as PostgreSQL
    participant Judge as Judge0 CE

    Usuario->>Frontend: Enviar solución
    Frontend->>API: POST /submit (código + problema_id)
    API->>Auth: Validar token JWT
    Auth-->>API: Token válido
    API->>DB: GET problema + casos_de_prueba
    DB-->>API: Datos del problema
    API->>Judge: Ejecutar código contra casos de prueba
    Judge-->>API: Resultado estructurado (JSON)
    API->>DB: INSERT envío (resultado_juez JSONB)
    API->>DB: UPDATE progreso_usuario
    API-->>Frontend: Respuesta con resultado
    Frontend-->>Usuario: Mostrar veredicto
```

## Principios de Diseño Aplicados

- **Separación de responsabilidades:** cada contenedor tiene una función bien definida y acotada.
- **Comunicación asíncrona potencial:** el Servicio Juez puede evolucionar a un modelo de colas (Celery + Redis) para alta concurrencia.
- **Seguridad perimetral:** todos los endpoints protegidos requieren token JWT válido.
- **Extensibilidad:** la arquitectura permite añadir nuevos jueces o microservicios sin modificar la API principal.
