# Backlog - Sistema de Gestión de Trabajo Futuro

Este directorio contiene **trabajo futuro pendiente**: issues identificados, features propuestas, especificaciones técnicas, blueprints arquitectónicos y exploraciones.

---

## 📋 Sistema de Códigos

Cada documento usa un prefijo para identificar su tipo:

### `ISSUE-XXX`
**Problemas técnicos, bugs, tech debt**

- Problema identificado que frena o limita el sistema
- Requiere solución pero no es bloqueante inmediato
- Puede incluir análisis de opciones

**Ejemplo:** `ISSUE-001-error-carga-datos.md`

### `FEATURE-XXX`
**Nueva funcionalidad a implementar**

- Capacidad nueva que el sistema no tiene
- Describe qué se quiere lograr y por qué
- Puede incluir diseño preliminar

**Ejemplo:** `FEATURE-001-exportar-resultados-csv.md`

### `SPEC-XXX`
**Especificación técnica detallada**

- Documento técnico de cómo implementar algo específico
- Incluye API, estructura de datos, flujos
- Más detallado que un issue o feature

**Ejemplo:** `SPEC-001-estructura-datos-ejercicios.md`

### `BLUEPRINT-XXX`
**Diseño arquitectónico de alto nivel**

- Cambios significativos en arquitectura del sistema
- Decisiones de diseño con múltiples componentes
- Suele generar múltiples ADRs después

**Ejemplo:** `BLUEPRINT-001-sistema-validacion-automatica.md`

### `IMPROVEMENT-XXX`
**Mejora de funcionalidad existente**

- No es bug ni feature nueva
- Optimización, UX, performance de algo que ya existe
- Cambio incremental

**Ejemplo:** `IMPROVEMENT-001-optimizar-tiempo-ejecucion.md`

### `EXPLORATION-XXX`
**Investigación sin solución clara**

- Problema identificado sin solución obvia
- Requiere investigación, pruebas, experimentación
- Puede resultar en un SPEC o BLUEPRINT después

**Ejemplo:** `EXPLORATION-001-alternativas-visualizacion.md`

---

## 🔄 Workflow

### 1. Identificar Trabajo Futuro

Cuando surge un problema, idea o necesidad:
1. Crear documento con prefijo apropiado
2. Numerar secuencialmente por tipo (ISSUE-001, ISSUE-002, etc.)
3. Describir claramente el problema/necesidad
4. Estado inicial: **Abierto** o **Propuesto**

### 2. Trabajar en Items

Cuando decides trabajar en un item:
1. Cambiar estado a **En Progreso**
2. Documentar trabajo en sessions.yaml
3. Crear ADRs si hay decisiones arquitectónicas

### 3. Completar Items

Cuando el trabajo está completo:
1. Cambiar estado a **Completado** dentro del archivo + fecha de cierre
2. Agregar referencia a commits/PRs
3. **Mover a `backlog/archive/`** vía `git mv` (preserva blame)
4. Items completados sirven como documentación de decisiones

**Por qué archivar**: `ls memsys3/backlog/` muestra solo pendientes. Visibilidad inmediata sin abrir archivos.

### 4. Cancelar/Rechazar Items

Si decides no implementar algo:
1. Cambiar estado a **Cancelado** o **Rechazado**
2. Documentar por qué (cambio de prioridad, no viable, etc.)
3. **Mover a `backlog/archive/`** (mismo tratamiento que Completado: ya no es trabajo pendiente)

---

## 📊 Estados Posibles

- **Propuesto**: Idea inicial, no confirmada
- **Abierto**: Confirmado, pendiente de trabajar
- **En Progreso**: Trabajo activo
- **Bloqueado**: Dependiente de otra cosa
- **Completado**: Implementado y cerrado
- **Cancelado**: Decidido no implementar
- **Rechazado**: Evaluado y descartado

---

## 📝 Estructura de Documentos

Cada documento debe incluir como mínimo:

```markdown
# [PREFIJO-XXX]: Título

**Estado:** Abierto/En Progreso/Completado/etc.
**Prioridad:** Alta/Media/Baja
**Tipo:** [Según prefijo]
**Plazo:** Corto/Medio/Largo plazo
**Fecha identificación:** YYYY-MM-DD

---

## Problema / Necesidad

[Descripción clara del qué y por qué]

## Propuesta / Opciones

[Posibles aproximaciones, análisis]

## Decisiones / Acciones

[Qué se decidió hacer o pasos siguientes]

## Referencias

- [Commits, ADRs, sesiones relacionadas]
- **Informe:** `docs/informe_PREFIJO-XXX.md` (si existe)
- **Plan:** `docs/plan_PREFIJO-XXX.md` (si existe)
```

---

## 📂 Documentación extendida: `docs/` (opcional, ADR-021)

Para items complejos, el item corto puede no dar suficiente contexto a un agente fresco que lo ejecute en otra sesión. Esto se llama **CDC (Casualidad de Contexto)**: cuando la lucidez agéntica depende del azar del contexto de sesión, no de archivos canónicos.

memsys3 combate CDC con dos documentos OPCIONALES por item:

```
backlog/
├── PREFIJO-NNN-titulo.md         ← item: corto, escaneable (~50-150 líneas)
└── docs/
    ├── informe_PREFIJO-NNN.md    ← contexto profundo: por qué, hallazgos
    └── plan_PREFIJO-NNN.md       ← pasos ejecutables: cómo, criterios done
```

### Cuándo crear informe / plan

