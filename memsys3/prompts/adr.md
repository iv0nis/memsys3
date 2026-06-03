# Gestionar Architecture Decision Records (ADRs)

**Contexto:** Los ADRs (`memsys3/memory/full/adr.yaml`) documentan decisiones arquitectónicas del proyecto: qué decidimos, por qué, qué alternativas consideramos y qué impacto tiene.

## 0. Identificar tu memsys3

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
```

**Usa `$MEMSYS3_ROOT` como base para todas las operaciones.**

**Tu tarea:**

## 1. Consultar ADRs

Si el usuario quiere ver el estado de las ADRs:
1. Lee `memsys3/memory/full/adr.yaml`
2. Lee `memsys3/memory/templates/adr-template.yaml` para entender la estructura
3. Muestra: ID, título, área, estado, fecha de cada ADR
4. Opcional: filtrar por área o estado si el usuario lo pide

## 2. Crear Nuevo ADR

Si el usuario quiere crear un ADR:
1. Lee `memsys3/memory/templates/adr-template.yaml` para entender la estructura completa
2. Verifica el último ID numérico usado en `adr.yaml`
3. Crea la nueva ADR con el siguiente ID secuencial
4. Incluye todas las secciones:
   - **id**: Número secuencial (001, 002, ...)
   - **titulo**: Descripción clara de la decisión
   - **data**: Fecha formato YYYY-MM-DD
   - **estado**: Estado actual (ver leyenda abajo)
   - **area**: Área afectada (ver leyenda abajo)
   - **context**: Contexto y problema que motivó la decisión
   - **decision**: Qué se decidió hacer
   - **alternatives**: Alternativas consideradas (nombre, pros, contras, por qué descartada)
   - **consequencies**: Consecuencias positivas, negativas e impacto
   - **notes**: Información adicional (opcional)
5. Añade al final de `adr.yaml` (NO borres ADRs antiguas)
6. Actualiza el índice al final del archivo

## 3. Actualizar un ADR existente

**Principio de inmutabilidad (convención Nygard, ADR-029).** Un ADR aceptado es un registro histórico: captura *por qué* decidimos algo *en su momento*. Por eso `id`, `titulo`, `data`, `context`, `decision`, `alternatives` son **inmutables** — nunca se editan para borrar, reescribir o contradecir lo decidido. Editarlos destruye la trazabilidad del razonamiento, que es el valor del ADR.

Antes de tocar un ADR aplica el **test del tipo de cambio**: *¿lo que voy a escribir contradice lo que el ADR ya decidió?*

- **NO contradice (refinamiento aditivo)** → patrón `update_YYYY_MM_DD`. Para aclarar, registrar impacto real tras implementar, o enlazar trabajo derivado. Añade una **clave fechada** al final del cuerpo del ADR, sin tocar `decision`/`context`:
  ```yaml
  update_2026_06_03: |
    Aclaración o dato nuevo que NO contradice lo decidido.
  ```

- **SÍ contradice (la decisión cambia)** → **ADR nuevo**, nunca editar el viejo. Crea el ADR con el siguiente ID (sección 2); en su cuerpo indica a quién supersede; en el ADR viejo cambia SOLO su `estado` a `superseded_by: "NNN"` apuntando al nuevo. La contradicción vive *entre* ADRs (cadena de supersesión), jamás *dentro* de uno.

Pasos:
1. Lee `memsys3/memory/full/adr.yaml` y localiza la ADR por ID.
2. Aplica el test del tipo de cambio para elegir camino.
3. Cambios in-place permitidos: `estado` (aceptado → deprecated / superseded_by) y `consecuencias` (impacto real tras implementación). Refinamientos textuales → clave `update_YYYY_MM_DD`.
4. NUNCA edites `id`, `titulo`, `data`, `context`, `decision`, `alternatives`.

> Disciplina **única** (dogfooding y proyectos desplegados): el híbrido es superconjunto del Nygard puro. Un proyecto que nunca use `update_` y siempre supersede ya es 100% estricto — el rigor extra es elección local, no una convención distinta.

---

## Leyenda de Estados

- **accepted**: Decisión aceptada y activa
- **deprecated**: Decisión obsoleta, ya no se aplica
- **superseded_by**: Decisión sustituida por otra ADR (especificar ID)

## Leyenda de Áreas

**Técnicas:**
- **arquitectura**: Decisiones de diseño arquitectónico del sistema
- **frontend**: Decisiones sobre tecnología/patrones frontend
- **backend**: Decisiones sobre tecnología/patrones backend
- **infrastructure**: Decisiones sobre despliegue, hosting, CI/CD
- **escalabilidad**: Decisiones sobre cómo escalar el sistema
- **format**: Decisiones sobre formatos de datos (YAML, JSON, etc.)

**Proceso:**
- **workflow**: Decisiones sobre flujo de trabajo del equipo
- **documentación**: Decisiones sobre cómo documentar el proyecto
- **usabilidad**: Decisiones sobre experiencia de usuario/desarrollador
- **process**: Decisiones sobre procesos de desarrollo

Ver `memsys3/memory/templates/adr-template.yaml` para estructura completa y ejemplos.
<!-- version: 0.1.0 -->
