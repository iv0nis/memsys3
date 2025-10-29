# Guía de Desarrollo de memsys3

> Documento para desarrolladores que contribuyen o modifican memsys3

## Estructura del Repositorio

```
memsys3/                          # Repositorio GitHub
├── README.md                    # README principal (público)
├── docs/                        # Documentación del desarrollo
│   ├── DEVELOPMENT.md          # Este archivo
│   └── UPDATE.md               # Guía de actualización
├── memsys3_templates/           # ⭐ PRODUCTO FINAL (lo que se distribuye)
│   ├── README.md               # Docs del sistema
│   ├── agents/                 # Templates de agents
│   ├── memory/                 # Templates de memory
│   └── prompts/                # Templates de prompts
└── memsys3/                     # 🔧 Dog-fooding (desarrollo interno)
    └── (Instancia específica para desarrollar memsys3)
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

5. **memsys3_templates/prompts/mind.md**
   - Comando: `cd memsys3/memory/viz && python3 serve.py`

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

**Última actualización**: 2025-10-29
**Mantenedor**: Dog-fooding con memsys3
