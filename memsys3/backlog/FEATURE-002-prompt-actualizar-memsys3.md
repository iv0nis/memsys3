# FEATURE-002: Prompt actualizar.md para Updates de memsys3

**Estado:** ✅ Implementado
**Prioridad:** Media → Alta (escalada durante implementación)
**Tipo:** Nueva funcionalidad
**Plazo:** Medio plazo → Completado
**Fecha identificación:** 2025-11-12
**Fecha implementación:** 2025-11-12
**Contexto:** Deployment en Soluzzia - necesidad de trackear versiones
**Testing:** Actualización real en deCastro_inmobiliaria (v1.0 → v0.5.0)

---

## 📋 Problema

### Falta Proceso Documentado para Actualizar memsys3

Actualmente existe `deploy.md` para deployment inicial, pero NO hay proceso documentado para actualizar memsys3 en proyectos existentes.

**Situación actual:**
- `deploy.md` solo cubre deployment inicial (proyecto sin memsys3)
- No hay guía para actualizar de v0.3.0 → v0.4.0, por ejemplo
- No está claro qué archivos se pueden sobrescribir y cuáles NO
- Riesgo de pérdida de datos si se sobrescribe memsys3/ sin cuidado

**Necesidad identificada:**
- Durante deployment en Soluzzia se agregó tracking de versión en `project-status.yaml`
- Campos: `memsys3_version`, `memsys3_deployed`
- Estos permitirán comparar versión actual vs disponible

**¿Qué hacer cuando hay nueva versión de memsys3?**
- ¿Qué archivos actualizar?
- ¿Qué archivos NUNCA tocar? (memory/full/, memory/project-status.yaml)
- ¿Cómo hacer merge de cambios en templates/?
- ¿Cómo actualizar prompts/ sin perder personalizaciones?

---

## 🎯 Objetivo

Crear prompt `@memsys3/prompts/actualizar.md` que guíe el proceso de actualización segura de memsys3.

---

## ✅ Solución Propuesta

### Crear `memsys3_templates/prompts/actualizar.md`

Contenido propuesto:

**1. Verificar versión actual**
- Leer `memsys3/memory/project-status.yaml` → `memsys3_version`
- Comparar con última versión disponible en GitHub

**2. Clonar nueva versión temporalmente**
```bash
git clone https://github.com/iv0nis/memsys3 memsys3_update_temp
cd memsys3_update_temp
NEW_VERSION=$(git describe --tags --always)
```

**3. Categorizar archivos según estrategia de actualización**

**NUNCA SOBRESCRIBIR** (datos del proyecto):
- `memory/full/adr.yaml`
- `memory/full/sessions.yaml`
- `memory/project-status.yaml`
- `memory/context.yaml`
- `memory/history/*`

**ACTUALIZAR SIEMPRE** (lógica del sistema):
- `prompts/*.md` (excepto personalizaciones específicas)
- `agents/*.yaml` (templates base)
- `viz/*` (visualizador)
- `memory/templates/*.yaml` (templates actualizados)

**REVISAR MANUALMENTE** (puede haber personalizaciones):
- `prompts/newSession.md` (si usuario personalizó)
- `agents/main-agent.yaml` (si usuario personalizó)

**4. Estrategia de actualización segura**
- Opción A: Backup + sobrescritura selectiva
- Opción B: Diff manual archivo por archivo
- Opción C: Clone en directorio temporal, copiar selectivamente

**5. Actualizar metadata**
```yaml
metadata:
  memsys3_version: "[NEW_VERSION]"
  memsys3_deployed: "[FECHA_UPDATE]"
```

**6. Verificar que todo funciona**
- Ejecutar `@memsys3/prompts/compile-context.md`
- Verificar visualizador: `@memsys3/prompts/mind.md`

**7. Documentar en sessions.yaml**
- Crear entry de sesión documentando:
  - Versión anterior → nueva
  - Archivos actualizados
  - Problemas encontrados (si hubo)

