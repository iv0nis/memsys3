# Actualitzar memsys3 - Prompt d'Actualització Segura

**ARA ACTUES COM A MAIN AGENT realitzant una actualització de memsys3**

- La teva missió és **actualitzar la versió de memsys3** en aquest projecte de forma segura
- **IMPORTANT: Treballa en CATALÀ sempre**
- Aquest prompt complementa `deploy.md` (que és per deployment inicial)

---

## ⚠️ ABANS DE COMENÇAR

**Verifica que estàs en el projecte correcte:**
1. Aquest projecte JA té memsys3 instal·lat (carpeta `memsys3/`)
2. Si NO té memsys3, utilitza `@memsys3/prompts/deploy.md` en el seu lloc

---

## 🚨 PAS 0: Detectar Estructura Antiga Incompatible

**CRÍTIC:** Abans d'actualitzar, hem de verificar si existeix una estructura antiga PRE-ADR-006 (pre-v0.2.0).

### Detectar estructura antiga

Executa:

```bash
# Verificar si existeix carpeta /memory en arrel (NO dins de memsys3/)
ls -la memory/ 2>/dev/null && echo "⚠️ ESTRUCTURA ANTIGA DETECTADA" || echo "✅ Estructura nova OK"

# Verificar si memsys3/ existeix
ls -la memsys3/ 2>/dev/null && echo "✅ memsys3/ existeix" || echo "❌ memsys3/ NO existeix"
```

**Escenaris possibles:**

### Escenari A: Només `/memory` (estructura pre-ADR-006)

```
projecte/
├── memory/           ← Estructura antiga (sense prefix memsys3/)
│   ├── full/
│   ├── templates/
│   ├── prompts/
│   └── project-status.yaml
└── (NO hi ha memsys3/)
```

**Diagnòstic:** Sistema de memòria antiga, **incompatible** amb memsys3 actual.

**Acció:** **NO utilitzar actualizar.md**. Això requereix **migració completa**:
1. Backup complet de `/memory`
2. Executar `@memsys3/prompts/deploy.md` (deployment des de zero)
3. Migrar dades manualment:
   - Copiar `memory/full/sessions.yaml` → `memsys3/memory/full/`
   - Copiar `memory/full/adr.yaml` → `memsys3/memory/full/`
   - Copiar `memory/project-status.yaml` → `memsys3/memory/` (afegir camps versió)
4. Esborrar `/memory` antiga després de validar

### Escenari B: `/memory` + `/memsys3` coexistint

```
projecte/
├── memory/           ← Estructura antiga AMB DADES REALS
│   ├── full/
│   └── project-status.yaml
└── memsys3/          ← Estructura nova PERÒ amb dades template sense personalitzar
    └── memory/
```

**Diagnòstic:** Deployment inicial es va fer INCORRECTAMENT. Es va desplegar memsys3/ però NO es van migrar dades de /memory.

**🚨 AIXÒ ÉS EL QUE VA PASSAR A deCastro_inmobiliaria**

**Símptomes:**
- `/memory/project-status.yaml` té dades del projecte real
- `/memsys3/memory/project-status.yaml` té dades copiades del template memsys3 (descripcions genèriques, "Sistema de gestió de context...", etc.)

**Acció:** **Migració de dades abans d'actualitzar**:

```bash
# 1. Backup d'ambdues estructures
cp -r memory memory_backup_old_$(date +%Y%m%d)
cp -r memsys3 memsys3_backup_$(date +%Y%m%d)

# 2. Migrar dades REALS de /memory a /memsys3/memory
cp memory/full/sessions.yaml memsys3/memory/full/
cp memory/full/adr.yaml memsys3/memory/full/
cp memory/project-status.yaml memsys3/memory/

# 3. Afegir camps de versió a memsys3/memory/project-status.yaml
# (editar manualment metadata: afegir memsys3_version, memsys3_deployed)

# 4. ARA SÍ, continuar amb actualizar.md des del Pas 1
```

**Després de validar que funciona:**
```bash
# Esborrar estructura antiga (només després de validar)
rm -rf memory_backup_old_* memory/
```

### Escenari C: Només `/memsys3` (estructura nova)

```
projecte/
└── memsys3/          ← Estructura correcta
    └── memory/
        ├── full/
        ├── templates/
        └── project-status.yaml (amb memsys3_version)
```

**Diagnòstic:** Estructura correcta, deployment fet correctament.

**Acció:** ✅ Continuar amb **Pas 1** normalment.

---

## Pas 1: Verificar Versió Actual

Llegeix l'arxiu del projecte:

```bash
cat memsys3/memory/project-status.yaml | grep -A2 "metadata:"
```

