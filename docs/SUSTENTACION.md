# Guia de Sustentacion

## Discurso Corto

AlgoArena es una plataforma academica inspirada en LeetCode. Permite que un estudiante inicie sesion, consulte retos de programacion, vea datos de prueba, escriba una solucion y reciba retroalimentacion por cada caso. Tambien incluye una parte administrativa para crear problemas y revisar la trazabilidad del sistema.

## Flujo de Demostracion

1. Abrir `http://127.0.0.1:5000/`.
2. Iniciar sesion con `admin` y `admin123`.
3. Mostrar la lista de problemas y filtrar por dificultad.
4. Seleccionar un problema.
5. Cambiar entre Python, Java y C++ para mostrar las plantillas.
6. Usar "Cargar solucion demo".
7. Hacer clic en "Probar previo a envio".
8. Mostrar los resultados por caso de prueba.
9. Ir a "Admin" y crear un problema nuevo.
10. Ir a "Historial" y mostrar los eventos registrados.

## Requerimientos Cubiertos

### Corte Dos

- Login de usuario.
- Listado de problemas.
- Filtro por dificultad.
- Datos de prueba por problema.
- Validacion de soluciones.
- Retroalimentacion clara.

### Corte Tres

- Registro de actividades del sistema.
- Consulta de historial por administrador.
- Soporte visual para Python, Java y C++.
- Creacion de problemas por administrador.
- Asociacion de datos de prueba a problemas nuevos.

## Decisiones Tecnicas

- Flask expone la API y sirve la interfaz principal.
- SQLite almacena usuarios, problemas y eventos.
- El usuario `admin/admin123` se crea automaticamente para facilitar la demo.
- El motor de evaluacion es controlado y no ejecuta codigo arbitrario por seguridad.

## Preguntas Probables

### Por que no se ejecuta codigo real del usuario?

Porque ejecutar codigo arbitrario implica riesgos de seguridad. Para esta entrega se implemento una validacion controlada que mantiene el flujo funcional de LeetCode sin exponer el sistema.

### Donde se guarda el historial?

En la tabla `eventos`, creada en `src/app/db.py`.

### Como se diferencia un administrador?

Los usuarios tienen un campo `rol`. El usuario `admin` tiene rol `admin` y puede crear problemas y consultar historial.

### Donde estan los datos de prueba?

En la columna `test_cases` de la tabla `problemas`, guardados como JSON.
