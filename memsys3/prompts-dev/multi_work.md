# Multi-work — Coordinación entre agentes paralelos

Sistema de **locks explícitos** para evitar conflictos cuando varios agentes trabajan el mismo repositorio en paralelo. Cada agente declara por adelantado qué ficheros escribirá; si otro agente ya los tiene bloqueados, espera.

## Fichero central

`memsys3/blocked_files_log.md` (relativa a la raíz del repo).

Contiene una línea por cada fichero bloqueado actualmente. Formato:

```
- <path-relativo> | <Agent> | <tarea-corta> | <YYYY-MM-DD HH:MM>
```

Ejemplo:

```
- backend/database/migrations/023_facturas_venta.sql | Agent B | F2a SQL | 2026-04-29 14:30
- frontend/src/components/AddLineaOrdenModal.tsx | Agent A | bug cero-izquierda | 2026-04-29 14:25
- backend/database/migrations/ | Agent B | F2a SQL (reserva número) | 2026-04-29 14:30
```

## Reglas

1. **Solo bloquea escrituras.** Lecturas de cualquier fichero siempre permitidas (necesarias para contexto).
2. **Granularidad = fichero.** Excepción: si reservas un número de migración SQL, bloquea también el directorio `backend/database/migrations/` para que ningún otro agente coja el mismo número.
3. **Comprobar solo ficheros que ESCRIBIRÁS** (crear o modificar). No los que solo leerás.
4. **Conflicto parcial = pausa total.** Si cualquier fichero de tu plan está en el log por otro agente, NO inicies el plan. Esperas a que se desbloquee. No hagas "medio plan".
5. **Caducidad:** si una entrada tiene > 4h, NO la quites tú solo. Avisa al usuario ("el lock de X por Agent A es de hace 5h, ¿lo quito?"). Probable que esté caducado, pero confirmación humana primero.

## Flujo de trabajo

### Paso 1 — Pre-plan (después de definir qué hace el plan)

Lee `blocked_files_log.md`. Por cada fichero que tu plan **escribirá**:

- Si NO aparece en el log → OK, continúa.
- Si aparece con TU `agent_id` → OK (continuación de trabajo).
- Si aparece con OTRO agente → **STOP**. Avisa al usuario con la línea conflictiva y espera. No propongas plan alternativo sin confirmación.

### Paso 2 — Post-aprobación plan (justo antes de empezar a escribir)

Append al log una línea por cada fichero del plan. Lee el `agent_id` de `~/.claude/memsys3_agent_id`. Timestamp `YYYY-MM-DD HH:MM` hora local.

### Paso 3 — Durante el trabajo

Trabaja libremente en los ficheros reservados. Puedes leer cualquier otro fichero del repositorio.

### Paso 4 — Post-completado

Después del commit + push (o de todo el flujo completo, incluyendo tag si aplica), elimina **tus líneas** del log. NO toques líneas de otros agentes.

### Paso 5 — Aborted / crash

Si el agente se queda colgado o se cancela, sus líneas quedan en el log. El usuario las edita manualmente cuando haga falta. No hay limpieza automática.

## Formato del log

Cabecera fija en el fichero (no se borra nunca):

```markdown
# Blocked Files Log

Ficheros bloqueados por agentes en paralelo. Ver `memsys3/prompts-dev/multi_work.md`.

Formato: `- <path> | <Agent> | <tarea> | <YYYY-MM-DD HH:MM>`

---

<!-- entries -->
```

Las entries van debajo de `<!-- entries -->`. Al leer, parsea solo líneas que empiezan por `- ` después de este marcador.

## Ejemplos

### Pre-plan OK

Plan: editar `backend/api/foo.py`. Log contiene:
```
- frontend/src/components/Bar.tsx | Agent A | feature X | 2026-04-29 14:00
```
→ Sin conflicto. Puedes continuar.

### Pre-plan con conflicto

Plan: editar `frontend/src/components/Bar.tsx`. Log contiene la misma línea.
→ STOP. Mensaje al usuario:

> Conflicto: `frontend/src/components/Bar.tsx` está bloqueado por Agent A desde 2026-04-29 14:00 (feature X). Espero a que se desbloquee.

### Caducidad

Log contiene:
```
- backend/api/foo.py | Agent A | refactor | 2026-04-29 09:00
```
Hora actual: 2026-04-29 14:30 (>4h). Plan del nuevo agente quiere tocar `foo.py`.
→ Mensaje al usuario:

> El lock de `backend/api/foo.py` por Agent A es de hace 5h 30min (>4h). Probablemente caducado. ¿Lo quito del log para continuar?

Espera respuesta. Si OK, edita el log eliminando la línea, después añade la tuya.