**Busca els camps:**
- `memsys3_version`: Versió actual instal·lada
- `memsys3_deployed`: Data de l'últim deployment/actualització

**Si NO existeixen aquests camps:**
- Significa que tens una versió molt antiga (pre-v0.5.0)
- L'actualització serà més complexa (molts canvis estructurals)

**Anota la versió actual aquí:** `[VERSIÓ_ACTUAL]`

---

## Pas 2: Verificar Última Versió Disponible

Consulta GitHub per veure l'última versió:

```bash
git ls-remote --tags https://github.com/iv0nis/memsys3 | tail -5
```

**Identifica l'última versió estable (tag més recent):** `[VERSIÓ_NOVA]`

**Val la pena actualitzar?**
- Si la diferència és < 2 versions patch (ex: v0.5.1 → v0.5.2): actualització menor
- Si la diferència és >= 1 versió minor (ex: v0.4.0 → v0.5.0): actualització important
- Si és >= 1 versió major (ex: v0.x → v1.x): actualització crítica (revisar CHANGELOG)

---

## Pas 3: Clonar Nova Versió Temporalment

**IMPORTANT:** NO esborris res encara, només clona per comparar.

```bash
# Clonar en directori temporal
git clone https://github.com/iv0nis/memsys3 memsys3_update_temp

cd memsys3_update_temp

# Obtenir versió exacta
NEW_VERSION=$(git describe --tags --always)
NEW_COMMIT=$(git log -1 --format=%h)

echo "Nova versió: $NEW_VERSION (commit: $NEW_COMMIT)"

cd ..
```

---

## Pas 4: Categoritzar Arxius Segons Estratègia

### 🚫 MAI SOBREESCRIURE (dades del projecte actual)

Aquests arxius contenen l'històric i estat del projecte. **MAI els toquis:**

- `memsys3/memory/full/adr.yaml`
- `memsys3/memory/full/sessions.yaml`
- `memsys3/memory/full/sessions_*.yaml` (si hi ha rotacions)
- `memsys3/memory/full/adr_*.yaml` (si hi ha rotacions)
- `memsys3/memory/project-status.yaml` (excepte metadata de versió)
- `memsys3/memory/context.yaml` (es regenera amb compile-context)
- `memsys3/memory/history/*` (si existeix)

### ✅ ACTUALITZAR SEMPRE (lògica del sistema)

Aquests són part del "motor" de memsys3, es poden sobreescriure:

**Prompts:**
- `memsys3/prompts/compile-context.md`
- `memsys3/prompts/endSession.md`
- `memsys3/prompts/mind.md`
- `memsys3/prompts/github.md`
- `memsys3/prompts/deploy.md`
- `memsys3/prompts/actualizar.md` ← (aquest mateix arxiu)

**Agents:**
- `memsys3/agents/context-agent.yaml`

**Visualitzador:**
- `memsys3/viz/index.html`
- `memsys3/viz/viewer.js`
- `memsys3/viz/styles.css`
- `memsys3/viz/serve.py`

**Templates:**
- `memsys3/memory/templates/adr-template.yaml`
- `memsys3/memory/templates/sessions-template.yaml`
- `memsys3/memory/templates/context-template.yaml`
- `memsys3/memory/templates/project-status-template.yaml`

**Documentació del sistema:**
- `memsys3/memory/README.md`
- `memsys3/viz/README.md`

### 🔍 REVISAR MANUALMENT (pot haver-hi personalitzacions)

Aquests arxius poden haver estat personalitzats per l'usuari:

- `memsys3/prompts/newSession.md` → Pot tenir context específic del projecte
- `memsys3/agents/main-agent.yaml` → Pot tenir responsabilitats personalitzades

**Estratègia:**
1. Fer diff entre versió actual i nova
2. Si NO hi ha canvis de l'usuari → sobreescriure
3. Si HI HA canvis de l'usuari → fer merge manual (conservar personalitzacions + aplicar millores)

---

## Pas 5: Crear Backup de Seguretat

Abans de tocar RES, crea un backup:

```bash
# Crear backup amb timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp -r memsys3 memsys3_backup_$TIMESTAMP

echo "Backup creat a: memsys3_backup_$TIMESTAMP"
```

**CRÍTIC:** Si alguna cosa surt malament, pots restaurar amb:
```bash
rm -rf memsys3
mv memsys3_backup_$TIMESTAMP memsys3
```

---

## Pas 6: Actualitzar Arxius del Sistema

### 6.1 Actualitzar Prompts

