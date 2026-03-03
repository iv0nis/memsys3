# ISSUE-012: Resumen TL;DR automático al final de reuniones

**Estado:** Completado
**Prioridad:** Media
**Tipo:** Mejora / UX
**Fecha identificación:** 2026-02-20

---

## Problema / Necesidad

Al finalizar una reunión entre agentes, el moderador tiene que pedir manualmente un resumen de lo que se acordó. No hay ningún paso obligatorio en el protocolo que genere automáticamente un TL;DR al cerrar.

## Comportamiento esperado

Al escribir `CIERRE` o al cerrar la reunión, el agente genera automáticamente un bloque TL;DR en el chat con:
- Qué se decidió
- Qué queda pendiente
- Quién tiene el próximo paso

## Propuesta

Añadir en `meet.md` (Protocolo común, sección CIERRE) la instrucción:

> Tras escribir CIERRE, envía al moderador en el chat:
> ```
> TL;DR: [1-2 líneas de qué se acordó]
> Pendiente: [próximo paso + responsable]
> ```

## Referencias

- Detectado en sesión 200226 tras reuniones 200226_2 al 200226_5
- Relacionado con `meet.md` (Protocolo común)
