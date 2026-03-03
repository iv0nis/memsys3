# Sessions y ADRs

## Sessions

Cada sesión de trabajo se documenta en `memsys3/memory/full/sessions.yaml`.

### Estructura

```yaml
sessions:
  - id: YYYY-MM-DD-titulo-descriptivo
    data: YYYY-MM-DD
    duracion: ~Xh
    peso: bajo|medio|alto
    titulo: Título conciso
    highlights:
      - Feature implementada
      - Bug resuelto
    features_implementadas:
      - nom: nombre
        descripcio: descripción
    problemas_resueltos:
      - descripción del problema y solución
    decisions_presas:
      - decisio: qué se decidió
        justificacio: por qué
        alternatives: qué se descartó
    gotchas:
      - tipus: error|warning|trap
        problema: descripción
        solucio: cómo resolverlo
        criticitat: alta|media|baja
    proximos_pasos:
      - tarea pendiente
```

### Gotchas

Los gotchas son errores críticos, warnings o traps encontrados durante la sesión. El Context Agent extrae los top 5 más críticos de todas las sesiones y los incluye en `context.yaml` (máx 150 caracteres cada uno).

Solo documentar gotchas que:
- Rompen el sistema si no se conocen
- Son contra-intuitivos
- Tienden a repetirse

### Cuándo documentar

Siempre al final de cada sesión con `@memsys3/prompts/endSession.md`. Nunca usar `Write tool` — sobrescribiría el histórico. Siempre usar `Edit tool` para añadir al principio del array.

---

## ADRs (Architecture Decision Records)

Las decisiones arquitectónicas importantes se registran en `memsys3/memory/full/adr.yaml`.

### Cuándo crear un ADR

**SÍ:**
- Elegir librería/framework en lugar de otro
- Cambiar arquitectura del sistema
- Decidir patrón de diseño
- Cambiar stack tecnológico

**NO:**
- Cambios cosméticos
- Validaciones de formularios
- Bugs menores
- Refactorings de funciones

### Estructura

```yaml
decisiones:
  - id: ADR-001
    titol: Título descriptivo
    data: YYYY-MM-DD
    estat: accepted|deprecated|superseded_by
    area: arquitectura|frontend|backend|infrastructure|workflow|documentación
    context: por qué se necesitaba una decisión
    decisio: qué se decidió
    alternatives:
      - alternativa considerada y por qué se descartó
    consequencies:
      - consecuencias de la decisión
    notes: observaciones adicionales
```

### Estados

- `accepted` — decisión vigente
- `deprecated` — ya no aplica
- `superseded_by: ADR-XXX` — reemplazada por otra ADR

### Project Status

`memsys3/memory/project-status.yaml` documenta el estado actual del proyecto: fase, features operativas, stack, URLs, pendientes prioritarios. Se actualiza al final de cada sesión relevante.
