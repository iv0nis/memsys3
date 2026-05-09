# FEATURE-013: Prompt `@logdone` para enforcement de cierre de items

**Estado:** Propuesto
**Prioridad:** Baja
**Tipo:** Feature (post-v1.0)
**Plazo:** Largo plazo (post-v1.0, cuando memsys3 escale a usuarios externos)
**Fecha identificación:** 2026-05-09
**Sesión origen:** 2026-05-09 (meta-orquestador BLUEPRINT-001 Frente 8)

---

## Problema / Necesidad

La convención actual (Frente 8 v1.0): items de backlog completados se mueven a `memsys3/backlog/archive/` con `Estado: Completado` + `Fecha cierre`. El paso 2.8 de `endSession.md` automatiza la detección y archivado.

Esto funciona bien con:
- Single maintainer (dogfooting de memsys3 mismo)
- Agentes IA controlados por el maintainer

**Pero a escala**: cuando memsys3 lo usen agentes IA de terceros, distintos hábitos producirán inconsistencia:
- Un día `Estado: Completado`, otro `[DONE]`, otro nada
- A veces se actualiza fecha cierre, a veces no
- A veces se hace `git mv`, otras `mv` (perdiendo blame)
- A veces queda en `backlog/`, otras en `archive/`

**Anti-CDC operacional**: el principio "olvidan que olvidan" (PRINCIPLES.md #1 corolario) garantiza que la disciplina humana/IA falla con suficiente escala. La convención escrita en README requiere lectura + interpretación + memoria. Un prompt es ejecutable directamente.

## Propuesta / Opciones

### Diseño nivel 2 (intent + bash POSIX + verificación literal)

Validado en sesión 2026-05-09. Estructura:

```markdown
# @logdone PREFIJO-NNN

Marcar item de backlog como completado:
1. Actualizar Estado del archivo
2. Mover a backlog/archive/ via git mv
3. Verificar literal el resultado

[bash POSIX agnóstico de SO como referencia]

Si el entorno difiere (ej. macOS sin GNU sed), adáptate manteniendo idempotencia.

Verificación literal final:
- test -f memsys3/backlog/archive/PREFIJO-NNN-*.md
- grep -q "Estado:.*Completado" memsys3/backlog/archive/PREFIJO-NNN-*.md
```

### Por qué nivel 2 (no 1 ni 3)

- **Nivel 1 (bash literal puro)**: frágil ante cambios de SO/sintaxis. Maintenance burden.
- **Nivel 3 (intent puro)**: pierde idempotencia, riesgo regresión silenciosa.
- **Nivel 2**: bash cubre 90%, agente adapta el 10% restante, verificación literal cierra el bucle.

Análisis completo en `informe_logdone_hibrido.html` (raíz repo, sesión 2026-05-09).

## Decisiones / Acciones

**Diferido a post-v1.0**:
- Hoy (v1.0 dogfooting): convención + paso 2.8 endSession son suficientes. Single maintainer.
- Futuro (cuando aparezcan usuarios externos): evaluar si la inconsistencia observada justifica el prompt.

**Trigger de implementación**: cuando se observe drift de formato en backlogs de proyectos externos que usen memsys3.

**Ubicación destino (cuando se implemente)**:
- `memsys3_templates/prompts/logdone.md` (distribuible)
- `memsys3/prompts/logdone.md` (mirror dogfooting)

**Integración esperada con `endSession.md` paso 2.8**: el paso actual ejecuta directamente `git mv`. Cuando exista `@logdone`, paso 2.8 invocará `@memsys3/prompts/logdone.md PREFIJO-NNN` por cada item, en vez de hacer la operación inline. Centraliza el formato.

## Referencias

- **Origen**: propuesta de Viki (contributor) compartida 2026-05-08
- **Análisis**: informe_logdone_hibrido.html + informe_logdone_hibrido_resumen.html (raíz repo)
- **Convención actual (v1.0)**: `memsys3/backlog/README.md` sección "Completar Items" + `memsys3/prompts/endSession.md` paso 2.8
- **Principio motivador**: PRINCIPLES.md #1 corolario meta-amnesia ("olvidan que olvidan")
- **Items relacionados**: EXPLORATION-004 (canonización proactiva — paso 2.7 endSession ya prototipa la idea)

<!-- version: 0.1.0 -->