---

## 📊 Impacto

**Positivo:**
- Proceso seguro y documentado para updates
- Reducción de riesgo de pérdida de datos
- Claridad sobre qué se puede sobrescribir
- Tracking de versiones útil

**Riesgo:**
- Si no se implementa: usuarios pueden sobrescribir datos accidentalmente
- Inconsistencias entre versiones de memsys3 en diferentes proyectos

---

## 🔧 Implementación

### Tareas

1. **Crear `actualizar.md`** en `memsys3_templates/prompts/`
2. **Definir estrategia de actualización** (backup, diff, etc.)
3. **Documentar casos especiales**:
   - Actualización con personalizaciones
   - Actualización con rotación activa (sessions_N.yaml)
   - Actualización con archivado en history/
4. **Agregar sección en README** enlazando a actualizar.md
5. **Probar flujo completo** actualizando un proyecto real

### Prerequisitos

- Campo `memsys3_version` ya implementado en templates ✅
- Campo documentado en `deploy.md` ✅

---

## 📝 Notas

- Este prompt será especialmente útil cuando memsys3 evolucione (v0.5.0, v1.0.0, etc.)
- Permitirá mantener proyectos actualizados sin miedo a romper datos
- Complementa el ciclo: deploy.md (inicial) → actualizar.md (updates)

---

## 🔗 Referencias

- Issue relacionado: ISSUE-001 (escalabilidad mantenimiento)
- Improvement relacionado: IMPROVEMENT-001 (contexto docs críticos)
- Cambio que lo motivó: Agregado tracking versión en project-status.yaml (2025-11-12)

---

## ✅ Implementación Completada

### Archivos creados

1. **`memsys3_templates/prompts/actualizar.md`** (493 líneas)
   - Proceso completo de actualización paso a paso
   - 12 pasos documentados con comandos bash
   - Checklist final de validación
   - Sección de resolución de problemas

### Testing real: deCastro_inmobiliaria

**Proyecto:** Suite de herramientas IA para inmobiliaria (Astro + Claude API)
**Versión inicial:** v1.0 (2025-10-28, estructura antigua `/memory`)
**Versión actualizada:** v0.5.0 (2025-11-12, estructura nueva `/memsys3`)

**Resultado:**
- ✅ 18 archivos actualizados (prompts, agents, templates, viz)
- ✅ Migración de datos críticos (sessions.yaml, adr.yaml, project-status.yaml)
- ✅ Campos versión agregados correctamente
- ✅ Estructura `viz/` movida a raíz
- ✅ `history/` creado con .gitkeep
- ✅ Backups creados (seguridad)

---

## 🚨 Descubrimientos Críticos Durante Testing

### Escenario NO contemplado inicialmente: Estructura Antigua Incompatible

**Problema detectado:**

Durante la actualización de deCastro se descubrió que el proyecto tenía **DOS estructuras** coexistiendo:

```
deCastro_inmobiliaria/
├── memory/              ← Estructura ANTIGUA (pre-ADR-006, sin prefijo memsys3/)
│   ├── full/
│   │   ├── sessions.yaml (134 líneas - DATOS REALES del proyecto)
│   │   └── adr.yaml (320 líneas - DATOS REALES)
│   ├── project-status.yaml (222 líneas - DATOS REALES: "Suite d'eines IA per immobiliàries")
│   ├── templates/
│   ├── prompts/
│   └── viz/
└── memsys3/             ← Estructura NUEVA (post-ADR-006)
    └── memory/
        ├── full/
        │   ├── sessions.yaml (148 líneas - datos TEMPLATE memsys3, NO del proyecto)
        │   └── adr.yaml (238 líneas - datos TEMPLATE memsys3)
        └── project-status.yaml (81 líneas - datos TEMPLATE: "Sistema de gestió de context...")
```

**Diagnóstico:**

