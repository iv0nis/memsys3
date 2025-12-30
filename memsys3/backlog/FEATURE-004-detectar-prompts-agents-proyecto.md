# FEATURE-004: Detectar y preservar prompts/agents del proyecto durante deployment

**Estado:** Propuesto
**Prioridad:** Media
**Tipo:** Feature / Mejora de Usabilidad
**Plazo:** Medio plazo
**Fecha propuesta:** 2025-12-30

---

## Problema / Necesidad

Algunos proyectos pueden tener sus propios directorios `/prompts` o `/agents` en la raíz (fuera de memsys3/) con contenido específico del proyecto:

**Ejemplos:**
```
proyecto/
├── prompts/                    # Prompts específicos del proyecto
│   ├── deploy-app.md
│   ├── test-integration.md
│   └── ...
├── agents/                     # Agents específicos del proyecto
│   ├── deployment-agent.yaml
│   └── ...
└── memsys3/                   # Sistema memsys3 (puede no existir todavía)
    ├── prompts/
    └── agents/
```

**Problemas actuales:**

1. **Durante deploy/actualizar:** No se detectan estos directorios existentes
2. **Riesgo de sobrescritura:** Si usuario tiene /prompts propios, puede confundirse
3. **Pérdida de oportunidad:** Esos prompts/agents podrían ser útiles para personalizar memsys3
4. **No hay preservación:** Si se sobrescriben accidentalmente, se pierden

**Caso de uso real:**
- Usuario tiene `/prompts/deploy-production.md` con lógica específica de su app
- Despliega memsys3 → crea `memsys3/prompts/`
- Usuario podría querer:
  - Usar deploy-production.md como base para personalizar memsys3
  - Mover deploy-production.md a memsys3/prompts/ para centralizar
  - Preservar deploy-production.md en backup por si cambia de opinión

---

## Propuesta / Diseño

### PASO 1: Detección (durante deploy.md / actualizar.md)

Antes de crear `memsys3/`, detectar si existen `/prompts` o `/agents` en raíz:

```bash
# Detección de directorios existentes
EXISTING_PROMPTS=""
EXISTING_AGENTS=""

if [ -d "prompts" ] && [ "$(ls -A prompts 2>/dev/null)" ]; then
  EXISTING_PROMPTS="prompts"
  echo "⚠️ Detectado directorio /prompts/ con archivos del proyecto"
fi

if [ -d "agents" ] && [ "$(ls -A agents 2>/dev/null)" ]; then
  EXISTING_AGENTS="agents"
  echo "⚠️ Detectado directorio /agents/ con archivos del proyecto"
fi
```

### PASO 2: Consulta al usuario (solo si detectó algo)

Si se detectaron directorios existentes:

```
⚠️ Detectados archivos del proyecto:
   - /prompts/ (X archivos)
   - /agents/ (Y archivos)

Estos NO son parte de memsys3. Son específicos de tu proyecto.

¿Qué quieres hacer?

A) Listar archivos para revisión
B) Usar como fuente de info para personalizar memsys3 (recomendado)
C) Ignorar (continuar con deployment estándar)

Selección: __
```

### PASO 3A: Listar archivos (si usuario eligió A)

```bash
echo "📁 Contenido de /prompts/:"
ls -1 prompts/

echo "📁 Contenido de /agents/:"
ls -1 agents/

# Volver a preguntar B o C
```

### PASO 3B: Usar como fuente de info (si usuario eligió B)

**Durante briefing (deploy.md PASO 2):**

Agregar preguntas adicionales:

```
📋 PASO 2: Briefing - Información Adicional

Detectamos que tienes prompts/agents propios:

- /prompts/deploy-production.md
- /prompts/test-integration.md
- /agents/deployment-agent.yaml

¿Quieres que los lea para:
1. Entender mejor tu proyecto
2. Personalizar memsys3/prompts/newSession.md con contexto específico
3. Sugerir adaptaciones de tus prompts para memsys3?

(sí / no): __
```

Si usuario dice "sí":
1. Leer archivos existentes
2. Extraer información útil (stack, workflow, convenciones)
3. Usar esa info para personalizar deployment de memsys3

### PASO 4: Preservación post-deployment

**Al finalizar deploy/actualizar:**

```
✅ Deployment de memsys3 completado.

⚠️ Detectamos /prompts/ y /agents/ del proyecto (fuera de memsys3/).

¿Quieres crear backup de estos directorios?

Opción A: Copiar a memsys3_backup_original/ (recomendado)
Opción B: No hacer backup (puedes gestionarlo manualmente)

Selección: __
```

Si usuario elige A:
```bash
mkdir -p memsys3_backup_original/
[ -d "prompts" ] && cp -r prompts memsys3_backup_original/
[ -d "agents" ] && cp -r agents memsys3_backup_original/

echo "✅ Backup creado en memsys3_backup_original/"
echo "   Puedes recuperarlos si necesitas"
```