```bash
# Copiar prompts actualitzats (excepte newSession.md de moment)
cp memsys3_update_temp/memsys3_templates/prompts/compile-context.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/endSession.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/mind.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/github.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/deploy.md memsys3/prompts/
cp memsys3_update_temp/memsys3_templates/prompts/actualizar.md memsys3/prompts/
```

### 6.2 Revisar newSession.md

```bash
# Comparar versions
diff memsys3/prompts/newSession.md memsys3_update_temp/memsys3_templates/prompts/newSession.md
```

**Si hi ha diferències:**
- Llegeix ambdues versions
- Conserva personalitzacions del projecte (descripcions específiques, context únic)
- Aplica millores estructurals de la nova versió
- Edita manualment si cal

**Si NO hi ha diferències (arxiu base sense personalitzar):**
```bash
cp memsys3_update_temp/memsys3_templates/prompts/newSession.md memsys3/prompts/
```

### 6.3 Actualitzar Agents

```bash
# Context Agent (sempre actualitzar)
cp memsys3_update_temp/memsys3_templates/agents/context-agent.yaml memsys3/agents/

# Main Agent (revisar personalitzacions)
diff memsys3/agents/main-agent.yaml memsys3_update_temp/memsys3_templates/agents/main-agent.yaml
```

**Estratègia main-agent.yaml:** igual que newSession.md (conservar personalitzacions + aplicar millores)

### 6.4 Actualitzar Templates

```bash
cp memsys3_update_temp/memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/
```

### 6.5 Actualitzar Visualitzador

**IMPORTANT:** Verificar ubicació segons versió.

**Si tens memsys3/memory/viz/ (versió antiga):**
```bash
# Moure a arrel (nova ubicació segons ADR-009)
mkdir -p memsys3/viz
cp memsys3_update_temp/memsys3_templates/viz/* memsys3/viz/

# Opcional: esborrar ubicació antiga (després de verificar que funciona)
# rm -rf memsys3/memory/viz/
```

**Si ja tens memsys3/viz/ (versió nova):**
```bash
cp memsys3_update_temp/memsys3_templates/viz/* memsys3/viz/
```

### 6.6 Crear history/ si no existeix

```bash
# Crear directori per Pla de Contingència (si no existeix)
mkdir -p memsys3/memory/history
touch memsys3/memory/history/.gitkeep
```

### 6.7 Actualitzar Documentació del Sistema

```bash
cp memsys3_update_temp/memsys3_templates/memory/README.md memsys3/memory/
cp memsys3_update_temp/memsys3_templates/viz/README.md memsys3/viz/ 2>/dev/null || true
```

---

## Pas 7: Actualitzar Metadata de Versió

Edita `memsys3/memory/project-status.yaml`:

**Actualitzar només el bloc metadata:**

```yaml
metadata:
  ultima_actualizacion: "[DATA_AVUI]"  # Format: 2025-11-12
  actualizado_por: "Claude (Actualització memsys3 [VERSIÓ_ACTUAL] → [VERSIÓ_NOVA])"
  fase: "[FASE_ACTUAL_DEL_PROJECTE]"  # NO canviar, conservar la del projecte
  memsys3_version: "[VERSIÓ_NOVA]"  # Exemple: v0.5.0 (commit: abc1234)
  memsys3_deployed: "[DATA_AVUI]"
```

**IMPORTANT:**
- NO toquis `visio_general`, `estat_actual`, `features`, `stack_tecnologic`, etc.
- Només actualitza el bloc `metadata`

---

## Pas 8: Netejar Arxius Temporals

```bash
# Esborrar clone temporal
rm -rf memsys3_update_temp

echo "Clone temporal eliminat"
```

**NO esborris el backup encara** (memsys3_backup_$TIMESTAMP). Ho esborrarem després de verificar.

---

## Pas 9: Verificar que Tot Funciona

### 9.1 Verificar Compilació de Context

Executa en una **NOVA INSTÀNCIA** (per no saturar tokens):

```bash
@memsys3/prompts/compile-context.md
```

**Verifica:**
- ✅ Es genera `memsys3/memory/context.yaml`
- ✅ No hi ha errors de camps faltants
- ✅ context.yaml té < 2000 línies
- ✅ notas_compilacion documenta el procés

### 9.2 Verificar Visualitzador

```bash
@memsys3/prompts/mind.md
```

**Verifica:**
- ✅ Servidor arrenca sense errors
- ✅ Dashboard es veu correctament a http://localhost:8000
- ✅ Les 4 pestanyes funcionen (Overview, ADRs, Sessions, Gotchas)

### 9.3 Provar newSession

En una **NOVA INSTÀNCIA**:

```bash
@memsys3/prompts/newSession.md
```

