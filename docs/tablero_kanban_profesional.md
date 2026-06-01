# Propuesta profesional de tablero Kanban para AlgoArena

Repositorio: https://github.com/Osarik/Algoarena  
Fecha de revision: 2026-05-31

## Diagnostico rapido

El repositorio tiene issues de historias de usuario, pero el tablero se ve basico porque faltan senales de gestion:

- Varias historias estan abiertas aunque el proyecto entregado ya implementa esas funciones.
- La mayoria de issues no tienen labels, responsables, comentarios de avance ni criterio de cierre.
- No se ve separacion entre trabajo terminado, trabajo en revision y mejoras futuras.
- Hay historias repetidas o equivalentes: por ejemplo login aparece como HU01 y HU12.

Con el ZIP `algoarena_v2.zip` se evidencia una version funcional con Flask, SQLite, autenticacion, catalogo de problemas, envio/ejecucion de codigo, casos de prueba, historial, auditoria y gestion admin.

## Tablero recomendado

Nombre del Project:

`AlgoArena - Desarrollo y entrega v2`

Descripcion:

`Seguimiento profesional del desarrollo de AlgoArena, plataforma web para retos de programacion con autenticacion, catalogo de problemas, ejecucion de codigo, validacion por casos de prueba, historial y administracion.`

Columnas:

1. `Backlog`
2. `Ready`
3. `In progress`
4. `Review / QA`
5. `Done`

Campos recomendados:

- `Status`: Backlog, Ready, In progress, Review / QA, Done
- `Prioridad`: Alta, Media, Baja
- `Modulo`: Frontend, Backend, Base de datos, Testing, Documentacion, UX, Seguridad
- `Tipo`: Historia de usuario, Bug, Mejora, Tarea tecnica
- `Sprint`: Entrega v2

## Labels recomendados

- `tipo: historia` - Historias funcionales de usuario.
- `tipo: tecnica` - Tareas de estructura, arquitectura o configuracion.
- `tipo: mejora` - Mejoras no indispensables para la entrega actual.
- `modulo: frontend` - Interfaz HTML/CSS/JS.
- `modulo: backend` - Rutas, logica Flask y servicios.
- `modulo: db` - SQLite, tablas, seed y persistencia.
- `modulo: qa` - Validacion, pruebas y verificacion.
- `prioridad: alta` - Necesario para entrega funcional.
- `prioridad: media` - Importante, pero no bloqueante.
- `prioridad: baja` - Deseable o futuro.
- `estado: implementado` - Ya esta desarrollado.
- `estado: pendiente` - Falta implementar o completar.
- `estado: futuro` - Mejora posterior a la entrega.

## Clasificacion sugerida de issues existentes

| Issue | Estado sugerido | Labels | Comentario |
| --- | --- | --- | --- |
| #1 HU01 - Login | Done | tipo: historia, modulo: backend, prioridad: alta, estado: implementado | Implementado por `/login` en Flask. Cerrar. |
| #2 HU02 - Ver problemas | Done | tipo: historia, modulo: backend, prioridad: alta, estado: implementado | Implementado por `/problemas` y detalle por id. Cerrar. |
| #3 HU03 - Ejecutar codigo | Done | tipo: historia, modulo: backend, modulo: qa, prioridad: alta, estado: implementado | Implementado por `/enviar`, validacion sintactica y ejecucion Python/simulacion Java/C++. Cerrar. |
| #4 HU04 - Casos de prueba | Done | tipo: historia, modulo: qa, prioridad: alta, estado: implementado | Los problemas incluyen `test_cases` y validacion por salida esperada. Cerrar. |
| #7 HU01 - Inicializacion del proyecto | Done | tipo: tecnica, prioridad: alta, estado: implementado | Ya cerrado. Mantener. |
| #8 HU02 - Configuracion basica del entorno | Done | tipo: tecnica, prioridad: alta, estado: implementado | Ya cerrado. Mantener. |
| #9 HU03 - Definicion de estructura del proyecto | Done | tipo: tecnica, prioridad: alta, estado: implementado | Ya cerrado. Mantener. |
| #10 HU04 - Documentacion tecnica inicial | Done | tipo: tecnica, modulo: documentacion, prioridad: media, estado: implementado | Ya cerrado. Mantener. |
| #11 HU05 - Creacion de rutas base del sistema | Done | tipo: tecnica, modulo: backend, prioridad: alta, estado: implementado | Ya cerrado. Mantener. |
| #12 HU06 - Configuracion de endpoints en routes.py | Done | tipo: tecnica, modulo: backend, prioridad: alta, estado: implementado | El archivo `routes.py` contiene endpoints principales. Cerrar. |
| #13 HU07 - Integracion inicial del backend | Done | tipo: tecnica, modulo: backend, prioridad: alta, estado: implementado | Flask Blueprint, DB y rutas conectadas. Cerrar. |
| #14 HU08 - Implementacion de logica de negocio | Done | tipo: tecnica, modulo: backend, prioridad: alta, estado: implementado | Incluye autenticacion, admin, validacion y envio. Cerrar. |
| #15 HU09 - Definicion de modelos de datos en codigo | Done | tipo: tecnica, modulo: db, prioridad: alta, estado: implementado | Tablas `usuarios`, `problemas`, `eventos`. Cerrar. |
| #16 HU10 - Conexion con base de datos | Done | tipo: tecnica, modulo: db, prioridad: alta, estado: implementado | `get_db()` e inicializacion SQLite presentes. Cerrar. |
| #17 HU11 - Registro de usuarios | Done | tipo: historia, modulo: backend, prioridad: alta, estado: implementado | Implementado por `/registro`. Cerrar. |
| #18 HU12 - Login de usuarios | Done | tipo: historia, modulo: backend, prioridad: alta, estado: implementado | Duplicado funcional de #1; cerrar referenciando #1. |
| #19 HU13 - Gestion de problemas | Done | tipo: historia, modulo: backend, prioridad: alta, estado: implementado | Listado, detalle y creacion admin disponibles. Cerrar. |
| #20 HU14 - Envio de soluciones | Done | tipo: historia, modulo: backend, modulo: qa, prioridad: alta, estado: implementado | Implementado por `/enviar`. Cerrar. |
| #21 HU15 - Ranking de usuarios | Backlog | tipo: mejora, modulo: frontend, modulo: backend, prioridad: media, estado: futuro | Hay contadores de correctos/incorrectos, pero falta ranking formal. Mantener abierto. |
| #22 HU16 - Historial de envios | Done | tipo: historia, modulo: backend, prioridad: media, estado: implementado | Implementado por `/historial`. Cerrar. |
| #23 HU17 - Sistema de logros | Backlog | tipo: mejora, prioridad: baja, estado: futuro | No se evidencia sistema de logros completo. Mantener abierto. |

