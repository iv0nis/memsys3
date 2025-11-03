# Backlog - memsys3

Este directorio contiene **trabajo futuro pendiente**: issues identificados, features propuestas, especificaciones técnicas, blueprints arquitectónicos y exploraciones.

---

## 📋 Sistema de Códigos

Cada documento usa un prefijo para identificar su tipo:

### `ISSUE-XXX`
**Problemas técnicos, bugs, tech debt**

- Problema identificado que frena o limita el sistema
- Requiere solución pero no es bloqueante inmediato
- Puede incluir análisis de opciones

**Ejemplo:** `ISSUE-001-escalabilidad-mantenimiento.md`

### `FEATURE-XXX`
**Nueva funcionalidad a implementar**

- Capacidad nueva que el sistema no tiene
- Describe qué se quiere lograr y por qué
- Puede incluir diseño preliminar

**Ejemplo:** `FEATURE-001-exportar-contexto-markdown.md`

### `SPEC-XXX`
**Especificación técnica detallada**

- Documento técnico de cómo implementar algo específico
- Incluye API, estructura de datos, flujos
- Más detallado que un issue o feature

**Ejemplo:** `SPEC-001-api-compilacion-contexto.md`

### `BLUEPRINT-XXX`
**Diseño arquitectónico de alto nivel**

- Cambios significativos en arquitectura del sistema
- Decisiones de diseño con múltiples componentes
- Suele generar múltiples ADRs después

**Ejemplo:** `BLUEPRINT-001-sistema-plugins.md`

### `IMPROVEMENT-XXX`
**Mejora de funcionalidad existente**

- No es bug ni feature nueva
- Optimización, UX, performance de algo que ya existe
- Cambio incremental

**Ejemplo:** `IMPROVEMENT-001-optimizar-compilacion.md`

### `EXPLORATION-XXX`
**Investigación sin solución clara**

- Problema identificado sin solución obvia
- Requiere investigación, pruebas, experimentación
- Puede resultar en un SPEC o BLUEPRINT después

**Ejemplo:** `EXPLORATION-001-cache-inteligente.md`

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
1. Cambiar estado a **Completado**
2. Agregar referencia a commits/PRs
3. **NO mover a archivo/** - mantener en backlog/ como referencia
4. Items completados sirven como documentación de decisiones

### 4. Cancelar/Rechazar Items

Si decides no implementar algo:
1. Cambiar estado a **Cancelado** o **Rechazado**
2. Documentar por qué (cambio de prioridad, no viable, etc.)
3. Mantener en backlog/ como referencia histórica

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

[Commits, ADRs, sesiones relacionadas]
```

---

## 🎯 Priorización

No hay sistema formal de priorización en memsys3, pero usa estos criterios:

- **Alta**: Bloquea trabajo o frena escalabilidad significativamente
- **Media**: Importante pero no urgente, puede esperar
- **Baja**: Nice to have, mejora incremental

---

## 📚 Relación con Otros Documentos

- **ADRs** (`memory/full/adr.yaml`): Decisiones arquitectónicas TOMADAS
- **Backlog**: Trabajo PENDIENTE de hacer
- **Sessions** (`memory/full/sessions.yaml`): Trabajo REALIZADO
- **Project Status** (`memory/project-status.yaml`): Estado ACTUAL

**Flujo:**
```
Backlog (futuro) → Sessions (hacer) → ADRs (decidir) → Project Status (ahora)
```

---

## 🗂️ Organización

- Un archivo por item
- Numeración secuencial por tipo (no global)
- Mantener completados en backlog/ (no archivar)
- README.md (este archivo) documenta el sistema

---

## 💡 Tips

1. **No borres items completados** - son documentación valiosa
2. **Sé específico en títulos** - deben ser descriptivos por sí solos
3. **Actualiza estados** - backlog desactualizado no sirve
4. **Referencia sesiones** - conecta backlog con trabajo real
5. **No sobre-ingenierices** - backlog es herramienta, no burocracia

---

**Última actualización:** 2025-11-03