**Verifica:**
- ✅ Carrega el context correctament
- ✅ No hi ha errors de rutes
- ✅ Mostra informació rellevant del projecte

---

## Pas 10: Documentar Actualització a sessions.yaml

Utilitza el template de sessions per documentar aquesta actualització:

**Camps clau a documentar:**
```yaml
- id: "YYYY-MM-DD-actualizacion-memsys3"
  data: "[DATA_AVUI]"
  duracion: "~Xh"
  titulo: "Actualització memsys3 [VERSIÓ_ACTUAL] → [VERSIÓ_NOVA]"

  features_implementades:
    - "Actualitzat memsys3 de [VERSIÓ_ACTUAL] a [VERSIÓ_NOVA]"
    - "[LLISTA_D'ARXIUS_ACTUALITZATS]"
    - "[MILLORES_PRINCIPALS]"

  problemas_resueltos:
    - "[SI_HI_VA_HAVER_CONFLICTES_O_PROBLEMES]"

  decisions_tomadas:
    - "[SI_VA_CALDRE_FER_MERGE_MANUAL]"

  gotchas_documentados:
    - tipo: "warning"
      problema: "[SI_VAS_TROBAR_ALGUNA_COSA_RARA]"
      solucion: "[COM_HO_VAS_RESOLDRE]"
      criticidad: "media"

  proximos_pasos:
    - "Validar funcionament en properes sessions de desenvolupament"
```

**Afegeix aquesta entry al principi de `memsys3/memory/full/sessions.yaml`**

---

## Pas 11: Commit d'Actualització (Opcional)

Si el projecte utilitza git:

```bash
git add memsys3/
git commit -m "actualitzar: memsys3 [VERSIÓ_ACTUAL] → [VERSIÓ_NOVA]

- Prompts actualitzats (compile-context, endSession, etc.)
- Agents actualitzats (context-agent.yaml)
- Templates actualitzats
- Visualitzador actualitzat
- history/ creat (Pla Contingència)
- Metadata versió actualitzada a project-status.yaml

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Pas 12: Eliminar Backup (Després de Validar)

**NOMÉS després de validar que tot funciona correctament** (mínim 1-2 sessions d'ús):

```bash
rm -rf memsys3_backup_$TIMESTAMP
```

---

## 🚨 Resolució de Problemes

### Problema: "Camp X no existeix a project-status.yaml"

**Causa:** Versió molt antiga sense camps nous.

**Solució:**
1. Compara `project-status.yaml` actual amb template nou
2. Afegeix camps faltants manualment (seguint estructura del template)
3. NO copiïs tot el template (perdries dades del projecte)

### Problema: "viz/ no es troba"

**Causa:** Versió antiga amb viz a `memory/viz/` vs nova ubicació `viz/`

**Solució:** Veure Pas 6.5 (moure de memory/viz/ a viz/)

### Problema: "Conflicte a newSession.md - personalitzacions vs millores"

**Solució:**
1. Llegeix ambdues versions completes
2. Identifica quines línies són personalitzacions del projecte (descripcions úniques)
3. Identifica quines línies són millores estructurals (noves instruccions)
4. Crea versió híbrida: conserva personalitzacions + aplica millores

### Problema: "context.yaml no compila - errors de camps"

**Causa:** context-agent.yaml nou espera camps que project-status.yaml antic no té.

**Solució:**
1. Llegeix l'error específic (quin camp falta?)
2. Afegeix camp faltant a project-status.yaml seguint template
3. Re-executa compile-context.md

---

## 📊 Checklist Final

Abans de donar per finalitzada l'actualització, verifica:

- [ ] Versió actualitzada a `project-status.yaml` metadata
- [ ] Backup creat (memsys3_backup_$TIMESTAMP)
- [ ] Arxius del sistema actualitzats (prompts, agents, templates, viz)
- [ ] history/ creat (si no existia)
- [ ] compile-context.md executat exitosament
- [ ] Visualitzador funciona (mind.md)
- [ ] newSession.md funciona (nova instància)
- [ ] Actualització documentada a sessions.yaml
- [ ] (Opcional) Commit creat
- [ ] Clone temporal esborrat (memsys3_update_temp)
- [ ] Backup esborrat (després de 1-2 sessions de validació)

---

## 🔗 Referències

- Prompt relacionat: `@memsys3/prompts/deploy.md` (per deployment inicial)
- ADR relacionada: ADR-009 (templates permanents, estructura)
- Backlog: FEATURE-002 (aquest prompt)

---

**Actualització completada!** 🎉

El sistema memsys3 d'aquest projecte ara està actualitzat a l'última versió, conservant totes les dades històriques i personalitzacions.