---

## Alternativas Consideradas

### Alternativa A: Mover automáticamente a memsys3/

Mover `/prompts` → `memsys3/prompts/custom/`

**Pros:** Centralización automática
**Contras:**
- Muy invasivo (modifica estructura del proyecto)
- Puede romper aliases/referencias existentes
- Usuario puede no querer mezclarlos

**Descartada:** Demasiado invasivo

### Alternativa B: Ignorar completamente

No detectar ni preguntar nada.

**Pros:** Simplicidad máxima
**Contras:**
- Pierde oportunidad de personalización
- No preserva datos si usuario sobrescribe accidentalmente
- No aprovecha información valiosa del proyecto

**Descartada:** Pierde valor potencial

### Alternativa C: Solo detectar y avisar (sin interacción)

Mostrar warning pero no hacer nada:

```
⚠️ Detectado /prompts/ y /agents/ en raíz.
   Estos NO son parte de memsys3.
   Puedes gestionarlos manualmente.
```

**Pros:** No invasivo, simple
**Contras:** No ayuda al usuario, pierde oportunidad de personalización

**Descartada:** No aporta valor suficiente

---

## Decisiones / Acciones

**Decisión:** Implementar propuesta completa (PASOS 1-4)

**Fase 1 (MVP - Prioridad Media):**
- [ ] PASO 1: Detección automática en deploy.md y actualizar.md
- [ ] PASO 2: Consulta básica (A, B, C)
- [ ] PASO 3A: Listar archivos
- [ ] PASO 4: Preservación en backup

**Fase 2 (Mejora - Prioridad Baja):**
- [ ] PASO 3B: Usar como fuente de info para personalización inteligente
- [ ] Integración con briefing (leer prompts existentes)
- [ ] Sugerencias de adaptación

**Implementación:**

1. **deploy.md:** Agregar detección ANTES de PASO 1 (clone temp)
2. **actualizar.md:** Agregar detección ANTES de PASO 1 (clone temp)
3. **Ubicación lógica:** Después de "Verificar que estás en el proyecto correcto"

**Archivos a modificar:**
- `memsys3_templates/prompts/deploy.md`
- `memsys3_templates/prompts/actualizar.md`

---

## Casos de Uso

### Caso 1: Proyecto con prompts deployment

**Contexto:**
```
proyecto/
├── prompts/
│   ├── deploy-staging.md
│   └── deploy-production.md
```

**Resultado:**
1. Deploy detecta /prompts/
2. Usuario elige "Usar como fuente de info"
3. memsys3 lee deploy-staging.md y deploy-production.md
4. Extrae info: stack (Docker, AWS), workflow (CI/CD)
5. Personaliza newSession.md: "Proyecto usa Docker + AWS, CI/CD con GitHub Actions"
6. Crea backup en memsys3_backup_original/prompts/

### Caso 2: Proyecto con agents específicos

**Contexto:**
```
proyecto/
├── agents/
│   ├── code-reviewer.yaml
│   └── test-runner.yaml
```

**Resultado:**
1. Deploy detecta /agents/
2. Usuario elige "Listar para revisión"
3. Ve: code-reviewer.yaml, test-runner.yaml
4. Decide: "No mezclar con memsys3, son diferentes"
5. Elige "Crear backup"
6. Backup creado en memsys3_backup_original/agents/

### Caso 3: Proyecto limpio (sin prompts/agents propios)

**Contexto:**
```
proyecto/
├── src/
└── README.md
```

**Resultado:**
1. Deploy NO detecta /prompts ni /agents
2. Continúa deployment estándar sin preguntar
3. No hay preservación (no hay nada que preservar)

---

## Referencias

- **Prompts afectados:** `deploy.md`, `actualizar.md`
- **Relacionado:** ISSUE-006 (backups siempre .gitignore)
- **Filosofía:** memsys3 debe adaptarse al proyecto, no al revés
- **Conversación:** Sesión 2025-12-30, sugerencia del usuario

---

## Notas Adicionales

**Ventajas de esta feature:**
1. **No invasiva:** Solo pregunta, no modifica nada sin permiso
2. **Preservación:** Backup automático evita pérdidas
3. **Personalización:** Usa info existente para mejor deployment
4. **Flexible:** Usuario decide qué hacer (A, B, C)

**Complejidad:**
- Fase 1 (MVP): Baja-Media (detección + backup simple)
- Fase 2 (personalización inteligente): Media-Alta (parsing, extracción info)

**Prioridad:**
- Fase 1: Media (útil pero no crítica)
- Fase 2: Baja (nice to have)

**Compatibilidad:**
- No rompe deployments existentes
- Solo añade pasos opcionales si detecta directorios
- Proyectos sin /prompts ni /agents: comportamiento actual (sin cambios)
