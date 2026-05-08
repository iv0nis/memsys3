# Guía de Desarrollo de memsys3

> Documento para desarrolladores que contribuyen o modifican memsys3

## Estructura del Repositorio

```
memsys3/                          # Repositorio GitHub
├── README.md                    # README principal (público)
├── docs/                        # 📚 DESARROLLO DE MEMSYS3 (NO se distribuye)
│   ├── DEVELOPMENT.md          # Este archivo
│   ├── UPDATE.md               # Guía de actualización
│   ├── backlog/                # Issues, features, specs del proyecto memsys3
│   └── archivo/                # Histórico de documentos completados
├── memsys3_templates/           # ⭐ PRODUCTO FINAL (lo que se distribuye)
│   ├── README.md               # Docs del sistema
│   ├── agents/                 # Templates de agents
│   ├── memory/                 # Templates de memory
│   └── prompts/                # Templates de prompts
└── memsys3/                     # 🔧 Dog-fooding (desarrollo interno)
    └── (Instancia específica para desarrollar memsys3)
```

## 📚 Sobre la Carpeta docs/

### ¿Qué es docs/?

**`docs/` es la carpeta estándar de desarrollo de software** usada en la industria para documentar el proceso de desarrollo, arquitectura, decisiones técnicas, issues, y trabajo futuro del proyecto.

memsys3 es un proyecto de software, por lo tanto **usamos docs/ como cualquier otro proyecto** de la industria, pero adaptado a nuestra manera.

### ¿Qué contiene docs/?

```
docs/
├── DEVELOPMENT.md     # Guía para contributors
├── UPDATE.md          # Guía de actualización
├── backlog/           # Trabajo futuro (issues, features, specs)
│   ├── README.md
│   └── ISSUE-XXX-*.md, FEATURE-XXX-*.md, etc.
└── archivo/           # Histórico (documentos completados)
    └── (auditorías, reportes, referencias)
```

### ⚠️ IMPORTANTE: docs/ NO se Distribuye

**docs/ es específico del desarrollo de memsys3 como producto.**

