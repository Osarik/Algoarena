# API de AlgoArena

Base URL local:

```text
http://127.0.0.1:5000
```

## Estado

```http
GET /health
```

Respuesta:

```json
{
  "app": "AlgoArena",
  "status": "ok",
  "version": "1.0.0"
}
```

## Registro

```http
POST /registro
Content-Type: application/json
```

Body:

```json
{
  "username": "estudiante1",
  "password": "123456"
}
```

## Login

```http
POST /login
Content-Type: application/json
```

Body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

## Listar Problemas

```http
GET /problemas
```

Devuelve id, titulo, descripcion, dificultad, categoria y plantillas por lenguaje.

## Detalle de Problema

```http
GET /problemas/1
```

Incluye los datos de prueba publicos asociados al problema.

## Crear Problema

```http
POST /problemas
Content-Type: application/json
```

Requiere usuario administrador.

Body:

```json
{
  "usuario_id": 1,
  "titulo": "Suma simple",
  "descripcion": "Recibe dos numeros y retorna la suma.",
  "dificultad": "facil",
  "categoria": "matematica",
  "test_cases": [
    {
      "descripcion": "Caso publico",
      "input": "2 3",
      "output": "5"
    }
  ]
}
```

## Enviar Solucion

```http
POST /enviar
Content-Type: application/json
```

Body:

```json
{
  "usuario_id": 1,
  "problema_id": 1,
  "lenguaje": "python",
  "codigo": "def resolver(entrada): return sum(map(int, entrada.split()))"
}
```

## Historial

```http
GET /historial?usuario_id=1
```

Filtros opcionales:

```text
tipo=login
username=admin
```
