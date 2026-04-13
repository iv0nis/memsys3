# EXPLORATION-001: Consulta del historial bajo demanda (query.md)

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Exploration
**Plazo:** Medium-term
**Fecha identificación:** 2026-03-27
**Origen:** Análisis comparativo gentle-ai/Engram vs memsys3

---

## Problema / Necesidad

Actualmente memsys3 carga contexto compilado al inicio (newSession) y documenta al final (endSession). No hay mecanismo para consultar el historial completo durante la sesión.

**Situación actual:**
- Si el agente necesita saber "¿qué decidimos sobre autenticación hace 3 sesiones?" debe leer sessions.yaml manualmente
- El contexto compilado (context.yaml) es un resumen — puede no incluir el detalle específico que se necesita
- No hay forma estructurada de buscar en ADRs, sessions, reuniones por tema

**Inspiración:**
Engram (gentle-ai) ofrece `mem_search("tema")` que devuelve solo resultados relevantes sin cargar todo el historial. El concepto de "progressive disclosure" (buscar antes de cargar todo) es valioso, aunque la implementación vía MCP/SQLite es innecesariamente compleja para memsys3.

**Oportunidad:**
Un prompt `query.md` que permita al agente (o al usuario) buscar en el historial completo por tema, sin necesidad de infraestructura adicional — solo leyendo archivos YAML/Markdown con criterio.

---

## Propuesta / Opciones

### Opción A: Prompt query.md con búsqueda por grep + lectura selectiva

```markdown
# Prompt query.md
1. Recibe un tema/pregunta del usuario
2. Grep en sessions.yaml, adr.yaml, reuniones por keywords
3. Lee solo las secciones relevantes
4. Presenta resumen enfocado al tema
```

**Pros:** Cero infraestructura, consistente con filosofía memsys3
**Contras:** Grep puede ser impreciso, depende de keywords

### Opción B: Índice temático en context.yaml

Agregar sección `indice_tematico` en context.yaml con keywords → sesión/ADR mapping.

**Pros:** Búsqueda rápida, compilado por CA con criterio
**Contras:** Más trabajo para CA, índice puede quedar desactualizado

### Opción C: Delegación a subagente de búsqueda

El Main Agent lanza un subagente con la pregunta, el subagente lee el historial completo y devuelve solo la respuesta.

**Pros:** No contamina contexto del Main Agent, lectura exhaustiva
**Contras:** Coste de tokens del subagente, latencia

---

## Preguntas Abiertas

1. ¿Con qué frecuencia se necesita consultar historial durante una sesión? ¿Es un problema real o teórico?
2. ¿Opción A (simple) es suficiente o necesitamos algo más sofisticado?
3. ¿Debería el Main Agent poder invocar query.md él mismo, o solo el usuario?

---

## Referencias

- **Análisis comparativo:** gentle-ai/Engram (progressive disclosure, mem_search)
- **ADR relacionado:** ADR-001 (criterio inteligente CA)
- **Feature relacionada:** FEATURE-005 (optimizar ventana de contexto)
- **Filosofía memsys3:** Archivos planos, cero infraestructura, agnóstico de modelo
