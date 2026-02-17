# ISSUE-010: Agentes no actualizan estado del backlog al completar tareas

**Estado**: Abierto
**Prioridad**: Media
**Tipo**: Bug / UX
**Plazo**: Corto plazo
**Fecha creación**: 2026-02-17

---

## Problema

Cuando un agente implementa un item del backlog, el archivo `.md` del item permanece con `**Estado**: Abierto` indefinidamente. El agente no lo actualiza automáticamente a `Completado`.

Esto provoca que el backlog acumule items resueltos mezclados con pendientes, dificultando saber el estado real del trabajo.

**Ejemplo observado**: ISSUE-009 fue implementado en sesión 2026-02-17 pero su estado permaneció `Abierto` hasta que el usuario lo indicó explícitamente.

---

## Causa Raíz

Los prompts que ejecutan trabajo (endSession.md, backlog.md, los propios flujos de implementación) no incluyen instrucción de cerrar el item de backlog correspondiente una vez completado.

---

## Propuesta de Solución

### Opción A: Instrucción en endSession.md (RECOMENDADO)

Agregar sección en PASO 4 de endSession.md:

```markdown
**D. Cerrar items de backlog completados:**

Si durante esta sesión se ha implementado algún item del backlog:
1. Leer el archivo `memsys3/backlog/[ITEM].md`
2. Cambiar `**Estado**: Abierto` → `**Estado**: Completado`
3. Añadir `**Fecha completado**: YYYY-MM-DD`
```

### Opción B: Instrucción en backlog.md (operación "actualizar")

La operación `actualizar` de backlog.md ya existe pero no se invoca automáticamente al final de una implementación. Añadir recordatorio explícito.

### Opción C: Checkpoint en compile-context.md

El Context Agent detecta items implementados (cruzando sessions.yaml con backlog/) y alerta si hay items con estado desactualizado.

---

## Recomendación

**Opción A**: Mínimo cambio, máximo impacto. endSession.md es el punto natural donde el agente reflexiona sobre lo que ha hecho.

---

## Referencias

- Prompt afectado: `memsys3/prompts/endSession.md` (PASO 4)
- Prompt relacionado: `memsys3/prompts/backlog.md`
- Ejemplo: ISSUE-009 completado 2026-02-17 sin actualizar estado automáticamente