- ✅ **Está en el repositorio GitHub** (público, parte del código fuente)
- ❌ **NO está en memsys3_templates/** (no se copia a proyectos)
- ❌ **NO se distribuye** durante deployment

**Razón:** Los proyectos que usan memsys3 tienen sus propios sistemas de tracking (GitHub Issues, Jira, etc.). No necesitan ver los issues internos de cómo desarrollamos memsys3.

### Contenido de docs/backlog/

Sistema de códigos para trabajo futuro:

- **ISSUE-XXX**: Problemas técnicos, bugs, tech debt
- **FEATURE-XXX**: Nueva funcionalidad a implementar
- **SPEC-XXX**: Especificaciones técnicas detalladas
- **BLUEPRINT-XXX**: Diseño arquitectónico de alto nivel
- **IMPROVEMENT-XXX**: Mejoras de funcionalidad existente
- **EXPLORATION-XXX**: Investigación sin solución clara

Ver `docs/backlog/README.md` para detalles del sistema.

```

## 🎯 Filosofía: Estructura y Deployment

### Concepto de memsys3_templates/ (ms3t)

**`memsys3_templates/` = Estructura EXACTA del producto final**

Todo lo que está en `memsys3_templates/` se copia al proyecto del usuario durante deployment. No hay "cosas que se borran después" ni "cosas temporales". La estructura es:

```
memsys3_templates/                # TODO esto se copia
├── agents/
│   ├── context-agent.yaml        # Agnóstico (se copia tal cual)
│   └── main-agent.yaml           # Con campos [PLACEHOLDER] para rellenar
├── memory/
│   ├── full/
│   │   ├── adr.yaml              # Vacío: adrs: []
│   │   └── sessions.yaml         # Vacío: sessions: []
│   ├── templates/                # ⭐ GUÍAS PERMANENTES (NO se borran)
│   │   ├── adr-template.yaml
│   │   ├── sessions-template.yaml
│   │   ├── project-status-template.yaml
│   │   └── context-template.yaml
│   ├── history/                  # Vacío (para Plan Contingencia)
│   ├── project-status.yaml       # Con campos [PLACEHOLDER] para rellenar
│   └── README.md                 # Agnóstico
├── prompts/                      # Agnósticos (todos se copian)
└── README.md                     # Agnóstico
```

### ¿Qué es memory/templates/?

**NO son "templates de templates"**. Son **guías permanentes** que:

1. **Durante deployment**: El agente las lee para hacer el briefing
   - "¿Qué campos necesito rellenar en project-status?" → lee project-status-template.yaml
   - "¿Qué estructura tiene una sesión?" → lee sessions-template.yaml

2. **Durante desarrollo**: Main-Agent las consulta durante endSession
   - "¿Cómo documento esta sesión?" → consulta sessions-template.yaml
   - "¿Qué campos tiene una ADR?" → consulta adr-template.yaml
   - "¿Qué ejemplos hay de buena documentación?" → ve ejemplos en templates

3. **Contienen**:
   - Estructura completa de cada archivo
   - Instrucciones de uso (orden cronológico, límites de palabras, etc.)
   - Ejemplos de buenas vs malas prácticas
   - Comentarios explicativos

**Por eso NO se borran después del deployment**: Son documentación activa.

### Workflow de Deployment

```bash
# Usuario dice (desde root_proyecto/):
"Clona https://github.com/iv0nis/memsys3 como memsys3_temp
 y ejecuta memsys3_temp/memsys3/prompts/deploy.md"

# El agente:
1. git clone https://github.com/iv0nis/memsys3 memsys3_temp
2. cp -r memsys3_temp/memsys3/* ./memsys3/
3. Lee memory/templates/ para guiar briefing
4. Hace preguntas según project-status-template.yaml
5. Rellena campos vacíos: [NOMBRE] → "Mi Proyecto"
6. rm -rf memsys3_temp/

# Resultado final en root_proyecto/:
memsys3/
├── agents/                       # Copiado, main-agent.yaml rellenado
├── memory/
│   ├── full/                     # adr.yaml y sessions.yaml vacíos
│   ├── templates/                # ⭐ PERMANENTE, guías para Main-Agent
│   ├── history/                  # Vacío
│   ├── project-status.yaml       # Rellenado con info del proyecto
│   └── README.md
├── prompts/                      # Copiados tal cual
└── README.md
```

### Gotchas: Dónde se documentan

**NO en project-status.yaml** (como sugiere project-status-template.yaml).

**SÍ en sessions.yaml**, porque:
- Los gotchas surgen DURANTE sesiones de trabajo
- Deben estar contextualizados (cuándo aparecieron, en qué sesión)
- Context-Agent los lee de TODAS las sessions y selecciona los más críticos

Estructura en sessions.yaml:
```yaml
sessions:
  - id: "2025-10-31"
    objectiu: "Implementar autenticación"
    features_implementades: [...]

    gotchas:  # ← Aquí se documentan
      - tipus: "warning"
        problema: "useAuth() solo funciona dentro de AuthProvider"
        solucio: "Wrap App con <AuthProvider>"
        criticitat: "alta"
```

Context-Agent:
1. Lee todas las sessions
2. Extrae todos los gotchas
3. Selecciona top 5 más críticos (criticitat + recencia)
4. Los incluye en context.yaml compilado

**Resultado**: project-status.yaml más limpio (solo info general), gotchas contextualizados.

### Repositorios: Dev vs Público

En el futuro, la estructura será:

1. **github.com/iv0nis/memsys3_dev** (PRIVADO)
   - Desarrollo con dog-fooding
   - Contiene: `memsys3_templates/` + `memsys3/`
   - Aquí se hacen los cambios y pruebas

2. **github.com/iv0nis/memsys3** (PÚBLICO)
   - Solo contiene `memsys3/` (renombrado desde memsys3_templates/)
   - Es el producto final que usuarios clonan
   - Solo deployment, sin desarrollo interno visible

Workflow:
```
Desarrollo en memsys3_dev:
  Editar memsys3_templates/
       ↓
  Probar en memsys3/ (dog-fooding)
       ↓
Desplegar a memsys3 público:
  Copiar memsys3_templates/ → memsys3_templates/memsys3/
  Push a github.com/iv0nis/memsys3
```

## ⚠️ CRÍTICO: Sistema de Rutas

### Regla de Oro

**TODAS las rutas en `memsys3_templates/` deben apuntar a `memsys3/`**

### Explicación

Cuando un usuario hace deployment:
1. Copia `memsys3_templates/` a su proyecto como `memsys3/`
2. Todos los archivos quedan en: `su-proyecto/memsys3/`
3. Las rutas relativas funcionan correctamente

### Ejemplos Correctos

En `memsys3_templates/prompts/compile-context.md`:
```markdown
- Actúa según las instrucciones en 'memsys3/agents/context-agent.yaml'
- Llegeix `@memsys3/memory/full/adr.yaml`
- Genera `@memsys3/memory/context.yaml`
```

En `memsys3_templates/prompts/newSession.md`:
```markdown
- Actúa segons 'memsys3/agents/main-agent.yaml'
- Llegeix memsys3/memory/project-status.yaml
```

En `memsys3_templates/prompts/deploy.md`:
```bash
mkdir -p memsys3/memory/full
cp memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/
```

### Ejemplos Incorrectos

❌ `memory/context.yaml` (sin prefijo memsys3/)
❌ `@memory/full/adr.yaml` (sin prefijo memsys3/)
❌ `agents/main-agent.yaml` (sin prefijo memsys3/)

### ¿Por qué este sistema?

1. **Portabilidad**: Cualquier proyecto puede tener memsys3 sin conflictos
2. **Claridad**: Siempre está claro qué archivos son de memsys3
3. **Actualizaciones**: Fácil saber qué actualizar
4. **Consistencia**: Todos los proyectos tienen la misma estructura

## Workflow de Desarrollo

### 1. Hacer Cambios en memsys3_templates/

**Los cambios SIEMPRE van primero en `memsys3_templates/`** (el producto final).

Ejemplo: Mejorar el Context Agent
```bash
# Editar el template
vi memsys3_templates/prompts/compile-context.md
```

### 2. Probar en memsys3/ (Dog-fooding)

Después de hacer cambios en templates, despliégalos en `memsys3/` para probarlos:

```bash
# Opción A: Copiar archivo específico
cp memsys3_templates/prompts/compile-context.md memsys3/prompts/

# Opción B: Usar guía de actualización
# Ver docs/UPDATE.md
```

### 3. Validar Rutas

Antes de commit, verifica que todas las rutas sean correctas:

```bash
# Buscar rutas incorrectas (sin memsys3/)
grep -r "@memory/" memsys3_templates/prompts/
grep -r "agents/" memsys3_templates/prompts/ | grep -v "memsys3/agents"
grep -r "prompts/" memsys3_templates/prompts/ | grep -v "memsys3/prompts"

# No debería haber resultados
```

### 4. Documentar en ADRs

Si el cambio es significativo, documentarlo en:
- `memsys3/memory/full/adr.yaml` (nuestra instancia)
- Después, al hacer endSession, quedará registrado

## Archivos Críticos de Rutas

Archivos que contienen muchas referencias a rutas y deben revisarse siempre:

1. **memsys3_templates/prompts/compile-context.md**
   - Inputs: `@memsys3/memory/full/adr.yaml`, etc.
   - Output: `@memsys3/memory/context.yaml`
   - Reference: `memsys3/agents/context-agent.yaml`

2. **memsys3_templates/prompts/deploy.md**
   - Estructura a crear: `memsys3/memory/full/`, etc.
   - Copias desde: `memsys3_templates/` hacia `memsys3/`

3. **memsys3_templates/prompts/newSession.md**
   - Lee: `memsys3/memory/project-status.yaml`
   - Reference: `memsys3/agents/main-agent.yaml`

4. **memsys3_templates/prompts/endSession.md**
   - Escribe en: `memsys3/memory/full/sessions.yaml`
   - Usa templates: `memsys3/memory/templates/`

## Main-Agent vs Context-Agent

### Main-Agent (Development)
- **Archivo**: `memsys3/agents/main-agent.yaml`
- **Responsabilidades**: Desarrollo, documentación, features
- **NO debe**: Compilar context.yaml (consume muchos tokens)
- **Prompt final**: Puede sugerir endSession

### Context-Agent (Compilation)
- **Archivo**: `memsys3/agents/context-agent.yaml`
- **Responsabilidades**: Compilar context.yaml con criterio inteligente
- **Invocado por**: `@memsys3/prompts/compile-context.md`
- **Momento**: Nueva instancia limpia (sin tokens acumulados)

## Checklist Antes de Commit

- [ ] Cambios hechos primero en `memsys3_templates/`
- [ ] Todas las rutas apuntan a `memsys3/`
- [ ] No hay referencias a `memory/` sin prefijo
- [ ] No hay referencias a `agents/` sin prefijo
- [ ] No hay referencias a `prompts/` sin prefijo
- [ ] Probado en `memsys3/` (dog-fooding)
- [ ] README de templates actualizado si aplica
- [ ] ADR creada si es decisión arquitectónica

## Testing

### Test Manual de Rutas

```bash
# Buscar rutas potencialmente incorrectas
cd memsys3_templates

# Estas búsquedas NO deberían tener resultados (o muy pocos falsos positivos):
grep -r "@memory/" prompts/
grep -r "@agents/" prompts/
grep -r "cp memory/" prompts/
grep -r "cp agents/" prompts/
grep -r "cd memory/" prompts/
```

### Test de Deployment

1. Crear proyecto de prueba temporal
2. Copiar `memsys3_templates/` como `memsys3/`
3. Ejecutar `@memsys3/prompts/newSession.md`
4. Verificar que todas las rutas funcionan

## Preguntas Frecuentes

### ¿Por qué no usar rutas relativas simples?

Porque cuando el usuario copia `memsys3_templates/` a su proyecto, necesita una carpeta con nombre fijo (`memsys3/`) para que todas las referencias funcionen.

### ¿Puedo cambiar la estructura de carpetas?

Técnicamente sí, pero requiere:
1. Actualizar TODOS los archivos que referencian rutas
2. Actualizar documentación
3. Actualizar guías de deployment
4. Crear ADR documentando el cambio

**Recomendación**: Solo si hay razón muy fuerte.

### ¿Qué hago si encuentro una ruta incorrecta?

1. Corregirla en `memsys3_templates/`
2. Probar en `memsys3/`
3. Commit con mensaje claro: `fix: corregir ruta en [archivo]`

### ¿Los archivos en memsys3/ necesitan las mismas rutas?

Sí, porque `memsys3/` es una instancia real del sistema. Cuando actualizamos templates, copiamos a `memsys3/` para probar.

## Convenciones

- **Templates**: `memsys3_templates/` (agnósticos)
- **Dog-fooding**: `memsys3/` (específico de memsys3)
- **Rutas en templates**: SIEMPRE con prefijo `memsys3/`
- **Commits**: Descriptivos, mencionar si afectan rutas
- **ADRs**: Para decisiones arquitectónicas significativas

---

**Última actualización**: 2025-10-31
**Mantenedor**: Dog-fooding con memsys3
**Cambios**: Añadida sección "Filosofía: Estructura y Deployment" con ADR-009
