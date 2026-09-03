# Actualizar memsys3 - Prompt de Actualización Segura

## Paso 0: Rol — Setup Agent (ADR-028)

Para este prompt actúas como **Setup Agent (SA)** — el rol responsable del **lifecycle de memsys3** en el proyecto. Tu misión es actualizar la versión instalada **sin perder nada** de lo que el proyecto haya construido encima.

- **Operaciones autorizadas del rol:** `deploy.md` (instalación inicial) + `actualizar.md` (este prompt).
- **Fuera de alcance:** sesiones de desarrollo del proyecto, `endSession.md`, backlog y ADRs (Main Agent); compilación de `context.yaml` fuera de deploy (Context Agent).
- **Referencia del rol:** `memsys3/agents/setup-agent.yaml`. **NO cargues `agents/main-agent.yaml`** — es otro rol.

**Disposición del rol — máxima atención antes de destruir nada.** Este prompt escribe sobre infraestructura que el proyecto puede haber personalizado legítimamente (ADR-032: prompts y agents son personalizables con autorización explícita del usuario, con `file_version` intocado y la divergencia documentada en `sessions.yaml`). Tu criterio contextualizado —no una lista de archivos— es lo que separa una actualización de una regresión. Regla canónica:

> **La pérdida silenciosa es peor que el conflicto ruidoso.** Toda personalización que detectes se reporta, aunque el usuario decida descartarla.

**El verbo de este prompt es MODIFICAR, no sustituir.** memsys3 se instala en proyectos cuya naturaleza no conocemos; sus prompts y agents son un punto de partida que cada proyecto amolda. Actualizar es llevarle al proyecto las mejoras de upstream **editando sus archivos**, no pisándolos con una copia. Solo se copia donde no hay destino (archivos nuevos) o donde el contrato lo dice (`memory/templates/`, `PRINCIPLES.md` — ADR-018).

**Contrato de ejecución agnóstico:** este prompt asume solo tooling estándar (lectura/escritura de archivos, shell, git). Donde se menciona una herramienta de pregunta estructurada, es opcional: si tu harness no la tiene, presenta las opciones al usuario en texto y espera respuesta.

**Contrato de idioma:** documenta y responde en el idioma predominante de los canónicos del proyecto destino (`README.md`, `memsys3/memory/project-status.yaml`, `memsys3/memory/memory.yaml`), no en el default de tu harness.

**Compilación inline NO aplica aquí** (cf. `setup-agent.yaml`, sección `compilacion_inline_en_deploy`): una sesión de actualización puede llegar cargada de tokens y sesgaría la síntesis del Context Agent. `actualizar.md` cierra sin compilar — el usuario decide cuándo ejecutar `compile-context.md` en sesión nueva.

Este prompt complementa `deploy.md` (que es para deployment inicial).

---

## ⚠️ ANTES DE EMPEZAR

### Paso 0a: Identificar tu memsys3

**CRÍTICO — ejecuta esto ANTES de cualquier otra operación:**

```bash
PROJECT_ROOT=$(pwd)
MEMSYS3_ROOT="$PROJECT_ROOT/memsys3"

if [ -f "$MEMSYS3_ROOT/memory/project-status.yaml" ]; then
  echo "✅ memsys3 encontrado: $MEMSYS3_ROOT"
  grep "memsys3_version" "$MEMSYS3_ROOT/memory/project-status.yaml" | head -1
else
  echo "⚠️ memsys3/ no encontrado en $(pwd)"
  echo "Buscando memsys3/ disponibles (máx profundidad 4)..."
  CANDIDATES=$(find . -maxdepth 4 -path "*/memsys3/memory/project-status.yaml" 2>/dev/null | sed 's|/memory/project-status.yaml$||')
  COUNT=$(echo "$CANDIDATES" | grep -c . 2>/dev/null || echo 0)
  if [ "$COUNT" -eq 1 ]; then
    MEMSYS3_ROOT="$(cd "$CANDIDATES" && pwd)"
    echo "✅ memsys3 encontrado (único): $MEMSYS3_ROOT"
  elif [ "$COUNT" -gt 1 ]; then
    echo "⚠️ Múltiples memsys3 encontrados:"
    echo "$CANDIDATES"
    echo "Pregunta al usuario cuál usar para esta actualización."
  else
    echo "❌ No se encontró ningún memsys3. ¿Has desplegado memsys3? Usa @memsys3/prompts/deploy.md"
  fi
fi

# Limpiar artefactos de ejecuciones anteriores
rm -rf memsys3_update_temp memsys3_templates 2>/dev/null
echo "Artefactos previos limpiados"
echo "PROJECT_ROOT=$PROJECT_ROOT"
echo "MEMSYS3_ROOT=$MEMSYS3_ROOT"
```

**Si no encuentra memsys3 o hay múltiples:** detente. Pregunta al usuario y NO continúes hasta confirmarlo.

**Si encuentra memsys3:** continúa con el bootstrap.

**IMPORTANTE:** Todos los pasos siguientes deben usar `$MEMSYS3_ROOT` para referirse a memsys3 y `$PROJECT_ROOT` para la raíz del proyecto. Evita `cd` siempre que sea posible.

> **Nota sobre monorepos/submodules:** Un proyecto puede contener múltiples instancias de memsys3 (monorepo, submodules, workspaces). La detección automática prioriza `$(pwd)/memsys3`. Si hay ambigüedad, el usuario decide.

### Paso 0b: Bootstrap — actualizar este prompt antes de continuar

```bash
git clone https://github.com/iv0nis/memsys3 memsys3_update_temp
echo "Bootstrap: la versión más reciente de este prompt está en memsys3_update_temp/memsys3_templates/prompts/actualizar.md"
```

**Ahora lee `memsys3_update_temp/memsys3_templates/prompts/actualizar.md` y continúa desde el Paso 1 de ESE archivo.** El resto de este prompt puede estar desactualizado.

> **Por qué el bootstrap NO sobrescribe `memsys3/prompts/actualizar.md`:** este prompt es infraestructura de `prompts/` como cualquier otro y ADR-032 lo hace personalizable. Sobrescribirlo aquí, antes de recuperar su base, sería exactamente la pérdida silenciosa que el Paso 6.2 prohíbe. La copia local se reconcilia en la matriz del Paso 6.1 como todos los demás; para ejecutar, se lee directamente del clone.

---

**Verifica que estás en el proyecto correcto:**
1. Este proyecto YA tiene memsys3 instalado (carpeta `memsys3/`)
2. Si NO tiene memsys3, usa `@memsys3/prompts/deploy.md` en su lugar

---

## 🚨 PASO 0: Detectar Estructura Antigua Incompatible

**CRÍTICO:** Antes de actualizar, debemos verificar si existe una estructura antigua PRE-ADR-006 (pre-v0.2.0).

### Detectar estructura antigua

Ejecuta:

```bash
# Verificar si existe carpeta /memory en raíz (NO dentro de memsys3/)
ls -la memory/ 2>/dev/null && echo "⚠️ ESTRUCTURA ANTIGUA DETECTADA" || echo "✅ Estructura nueva OK"

# Verificar si memsys3/ existe
ls -la memsys3/ 2>/dev/null && echo "✅ memsys3/ existe" || echo "❌ memsys3/ NO existe"
```

**Escenarios posibles:**

### Escenario A: Solo `/memory` (estructura pre-ADR-006)

```
proyecto/
├── memory/           ← Estructura antigua (sin prefijo memsys3/)
│   ├── full/
│   ├── templates/
│   ├── prompts/
│   └── project-status.yaml
└── (NO hay memsys3/)
```

**Diagnóstico:** Sistema de memoria antigua, **incompatible** con memsys3 actual.

**Acción:** **NO usar actualizar.md**. Esto requiere **migración completa**:
1. Backup completo de `/memory`
2. Ejecutar `@memsys3/prompts/deploy.md` (deployment desde cero)
3. Migrar datos manualmente:
   - Copiar `memory/full/sessions.yaml` → `memsys3/memory/full/`
   - Copiar `memory/full/adr.yaml` → `memsys3/memory/full/`
   - Copiar `memory/project-status.yaml` → `memsys3/memory/` (agregar campos versión)
4. Borrar `/memory` antigua después de validar

### Escenario B: `/memory` + `/memsys3` coexistiendo

```
proyecto/
├── memory/           ← Estructura antigua CON DATOS REALES
│   ├── full/
│   └── project-status.yaml
└── memsys3/          ← Estructura nueva PERO con datos template sin personalizar
    └── memory/
```

**Diagnóstico:** Deployment inicial se hizo INCORRECTAMENTE. Se desplegó memsys3/ pero NO se migraron datos de /memory.

**🚨 ESTO ES LO QUE PASÓ EN UN PROYECTO CLIENTE ANTERIOR**

**Síntomas:**
- `/memory/project-status.yaml` tiene datos del proyecto real
- `/memsys3/memory/project-status.yaml` tiene datos copiados del template memsys3 (descripciones genéricas, "Sistema de gestió de context...", etc.)

