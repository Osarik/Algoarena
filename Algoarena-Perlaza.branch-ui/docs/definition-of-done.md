# Definition of Done — AlgoArena

**Proyecto:** AlgoArena  
**Equipo:** Juan Pablo Perlaza Navarro · Juan Felipe Vergara

---

## ¿Qué significa que una tarea está "Done"?

Una historia de usuario o tarea se considera completada cuando cumple **todos** los criterios siguientes:

---

## Criterios

### Código
- [ ] El código fue escrito y funciona sin errores en ejecución local
- [ ] El código sigue las convenciones del proyecto (nombres, estructura de carpetas)
- [ ] No hay código comentado innecesario ni archivos de prueba olvidados

### Revisión
- [ ] Se creó un Pull Request hacia `main`
- [ ] Al menos un integrante del equipo revisó y aprobó el PR
- [ ] Los comentarios del revisor fueron atendidos antes del merge

### Pruebas
- [ ] Se escribieron pruebas unitarias para la funcionalidad nueva
- [ ] Todas las pruebas existentes pasan sin errores (`pytest`)

### Documentación
- [ ] El README está actualizado si la funcionalidad afecta el setup
- [ ] La Wiki refleja cambios en arquitectura o flujos si aplica
- [ ] Los diagramas C1/C2/C3 están actualizados si hubo cambios estructurales

### Integración
- [ ] El código fue integrado a `main` mediante PR aprobado
- [ ] No hay conflictos pendientes después del merge

---

## Lo que NO cuenta como Done

- Código que solo funciona en la máquina de quien lo hizo
- PR sin revisión del compañero
- Funcionalidad sin prueba alguna
- Cambios pusheados directamente a `main`
