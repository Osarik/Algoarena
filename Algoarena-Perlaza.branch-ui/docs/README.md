# AlgoArena - Plataforma de Retos de Programacion

Plataforma inspirada en LeetCode que permite a los estudiantes resolver problemas de programacion, ejecutar codigo en tiempo real y validar soluciones mediante casos de prueba automatizados.

---

## Integrantes

| Nombre | Rol |
|---|---|
| Juan Pablo Perlaza Navarro | Desarrollador Backend y mejora de experiencia visual |
| Juan Felipe Vergara | Desarrollador Backend |
| Brayan Stiven Agudelo Quintero | Desarrollador Backend |

---

## De que va este proyecto

AlgoArena es un sistema web donde los estudiantes pueden:

- Explorar un catalogo de problemas de programacion por dificultad.
- Escribir y ejecutar codigo directamente en el navegador.
- Recibir retroalimentacion inmediata con casos de prueba.
- Llevar un registro de sus soluciones.

**Stack principal:** Python, Flask y SQLite.

---

## Aporte visual en `Perlaza.branch`

La rama `Perlaza.branch` incorpora una portada profesional para la aplicacion Flask, estilos responsivos y una ruta `/health` para conservar una verificacion tecnica rapida del servicio.

Cambios destacados:

- Interfaz inicial con secciones de propuesta, flujo, metricas y contribucion.
- Hoja de estilos dedicada en `src/app/static/css/styles.css`.
- Plantilla HTML en `src/app/templates/index.html`.
- Endpoint `/health` para validar disponibilidad de la API.

---

## Estructura del proyecto

![diagrama c1](https://github.com/user-attachments/assets/cd9547b5-a99c-4f33-a004-150d6befc537)

<img width="1534" height="771" alt="diagrama c2" src="https://github.com/user-attachments/assets/ddd8ce42-f9f6-492a-a1f2-3fb97b7d0af1" />

---

## Alcance

Incluye:

- Backend en Flask.
- Gestion de problemas.
- Ejecucion de codigo.
- Casos de prueba.
- Presentacion visual inicial de la plataforma.