**Acción:** **Migración de datos antes de actualizar**:

```bash
# 1. Backup de ambas estructuras
cp -r memory memory_backup_old_$(date +%Y%m%d)
cp -r memsys3 memsys3_backup_$(date +%Y%m%d)

# 2. Migrar datos REALES de /memory a /memsys3/memory
cp memory/full/sessions.yaml memsys3/memory/full/
cp memory/full/adr.yaml memsys3/memory/full/
cp memory/project-status.yaml memsys3/memory/

# 3. Agregar campos de versión a memsys3/memory/project-status.yaml
# (editar manualmente metadata: agregar memsys3_version, memsys3_deployed)

# 4. AHORA SÍ, continuar con actualizar.md desde Paso 1
```

**Después de validar que funciona:**
```bash
# Borrar estructura antigua (solo después de validar)
rm -rf memory_backup_old_* memory/
```

### Escenario C: Solo `/memsys3` (estructura nueva)

```
proyecto/
└── memsys3/          ← Estructura correcta
    └── memory/
        ├── full/
        ├── templates/
        └── project-status.yaml (con memsys3_version)
```

**Diagnóstico:** Estructura correcta, deployment hecho correctamente.

**Acción:** ✅ Continuar con **Paso 0.5** normalmente.

---

## Paso 0.5: Contexto del proyecto — ingesta tipo Context Agent

**DEBES ejecutar este paso AHORA, antes de tocar ningún archivo.** Sin contexto del proyecto, las operaciones inteligentes de este prompt (sustitución diferencial ADR-018, deprecation contextualizada ADR-019, reconciliación de personalizaciones ADR-032) degradan a sustitución ciega — que es exactamente el fallo que este prompt existe para evitar.

Hazte una ingesta del proyecto destino con criterio inteligente, equivalente a lo que hace el Context Agent, **solo para tu propio uso en esta ejecución**: NO compilas `context.yaml`, NO escribes nada en `memory/`.

```bash
# Identidad del proyecto destino
cat "$PROJECT_ROOT/README.md" 2>/dev/null

# Estado y memoria del proyecto
cat "$MEMSYS3_ROOT/memory/project-status.yaml"
cat "$MEMSYS3_ROOT/memory/memory.yaml" 2>/dev/null

# Principios y decisiones locales (overrides si existen)
[ -f "$MEMSYS3_ROOT/PRINCIPLES.md" ] && cat "$MEMSYS3_ROOT/PRINCIPLES.md"
[ -f "$MEMSYS3_ROOT/memory/full/adr.yaml" ] && cat "$MEMSYS3_ROOT/memory/full/adr.yaml"
```

**Divergencias documentadas (ADR-032) — lectura OBLIGATORIA.** Cuando un proyecto personaliza un prompt o un agent con autorización explícita, el contrato le exige documentar esa divergencia en su bitácora. Ahí está el **por qué** de cada personalización que vas a encontrar en el Paso 6:

```bash
# Buscar divergencias / personalizaciones declaradas en la bitácora del proyecto
grep -niE "divergencia|personaliza|ADR-032|parche local" \
  "$MEMSYS3_ROOT/memory/full/sessions.yaml" \
  "$MEMSYS3_ROOT/memory/full/sessions_"*.yaml 2>/dev/null | head -40
```

**NO leer:** `agents/main-agent.yaml` (SA es otro rol; cargar MA cruza alcance).

