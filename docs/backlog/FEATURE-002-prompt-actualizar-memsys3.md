# FEATURE-002: Prompt actualizar.md para Updates de memsys3

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Nueva funcionalidad
**Plazo:** Medio plazo
**Fecha identificación:** 2025-11-12
**Contexto:** Deployment en CLIENT_F - necesidad de trackear versiones

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
- Durante deployment en CLIENT_F se agregó tracking de versión en `project-status.yaml`
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