## Comentario profesional de cierre para issues implementados

Usar este formato en cada issue que se cierre:

```md
Implementado y verificado para la entrega v2.

Evidencia tecnica:
- Endpoint/ruta relacionado: `...`
- Modulo revisado: `src/app/routes.py` / `src/app/db.py` / `index.html`
- Criterio funcional cubierto: ...

Resultado:
- La historia cumple el flujo esperado dentro de AlgoArena.
- Se deja cerrada para reflejar correctamente el avance del tablero Kanban.
```

## Comentarios especificos sugeridos

### #1 y #18 Login

```md
Implementado y verificado para la entrega v2.

Evidencia tecnica:
- Endpoint relacionado: `POST /login`
- Modulo revisado: `src/app/routes.py`
- Se valida usuario y contrasena contra SQLite.
- Se retorna informacion basica del usuario, rol y estadisticas.

Resultado:
- El flujo de autenticacion queda cubierto.
- Esta HU se cierra para que el tablero refleje el avance real.
```

### #2 Ver problemas

```md
Implementado y verificado para la entrega v2.

Evidencia tecnica:
- Endpoint de listado: `GET /problemas`
- Endpoint de detalle: `GET /problemas/<id>`
- Modulo revisado: `src/app/routes.py`
- La base inicial carga problemas con dificultad, categoria, descripcion, plantillas y casos de prueba.

Resultado:
- El catalogo de problemas queda disponible para el usuario.
- Se cierra la historia como completada.
```

### #3, #4 y #20 Ejecucion, casos de prueba y envio

```md
Implementado y verificado para la entrega v2.

Evidencia tecnica:
- Endpoint relacionado: `POST /enviar`
- Funciones revisadas: `validar_sintaxis`, `ejecutar_codigo`, `_ejecutar_python`
- Los casos de prueba se leen desde la definicion del problema.
- El resultado compara salida obtenida contra salida esperada.

Resultado:
- El usuario puede enviar soluciones y recibir retroalimentacion.
- La HU se cierra porque el flujo principal de evaluacion esta operativo.
```

### #12 a #16 Backend, rutas, logica y DB

```md
Implementado y verificado para la entrega v2.

Evidencia tecnica:
- Rutas principales definidas en `src/app/routes.py`.
- Persistencia configurada en `src/app/db.py`.
- Tablas disponibles: `usuarios`, `problemas`, `eventos`.
- Seed inicial de problemas y usuario administrador.

Resultado:
- La base tecnica del sistema esta integrada.
- Se cierra la tarea para mantener el tablero actualizado.
```

### #21 Ranking

```md
Se mantiene abierto como mejora futura.

Observacion:
- La base de datos ya guarda contadores `correctos` e `incorrectos` por usuario.
- Falta exponer una vista o endpoint formal de ranking ordenado por desempeno.

Siguiente paso sugerido:
- Crear endpoint `GET /ranking`.
- Agregar vista en frontend con posicion, usuario, correctos, incorrectos y porcentaje de acierto.
```

### #23 Logros

```md
Se mantiene abierto como mejora futura.

Observacion:
- No se evidencia aun un modulo completo de logros, insignias o recompensas.

Siguiente paso sugerido:
- Definir reglas de logros.
- Crear tabla `logros` o estructura equivalente.
- Mostrar insignias en el perfil o panel del usuario.
```

## Vista final esperada del Kanban

Backlog:

- #21 HU15 - Ranking de usuarios
- #23 HU17 - Sistema de logros

Ready:

- Mejoras futuras que el equipo agregue despues de la entrega v2.

In progress:

- Vacio si la entrega actual ya finalizo.

Review / QA:

- PR #5 Perlaza.branch
- PR #6 docs: agrega comentario para prueba de code review

Done:

- #1, #2, #3, #4, #7, #8, #9, #10, #11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #22

## Recomendacion visual para que se vea profesional

- Cerrar lo implementado con comentario tecnico, no solo cerrar.
- Dejar abiertos solo los pendientes reales.
- Agregar labels por tipo, modulo, prioridad y estado.
- Crear milestone `Entrega v2 - MVP funcional`.
- Asociar todos los issues cerrados al milestone.
- Mover PRs abiertas a `Review / QA`.
- En el README o descripcion del Project, explicar que el tablero refleja el estado de la entrega v2.
