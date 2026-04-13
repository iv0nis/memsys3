# FEATURE-012: Glosario de conceptos

**Estado:** Propuesto
**Prioridad:** Media-Alta
**Tipo:** Feature
**Plazo:** Short-term
**Fecha identificación:** 2026-03-27
**Origen:** Reunión 20260327_1 (Agent A memsys3 + Agent B gitkigai)

---

## Problema / Necesidad

El usuario dice "¿recuerdas [concepto]?" y no hay forma de encontrarlo. El concepto puede estar enterrado en una sesión, un ADR, un archivo, una reunión. No existe un índice.

El contexto compilado (context.yaml) es un resumen que puede no incluir el detalle específico. Buscar en el historial completo requiere leer múltiples archivos sin saber dónde mirar.

---

## Propuesta (acordada en meet 20260327_1)

### Ubicación

`memsys3/memory/full/glosario.yaml` — al lado de sessions.yaml y adr.yaml.

### Formato

Punteros simples, sin explicación inline. El concepto se explica en su referencia, no en el glosario. Orden alfabético.

```yaml
conceptos:
  - nombre: "Estructura de dos capas"
    ref: "memsys3/docs/parcelas/"
    sesion: "2026-01-14"

  - nombre: "Progressive disclosure"
    ref: "memsys3/docs/meets/20260327_1.md"
    sesion: "2026-03-27"
```

### Quién lo lee

**Bajo demanda por el Main Agent.** Cuando el usuario pregunta por un concepto, el agente busca en glosario.yaml por orden alfabético y sigue la referencia.

**NO lo lee el Context Agent.** No se carga en context.yaml ni en newSession. Es un índice de lookup, no contexto de arranque.

### Quién lo mantiene

**Híbrido (Opción C):** Paso final de endSession:
1. El agente documenta la sesión normalmente (pasos actuales)
2. **Nuevo paso final:** revisa lo documentado → detecta conceptos nuevos → AskUserQuestion: "¿Añadir estos conceptos al glosario? [lista]" → usuario confirma/descarta
3. Conceptos confirmados se añaden a glosario.yaml en orden alfabético

### Alcance

Feature agnóstica — útil en cualquier proyecto con memsys3, no específica de gitkigai.

---

## Implementación

1. **Crear template** `memsys3_templates/memory/full/glosario.yaml` (vacío, con estructura base)
2. **Crear template** `memsys3_templates/memory/templates/glosario-template.yaml` (guía permanente)
3. **Modificar endSession.md** — agregar paso final para propuesta de conceptos nuevos
4. **Modificar main-agent.yaml** — instruir que ante "¿recuerdas X?" busque en glosario.yaml
5. **Sincronizar con memsys3/** (dog-fooding)

---

## Relación con otros items

- **EXPLORATION-001** (consulta bajo demanda): glosario es índice rápido; EXPLORATION-001 es búsqueda profunda cuando el glosario no tiene la respuesta
- **FEATURE-011** (Main Agent proactivo): el agente podría sugerir consultar el glosario cuando detecta referencia a conceptos previos
- **FEATURE-010** (checkpoint mid-session): conceptos descubiertos mid-session podrían proponerse en el checkpoint

---

## Referencias

- **Reunión:** memsys3/docs/meets/20260327_1.md
- **Inspiración:** Engram mem_search (progressive disclosure), análisis comparativo gentle-ai