El deployment inicial (pre-ADR-006) se hizo con estructura `/memory` en raíz. Cuando se intentó "actualizar" posteriormente, se creó `/memsys3` pero:
1. NO se migraron los datos de `/memory` antigua
2. Se copiaron datos del template de memsys3 (genéricos, no del proyecto real)
3. Quedaron DOS sistemas coexistiendo - uno con datos reales (antigua) y otro vacío (nueva)

**Impacto:**

- ❌ Context Agent leería datos INCORRECTOS (template memsys3, no proyecto real)
- ❌ Pérdida efectiva de histórico (sessions/ADRs reales quedan en `/memory` no leída)
- ❌ project-status.yaml con información genérica de memsys3, no del proyecto inmobiliaria

**Solución implementada:**

Se agregó **PASO 0** a `actualizar.md` que detecta 3 escenarios:

1. **Escenario A:** Solo `/memory` (estructura antigua)
   - Diagnóstico: Sistema incompatible, migración completa requerida
   - Acción: Ejecutar deploy.md desde cero + migrar datos manualmente

2. **Escenario B:** `/memory` + `/memsys3` coexistiendo 🚨
   - Diagnóstico: Deployment incorrecto, datos en ubicación antigua
   - Acción: Migrar datos ANTES de actualizar:
     ```bash
     cp memory/full/sessions.yaml memsys3/memory/full/
     cp memory/full/adr.yaml memsys3/memory/full/
     cp memory/project-status.yaml memsys3/memory/
     ```

3. **Escenario C:** Solo `/memsys3` (estructura correcta)
   - Diagnóstico: Deployment correcto
   - Acción: Continuar normalmenteCON actualización

**Comandos de detección:**
```bash
ls -la memory/ 2>/dev/null && echo "⚠️ ESTRUCTURA ANTIGUA" || echo "✅ OK"
ls -la memsys3/ 2>/dev/null && echo "✅ memsys3/ existe" || echo "❌ NO existe"
```

**Validación:**

La migración en deCastro fue exitosa:
- ✅ Datos reales migrados a `/memsys3/memory/`
- ✅ Backup de `/memory` antigua creado
- ✅ project-status.yaml con información correcta del proyecto inmobiliaria
- ✅ 134 líneas de sessions (reales) + 320 líneas adr (reales) preservadas

---

## 📝 Lecciones Aprendidas

1. **Versiones pre-ADR-006 son incompatibles** con estructura actual
   - ADR-006 introdujo prefijo `memsys3/` (breaking change)
   - No se puede hacer "actualización suave" desde pre-v0.2.0

2. **Deployment inicial debe validarse exhaustivamente**
   - Verificar que project-status.yaml tiene datos del PROYECTO, no del template
   - Verificar que sessions.yaml y adr.yaml tienen histórico real

3. **actualizar.md debe ser defensivo**
   - Detectar escenarios edge-case ANTES de proceder
   - Siempre crear backups antes de tocar datos
   - Validar que datos migrados son correctos

4. **Tracking de versión es CRÍTICO**
   - Campo `memsys3_version` permite saber si actualización es necesaria
   - Campo `memsys3_deployed` ayuda a entender edad del deployment

---

## 🎯 Estado Final

**FEATURE-002:** ✅ **Completado e implementado con éxito**

- [x] Prompt `actualizar.md` creado (493 líneas)
- [x] Testing real en proyecto deCastro_inmobiliaria
- [x] Escenario crítico (estructura antigua) detectado y documentado
- [x] PASO 0 agregado para detección de incompatibilidades
- [x] Migración de datos validada (134 líneas sessions + 320 líneas adr)
- [x] Documentación completa en backlog

**Próximos pasos:**

- Testear actualización en segundo proyecto con estructura correcta (Escenario C)
- Validar que compile-context funciona con datos migrados
- Crear entry en sessions.yaml documentando esta implementación