| Tipo de item | informe | plan |
|---|---|---|
| BLUEPRINT-XXX | **siempre** | **siempre** |
| FEATURE/SPEC grande | recomendado | recomendado si se delega ejecución |
| ISSUE con causa raíz no obvia | recomendado | opcional |
| IMPROVEMENT pequeño / typo fix | innecesario | innecesario |
| EXPLORATION | recomendado (es el formato natural) | si deriva en ejecución |

### Templates

- `memsys3/memory/templates/informe-template.md`
- `memsys3/memory/templates/plan-template.md`

### Reglas

- **Link bidireccional**: el item referencia los docs en `Referencias`; los docs referencian el item en su encabezado
- **NO duplicar info**: el item es índice, el informe es contexto, el plan es ejecución
- **Mantener sincronizado**: si el item cambia de alcance, actualiza informe/plan
- **Context Agent**: NO lee `docs/` por defecto en Tier 3 (evita explosión de tokens). Solo si el item está en pendientes prioritarios y los docs aportan info no derivable del item

---

## 🎯 Priorización

Usa estos criterios para asignar prioridades:

- **Alta**: Bloquea trabajo o frena progreso significativamente
- **Media**: Importante pero no urgente, puede esperar
- **Baja**: Nice to have, mejora incremental

---

## 📚 Relación con Otros Documentos

Si estás usando memsys3 o un sistema similar de documentación:

- **ADRs**: Decisiones arquitectónicas TOMADAS
- **Backlog**: Trabajo PENDIENTE de hacer
- **Sessions**: Trabajo REALIZADO
- **Project Status**: Estado ACTUAL

**Flujo:**
```
Backlog (futuro) → Sessions (hacer) → ADRs (decidir) → Project Status (ahora)
```

---

## 🗂️ Organización

- Un archivo por item
- Numeración secuencial por tipo (no global). **Para próximo ID, escanea `backlog/` Y `backlog/archive/`** (numeración monótona ininterrumpida)
- **Items pendientes**: en `backlog/` raíz
- **Items completados/cancelados/rechazados**: en `backlog/archive/`
- README.md (este archivo) documenta el sistema

---

## 💡 Tips

1. **No borres items completados** - son documentación valiosa
2. **Sé específico en títulos** - deben ser descriptivos por sí solos
3. **Actualiza estados** - backlog desactualizado no sirve
4. **Referencia sesiones** - conecta backlog con trabajo real
5. **No sobre-ingenierices** - backlog es herramienta, no burocracia

---

## 📚 Ejemplos Ilustrativos

### Ejemplo de ISSUE

```markdown
# ISSUE-001: Error al validar entrada de usuario en ejercicio 3

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Bug
**Plazo:** Corto plazo
**Fecha identificación:** 2025-11-14

---

## Problema / Necesidad

Al ejecutar el ejercicio 3 de la PEC2, si el usuario introduce un string vacío,
el programa lanza una excepción no controlada en lugar de mostrar un mensaje
de error amigable.

## Propuesta / Opciones

**Opción A:** Agregar validación con try/except antes del procesamiento
**Opción B:** Usar función auxiliar validate_input() reutilizable
**Opción C:** Agregar validación con if/else simple

## Decisiones / Acciones

Pendiente de análisis. Revisar si otros ejercicios tienen el mismo problema.

## Referencias

- Archivo: `Activity_2/ejercicio_3.py`
- Línea: 42
```

### Ejemplo de FEATURE

```markdown
# FEATURE-001: Sistema de tests automatizados para ejercicios

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Feature
**Plazo:** Medio plazo
**Fecha identificación:** 2025-11-14

---

## Problema / Necesidad

Actualmente validamos ejercicios manualmente ejecutando y revisando output.
Sería útil tener tests automatizados que validen las soluciones antes de entregar.

## Propuesta / Opciones

**Opción A:** Usar pytest para cada ejercicio
- Pros: Estándar de la industria, fácil de usar
- Contras: Requiere aprender pytest

**Opción B:** Crear scripts de validación custom
- Pros: Control total, más simple
- Contras: Reinventar la rueda

## Decisiones / Acciones

No decidido aún. Explorar pytest en próxima sesión.

## Referencias

- PEC1, PEC2 completadas sin tests
- Interés en mejorar workflow de validación
```

### Ejemplo de IMPROVEMENT

```markdown
# IMPROVEMENT-001: Optimizar tiempo de ejecución del análisis de datos

**Estado:** Completado
**Prioridad:** Baja
**Tipo:** Optimization
**Plazo:** Corto plazo
**Fecha identificación:** 2025-11-10
**Fecha completado:** 2025-11-12

---

## Problema / Necesidad

El ejercicio 4 de PEC2 tarda 45 segundos en ejecutarse con dataset grande.
Podemos optimizar usando pandas en lugar de loops manuales.

## Propuesta / Opciones

Reemplazar:
```python
for row in data:
    result.append(process(row))
```

Por:
```python
result = df.apply(process, axis=1)
```

## Decisiones / Acciones

✅ Implementado con pandas.apply()
✅ Tiempo reducido de 45s a 2.3s
✅ Código más limpio y pythonic

## Referencias

- Commit: a1b2c3d
- Archivo: `Activity_2/ejercicio_4.py`
- Session: 2025-11-12
```

---

**Sistema de backlog basado en memsys3**
**Última actualización:** 2026-05-07 (ADR-021: docs/ opcionales para anti-CDC)
