# Deploy memsys3 - Configura el Sistema Memory para tu Proyecto

Tu (DevAgent) debes configurar memsys3 por primera vez en este proyecto.

## Objetivo

Desplegar la estructura completa de memsys3 al proyecto actual desde GitHub, personalizarla e inicializarla.

## Workflow de Deployment

### Paso 1: Clonar Temporalmente memsys3

El usuario te indicará desde qué directorio trabajas. Normalmente será el directorio raíz de su proyecto.

```bash
# Verificar que no hay deployment previo
if [ -d "memsys3" ]; then
  echo "⚠️  ERROR: memsys3/ ya existe en este proyecto"
  echo ""
  echo "Parece que ya has desplegado memsys3 aquí."
  echo "Si quieres reinstalar, renombra o elimina primero:"
  echo "  mv memsys3 memsys3_backup"
  echo "  # o"
  echo "  rm -rf memsys3"
  exit 1
fi

# Limpiar memsys3_temp si existe de ejecución previa
if [ -d "memsys3_temp" ]; then
  echo "Limpiando memsys3_temp/ de ejecución previa..."
  rm -rf memsys3_temp
fi

# Clonar el repositorio como directorio temporal
git clone https://github.com/iv0nis/memsys3 memsys3_temp
```

### Paso 2: Copiar Estructura a memsys3/

Copia TODA la estructura de memsys3_templates/ al directorio memsys3/ del proyecto:

```bash
# Crear estructura base
mkdir -p memsys3/memory/full
mkdir -p memsys3/memory/templates
mkdir -p memsys3/memory/history
mkdir -p memsys3/viz
mkdir -p memsys3/prompts
mkdir -p memsys3/agents

# Crear .gitkeep en history/ para que se suba a git
touch memsys3/memory/history/.gitkeep

# Copiar templates
cp memsys3_temp/memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/

# Copiar visualizador
cp -r memsys3_temp/memsys3_templates/viz/* memsys3/viz/

# Copiar prompts
cp memsys3_temp/memsys3_templates/prompts/*.md memsys3/prompts/

# Copiar agents
cp memsys3_temp/memsys3_templates/agents/*.yaml memsys3/agents/

# Copiar README
cp memsys3_temp/memsys3_templates/memory/README.md memsys3/memory/

# Crear archivos vacíos memory/full/
cat > memsys3/memory/full/adr.yaml << 'EOF'
# ADR Log - [NOMBRE_PROYECTO]
# Architecture Decision Records del proyecto

adrs: []
EOF

cat > memsys3/memory/full/sessions.yaml << 'EOF'
# Sessions Log - [NOMBRE_PROYECTO]
# Histórico de sesiones de desarrollo

sessions: []
EOF
```

### Paso 3: Briefing con el Usuario

Antes de personalizar, lee `memsys3/memory/templates/project-status-template.yaml` para saber qué campos necesitas.

Pregunta al usuario:

1. **Nombre del proyecto**: ¿Qué estamos construyendo?
2. **Descripción 1 línea**: ¿Qué hace el proyecto?
3. **Objetivo principal**: ¿Cuál es el goal del proyecto?
4. **Stack tecnológico**:
   - Frontend (framework + versión)?
   - Backend (si aplica)?
   - Deployment platform?
5. **Fase actual**: Planificación, MVP, Beta, Producción?
6. **URLs**: Producción, staging (si existen)?
7. **Convenciones**:
   - Idioma UI?
   - Idioma variables/comentarios?

### Paso 4: Registrar Versión de memsys3

Obtén la versión y commit del repositorio clonado:

```bash
cd memsys3_temp
MEMSYS3_VERSION=$(git describe --tags --always)
MEMSYS3_COMMIT=$(git log -1 --format=%h)
cd ..
```

### Paso 5: Crear project-status.yaml

> ⚠️ **IMPORTANTE:** Este archivo va en `memsys3/memory/` (raíz de memory),
> **NO** en `memsys3/memory/full/` como `adr.yaml` y `sessions.yaml`.

Con la info recopilada, crea `memsys3/memory/project-status.yaml`:

```yaml
# Project Status - [NOMBRE_PROYECTO]

metadata:
  ultima_actualitzacio: "[DATA_AVUI]"
  actualitzat_per: "Claude (Initial Deployment)"
  fase: "[FASE]"
  memsys3_version: "[MEMSYS3_VERSION obtenida en Paso 4]"
  memsys3_deployed: "[DATA_AVUI]"

visio_general:
  que_es: "[DESCRIPCIO_1_LINIA]"
  objectiu: "[OBJECTIU_PRINCIPAL]"
  client: "[CLIENT_O_STAKEHOLDER_SI_APLICA]"

estat_actual:
  fase: "[FASE_ACTUAL]"
  ultima_feature: "Deployment inicial de memsys3"
  seguent_milestone: "[PROPER_OBJECTIU]"

features: {}

stack_tecnologic:
  frontend:
    framework: "[FRAMEWORK]"
    # Añade campos según respuesta usuario

  backend:
    # Si aplica

  deploy:
    platform: "[PLATFORM]"

urls:
  # production: "[URL_SI_EXISTE]"
  # staging: "[URL_SI_EXISTE]"

pendientes_prioritarios:
  # Si user ha mencionado tareas, añádelas
  # De lo contrario deja vacío

decisions_clau: {}
convencions_codi: {}
historic_sessions: []
```

### Paso 6: Personalizar prompts/newSession.md

Edita `memsys3/prompts/newSession.md` con la información del proyecto:

```markdown
- En este proyecto trabajaremos en [DESCRIPCION_DEL_PROYECTO].
- Actúa según las instrucciones en '@memsys3/agents/main-agent.yaml'
- [COMPORTAMIENTO_ESPECIFICO_SI_USER_HA_PEDIDO]
- Lee @memsys3/memory/project-status.yaml y @memsys3/memory/context.yaml
```

### Paso 7: Personalizar agents/main-agent.yaml (opcional)

Si el usuario ha especificado algo particular sobre el comportamiento del agente, añádelo:

```yaml
comportamiento_especific:
  [SI_USER_HA_PEDIDO]: "[INSTRUCCION]"
```

### Paso 8: Configurar .gitignore (Excluir memsys3 de GitHub)

**IMPORTANTE:** Pregunta al usuario si quiere excluir memsys3/ de GitHub.

**Razón para excluir:**
- memsys3 contiene información específica de tu flujo de trabajo con IA
- Incluye sesiones de trabajo, decisiones internas, gotchas del desarrollo
- Es contexto local que NO debe ser público en el repositorio
- Se regenera/actualiza constantemente en cada sesión

Pregunta al usuario:

---

**🔒 ¿Quieres excluir memsys3/ de GitHub?**

memsys3 contiene tu contexto de desarrollo local (sesiones, decisiones, gotchas). Esta información es útil para ti pero generalmente NO debe subirse al repositorio público.

**Opciones:**

**A) Sí, excluir memsys3/ de git (RECOMENDADO)**
- memsys3/ será ignorado por git
- No se subirá al repositorio
- Permanecerá solo en tu máquina local

⚠️ **IMPORTANTE - Limitación de Claude Code:**
Si eliges esta opción, las @ menciones NO funcionarán (ej: `@memsys3/prompts/newSession.md`).
Esto es una limitación de seguridad de Claude Code con archivos ignorados.

**Solución/Workaround:**
En lugar de usar @ menciones, dale instrucciones directas a Claude:
- ✅ **"Ejecuta memsys3/prompts/newSession.md"**
- ✅ **"Lee y ejecuta las instrucciones en memsys3/prompts/compile-context.md"**
- ❌ ~~`@memsys3/prompts/newSession.md`~~ (no funcionará)

El sistema funcionará perfectamente, solo cambia la forma de invocar los prompts.

**B) No, permitir que memsys3/ se suba a git**
- memsys3/ se incluirá en commits
- Se subirá al repositorio (público o privado)
- Útil si quieres compartir el contexto con tu equipo
- ✅ Las @ menciones funcionarán normalmente

---

**Si el usuario elige OPCIÓN A (recomendado):**

1. Lee el .gitignore existente (si existe):
   ```bash
   cat .gitignore 2>/dev/null || echo "# .gitignore no existe, se creará"
   ```

2. Verifica si memsys3/ ya está excluido:
   ```bash
   grep -q "memsys3" .gitignore 2>/dev/null && echo "✅ Ya está excluido" || echo "➕ Necesita agregarse"
   ```

3. Si NO está excluido, agrégalo al .gitignore:
   - Si .gitignore existe → usa Edit tool para agregar al final:
     ```
     # memsys3 - Sistema de gestión de contexto (local only)
     memsys3/
     ```
   - Si .gitignore NO existe → usa Write tool para crearlo:
     ```
     # memsys3 - Sistema de gestión de contexto (local only)
     memsys3/
     ```

4. Verifica que funciona:
   ```bash
   git status --short | grep memsys3
   # Si no aparece nada → ✅ correctamente ignorado
   ```

**Si el usuario elige OPCIÓN B:**

- No modificar .gitignore
- Informar que memsys3/ se incluirá en commits

### Paso 9: Eliminar Clone Temporal

```bash
rm -rf memsys3_temp
```

### Paso 10: Informar al Usuario

Confirma que el deployment se ha completado correctamente:

```
✅ memsys3 deployment completado!

Estructura creada:
- memsys3/memory/full/ (adr.yaml, sessions.yaml inicializados)
- memsys3/memory/templates/ (guías permanentes)
- memsys3/memory/history/ (para Plan Contingencia)
- memsys3/viz/ (visualizador web)
- memsys3/prompts/ (newSession, endSession, compile-context, etc.)
- memsys3/agents/ (main-agent, context-agent)

Archivos personalizados:
- memsys3/memory/project-status.yaml
- memsys3/prompts/newSession.md

Próximos pasos:
1. Compila context inicial: @memsys3/prompts/compile-context.md
2. Visualiza la memoria: @memsys3/prompts/mind.md
3. Comienza a trabajar con sesiones: @memsys3/prompts/newSession.md

Escalabilidad automática:
📈 Rotación automática: >1800 líneas → sessions_N.yaml, adr_N.yaml
📦 Plan Contingencia: >150K tokens → archivado a history/
🔍 Context compilado: máximo 2000 líneas por sesión
```

## Notas Importantes

- **Templates permanentes**: `memory/templates/` son guías que Main-Agent consultará durante endSession. NO los borres.
- **Clone temporal**: memsys3_temp/ se borra después de copiar. Es solo para deployment.
- **Personalización mínima**: Solo project-status.yaml y newSession.md necesitan personalización. Resto de archivos son agnósticos.
- **Idioma**: Pregunta al usuario qué idioma quiere para la interfaz y el código.

## Troubleshooting

**"git clone falla":**
- Verifica conexión a internet
- Comprueba que git está instalado: `git --version`

**"mkdir falla":**
- Verifica que estás en el directorio correcto del proyecto
- Comprueba permisos de escritura

**"Templates no se copian":**
- Verifica que memsys3_temp/ existe
- Comprueba que la ruta memsys3_temp/memsys3_templates/ tiene los archivos

---

**Deployment completado. El sistema está listo para usar.**
