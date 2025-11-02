# Traducción FASE 3 - Traducción TOTAL (Keys YAML + Estados)

## ⚠️ ADVERTENCIA CRÍTICA

Esta fase es **LA MÁS DELICADA** de todas. Vamos a traducir:
- **Nombres de campos YAML** (keys) que el código JavaScript busca
- **Estados técnicos** que CSS usa para styling
- **Valores enum** que el sistema valida

**UN ERROR aquí puede ROMPER el visualizador y el sistema completo.**

## Objetivo

Eliminar TODO el catalán visual del sistema, incluyendo nombres de campos técnicos y estados.

---

## Tabla de Traducción Completa

### GRUPO A: Nombres de Campos YAML (Keys)

| Catalán (actual) | Español (nuevo) | Archivos afectados |
|---|---|---|
| `descripcio` | `descripcion` | YAML + viewer.js |
| `objectiu` | `objetivo` | YAML + viewer.js |
| `titol` | `titulo` | YAML + viewer.js |
| `nom` | `nombre` | YAML + viewer.js |
| `estat` | `estado` | YAML + viewer.js + style.css |
| `durada` | `duracion` | YAML + viewer.js |
| `participants` | `participantes` | YAML + viewer.js |
| `que_es_va_fer` | `que_se_hizo` | YAML + viewer.js |
| `ultima_feature` | `ultima_feature` | YAML + viewer.js (ya español) |
| `seguent_milestone` | `siguiente_milestone` | YAML + viewer.js |
| `ultima_compilacio` | `ultima_compilacion` | YAML + viewer.js |
| `notes_compilacio` | `notas_compilacion` | YAML + viewer.js |
| `compilat_per` | `compilado_por` | YAML + viewer.js |
| `versio_context` | `version_context` | YAML + viewer.js |
| `ultima_actualitzacio` | `ultima_actualizacion` | YAML + viewer.js |
| `actualitzat_per` | `actualizado_por` | YAML + viewer.js |
| `que_es` | `que_es` | YAML (ya español) |
| `problemes_resolts` | `problemas_resueltos` | YAML + viewer.js |
| `decisions_preses` | `decisiones_tomadas` | YAML + viewer.js |
| `tecnologies_afegides` | `tecnologias_agregadas` | YAML + viewer.js |
| `proxims_passos` | `proximos_pasos` | YAML + viewer.js |
| `notes_addicionals` | `notas_adicionales` | YAML + viewer.js |

### GRUPO B: Estados Técnicos (Values de `estat`)

| Catalán (actual) | Español (nuevo) | Archivos afectados |
|---|---|---|
| `operatiu` | `operativo` | YAML + viewer.js + style.css |
| `desenvolupament` | `desarrollo` | YAML + viewer.js + style.css |
| `pendent` | `pendiente` | YAML + viewer.js + style.css |
| `accepted` | `aceptado` | YAML + viewer.js + style.css |
| `deprecated` | `obsoleto` | YAML + viewer.js + style.css |

### GRUPO C: Criticidad (Values de `criticitat`)

| Catalán (actual) | Español (nuevo) | Archivos afectados |
|---|---|---|
| `alta` | `alta` | YAML (ya español) |
| `mitjana` | `media` | YAML |
| `baixa` | `baja` | YAML |

---

## Estrategia de Ejecución SEGURA

### ORDEN CRÍTICO (no alterar):

**PASO 1: Actualizar código PRIMERO (viewer.js, style.css)**
- Hacer código **bilingüe** temporalmente (acepta ambos idiomas)
- Ejemplo: `f.descripcio || f.descripcion` (busca catalán O español)

**PASO 2: Actualizar archivos YAML**
- Una vez código es bilingüe, traducir keys en YAML
- Sistema funciona porque código acepta ambas versiones

**PASO 3: Limpiar código bilingüe**
- Eliminar referencias catalanas del código
- Dejar solo versión española

**PASO 4: Copiar a templates**
- Sincronizar memsys3_templates/

---

## Archivos a Modificar (en ORDEN)

### FASE 3A: Hacer Código Bilingüe

#### 1. **memsys3/viz/viewer.js** (338 líneas)

**Cambios línea por línea:**

