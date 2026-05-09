# Gestionar Backlog del Proyecto

**Contexto:** El backlog (`memsys3/backlog/`) organiza trabajo futuro del proyecto (issues, features, specs, blueprints, mejoras, exploraciones).

## 0. Identificar tu memsys3 y verificar backlog

```bash
MEMSYS3_ROOT="$(pwd)/memsys3"
if [ -f "$MEMSYS3_ROOT/memory/project-status.yaml" ]; then
  echo "✅ memsys3 encontrado: $MEMSYS3_ROOT"
else
  echo "⚠️ memsys3/ no encontrado en $(pwd)"
  CANDIDATES=$(find . -maxdepth 4 -path "*/memsys3/memory/project-status.yaml" 2>/dev/null | sed 's|/memory/project-status.yaml$||')
  COUNT=$(echo "$CANDIDATES" | grep -c . 2>/dev/null || echo 0)
  if [ "$COUNT" -eq 1 ]; then
    MEMSYS3_ROOT="$(cd "$CANDIDATES" && pwd)"
    echo "✅ memsys3 encontrado (único): $MEMSYS3_ROOT"
  elif [ "$COUNT" -gt 1 ]; then
    echo "⚠️ Múltiples memsys3 encontrados:"
    echo "$CANDIDATES"
    echo "Pregunta al usuario cuál usar."
  else
    echo "❌ No se encontró ningún memsys3."
  fi
fi

ls "$MEMSYS3_ROOT/backlog/README.md" 2>/dev/null && echo "OK: backlog existe" || echo "NO EXISTE: backlog"
```

Si no existe, créalo antes de continuar:

```bash
mkdir -p memsys3/backlog
```

Luego crea `memsys3/backlog/README.md` copiando el contenido de `memsys3_update_temp/memsys3_templates/backlog/README.md` si está disponible, o bien crea uno mínimo con esta estructura:

```markdown
# Backlog del Proyecto

## Códigos
- **ISSUE-XXX**: Problemas técnicos, bugs, tech debt
- **FEATURE-XXX**: Nueva funcionalidad
- **IMPROVEMENT-XXX**: Mejora de funcionalidad existente
- **SPEC-XXX**: Especificación técnica detallada
- **BLUEPRINT-XXX**: Diseño arquitectónico alto nivel
- **EXPLORATION-XXX**: Investigación sin solución clara

## Estados
Propuesto → Abierto → En Progreso → Completado / Cancelado / Rechazado / Bloqueado
```

**Tu tarea:**

## 1. Consultar Backlog
Si el usuario quiere ver el estado del backlog:
1. Lee `memsys3/backlog/README.md` para entender el sistema
2. Lista los ítems pendientes en `memsys3/backlog/` (excluye README.md, archive/, docs/)
3. Si el usuario pide "todos" o "incluye archivados", lista también `memsys3/backlog/archive/`
4. Muestra: prefijo, título, estado, prioridad de cada ítem

## 2. Crear Nuevo Item
Si el usuario quiere crear un item:
1. Pregunta qué tipo de item quiere crear (usa la leyenda abajo)
2. Lee `memsys3/backlog/README.md` para entender estructura de documentos
3. **Verifica numeración existente del prefijo escaneando AMBAS carpetas:**
   ```bash
   ls memsys3/backlog/[PREFIJO]-*.md memsys3/backlog/archive/[PREFIJO]-*.md 2>/dev/null \
     | grep -oE '[A-Z]+-[0-9]+' | sort -u | tail -3
   ```
   Esto garantiza numeración monótona ininterrumpida (items archivados cuentan).
4. Crea el archivo `memsys3/backlog/[PREFIJO]-[NUMERO]-[nombre].md` con estructura correcta
5. Incluye: Estado, Prioridad, Tipo, Plazo, Fecha, Problema/Propuesta, Referencias

## 3. Actualizar Item Existente
Si el usuario quiere actualizar un item:
1. Lee el archivo del item
2. Actualiza el campo correspondiente (Estado, Prioridad, etc.)
3. Agrega información en la sección apropiada

## 4. Documentar Item con Informe / Plan (ADR-021)

Si el usuario quiere añadir documentación extendida a un item (típicamente un BLUEPRINT, FEATURE grande o item que se delegará a otra sesión):

1. Pregunta qué quiere generar: `informe`, `plan`, o ambos
2. Verifica que existe `memsys3/backlog/docs/` (créalo si no: `mkdir -p memsys3/backlog/docs`)
3. Lee el item original y los templates relevantes:
   - `memsys3/memory/templates/informe-template.md`
   - `memsys3/memory/templates/plan-template.md`
4. Crea el / los archivo/s:
   - `memsys3/backlog/docs/informe_PREFIJO-NNN.md`
   - `memsys3/backlog/docs/plan_PREFIJO-NNN.md`
5. Rellena con la información disponible en sesión (contexto, hallazgos, decisiones). NO inventes — si no hay info, marca con `[PENDIENTE]` y notifica al usuario.
6. **Actualiza el item original**: añade en sección `Referencias`:
   ```
   - **Informe:** `docs/informe_PREFIJO-NNN.md`
   - **Plan:** `docs/plan_PREFIJO-NNN.md`
   ```

**Cuándo recomendar al usuario crear informe/plan:**
- BLUEPRINT-XXX → siempre ambos
- FEATURE/SPEC grande → ambos si se va a delegar ejecución
- ISSUE con causa raíz no obvia → al menos informe
- IMPROVEMENT pequeño, typo fix → no necesita docs

---

## Leyenda de Códigos

- **ISSUE-XXX**: Problemas técnicos, bugs, tech debt
- **FEATURE-XXX**: Nueva funcionalidad a implementar
- **SPEC-XXX**: Especificaciones técnicas detalladas
- **BLUEPRINT-XXX**: Diseño arquitectónico de alto nivel
- **IMPROVEMENT-XXX**: Mejoras de funcionalidad existente
- **EXPLORATION-XXX**: Investigación sin solución clara

Ver `memsys3/backlog/README.md` para workflow completo y estructura de documentos.
<!-- version: 0.2.0 -->
