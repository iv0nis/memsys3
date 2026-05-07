# ISSUE-024: ADRs 010 y 011 ausentes — investigar si fueron descartadas o nunca creadas

**Estado:** Abierto
**Prioridad:** Baja
**Tipo:** Issue (deuda histórica / meta)
**Plazo:** Sin urgencia (no bloquea release v1.0)
**Fecha identificación:** 2026-05-07
**Origen:** Auditoría BLUEPRINT-001 Frente 2 — meta-finding al verificar conteo real de ADRs.

---

## Problema

El índice de `memsys3/memory/full/adr.yaml` lista 20 ADRs aceptadas: 001-009 + 012-022. Los IDs **010 y 011 no existen** en ningún archivo del repo:

- No están en `adr.yaml` (índice ni cuerpo).
- No existe `adr_1.yaml` (no ha habido rotación).
- No están en `sessions*.yaml`.
- No hay registro histórico que explique el skip.

Mientras tanto, `BLUEPRINT-001-release-memsys3-v1.md` mencionaba "21 ADRs aceptadas" e `informe_BLUEPRINT-001.md` "22" — proyecciones erróneas. Conteo real: **20 ADRs**.

## Hipótesis

1. **Numeración reservada y no usada**: alguien planificó dos ADRs que nunca llegaron a draft.
2. **Drafts descartados**: existieron como WIP y fueron eliminados antes de aceptar.
3. **Renumeración silenciosa**: durante alguna sesión se renumeraron ADRs sin documentar.

`git log` selectivo sobre `adr.yaml` podría revelar el origen, pero no es prioritario.

## Acción propuesta

- (Opcional) `git log --follow --all memsys3/memory/full/adr.yaml | grep -i "010\|011"` para buscar pistas.
- Decidir: **(a)** dejar el gap como está y documentarlo en `PRINCIPLES.md` o `adr.yaml` notes; **(b)** renumerar 012-022 → 010-020 (breaking change, no recomendado); **(c)** reservar 010-011 como "RESERVED — see ISSUE-024" en el índice.

Recomendación: opción **(a)** — la numeración no garantiza secuencialidad y renumerar rompe referencias históricas en sessions.

## Impacto en release v1.0

Ninguno funcional. El blueprint mencionaba un conteo incorrecto que ya está corregido en `informe_BLUEPRINT-001-auditoria.md`. Este ISSUE deja huella histórica de la inconsistencia para futuras revisiones.

## Referencias

- Auditoría: `memsys3/backlog/docs/informe_BLUEPRINT-001-auditoria.md` §6
- BLUEPRINT origen: `memsys3/backlog/BLUEPRINT-001-release-memsys3-v1.md`
