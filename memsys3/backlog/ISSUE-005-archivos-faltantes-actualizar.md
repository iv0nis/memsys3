# ISSUE-005: Archivos faltantes en actualizar.md PASO 6.1

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Bug / Actualización Incompleta
**Plazo:** Inmediato
**Fecha identificación:** 2025-12-30

---

## Problema / Necesidad

El prompt `actualizar.md` (PASO 6.1 - Actualizar Prompts) **NO incluye** archivos críticos que fueron introducidos en versiones recientes, causando que proyectos actualizados pierdan funcionalidad.

**Comportamiento actual:**
- Usuario actualiza desde v0.6.1 → v0.8.1 siguiendo `actualizar.md` literalmente
- Archivos nuevos (`adr.md`, `backlog.md`) NO se copian al proyecto
- Usuario pierde acceso a funcionalidad de gestión de ADRs y backlog
- No hay warnings ni indicación de archivos faltantes

**Comportamiento esperado:**
- TODOS los prompts disponibles en la nueva versión deben copiarse
- Usuario debe tener acceso completo a todas las funcionalidades de memsys3

---

## Archivos Faltantes Confirmados

### ❌ adr.md
- **Introducido en:** v0.8.0 (commit 16ade95, 12 dic 2025)
- **Función:** Gestión de Architecture Decision Records (consultar, crear, actualizar)
- **Impacto:** Sin este archivo, usuarios no pueden gestionar ADRs conversacionalmente

### ❌ backlog.md
- **Introducido en:** v0.7.0 (commit 5efffb0, 14 nov 2025)
- **Función:** Gestión de backlog (consultar, crear, actualizar items)
- **Impacto:** Sin este archivo, usuarios no pueden gestionar backlog conversacionalmente

### ❌ commands.md
- **Introducido en:** v0.8.1 (commit dcf606e, 14 dic 2025)
- **Función:** Instalación de comandos globales de memsys3 (/deploy-memsys3, /actualizar-memsys3)
- **Impacto:** Sin este archivo, usuarios no pueden instalar comandos globales desde proyectos actualizados

---

## Evidencia

**Caso real confirmado:**
- **Proyecto:** Taller Colomer
- **Actualización:** v0.6.1 → v0.8.1
- **Fecha:** 2025-12-22
- **Resultado:** Archivo `adr.md` faltante tras seguir `actualizar.md` literalmente
- **Workaround aplicado:** Creación manual de comando local `/adr` personalizado

**Confirmación de otra instancia de Claude:**
> "Bug confirmado: El prompt actualizar.md NO incluye adr.md en la lista de prompts a actualizar en el Paso 6.1. [...] El único que falta es adr.md porque simplemente no está en las instrucciones de actualizar.md."

---

## Análisis de actualizar.md

**Archivo:** `memsys3_templates/prompts/actualizar.md`
**Líneas:** 262-268 (PASO 6.1)

**Prompts que SÍ actualiza:**
```bash
cp memsys3_update_temp/memsys3_templates/prompts/compile-context.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/endSession.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/mind.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/github.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/deploy.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/actualizar.md memsys3/prompts/
```

**Prompts que FALTAN:**
- ❌ `adr.md`
- ❌ `backlog.md`
- ❌ `commands.md`

---

## Causa Raíz

Cuando se agregaron nuevos prompts al sistema (`backlog.md` en v0.7.0, `adr.md` en v0.8.0, `commands.md` en v0.8.1), **se olvidó actualizar** la lista de archivos a copiar en `actualizar.md` PASO 6.1.

Esto genera una **deuda técnica** donde cada nuevo prompt debe recordarse agregar manualmente a `actualizar.md`, lo cual es propenso a errores (3 archivos olvidados en 3 versiones diferentes confirman el patrón).

---

## Propuesta / Opciones

### Opción A: Fix Manual (Corto Plazo) - ✅ APLICADO
Agregar líneas faltantes en PASO 6.1:

```bash
cp memsys3_update_temp/memsys3_templates/prompts/adr.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/backlog.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/commands.md memsys3/prompts/
```

**Pros:** Fix inmediato
**Contras:** No previene futuros olvidos

### Opción B: Copy All (Mediano Plazo) - RECOMENDADO
Reemplazar lista manual con copiado automático:

```bash
# Copiar TODOS los prompts (excepto newSession.md que requiere revisión manual)
for file in memsys3_update_temp/memsys3_templates/prompts/*.md; do
  filename=$(basename "$file")
  if [ "$filename" != "newSession.md" ]; then
    cp "$file" memsys3/prompts/
  fi
done
```

**Pros:** Previene olvidos futuros, auto-actualizable
**Contras:** Requiere testing de que no rompe nada

### Opción C: Verificación Post-Update (Largo Plazo)
Agregar PASO de verificación que compare `memsys3_update_temp/memsys3_templates/prompts/` vs `memsys3/prompts/` y reporte diferencias.

**Pros:** Detecta archivos faltantes antes de borrar temp
**Contras:** Más complejo, requiere lógica de diff

---

## Decisiones / Acciones

**Decisión:** Implementar **Opción A + Opción B**

1. **Inmediato (Opción A):** Agregar `adr.md` y `backlog.md` manualmente a PASO 6.1
2. **Próxima iteración (Opción B):** Evaluar reemplazar con loop automático

**Fix aplicado:**
- [x] Actualizar `memsys3_templates/prompts/actualizar.md` (PASO 6.1) - ✅ Agregados adr.md, backlog.md, commands.md
- [x] Actualizar `memsys3/prompts/actualizar.md` (dog-fooding) - ✅ Sincronizado
- [x] Verificar que no falten otros archivos en otras secciones - ✅ Todos los prompts están incluidos ahora
- [ ] Testing en proyecto con actualización pendiente (ej: Taller Colomer actualizarlo nuevamente)
- [ ] Actualizar PASO 4 lista de archivos para incluir nuevos prompts en documentación

---

## Referencias

- **Prompt afectado:** `memsys3/prompts/actualizar.md` (líneas 262-268)
- **Commits relevantes:**
  - `16ade95` - Introducción adr.md (v0.8.0)
  - `5efffb0` - Introducción backlog.md (v0.7.0)
- **Caso real:** Taller Colomer (actualización 2025-12-22)
- **Conversación:** Sesión 2025-12-30 con usuario reportando bug

---

## Notas Adicionales

- Este bug afecta a CUALQUIER proyecto que actualice desde versiones anteriores a v0.7.0
- Solución temporal: copiar archivos manualmente desde memsys3_update_temp/
- **Importante:** Verificar si hay otros archivos faltantes en otras secciones (agents, viz, templates, etc.)
- Considerar agregar checklist de archivos críticos al final de `actualizar.md`