**Criterio, no calculadora.** Con este contexto juzgarás en los Pasos 6.x qué adaptar de lo nuevo agnóstico al perfil específico de ESTE proyecto. No uses heurísticas de "peso de actualización" para decidir por ti: el agente contextualizado decide mejor que un calculador (principio #5).

**Salida del paso** (entendimiento interno, no archivo): (a) qué archivos de `prompts/`/`agents/` declara el proyecto como personalizados y por qué; (b) ADRs locales que puedan conflictuar con cambios agnósticos entrantes; (c) campos de `project-status.yaml` personalizados; (d) deprecations upstream que estén en uso real en `memory/full/`; (e) preferencias en `memory.yaml` que afecten a cómo aplicar los cambios.

> **Nota coop (multi-usuario).** Un proyecto puede tener varias personas trabajando en ramas distintas. No asumas un único usuario ni una rama concreta: las convenciones de identidad, rama y tag pertenecen al proyecto, no a este prompt.

---

## Paso 1: Verificar Versión Actual

Lee el archivo del proyecto:

```bash
cat "$MEMSYS3_ROOT/memory/project-status.yaml" | grep -A2 "metadata:"

# Fijar la versión desplegada como variable — se usa en los Pasos 2.5, 6.1 y 6.2.
# El campo aparece en formatos distintos según la versión que lo escribió:
#   "v0.29.0" · "v0.31.0-8-gbf0bff9" (git describe) · "v0.28.0 (commit: 93cde0f)"
# Solo los dos primeros son commit-ish válidos. Normalizar: si hay hash de commit
# explícito, es la señal más precisa (lo que se entregó de verdad); si no, el describe/tag.
RAW_VERSION=$(grep "memsys3_version" "$MEMSYS3_ROOT/memory/project-status.yaml" | head -1 | sed 's/.*: "\(.*\)"/\1/')
CURRENT_VERSION=$(echo "$RAW_VERSION" | grep -oE 'commit: [0-9a-f]{7,40}' | sed 's/commit: //')
[ -z "$CURRENT_VERSION" ] && CURRENT_VERSION=$(echo "$RAW_VERSION" | grep -oE '^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9]+-g[0-9a-f]+)?')
echo "memsys3_version bruto: '$RAW_VERSION' → CURRENT_VERSION='$CURRENT_VERSION'"
```

Tras el Paso 0b (clone disponible), **verifica que resuelve** antes de seguir:

```bash
git -C memsys3_update_temp cat-file -e "$CURRENT_VERSION^{commit}" 2>/dev/null \
  && echo "✅ CURRENT_VERSION resuelve en upstream" \
  || echo "🚨 CURRENT_VERSION NO resuelve — la base no será recuperable (ver Paso 6.2 §1)"
```

**Busca los campos:**
- `memsys3_version`: Versión actual instalada — **es la señal que permite recuperar la BASE** de cada archivo del template tal como se entregó (Paso 6.2). Si falta, no resuelve o es inexacta, la reconciliación degrada a revisión asistida: anótalo y avisa al usuario.
- `memsys3_deployed`: Fecha del último deployment/actualización

**Si NO existen estos campos:**
- Significa que tienes una versión muy antigua (pre-v0.5.0)
- La actualización será más compleja (muchos cambios estructurales)

**Anota la versión actual aquí:** `[VERSIÓN_ACTUAL]`

---

## Paso 2: Verificar Última Versión Disponible

Consulta GitHub para ver la última versión:

```bash
git ls-remote --tags https://github.com/iv0nis/memsys3 | tail -5
```

**Identifica la última versión estable (tag más reciente):** `[VERSIÓN_NUEVA]`

> ⚠️ **La fuente de verdad de la versión es el último tag** (`git tag --sort=-v:refname | head -1` tras `git fetch --tags`). `CHANGELOG.md` puede estar desactualizado respecto a tags publicados — NO uses su última entrada como `[VERSIÓN_NUEVA]`. Caso documentado: informe de campo `2026-05-27` §4.5.

**¿Vale la pena actualizar?**
- Si la diferencia es < 2 versiones patch (ej: v0.5.1 → v0.5.2): actualización menor
- Si la diferencia es >= 1 versión minor (ej: v0.4.0 → v0.5.0): actualización importante
- Si es >= 1 versión major (ej: v0.x → v1.x): actualización crítica (revisar CHANGELOG)

---

## Paso 2.5: Elegir Modo de Actualización

**Antes de preguntar, calcula el salto y muestra una recomendación** (el usuario decide, principio #4):

```bash
# Salto entre la versión desplegada y la última publicada
git -C memsys3_update_temp rev-list --count "$CURRENT_VERSION..HEAD" 2>/dev/null \
  | xargs -I{} echo "Commits upstream desde $CURRENT_VERSION: {}"
git -C memsys3_update_temp tag --sort=v:refname --contains "$CURRENT_VERSION" 2>/dev/null \
  | grep -vxF "$CURRENT_VERSION" | wc -l | xargs -I{} echo "Tags publicados después de $CURRENT_VERSION: {}"
```

**Criterio orientativo** (no bloqueante): salto < 2 versiones minor → *Rápida* suele bastar. Salto ≥ 2 minor, o cualquier major → recomienda *Extendida*: hay más superficie donde una personalización puede colisionar con un cambio estructural.

Pregunta al usuario (si tu harness tiene preguntas estructuradas, úsalas; si no, presenta las dos opciones en texto):

```
Pregunta: "¿Qué modo de actualización prefieres?"
Opciones:
  - "Rápida": usa git diff para detectar cambios. Eficiente en tokens.
  - "Extendida": lanza un subagente que se contextualiza con el memsys3 de desarrollo
    (lee sessions, ADRs, context.yaml del repo) para entender QUÉ cambió y POR QUÉ.
    Habilita evaluación contextualizada de deprecations y campos huérfanos (ADR-019).
    Consume más tokens pero da mejor comprensión de los cambios.
Recomendación: [la calculada arriba, con el salto medido]
```

**Si el usuario elige "Extendida":**

Lanza un subagente (Agent tool) con este prompt:

```
Carga el contexto del proyecto memsys3 desde el repo clonado en memsys3_update_temp/:

1. Lee memsys3_update_temp/memsys3/prompts/newSession.md y sigue sus instrucciones,
   pero usando memsys3_update_temp/memsys3/ como raíz (en lugar de ./memsys3/)
2. Una vez contextualizado, analiza qué cambió entre [VERSION_ACTUAL] y [VERSION_NUEVA]:
   - git log --oneline [VERSION_ACTUAL]..[VERSION_NUEVA] en memsys3_update_temp/
   - Cruza los commits con las sesiones documentadas en sessions.yaml
   - Identifica: features nuevas, breaking changes, archivos eliminados, decisiones arquitectónicas
3. Devuelve un informe estructurado:
   - Cambios críticos que afectan al proyecto del usuario
   - Breaking changes y cómo mitigarlos
   - Archivos nuevos/eliminados/modificados con contexto de por qué
   - Recomendaciones para la actualización
```

Espera el resultado del subagente y úsalo para guiar los pasos siguientes con mejor comprensión.

**Si el usuario elige "Rápida":** Continúa directamente con Paso 3.

---

## Paso 3: Clonar Nueva Versión Temporalmente

**IMPORTANTE:** NO borres nada aún, solo clona para comparar.

```bash
# Si el bootstrap (Paso 0b) ya clonó el repo, reutilizarlo — no clonar de nuevo
if [ -d "memsys3_update_temp" ]; then
  echo "Reutilizando clone del bootstrap"
else
  git clone https://github.com/iv0nis/memsys3 memsys3_update_temp
fi

cd memsys3_update_temp

# Obtener versión exacta
NEW_VERSION=$(git describe --tags --always)
NEW_COMMIT=$(git log -1 --format=%h)

echo "Nueva versión: $NEW_VERSION (commit: $NEW_COMMIT)"

cd ..
```

> **Nota:** Si `memsys3_update_temp/memsys3_templates/prompts/actualizar.md` difiere del archivo que estás leyendo ahora, usa el del repo clonado como referencia — tiene la versión más reciente.

---

## Paso 4: Categorizar Archivos — regla por categoría, NO lista por nombre

**La categoría de un archivo se deduce de DÓNDE VIVE, nunca de una lista de nombres.** Una lista hardcodeada envejece con cada release y, peor, decide a priori que un archivo "no está personalizado" cuando el único modo de saberlo es comprobarlo (Paso 6.2). Ese fue el mecanismo por el que actualizaciones anteriores borraron personalizaciones legítimas en silencio.

| Categoría | Qué incluye (regla, no lista) | Tratamiento |
|---|---|---|
| 🚫 **DATOS del proyecto** | **Todo** lo que cuelgue de `memsys3/memory/` **salvo** `memory/templates/`, más `memsys3/backlog/` y lo que viva en `memsys3/docs/` sin equivalente en el template (backups, actas, informes) | **NUNCA SOBRESCRIBIR.** Única excepción: el bloque `metadata` de `project-status.yaml` (Paso 7). |
| 🔄 **INFRAESTRUCTURA ADAPTABLE** | **Todo** archivo de `memsys3/prompts/` y `memsys3/agents/` | **El SA MODIFICA el destino** (Paso 6.2): lee origen, destino y base, aplica al destino los cambios de upstream y conserva lo que es del proyecto. Nunca se sustituye por copia. |
| 📐 **SCHEMA / CONTRATO** | `memsys3/memory/templates/*`, `memsys3/PRINCIPLES.md`, `AGENTS.md` raíz y stubs Capa 3 | **Sustitución diferencial** por `file_version` (Pasos 6.4, 6.6, 6.6.5, 6.6.6). El proyecto no los edita por contrato. |
| 📄 **DOCUMENTACIÓN DEL SISTEMA** | `memsys3/memory/README.md` y los archivos de `memsys3/docs/` que **sí** existen en el template (p. ej. `docs/reference.md`) | Copiar (Paso 6.1 fila "resto" / 6.7). Sin merge: son documentación de memsys3, no del proyecto. |
| 🧩 **CUSTOM del proyecto** | Archivos que existen en el proyecto y **no** en el template | **Preservar intactos** (detectados en Paso 5.5). |

**Por qué DATOS es una regla y no una lista:** así cubre por construcción los archivos de datos que aún no existen cuando lees esto (rotaciones `sessions_N.yaml`, `adr_N.yaml`, `operations_N.log`, `history/`, y cualquier fichero de datos que versiones futuras añadan a `memory/`, p. ej. configuración de equipo). Si dudas de si algo es dato o infraestructura, pregúntate quién lo escribe: **si lo escribe el proyecto trabajando, es dato.**

**Por qué `prompts/` y `agents/` van enteros a RECONCILIABLE:** ADR-032 los declara personalizables con autorización explícita del usuario (`file_version` intocado + divergencia documentada en `sessions.yaml`). Un proyecto que cumplió el contrato a la perfección **no puede** perder su trabajo aquí. Incluye `newSession.md`, `main-agent.yaml`, `context-agent.yaml` y **todos** los demás prompts sin distinción.

---

## Paso 5: Crear Backup de Seguridad

Antes de tocar NADA, crea un backup:

```bash
# Proteger los backups en .gitignore ANTES de crearlos (ISSUE-006).
# Los backups contienen sessions/memory/decisiones: NUNCA deben versionarse,
# aunque memsys3/ sí lo esté. Idempotente; si el proyecto no usa git, se omite.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BACKUPS_REL="${MEMSYS3_ROOT#$(pwd)/}/docs/backups/"
  if grep -qxF "$BACKUPS_REL" .gitignore 2>/dev/null; then
    echo "✅ $BACKUPS_REL ya está en .gitignore"
  else
    printf '\n# memsys3 — backups de actualización (temporales, nunca versionar)\n%s\n' "$BACKUPS_REL" >> .gitignore
    echo "✅ Añadido $BACKUPS_REL a .gitignore"
  fi
fi

# Crear directorio de backups si no existe
mkdir -p "$MEMSYS3_ROOT/docs/backups"

# Migrar backups antiguos de la raíz (si los hay)
for old_backup in memsys3_backup_*/; do
  [ -d "$old_backup" ] && mv "$old_backup" "$MEMSYS3_ROOT/docs/backups/$old_backup" && echo "Migrado: $old_backup"
done

# Crear backup actual (fuera de memsys3/ para evitar auto-recursión)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
rsync -a --exclude='docs/backups' "$MEMSYS3_ROOT/" memsys3_backup_temp_$TIMESTAMP/
mv memsys3_backup_temp_$TIMESTAMP "$MEMSYS3_ROOT/docs/backups/memsys3_backup_$TIMESTAMP"

echo "Backup creado en: $MEMSYS3_ROOT/docs/backups/memsys3_backup_$TIMESTAMP"

# Limpiar backups antiguos (máx 3: 2 anteriores + actual)
cd "$MEMSYS3_ROOT/docs/backups"
ls -dt memsys3_backup_* | tail -n +4 | xargs rm -rf
echo "Backups antiguos limpiados (máx 3)"
cd -
```

**CRÍTICO:** Si algo sale mal, puedes restaurar con:
```bash
cp -r memsys3/docs/backups/memsys3_backup_$TIMESTAMP memsys3_restored
# Luego renombrar memsys3_restored a memsys3 si es necesario
```

---

## Paso 5.5: Detectar Archivos Custom del Proyecto

**Antes de actualizar, identifica archivos que el usuario creó y NO pertenecen al template.**

```bash
echo "=== Detectando archivos custom del proyecto ==="
echo "MEMSYS3_ROOT=$MEMSYS3_ROOT"

# Pasada 0: raíz de memsys3/ NO recursiva (customs sueltos en la raíz quedaban ciegos)
for f in "$MEMSYS3_ROOT"/*.md "$MEMSYS3_ROOT"/*.yaml; do
  [ -f "$f" ] || continue
  relative="${f#$MEMSYS3_ROOT/}"
  if [ ! -f "memsys3_update_temp/memsys3_templates/$relative" ]; then
    echo "  CUSTOM (raíz): $relative"
  fi
done

for dir in prompts agents docs; do
  if [ -d "$MEMSYS3_ROOT/$dir" ]; then
    find "$MEMSYS3_ROOT/$dir" -type f | while read f; do
      relative="${f#$MEMSYS3_ROOT/}"
      if [ ! -f "memsys3_update_temp/memsys3_templates/$relative" ]; then
        echo "  CUSTOM: $relative"
      fi
    done
  fi
done

echo ""
echo "Los archivos CUSTOM se preservarán intactos durante la actualización."
echo "=== Fin detección ==="
```

**Si hay archivos custom:** No requiere acción. La actualización solo tocará archivos del template.

> ⚠️ **Punto ciego de este paso — cúbrelo en el Paso 6.2.** Aquí se detectan **ficheros** custom (existen en el proyecto y no en el template), no **contenido** custom. Un archivo del template con 40 líneas añadidas por el proyecto pasa este filtro como si estuviera intacto. Detectar eso es trabajo del Paso 6.2 (comparación contra la base), y es donde se perdían las personalizaciones antes de esta versión.

**Si detectas un archivo que existe tanto en el proyecto como en el template nuevo, pero NO existía en la versión anterior del template** (puedes verificar en el backup): es un potencial conflicto. En ese caso:

```
⚠️ CONFLICTO: [archivo] existe en tu proyecto Y en el template nuevo.
   Se preserva tu versión. Revisa manualmente si quieres la del template.
```

**Principio:** En caso de duda, preservar lo del usuario. Lo del template siempre se puede recuperar del repo.

---

## Paso 6: Actualizar Archivos del Sistema

```bash
# Crear directorios necesarios (siempre, antes de copiar nada)
mkdir -p "$MEMSYS3_ROOT/docs" "$MEMSYS3_ROOT/docs/backups" "$MEMSYS3_ROOT/prompts" "$MEMSYS3_ROOT/agents" "$MEMSYS3_ROOT/memory/templates"

# Crear backlog/ si no existe
if [ ! -f "$MEMSYS3_ROOT/backlog/README.md" ]; then
  mkdir -p "$MEMSYS3_ROOT/backlog"
  echo "# Backlog" > "$MEMSYS3_ROOT/backlog/README.md"
  echo "backlog/ creado"
fi

# Crear backlog/docs/ si no existe (ADR-021: informe/plan opcionales)
if [ ! -d "$MEMSYS3_ROOT/backlog/docs" ]; then
  mkdir -p "$MEMSYS3_ROOT/backlog/docs"
  touch "$MEMSYS3_ROOT/backlog/docs/.gitkeep"
  echo "backlog/docs/ creado (ADR-021)"
fi
```

### 6.0 Helpers (definir una vez, ANTES de 6.1)

Los pasos 6.2 a 6.6.6 los usan. Defínelos aquí para que el orden de ejecución no importe:

```bash
# file_version de un archivo, sea cual sea su formato:
#   .md → "<!-- version: X.Y.Z -->" · agents/*.yaml → 'file_version: "X.Y.Z"' · templates → "# version: X.Y.Z"
extract_any_version() {
  { grep -E "<!--\s*version:" "$1" 2>/dev/null | head -1 | sed -E 's/.*version:\s*([0-9.]+).*/\1/'
    grep -E "^file_version:" "$1" 2>/dev/null | head -1 | sed -E 's/.*:\s*//' | tr -d '"'
    grep -E "^#\s*version:" "$1" 2>/dev/null | head -1 | sed -E 's/^#\s*version:\s*//' | tr -d '"'
  } | grep . | head -1
}
extract_version()    { extract_any_version "$1"; }   # alias histórico (Paso 6.4)
extract_md_version() { extract_any_version "$1"; }   # alias histórico (Pasos 6.6, 6.6.5, 6.6.6)

# Comparar versiones (devuelve "gt", "eq", "lt": v1 respecto a v2)
compare_versions() {
  local v1="$1" v2="$2"
  if [ "$v1" = "$v2" ]; then echo "eq"; return; fi
  local sorted=$(printf "%s\n%s" "$v1" "$v2" | sort -V | head -1)
  if [ "$sorted" = "$v1" ]; then echo "lt"; else echo "gt"; fi
}

# Recuperar la BASE de un archivo del template (ruta relativa, p.ej. prompts/endSession.md)
# en $BASE_FILE. Devuelve 0 si la recuperó, 1 si no hay base fiable.
#   Señal 1: el commit desplegado ($CURRENT_VERSION) → lo que se entregó de verdad.
#   Señal 2: si la señal 1 no resuelve, el último commit upstream cuyo file_version
#            coincide con el del archivo LOCAL (sobrevive a actualizaciones parciales,
#            en las que project-status no describe bien lo instalado).
BASE_FILE="memsys3_update_temp/.base.tmp"
recover_base() {
  local rel="$1" local_file="$MEMSYS3_ROOT/$1" c v_local v_c
  rm -f "$BASE_FILE"
  if git -C memsys3_update_temp show "$CURRENT_VERSION:memsys3_templates/$rel" > "$BASE_FILE" 2>/dev/null \
     && [ -s "$BASE_FILE" ]; then
    echo "   base: señal 1 ($CURRENT_VERSION)"; return 0
  fi
  v_local=$(extract_any_version "$local_file")
  if [ -n "$v_local" ]; then
    for c in $(git -C memsys3_update_temp log --format=%H -- "memsys3_templates/$rel"); do
      git -C memsys3_update_temp show "$c:memsys3_templates/$rel" > "$BASE_FILE" 2>/dev/null || continue
      v_c=$(extract_any_version "$BASE_FILE")
      if [ "$v_c" = "$v_local" ]; then echo "   base: señal 2 (file_version $v_local → ${c:0:7})"; return 0; fi
    done
  fi
  rm -f "$BASE_FILE"; echo "   base: NO recuperable"; return 1
}
```

> Varios commits upstream pueden compartir `file_version` (fixes editoriales sin bump): la señal 2 toma el más reciente, que puede no ser exactamente el entregado → posibles falsos "personalizado" (ruido, nunca pérdida). Por eso la señal 1 es la principal.

### 6.1 Matriz A / M / D — qué hacer con cada archivo que cambió upstream

**Estrategia principal: `git diff --name-status`**

```bash
echo "Versión desplegada: $CURRENT_VERSION"

# Qué archivos cambiaron upstream, con estado (A=añadido, M=modificado, D=eliminado)
git -C memsys3_update_temp diff --name-status "$CURRENT_VERSION" HEAD -- memsys3_templates/
```

> ⚠️ Este diff responde a *"¿qué cambió upstream?"*, **nunca** a *"¿qué cambió el proyecto?"*. Por sí solo describe una sincronización unidireccional. La segunda pregunta la responde el Paso 6.2 comparando contra la BASE; sin él, esto no es un merge por mucho que lo llamemos así.

**Checkpoint antes de ejecutar.** Cuenta y muestra al usuario:

```
Archivos a añadir (A): X
Archivos a reconciliar (M): Y
Archivos eliminados upstream (D): Z
```

**Tabla de despacho — para cada archivo del diff:**

| Estado | Categoría del archivo (Paso 4) | Acción |
|---|---|---|
| **A** | cualquiera | ¿Ya existe en el proyecto? **No** → copiar. **Sí** → es un custom del proyecto con el mismo nombre: **preservar el del proyecto** y reportar `⚠️ CONFLICTO: [archivo] existe en tu proyecto Y en el template nuevo. Se preserva tu versión.` |
| **M** | 🔄 `prompts/` o `agents/` | **Paso 6.2**: el SA edita el destino aplicándole los cambios de upstream. NUNCA `cp`. |
| **M** | 📐 `memory/templates/`, `PRINCIPLES.md` | Pasos 6.4 / 6.6 (sustitución diferencial por `file_version`). |
| **M** | 🚫 datos | No tocar (no debería aparecer: el template no contiene datos del proyecto). |
| **M** | resto (`memory/README.md`, `docs/`) | Copiar al path equivalente en `memsys3/`. |
| **D** | cualquiera | **Paso 6.3** (leak vs custom). NUNCA borrar directo. |

Mapeo de rutas para las copias: `memsys3_templates/prompts/X` → `memsys3/prompts/X`; ídem `docs/`, `agents/`, `memory/`. Los archivos en la **raíz** del template (p. ej. `per-tool-stub-template.md`) van a la raíz de `memsys3/`; excepciones con paso propio: `PRINCIPLES.md` (6.6) y `AGENTS.md`, que va a la raíz del **proyecto** (6.6.5).

**IMPORTANTE:** los archivos custom detectados en el Paso 5.5 NO se tocan en ningún caso.

**Acumula un registro de reconciliación** mientras recorres la matriz — lo necesitarás en el resumen final, en `operations.log` (Paso 11) y en `sessions.yaml` (Paso 10):

```
RECONCILIACIÓN
  <ruta> · <A|M|D> · <sin-personalización | personalizado> · <acción tomada> · <ruta del backup>
```

**Si git diff funciona, NO ejecutes el fallback. Son mutuamente excluyentes.**

---

**Fallback: copia dinámica (SOLO si git diff falla — error de salida, versión no encontrada)**

Sin `git diff` no sabes qué cambió upstream, pero el Paso 6.2 no lo necesita: lee origen y destino (y la base si `recover_base` la trae) y edita. Por eso el fallback **no copia prompts ni agents** — los pasa por 6.2 uno a uno, igual que la ruta principal.

```bash
# Prompts y agents: NO se copian aquí. Recórrelos y aplícales el Paso 6.2 uno a uno.
find memsys3_update_temp/memsys3_templates/prompts/ memsys3_update_temp/memsys3_templates/agents/ -type f \
  | sed "s|memsys3_update_temp/memsys3_templates/||" \
  | sed 's/^/  RECONCILIAR (Paso 6.2): /'

# Copiar docs (sin borrar — preserva archivos custom del proyecto)
find memsys3_update_temp/memsys3_templates/docs/ -type f | while read f; do
  relative="${f#memsys3_update_temp/memsys3_templates/}"
  mkdir -p "$MEMSYS3_ROOT/$(dirname "$relative")"
  cp "$f" "$MEMSYS3_ROOT/$relative"
done
echo "Docs actualizados (sin borrar custom)"
```

> **⚠️ NUNCA hacer `rm -f memsys3/docs/*.md` ni borrar carpetas enteras.** Eso destruye archivos custom del proyecto. Solo sobrescribir archivos que vienen del template.

### 6.2 Actualizar `prompts/` y `agents/` — el SA MODIFICA el destino, no lo sustituye

**Aplica a TODO archivo `M` de `prompts/` o `agents/`, sin excepciones ni listas.**

**La idea de memsys3, aplicada a este paso.** memsys3 se instala en proyectos cuya naturaleza no conocemos de antemano; los prompts y agents son un punto de partida que cada proyecto amolda, y esa adaptación es lo valioso. El template trae **mejoras**; el destino tiene **sentido**. Por eso aquí el verbo nunca es *copiar*: es **leer el origen y el destino, entender qué cambió upstream y qué es del proyecto, y editar el destino para llevarle las mejoras sin quitarle el sentido**. Eso solo lo hace un agente que entiende el proyecto (Paso 0.5), no un script que compara bytes.

**1. Consigue los tres puntos de vista.** Un diff de dos puntos (destino vs origen) no distingue "línea que añadió el proyecto" de "línea que eliminó upstream". La **BASE** —el template tal como se entregó— es lo que te permite leer el diff con sentido. El helper `recover_base` (Paso 6.0) la trae; **es contexto para tu lectura, no un decisor**:

```bash
REL="prompts/endSession.md"          # ruta relativa dentro del template (ejemplo)
SRC="memsys3_update_temp/memsys3_templates/$REL"
DST="$MEMSYS3_ROOT/$REL"

echo "▶ $REL"
if recover_base "$REL"; then
  diff "$BASE_FILE" "$DST" ; echo "--- (arriba: lo que el PROYECTO cambió sobre la base) ---"
  diff "$BASE_FILE" "$SRC" ; echo "--- (arriba: lo que UPSTREAM cambió sobre la base) ---"
else
  echo "ℹ️ sin base recuperable — lees con dos puntos de vista; extrema la cautela"
  diff "$DST" "$SRC"        ; echo "--- (arriba: destino vs origen, sin base) ---"
fi
```

**2. Lee y entiende antes de tocar.** Con los dos diffs delante y el contexto del Paso 0.5:

- Lee la **divergencia documentada** de ese archivo en `sessions.yaml`: te dice **por qué** existe cada cambio del proyecto. Si no está documentada, no por eso es ruido — pregúntate qué necesidad del proyecto resuelve.
- Identifica qué trae upstream: nuevas secciones, pasos reordenados, fixes, texto reescrito.
- Identifica qué es del proyecto: pasos añadidos, redacciones adaptadas a su dominio, reglas propias, idioma.

**3. Edita el destino.** Aplícale al archivo del proyecto los cambios de upstream, **conservando lo que es del proyecto**:

- Si el proyecto no cambió nada sobre la base (el primer diff está vacío), el resultado de aplicar upstream coincide con el origen — es el único caso en que el destino acaba idéntico al template, y llegas ahí editando, no pisando.
- Si el cambio del proyecto toca una zona que upstream reescribió, **adapta** el cambio del proyecto a la estructura nueva; no lo descartes por incómodo.
- Si un cambio del proyecto y uno de upstream son genuinamente incompatibles, **pregunta al usuario** con ambos delante. No decidas tú una pérdida.
- **Nunca** resuelvas "a favor del template porque es lo canónico": el template siempre se recupera del repo; lo del proyecto puede no existir en ningún otro sitio.
- Sin base recuperable, la misma operación con menos certeza: ante cualquier duda de a quién pertenece una línea, conserva y pregunta.
- El archivo resultante lleva el **`file_version` de upstream** (la versión del template sobre la que ahora se asienta la adaptación del proyecto), para que la próxima actualización recupere la base correcta. Si reubicaste o adaptaste una personalización, dilo en la entrada del Paso 10.

**4. Reporta SIEMPRE.** Todo cambio del proyecto que hayas encontrado entra en el registro de reconciliación con: ruta, qué era (diff concreto), qué hiciste con él (conservado / adaptado / preguntado al usuario), y ruta del backup del Paso 5. Esa información viaja al resumen final, al Checklist, a `operations.log` (Paso 11) y a `sessions.yaml` del proyecto (Paso 10). *La pérdida silenciosa es peor que el conflicto ruidoso.*

> **Nota:** los archivos custom de `prompts/` y `agents/` detectados en el Paso 5.5 (no existen en el template) no entran aquí — se preservan intactos.
>
> **Sobre `cmp` y bytes:** si comparas base y destino byte a byte, diferencias de fin de línea (CRLF) o de newline final aparecen como cambios. Léelas como lo que son.

### 6.3 Eliminaciones upstream (`D`) — leak vs custom

Que upstream elimine un archivo **no** significa que el del proyecto sea desechable: puede ser el mismo fichero con una personalización encima. Antes de borrar, compara contra la base.

```bash
REL="prompts/meet.md"                 # ejemplo de archivo eliminado upstream
DST="$MEMSYS3_ROOT/$REL"

if [ ! -f "$DST" ]; then
  echo "· $REL — ya no existe en el proyecto, nada que hacer"
elif recover_base "$REL" && cmp -s "$DST" "$BASE_FILE"; then
  echo "🗑️ $REL — idéntico a la versión entregada: resto del scaffold viejo, se puede borrar"
else
  echo "🛑 $REL — DIFIERE de la versión entregada (o no hay base): personalización del proyecto"
  echo "   → NO borrar. Preservar y reportar al usuario para que decida."
fi
```

> Ojo con la señal 2 aquí: si upstream eliminó el archivo, `git log -- <ruta>` sigue devolviendo su historial, así que `recover_base` funciona igual.

- **Idéntico bit a bit a la base** → el proyecto nunca lo tocó: es residuo del scaffold anterior, bórralo.
- **Distinto, o base no recuperable** → **no borres**. Preserva, reporta en el registro de reconciliación y deja la decisión al usuario.

### 6.4 Actualizar Templates de schema (sustitución diferencial)

**Implementa ADR-018 (sustitución diferencial) + ADR-019 (deprecation contextualizada).**

`memory/templates/*-template.yaml` son templates de schema canónicos: el usuario NO los edita por contrato. Por eso usamos sustitución directa condicionada a comparación de `file_version` (no merge). Los datos vivos del usuario nunca se tocan aquí.

**Lógica por cada template:**

```bash
# Helpers extract_version / compare_versions definidos en el Paso 6.0
for src in memsys3_update_temp/memsys3_templates/memory/templates/*.yaml; do
  fname=$(basename "$src")
  dst="$MEMSYS3_ROOT/memory/templates/$fname"
  v_up=$(extract_version "$src")
  v_dst=$(extract_version "$dst" 2>/dev/null)

  if [ ! -f "$dst" ]; then
    echo "🆕 $fname — no existe en destino, copiando (v=$v_up)"
    cp "$src" "$dst"
  elif [ -z "$v_dst" ]; then
    echo "⚠️ $fname — destino sin file_version (legacy pre-ADR-017). Sustituyendo (v_up=$v_up)"
    cp "$src" "$dst"
  else
    cmp=$(compare_versions "$v_up" "$v_dst")
    case "$cmp" in
      gt) echo "⬆️ $fname — upstream $v_up > destino $v_dst, sustituyendo"; cp "$src" "$dst" ;;
      eq) echo "✅ $fname — versiones iguales ($v_up), no se toca" ;;
      lt) echo "🚨 $fname — destino $v_dst > upstream $v_up. Estado anómalo." ;;
    esac
  fi
done
```

**Si aparece `🚨` (destino > upstream) en algún archivo:**
Pregunta al usuario para cada caso (con preguntas estructuradas si tu harness las tiene; si no, en texto):
- "El template `<archivo>` tiene en tu proyecto la versión `<v_dst>`, mayor que upstream `<v_up>`. ¿Sobrescribir con upstream / preservar destino?"
- Si sobrescribir → `cp "$src" "$dst"`. Si preservar → no tocar.

### 6.4.5 Detección de campos deprecated y huérfanos (modo extendido)

**SOLO en modo Extendido (Paso 2.5).** En modo Rápido, saltar este sub-paso y avisar al usuario que la evaluación contextualizada de schema requiere modo Extendido.

**Implementa ADR-019.** Tras sustituir templates de schema, evalúa contextualmente si los campos del schema actual siguen siendo válidos para ESTE proyecto.

**1. Detectar deprecations marcadas por upstream:**

```bash
# Buscar comentarios "# DEPRECATED v0.X.Y — motivo: <razón>" en templates upstream
grep -rEn "^\s*#\s*DEPRECATED" "$MEMSYS3_ROOT/memory/templates/" || echo "(sin deprecations)"
```

Para cada `# DEPRECATED` encontrado:
1. Identifica qué campo está deprecado (línea siguiente al comentario o campo asociado).
2. Lee datos vivos relacionados (`memsys3/memory/project-status.yaml`, `memsys3/memory/full/sessions.yaml`, etc.) y verifica si el campo está en uso.
3. Si está en uso → pregunta al usuario: "Campo `<X>` marcado deprecated por upstream. Motivo: `<razón>`. ¿Mantener / migrar a `<alternativa>` / eliminar de tus datos vivos?"
4. Si no está en uso → solo informar al usuario, sin acción.

**2. Detectar campos huérfanos en datos vivos:**

Lee cada template de schema (`*-template.yaml`) y compara sus claves top-level con las del archivo operativo correspondiente:

| Template upstream | Datos vivos a comparar |
|---|---|
| `project-status-template.yaml` | `memsys3/memory/project-status.yaml` |
| `context-template.yaml` | `memsys3/memory/context.yaml` |
| `adr-template.yaml` | `memsys3/memory/full/adr.yaml` |
| `sessions-template.yaml` | `memsys3/memory/full/sessions.yaml` |

Para cada clave top-level presente en datos vivos pero NO en template upstream:
- Si la clave tiene contenido (no vacío) → pregunta al usuario: "Campo `<Y>` existe en tus datos pero no en el schema canónico. ¿Mantener (puede ser personalización legítima) / eliminar?"
- Si está vacío → eliminar silenciosamente.

**Importante:** Esta evaluación NUNCA elimina automáticamente. La filosofía memsys3 es human-in-the-loop: solo el usuario, contextualizado por el agente, decide qué es legítimo en su proyecto (ver ADR-019).

### 6.4.6 Detección de drift de cabecera (read-only)

Los archivos de datos creados **antes** de ADR-017 no llevan la cabecera `# version:` que sus scaffolds sí tienen hoy. No es un error del proyecto ni algo que debas arreglar por tu cuenta: es deriva histórica entre el scaffold y el output vivo. **Este paso solo reporta.**

```bash
for f in "$MEMSYS3_ROOT/memory/project-status.yaml" \
         "$MEMSYS3_ROOT/memory/context.yaml" \
         "$MEMSYS3_ROOT/memory/memory.yaml"; do
  [ -f "$f" ] || continue
  if grep -qE "^\s*#\s*version:|^\s*file_version:" "$f"; then
    echo "✅ $(basename "$f") — cabecera de versión presente"
  else
    echo "ℹ️ $(basename "$f") — sin cabecera de versión (dato creado pre-ADR-017)"
  fi
done
```

**NO auto-corrijas.** Informa al usuario del listado y sigue: añadir cabeceras a datos vivos es una decisión suya, no una consecuencia de actualizar.

### 6.5 Crear history/ si no existe

```bash
# Crear directorio para Plan de Contingencia (si no existe)
mkdir -p "$MEMSYS3_ROOT/memory/history"
touch "$MEMSYS3_ROOT/memory/history/.gitkeep"
```

### 6.6 Sincronizar PRINCIPLES.md (sustitución diferencial)

**Implementa ADR-022 + ADR-018.** `PRINCIPLES.md` es infraestructura versionada (vive en `memsys3/PRINCIPLES.md` en proyectos desplegados). Se sincroniza con la misma lógica que los templates de schema: comparar `file_version` upstream vs destino y sustituir condicionalmente. El usuario NO edita este archivo por contrato — los principios evolucionan en upstream y bajan vía `/actualizar-memsys3`.

```bash
src="memsys3_update_temp/memsys3_templates/PRINCIPLES.md"
dst="$MEMSYS3_ROOT/PRINCIPLES.md"

# Helpers extract_md_version / compare_versions definidos en el Paso 6.0
v_up=$(extract_md_version "$src")
v_dst=$(extract_md_version "$dst" 2>/dev/null)

if [ ! -f "$dst" ]; then
  echo "🆕 PRINCIPLES.md — no existe en destino, copiando (v=$v_up)"
  cp "$src" "$dst"
elif [ -z "$v_dst" ]; then
  echo "⚠️ PRINCIPLES.md — destino sin file_version (legacy). Sustituyendo (v_up=$v_up)"
  cp "$src" "$dst"
else
  cmp=$(compare_versions "$v_up" "$v_dst")
  case "$cmp" in
    gt) echo "⬆️ PRINCIPLES.md — upstream $v_up > destino $v_dst, sustituyendo"; cp "$src" "$dst" ;;
    eq) echo "✅ PRINCIPLES.md — versiones iguales ($v_up), no se toca" ;;
    lt) echo "🚨 PRINCIPLES.md — destino $v_dst > upstream $v_up. Estado anómalo (preguntar al usuario)" ;;
  esac
fi
```

> **Si aparece `🚨` (destino > upstream)**: preguntar al usuario con la misma lógica que el Paso 6.4 (sobrescribir / preservar).

### 6.6.5 Sincronizar `AGENTS.md` raíz (Capa 2 de ADR-027)

`AGENTS.md` vive en la **raíz del proyecto**, no dentro de `memsys3/` — es el estándar cross-tool que los harnesses auto-descubren. Misma lógica de sustitución diferencial que el Paso 6.6.

```bash
SRC="memsys3_update_temp/memsys3_templates/AGENTS.md"   # SSoT distribuible
DST="$PROJECT_ROOT/AGENTS.md"                           # raíz del proyecto destino

if [ ! -f "$SRC" ]; then
  echo "⚠️ AGENTS.md SSoT no encontrado en upstream — skip Capa 2"
elif [ ! -f "$DST" ]; then
  cp "$SRC" "$DST"
  echo "🆕 AGENTS.md creado en la raíz del proyecto (Capa 2, ADR-027)"
else
  v_up=$(extract_md_version "$SRC")
  v_dst=$(extract_md_version "$DST")
  if [ -z "$v_dst" ]; then
    echo "⚠️ AGENTS.md destino sin file_version (legacy pre-ADR-027) → sustituyendo"
    cp "$SRC" "$DST"
  else
    case "$(compare_versions "$v_up" "$v_dst")" in
      gt) cp "$SRC" "$DST"; echo "⬆️ AGENTS.md actualizado ($v_dst → $v_up)" ;;
      eq) echo "✅ AGENTS.md sincronizado ($v_up)" ;;
      lt) echo "🚨 AGENTS.md destino ($v_dst) > upstream ($v_up) — anómalo, preguntar al usuario" ;;
    esac
  fi
fi
```

> Helpers del Paso 6.0. Si el proyecto añadió contenido propio a su `AGENTS.md`, trátalo como personalización: aplica el criterio del Paso 6.2 antes de sustituir.

### 6.6.6 Sincronizar stubs per-tool (Capa 3 de ADR-027)

Los stubs Capa 3 (`CLAUDE.md`, `GEMINI.md`, `.cursor/rules/…`, `.clinerules`, etc.) los crea `newSession.md` por trigger declarativo. Aquí solo se **sincroniza** su contenido contra la SSoT genérica. **Este paso no enumera modelos**: detecta por la marca canónica del invariante, así que cubre harnesses que aún no existen.

```bash
SRC="memsys3_update_temp/memsys3_templates/per-tool-stub-template.md"
MARCA_CANONICA="Invariante de memoria agnóstica (ADR-027)"

if [ ! -f "$SRC" ]; then
  echo "⚠️ per-tool-stub-template.md no encontrado upstream — skip Capa 3"
else
  v_up=$(extract_md_version "$SRC")
  find "$PROJECT_ROOT" -maxdepth 3 \
       \( -name "*.md" -o -path "*/rules/*" -o -name ".clinerules" \) -type f \
       -not -path "*/memsys3_update_temp/*" -not -path "*/.git/*" \
       -not -path "$MEMSYS3_ROOT/*" -not -path "*/memsys3_templates/*" \
       -not -name "AGENTS.md" 2>/dev/null \
  | while read -r f; do
      grep -q "$MARCA_CANONICA" "$f" 2>/dev/null || continue
      grep -qE "<!--\s*version:\s*[0-9]+\.[0-9]+\.[0-9]+\s*-->" "$f" || continue
      v_dst=$(extract_md_version "$f")
      case "$(compare_versions "$v_up" "$v_dst")" in
        eq) echo "✅ stub $f sincronizado ($v_up)"; continue ;;
        lt) echo "🚨 stub $f destino ($v_dst) > upstream ($v_up) — preguntar al usuario"; continue ;;
      esac
      # gt: hay versión nueva. Un stub es un archivo que el harness lee siempre: el
      # proyecto puede haberle añadido reglas propias. Mismo verbo que en 6.2: EDITAR.
      echo "🔀 stub $f — plantilla $v_dst → $v_up: aplicar los cambios de la plantilla"
      echo "   al stub del proyecto conservando lo que el proyecto añadió (criterio del Paso 6.2)."
      diff "$f" "$SRC"
    done
fi
```

> **Exclusiones deliberadas del escaneo:** `AGENTS.md` (es Capa 2, tiene su propio Paso 6.6.5) y todo lo que cuelgue de `memsys3/` (incluida la copia local de la plantilla, que se actualiza por la matriz del Paso 6.1). Sin estas exclusiones el detector se traga sus propias fuentes: ambas llevan la marca canónica y `file_version`.
>
> Si el proyecto no tiene ningún stub que matchee, el paso es silencioso.

### 6.7 Actualizar Documentación del Sistema

```bash
cp memsys3_update_temp/memsys3_templates/memory/README.md "$MEMSYS3_ROOT/memory/"
```

---

## Paso 7: Actualizar Metadata de Versión

**Hacer esto ANTES de limpiar el clone temporal** (necesitas NEW_VERSION del Paso 3).

Edita `$MEMSYS3_ROOT/memory/project-status.yaml`:

**Actualizar solo el bloque metadata:**

```yaml
metadata:
  ultima_actualizacion: "[FECHA_HOY]"  # Formato: 2025-11-12
  actualizado_por: "Claude (Actualización memsys3 [VERSIÓN_ACTUAL] → [VERSIÓN_NUEVA])"
  fase: "[FASE_ACTUAL_DEL_PROYECTO]"  # NO cambiar, conservar la del proyecto
  memsys3_version: "[NEW_VERSION del Paso 3]"  # Ejemplo: v0.31.0-8-gbf0bff9 — salida literal de git describe
  memsys3_deployed: "[FECHA_HOY]"
```

> ⚠️ **Formato de `memsys3_version`: la salida literal de `git describe --tags --always` del Paso 3, sin adornos.** Es un commit-ish: la próxima actualización lo usa como BASE con `git show`. Formatos como `"v0.5.0 (commit: abc1234)"` NO resuelven y dejan al siguiente updater sin base (el Paso 1 los tolera extrayendo el hash, pero no los generes).

**IMPORTANTE:**
- NO toques `visio_general`, `estat_actual`, `features`, `stack_tecnologic`, etc.
- Solo actualiza el bloque `metadata`

**Verificar que el cambio se aplicó:**
```bash
grep "memsys3_version" "$MEMSYS3_ROOT/memory/project-status.yaml"
# Debe mostrar la versión NUEVA, no la anterior
```

---

## Paso 8: Limpiar Archivos Temporales

```bash
# Borrar clone temporal (ruta absoluta para evitar fallo si cwd cambió)
rm -rf "$PROJECT_ROOT/memsys3_update_temp"

echo "Clone temporal eliminado"
```

**NO borres el backup aún** (`memsys3/docs/backups/memsys3_backup_$TIMESTAMP`). Lo borraremos después de verificar.

---

## Paso 9: Verificar que Todo Funciona

### 9.1 Verificar Compilación de Contexto

Ejecuta en una **NUEVA INSTANCIA** (para no saturar tokens):

```bash
@memsys3/prompts/compile-context.md
```

**Verifica:**
- ✅ Se genera `memsys3/memory/context.yaml`
- ✅ No hay errores de campos faltantes
- ✅ context.yaml tiene < 2000 líneas
- ✅ notas_compilacion documenta el proceso

### 9.2 Probar newSession

En una **NUEVA INSTANCIA**:

```bash
@memsys3/prompts/newSession.md
```

**Verifica:**
- ✅ Carga el contexto correctamente
- ✅ No hay errores de rutas
- ✅ Muestra información relevante del proyecto

---

## Paso 10: Documentar Actualización en sessions.yaml

Usa el template de sessions para documentar esta actualización:

**Campos clave a documentar:**
```yaml
- id: "YYYY-MM-DD-actualizacion-memsys3"
  data: "[FECHA_HOY]"
  duracion: "~Xh"
  titulo: "Actualización memsys3 [VERSIÓN_ACTUAL] → [VERSIÓN_NUEVA]"

  features_implementadas:
    - "Actualizado memsys3 de [VERSIÓN_ACTUAL] a [VERSIÓN_NUEVA]"
    - "[LISTA_DE_ARCHIVOS_ACTUALIZADOS]"
    - "[MEJORAS_PRINCIPALES]"

  problemas_resueltos:
    - "[SI_HUBO_CONFLICTOS_O_PROBLEMAS]"

  decisions_tomadas:
    - "[SI_HUBO_QUE_HACER_MERGE_MANUAL]"

  gotchas_documentados:
    - tipo: "warning"
      problema: "[SI_ENCONTRASTE_ALGO_RARO]"
      solucion: "[CÓMO_LO_RESOLVISTE]"
      criticidad: "media"

  personalizaciones_reconciliadas:   # OBLIGATORIO si el Paso 6.2/6.3 detectó alguna
    - archivo: "[ruta]"
      detectado: "[qué añadía el proyecto respecto a la base]"
      accion: "[merge aplicado | sobrescrito con OK del usuario | preservado]"
      backup: "[ruta del backup del Paso 5]"

  proximos_pasos:
    - "Validar funcionamiento en próximas sesiones de desarrollo"
```

**Añade esta entry al principio de `memsys3/memory/full/sessions.yaml`**

> **Por qué `personalizaciones_reconciliadas` es obligatorio.** `sessions.yaml` es un archivo que el proyecto **sí lee al iniciar sesión**: es el único sitio donde una sobrescritura queda a la vista de quien trabaja después. Un resumen en pantalla se pierde al cerrar la terminal; `operations.log` no se lee en `newSession`. Si algo se pierde, que se pierda a la vista. Si no hubo ninguna personalización, omite la clave.

---

## Paso 11: Registrar en Operations Log

Registra esta actualización en `memsys3/memory/full/operations.log` para trazabilidad.

### 11.1 Verificar rotación

```bash
LOGFILE="$MEMSYS3_ROOT/memory/full/operations.log"
if [ -f "$LOGFILE" ]; then
  LINES=$(wc -l < "$LOGFILE" | tr -d '[:space:]')
  if [ "$LINES" -ge 1800 ]; then
    # Encontrar próximo número de rotación
    NEXT=1
    while [ -f "$MEMSYS3_ROOT/memory/full/operations_${NEXT}.log" ]; do
      NEXT=$((NEXT + 1))
    done
    cp "$LOGFILE" "$MEMSYS3_ROOT/memory/full/operations_${NEXT}.log"
    echo "Rotado: operations.log → operations_${NEXT}.log ($LINES líneas)"
    # Crear nuevo operations.log vacío
    cat > "$LOGFILE" << 'HEADER'
# Operations Log - memsys3
# Registro automático de operaciones del sistema (actualizar, compilar)
# Formato: YAML append-only, orden cronológico inverso (más reciente primero)
# Rotación: cuando >= 1800 líneas, rotar a operations_N.log (estilo sessions)
# Archivos rotados se pueden borrar libremente (no hay archivado)
# Este archivo NO se lee en newSession ni compile-context — solo consulta bajo demanda

operations:
HEADER
  fi
else
  echo "operations.log no existe, se creará"
fi
```

### 11.2 Escribir entrada

Usa **Edit tool** para añadir la entrada al PRINCIPIO del array `operations:` con el resumen estructurado de la actualización:

```yaml
operations:
  - timestamp: "[YYYY-MM-DDTHH:MM:SS]"
    operacion: "actualizar"
    version_origen: "[VERSIÓN_ACTUAL]"
    version_destino: "[VERSIÓN_NUEVA]"
    resultado: "ok"  # o "error: <detalle>"
    resumen:
      nuevos: "[N archivos (lista)]"
      actualizados: "[N archivos (lista)]"
      eliminados: "[N archivos (lista)]"
      merge_manual: "[archivos con merge manual, si los hubo]"
      preservados: "[archivos custom preservados]"
      personalizaciones:   # OBLIGATORIO — una entrada por archivo divergente del Paso 6.2/6.3
        - archivo: "[ruta]"
          diff: "[qué difería respecto a la base, concreto]"
          accion: "[merge | sobrescrito | preservado]"
          backup: "[ruta del backup]"
      backup: "[ruta del backup creado]"
      pendientes_validacion:
        - "[pendiente 1]"
        - "[pendiente 2]"
```

**El resumen debe reflejar lo que realmente ocurrió en esta actualización** — usa la misma información que mostrarías al usuario en el resumen final.

---

## Paso 12: Commit de Actualización (Opcional)

Si el proyecto usa git:

```bash
git add memsys3/
git commit -m "actualizar: memsys3 [VERSIÓN_ACTUAL] → [VERSIÓN_NUEVA]

- Prompts y agents reconciliados (base + merge donde había personalización)
- Templates de schema y PRINCIPLES.md sincronizados
- history/ creado (Plan Contingencia)
- Metadata de versión actualizada en project-status.yaml"
```

> **Coop / multi-usuario:** no asumas rama, identidad ni convención de tags. Quién commitea, sobre qué rama y si se tagea son convenciones **del proyecto** — si tiene un workflow de git propio (`memsys3/prompts/github.md` o equivalente), ejecútalo en lugar de este bloque. Nunca hardcodees una rama: `git push origin HEAD` respeta la rama activa.

---

## Paso 13: Eliminar Backup (Después de Validar)

**SOLO después de validar que todo funciona correctamente** (mínimo 1-2 sesiones de uso):

```bash
rm -rf memsys3/docs/backups/memsys3_backup_$TIMESTAMP
```

---

## 🚨 Resolución de Problemas

### Problema: "Campo X no existe en project-status.yaml"

**Causa:** Versión muy antigua sin campos nuevos.

**Solución:**
1. Compara `project-status.yaml` actual con template nuevo
2. Añade campos faltantes manualmente (siguiendo estructura del template)
3. NO copies todo el template (perderías datos del proyecto)

### Problema: "Conflicto en un prompt o agent — personalizaciones vs mejoras"

**Solución:** es el caso normal del Paso 6.2, no una excepción.
1. Recupera la BASE (`git show "$CURRENT_VERSION:memsys3_templates/<ruta>"`) — sin ella no distingues "añadido por el proyecto" de "eliminado por upstream".
2. `diff base local` te da **qué añadió el proyecto**; `diff base upstream` te da **qué cambió upstream**.
3. Busca en `sessions.yaml` la divergencia documentada: te da el **por qué** de la personalización.
4. Crea la versión híbrida: estructura y mejoras de upstream + intención de la personalización preservada.
5. Si son incompatibles, pregunta al usuario con las dos versiones delante. Reporta siempre lo que hiciste.

### Problema: "No puedo recuperar la BASE de un archivo"

**Causa:** `memsys3_version` ausente o inexacto en `project-status.yaml`, tag inexistente en upstream, o deployment hecho a mano.

**Solución:** la misma operación del Paso 6.2 con menos certeza: lees destino y origen, entiendes qué es de cada uno, y editas el destino conservando ante cualquier duda. Cuando no sepas a quién pertenece una línea, pregunta al usuario. Anótalo en el registro de reconciliación: es información valiosa sobre la salud del deployment.

### Problema: "context.yaml no compila - errores de campos"

**Causa:** context-agent.yaml nuevo espera campos que project-status.yaml antiguo no tiene.

**Solución:**
1. Lee el error específico (¿qué campo falta?)
2. Añade campo faltante a project-status.yaml siguiendo template
3. Re-ejecuta compile-context.md

---

## Paso 14: Actualizar file_version de archivos tocados

Cada archivo de infraestructura memsys3 tiene un `file_version` (formato `0.Y.Z`):
- Archivos `.md`: última línea `<!-- version: X.Y.Z -->`
- Archivos `.yaml` en agents/: campo `file_version: "X.Y.Z"`
- Archivos `.yaml` en memory/templates/: primera línea `# version: X.Y.Z`

**Para cada archivo copiado/modificado en los pasos anteriores:**

1. Lee el `file_version` del archivo nuevo (del repo clonado)
2. Ese ES el file_version correcto — ya viene actualizado desde el repo
3. No necesitas hacer nada extra: el file_version viaja con el archivo

**Registrar en operations.log:**

Usa **Edit tool** para añadir al PRINCIPIO del array `operations:` en `$MEMSYS3_ROOT/memory/full/operations.log`:

```yaml
operations:
  - timestamp: "[YYYY-MM-DDTHH:MM:SS]"
    operacion: "actualizar"
    version_anterior: "[VERSION_ACTUAL]"
    version_nueva: "[VERSION_NUEVA]"
    resultado: "ok"
    archivos_actualizados:
      - archivo: "prompts/compile-context.md"
        file_version: "0.2.0"
      - archivo: "agents/context-agent.yaml"
        file_version: "0.1.0"
      # ... (listar todos los archivos tocados con su file_version)
    resumen: "Actualización memsys3 [VERSION_ACTUAL] → [VERSION_NUEVA]. [N] archivos actualizados."
```

> **Nota:** Esta entrada complementa la del Paso 11. Si ya escribiste la entrada del Paso 11, **amplíala** añadiendo el campo `archivos_actualizados` con los file_version. No dupliques entradas — una sola entrada por operación de actualización.

---

## 📊 Checklist Final

Antes de dar por terminada la actualización, verifica:

- [ ] Contexto del proyecto ingerido ANTES de tocar nada (Paso 0.5), incluidas las divergencias documentadas en `sessions.yaml`
- [ ] Backup creado en `memsys3/docs/backups/memsys3_backup_$TIMESTAMP`
- [ ] `memsys3/docs/backups/` excluido en `.gitignore` del proyecto (Paso 5, ISSUE-006) — `git check-ignore memsys3/docs/backups/x`
- [ ] **Ningún archivo de `prompts/` o `agents/` se sustituyó por copia: todos se editaron leyendo origen, destino y base** (Paso 6.2)
- [ ] **Ninguna eliminación `D` se ejecutó sin el criterio leak-vs-custom** (Paso 6.3)
- [ ] **Toda personalización detectada quedó reportada en los TRES sitios**: resumen final, `operations.log` y `sessions.yaml` del proyecto — con diff concreto y ruta del backup
- [ ] Archivos del sistema actualizados (prompts, agents, templates)
- [ ] `PRINCIPLES.md` sincronizado (Paso 6.6, sustitución diferencial — ADR-022 + ADR-018)
- [ ] `AGENTS.md` raíz sincronizado (Paso 6.6.5, Capa 2 ADR-027)
- [ ] Stubs Capa 3 sincronizados o paso silencioso si no hay (Paso 6.6.6)
- [ ] Drift de cabecera reportado sin auto-corregir (Paso 6.4.6)
- [ ] `docs/` copiada (`ls memsys3/docs/reference.md`)
- [ ] `backlog/` existe (`ls memsys3/backlog/`)
- [ ] history/ creado (si no existía)
- [ ] Versión actualizada en `project-status.yaml` metadata (`grep memsys3_version memsys3/memory/project-status.yaml` muestra versión nueva)
- [ ] Clone temporal borrado (memsys3_update_temp)
- [ ] compile-context.md ejecutado exitosamente
- [ ] newSession.md funciona (nueva instancia)
- [ ] Actualización documentada en sessions.yaml
- [ ] Operación registrada en `memsys3/memory/full/operations.log`
- [ ] `archivos_actualizados` con `file_version` registrados en operations.log (Paso 14)
- [ ] (Opcional) Commit creado
- [ ] Backup borrado (después de 1-2 sesiones de validación)

---

## 📣 Resumen final al usuario (obligatorio)

Antes de dar por cerrada la actualización, presenta al usuario:

1. Versión: `[VERSIÓN_ACTUAL]` → `[VERSIÓN_NUEVA]`.
2. Recuento de archivos añadidos / reconciliados / eliminados / preservados.
3. **Sección destacada "Personalizaciones detectadas"** con el registro de reconciliación completo: una línea por archivo divergente, qué añadía el proyecto, qué se hizo y dónde está el backup. **Si no hubo ninguna, dilo explícitamente** ("ninguna personalización local detectada") — el silencio es ambiguo.
4. Pendientes de validación (compile-context en sesión nueva, `newSession` de prueba).

---

## 🔗 Referencias

- Prompt relacionado: `memsys3/prompts/deploy.md` (para deployment inicial)
- ADRs: ADR-009 (templates permanentes), ADR-017 (`file_version`), ADR-018 (sustitución diferencial), ADR-019 (deprecation contextualizada), ADR-022 (PRINCIPLES.md), ADR-027 (memoria agnóstica, Capas 2 y 3), ADR-028 (Setup Agent), ADR-032 (personalización autorizada de `prompts/` y `agents/`).
- **Por qué existen los Pasos 6.2 y 6.3:** auditoría del contrato de actualización (2026-08-23) — tres vectores de pérdida: sobrescritura incondicional por lista hardcodeada, borrado de `D` sin verificar, y merge a 2 bandas sin base. Evidencia de campo: informe de actualización real `2026-05-27` (§3.2, §4.1-4.2) y caso de pérdida silenciosa de un parche local reportado el 2026-08-27.

---

**¡Actualización completada!** 🎉

El sistema memsys3 de este proyecto ahora está actualizado a la última versión, conservando todos los datos históricos y personalizaciones.
<!-- version: 0.4.0 -->