```javascript
// Línea 105-109 - Project info
nom: ${project.nom || project.nombre || 'N/A'}
descripcio: ${project.descripcio || project.descripcion || 'N/A'}
ultima_feature: ${project.ultima_feature || 'N/A'}
seguent_milestone: ${project.seguent_milestone || project.siguiente_milestone || 'N/A'}

// Línea 118-120 - Features
estat: status-${f.estat || f.estado || 'pendiente'}
${f.estat || f.estado || 'pendiente'}
nom: ${f.nom || f.nombre || key}
descripcio: ${f.descripcio || f.descripcion || ''}

// Línea 132 - ADRs
titol: ${adr.titol || adr.titulo}

// Línea 145-148 - Session
durada: ${session.durada || session.duracion || 'N/A'}
que_es_va_fer: ${session.que_es_va_fer || session.que_se_hizo ? ...}

// Línea 186 - ADR badge
estat: badge-${adr.estat || adr.estado}
${adr.estat || adr.estado}

// Línea 203 - Features implementadas
features_implementades: session.features_implementades || session.features_implementadas
nom: ${f.nom || f.nombre}
descripcio: ${f.descripcio || f.descripcion}

// Línea 206-208 - Problemas
problemes_resolts: session.problemes_resolts || session.problemas_resueltos

// Línea 211-213 - Decisiones
decisions_preses: session.decisions_preses || session.decisiones_tomadas

// Línea 219-221 - Tecnologías
tecnologies_afegides: session.tecnologies_afegides || session.tecnologias_agregadas
nom: ${t.nom || t.nombre}

// Línea 229-231 - Próximos pasos
proxims_passos: session.proxims_passos || session.proximos_pasos

// Línea 236-242 - Session details
titol: ${session.titol || session.titulo || session.id}
durada: ${session.durada || session.duracion}
participants: ${session.participants || session.participantes}
objectiu: ${session.objectiu || session.objetivo}

// Línea 249 - Notas
notes_addicionals: ${session.notes_addicionals || session.notas_adicionales}

// Línea 311-315 - Compilation notes
notes_compilacio: notes_compilacio || notas_compilacion

// Línea 322 - Metadata
ultima_compilacio: metadata.ultima_compilacio || metadata.ultima_compilacion
```

**- [ ] Aplicar cambios bilingües en viewer.js**

#### 2. **memsys3/viz/style.css** (actualizar clases CSS)

```css
/* Línea 194-201 - Agregar versiones español */
.status-operatiu,
.status-operativo {
  background: rgba(34, 197, 94, 0.2);
  color: var(--success);
}

.status-desenvolupament,
.status-desarrollo {
  background: rgba(245, 158, 11, 0.2);
  color: var(--warning);
}

.status-pendent,
.status-pendiente {
  background: rgba(100, 116, 139, 0.2);
  color: var(--text-muted);
}

/* Línea 238-247 - Agregar versiones español */
.badge-accepted,
.badge-aceptado {
  background: rgba(34, 197, 94, 0.2);
  color: var(--success);
}

.badge-deprecated,
.badge-obsoleto {
  background: rgba(239, 68, 68, 0.2);
  color: var(--error);
}
```

**- [ ] Aplicar cambios bilingües en style.css**

#### 3. **Verificación código bilingüe**

**- [ ] Probar visualizador con archivos YAML actuales (catalán)**
  ```bash
  cd memsys3/viz
  python3 serve.py
  # Verificar que TODO funciona normalmente
  ```

---

### FASE 3B: Traducir Archivos YAML

Una vez código es bilingüe, traducir keys en TODOS los archivos YAML:

#### 4. Archivos de memoria (10 archivos)

**- [ ] `memsys3/memory/context.yaml`**
  - Reemplazar TODOS los keys del GRUPO A
  - Reemplazar TODOS los valores del GRUPO B y C
  - Usar find & replace masivo con cuidado

**- [ ] `memsys3/memory/project-status.yaml`**
  - Reemplazar keys y values

**- [ ] `memsys3/memory/full/sessions.yaml`**
  - Reemplazar keys y values

**- [ ] `memsys3/memory/full/adr.yaml`**
  - Reemplazar keys y values

**- [ ] `memsys3/memory/templates/context-template.yaml`**
  - Reemplazar keys (mantener placeholders)

**- [ ] `memsys3/memory/templates/sessions-template.yaml`**
  - Reemplazar keys (mantener placeholders)

**- [ ] `memsys3/memory/templates/adr-template.yaml`**
  - Reemplazar keys (mantener placeholders)

**- [ ] `memsys3/memory/templates/project-status-template.yaml`**
  - Reemplazar keys (mantener placeholders)

**- [ ] `memsys3/agents/context-agent.yaml`**
  - Reemplazar keys en inputs/outputs

**- [ ] `memsys3/agents/main-agent.yaml`**
  - Reemplazar keys si usa campos

#### 5. Verificación YAML traducidos

**- [ ] Probar visualizador con YAML en español**
  ```bash
  cd memsys3/viz
  python3 serve.py
  # Verificar que TODO funciona con nuevos keys
  ```

**- [ ] Ejecutar compile-context para verificar que CA funciona**
  ```bash
  # En nueva instancia Claude Code
  @memsys3/prompts/compile-context.md
  ```

---

### FASE 3C: Limpiar Código (Eliminar Catalán)

Una vez YAML está en español, eliminar fallbacks catalanes del código:

#### 6. **memsys3/viz/viewer.js** - Versión FINAL español

```javascript
// Eliminar TODAS las referencias catalanas (|| f.descripcio)
// Dejar SOLO versiones españolas:
${project.descripcion || 'N/A'}
${f.estado || 'pendiente'}
${f.nombre || key}
${session.titulo || session.id}
${session.duracion}
${session.participantes}
${session.objetivo}
// etc.
```

**- [ ] Limpiar viewer.js (solo español)**

#### 7. **memsys3/viz/style.css** - Versión FINAL español

```css
/* Eliminar clases catalanas:*/
.status-operativo { ... }  /* Mantener */
.status-desarrollo { ... }  /* Mantener */
.status-pendiente { ... }  /* Mantener */
.badge-aceptado { ... }  /* Mantener */
.badge-obsoleto { ... }  /* Mantener */

/* ELIMINAR:
.status-operatiu
.status-desenvolupament
.status-pendent
.badge-accepted
.badge-deprecated
*/
```

**- [ ] Limpiar style.css (solo español)**

#### 8. Verificación FINAL

**- [ ] Buscar catalán residual en código**
  ```bash
  grep -r "descripcio\|objectiu\|titol\|estat\|operatiu\|desenvolupament" memsys3/viz/
  # Debe dar 0 resultados
  ```

**- [ ] Probar visualizador completo**
  - Todas las pestañas funcionan
  - No hay errores en consola
  - CSS aplica correctamente

---

### FASE 3D: Sincronizar Templates

#### 9. Copiar TODOS los archivos a memsys3_templates/

**- [ ] Copiar archivos modificados**
  ```bash
  # YAML
  cp memsys3/memory/context.yaml memsys3_templates/memory/context.yaml
  cp memsys3/memory/project-status.yaml memsys3_templates/memory/project-status.yaml
  cp memsys3/memory/full/sessions.yaml memsys3_templates/memory/full/sessions.yaml
  cp memsys3/memory/full/adr.yaml memsys3_templates/memory/full/adr.yaml
  cp memsys3/memory/templates/*.yaml memsys3_templates/memory/templates/
  cp memsys3/agents/*.yaml memsys3_templates/agents/

  # Código
  cp memsys3/viz/viewer.js memsys3_templates/viz/viewer.js
  cp memsys3/viz/style.css memsys3_templates/viz/style.css
  ```

---

## Estrategia de Rollback

**SI ALGO FALLA EN FASE 3B o posterior:**

```bash
# Opción 1: Git reset (si hay commit previo)
git reset --hard HEAD

# Opción 2: Restaurar desde backup
# (Crear backup ANTES de empezar FASE 3)
tar -czf memsys3-backup-pre-fase3.tar.gz memsys3/ memsys3_templates/
```

**Puntos de no retorno:**
- ✅ FASE 3A: Reversible (solo código bilingüe)
- ⚠️ FASE 3B: Crítico (YAML traducidos, crear backup ANTES)
- ⚠️ FASE 3C: Crítico (código limpiado, difícil revertir)

---

## Verificaciones Críticas

Antes de declarar FASE 3 completada:

**- [ ] 1. Visualizador funciona al 100%**
  - Agent View muestra datos
  - Full History muestra ADRs y Sessions
  - Project Status muestra info
  - Stats muestra estadísticas

**- [ ] 2. compile-context funciona**
  - Genera context.yaml sin errores
  - Campos traducidos correctamente

**- [ ] 3. No hay catalán residual**
  ```bash
  grep -r "descripcio\|objectiu\|titol\|operatiu\|desenvolupament\|pendent\|mitjana\|baixa" \
    memsys3/ memsys3_templates/ \
    --include="*.yaml" --include="*.js" --include="*.css" --include="*.html"
  ```

**- [ ] 4. Templates sincronizados**
  ```bash
  diff -r memsys3/ memsys3_templates/ \
    --exclude=".git" --exclude="history" --exclude="full"
  # Solo deben diferir archivos específicos de dog-fooding
  ```

---

## Notas Finales

**Tiempo estimado:** 2-3 horas (con cuidado extremo)

**Dificultad:** ⚠️⚠️⚠️ MUY ALTA

**Impacto:** 🎯 Elimina TODO el catalán visual del sistema

**Riesgo:** 🚨 Puede romper visualizador si hay errores

**Recomendación:**
- Crear backup completo ANTES de empezar
- Hacer commit después de FASE 3A (código bilingüe)
- Hacer commit después de FASE 3B (YAML traducidos)
- Probar exhaustivamente en cada fase

**Resultado esperado:**
- ✅ Sistema 100% en español (keys + values + UI + código)
- ✅ Sin catalán visible en ninguna parte
- ✅ Visualizador totalmente funcional
- ✅ Templates sincronizados
