# FEATURE-009: Sistema Operations Log

- **Estado:** En Progreso
- **Prioridad:** Media
- **Tipo:** FEATURE
- **Fecha:** 2026-03-26

## Propuesta

Crear un log de operaciones (`memsys3/memory/full/operations.log`) que registre automáticamente cada ejecución de `actualizar.md` y `compile-context.md`.

## Motivación

- Trazabilidad: saber cuándo se actualizó memsys3, de qué versión a cuál, y qué cambió
- Trazabilidad: saber cuándo se compiló context.yaml y con qué métricas
- Consulta por IA o humano bajo demanda (no se lee en newSession ni compile-context)

## Diseño

### Ubicación
- `memsys3/memory/full/operations.log` — memoria a largo plazo, registro acumulativo

### Formato YAML (append-only)

**Entrada de actualización:**
```yaml
- timestamp: "2026-03-25T20:40:35"
  operacion: "actualizar"
  version_origen: "v0.12.0"
  version_destino: "v0.19.0"
  resultado: "ok"
  resumen:
    nuevos: "6 archivos (agent-identity, git, meet, migrate, reference, IMPROVEMENT-008)"
    actualizados: "8 archivos (prompts del sistema + context-agent + templates + viz)"
    eliminados: "2 archivos (meet-coord/meet-research → consolidados a meet.md)"
    merge_manual: "newSession.md (añadida detección auto + conservado contexto)"
    preservados: "main-agent.yaml (personalizado)"
    backup: "memsys3/docs/backups/memsys3_backup_20260325_204035"
    pendientes_validacion:
      - "Ejecutar compile-context.md para verificar compatibilidad"
      - "Probar newSession.md en nueva instancia"
```

**Entrada de compilación:**
```yaml
- timestamp: "2026-03-25T21:00:00"
  operacion: "compilar"
  version_context: "v0.12.0"
  resultado: "ok"
  resumen:
    lineas: 390
    adrs_incluidas: "10 de 14"
    sesiones_incluidas: "11 (8 alto, 3 medio)"
    gotchas: "5 críticos"
    reduccion_tokens: "78%"
```

### Rotación
- Estilo sessions: cuando >= 1800 líneas, rotar a `operations_N.log`
- Archivos rotados se pueden borrar libremente (no hay archivado ni history)

### Quién escribe
- `actualizar.md`: paso final tras completar actualización
- `compile-context.md`: paso final tras compilar context.yaml

### Quién NO lo lee
- `newSession.md`: NO
- `compile-context.md`: NO (solo escribe, no lee)
- Solo consulta bajo demanda (humano o IA)

## Referencias

- Rotación inspirada en sessions.yaml (ADR-002)
- Ubicación en memory/full/ (memoria a largo plazo)
