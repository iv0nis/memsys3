# End Session - Documenta la Sesión Actual

Tu (DevAgent) debes documentar esta sesión de trabajo en el sistema Memory del proyecto.

## Objetivo

Registrar qué se ha hecho durante esta sesión para que el próximo DevAgent tenga contexto completo.

## Workflow

### 1. Recopilar Evidencias Objetivas

Recopila evidencias de qué se ha hecho:

```bash
# Git (si disponible)
git status && git diff --stat && git log --oneline -5

# Archivos modificados (ajusta -mmin según duración sesión)
find . -type f -mmin -180 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*'

# Bash history
history | tail -30
```

**Notas:** Estas evidencias son opcionales pero recomendadas. Si alguna falla, continúa con tu contexto interno.

### 2. Auto-analizar la Sesión

Identifica:
- **Features/Tareas**: Qué has implementado, bugs resueltos, refactorings
- **Problemas Resueltos**: Obstáculos encontrados y cómo los has solucionado
- **Decisiones Tomadas**: Decisiones técnicas o arquitectónicas (importantes → ADR)
- **Tech añadida/eliminada**: Dependencies, tools y por qué
- **Deployments**: URLs, servicios desplegados
- **Gotchas**: Errores críticos, warnings, traps encontrados durante la sesión (con criticidad)
- **Próximos Pasos**: Qué queda pendiente

### 3. Comprobar Rotaciones Automáticas

**Sessions.yaml:**
```bash
wc -l memsys3/memory/full/sessions.yaml
# Si > 1800 líneas:
ls memsys3/memory/full/sessions_*.yaml 2>/dev/null  # Encontrar próximo número
cp memsys3/memory/full/sessions.yaml memsys3/memory/full/sessions_N.yaml  # Copiar
wc -l memsys3/memory/full/sessions_N.yaml  # Verificar
# Crear nuevo sessions.yaml con header YAML vacío
```

**adr.yaml:**
```bash
wc -l memsys3/memory/full/adr.yaml
# Si > 1800 líneas: mismo proceso → adr_N.yaml
```

**Rotación = Copia segura + Verificación + Nuevo archivo vacío**

### 4. Documentar

**A. Añadir Sesión a `memsys3/memory/full/sessions.yaml`:**
- Añadir al PRINCIPIO del array `sessions:`
- Usar `memsys3/memory/templates/sessions-template.yaml` como guía
- ID y data: YYYY-MM-DD de hoy
- Título descriptivo y conciso
- Sé completo pero evita detalles demasiado granulares
- **IMPORTANTE - Gotchas**: Si has encontrado errores críticos, warnings o traps:
  - Documentarlos en el campo `gotchas:` de la sesión
  - Incluir: `tipus`, `problema`, `solucio`, `criticitat` (alta|mitjana|baixa)
  - Solo gotchas relevantes (errores que rompen, contra-intuitivos, recurrentes)
  - Context-Agent extraerá los top 5 más críticos de TODAS las sesiones

**B. Crear ADRs si hace falta (en `memsys3/memory/full/adr.yaml`):**

Solo si has tomado **decisiones arquitectónicas importantes**:
- Elegir librería/framework en lugar de otro
- Cambiar arquitectura del sistema
- Decidir patrón de diseño
- Cambiar stack tecnológico

**NO crear ADR para:**
- Cambios cosméticos (colores, padding)
- Validaciones de formularios
- Bugs menores
- Refactorings de funciones

Si creas ADR:
1. Comprobar rotación adr.yaml (paso 3)
2. Usar `memsys3/memory/templates/adr-template.yaml`
3. Linkear ADR desde sesión (campo `adr_relacionada`)

**C. Actualizar `memsys3/memory/project-status.yaml`:**
- `metadata.ultima_actualitzacio`: Fecha de hoy
- `metadata.actualitzat_per`: "Claude (Session [Título])"
- `estat_actual.ultima_feature`: Si has completado feature
- `features`: Cambiar `estat: operatiu` si se ha completado
- `historic_sessions`: Añadir entrada resumida
- `pendents_prioritaris`: Actualizar según próximos pasos

### 5. Informar al Usuario

Resumen breve de qué se ha documentado:

```
✅ Sesión documentada en memsys3/memory/full/sessions.yaml
✅ [N] ADRs creadas (si las hay)
✅ memsys3/memory/project-status.yaml actualizado
✅ Rotación hecha (si hacía falta): sessions.yaml → sessions_N.yaml

Highlights de la sesión:
- [Feature principal implementada]
- [Problema crítico resuelto]
- [Decisión arquitectónica tomada]

Próximos pasos: [Top 2-3 tareas pendientes]
```

## Notas Importantes

- **Formato YAML**: Indentación estricta (2 espacios), usa `|` para multiline
- **Consistencia**: Sigue estilo de sessions/ADRs anteriores
- **NO preguntar**: Asume que la documentación es correcta (pregunta solo si falta contexto crítico)
- **Context Agent**: No te preocupes por tokens aquí, él filtrará después
- **Rotación automática**: Preserva SIEMPRE los datos (sessions_N.yaml, adr_N.yaml)

---

**Comienza ahora la documentación de la sesión actual.**
