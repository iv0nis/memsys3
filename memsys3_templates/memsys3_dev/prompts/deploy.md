# Deploy memsys3 - Configura el Sistema Memory per al teu Projecte

Tu (Main-Agent) has de configurar memsys3 per primer cop en aquest projecte.

## Objectiu

Crear l'estructura de carpetes necessària, copiar templates agnòstics i inicialitzar fitxers específics del projecte.

## Prerequisit

Aquest prompt assumeix que tens accés als fitxers de memsys3 (clonat o descarregat del repo).

## Tasques a Realitzar

### 1. Crear Estructura de Carpetes

Crea la següent estructura al directori arrel del projecte:

```bash
mkdir -p memory/full
mkdir -p memory/templates
mkdir -p memory/viz
mkdir -p prompts
mkdir -p agents
```

### 2. Copiar Fitxers Agnòstics

Copia els següents fitxers des de memsys3:

**Templates:**
```bash
cp memsys3/memory/templates/*.yaml memory/templates/
```

**Visualitzador:**
```bash
cp memsys3/memory/viz/* memory/viz/
```

**Prompts:**
```bash
cp memsys3/prompts/compile-context.md prompts/
cp memsys3/prompts/endSession.md prompts/
cp memsys3/prompts/mind.md prompts/
cp memsys3/prompts/newSession.md prompts/
```

**Agents:**
```bash
cp memsys3/agents/context-agent.yaml agents/
cp memsys3/agents/main-agent.yaml agents/
```

**README:**
```bash
cp memsys3/memory/README.md memory/
```

### 3. Briefing amb l'Usuari

Fes les següents preguntes a l'usuari per personalitzar el sistema:

**Sobre el projecte:**
- Nom del projecte?
- Descripció breu (1-2 línies)?
- En què esteu treballant? (ex: app web, API, sistema intern, etc.)
- Fase actual? (ex: Planificació, Development, MVP, Production)

**Stack tecnològic:**
- Framework frontend (si n'hi ha)?
- Framework/Runtime backend?
- Base de dades (si n'hi ha)?
- Plataforma de deployment?

**URLs (si ja existeixen):**
- URL de producció?
- URL de staging?

**Comportament del Main-Agent:**
- Com vols que es comporti l'agent? (ex: proactiu, només quan se li demani, balanç)
- Alguna instrucció específica per aquest projecte?

**Estat inicial:**
- Hi ha features ja implementades?
- Hi ha tasques pendents prioritàries?

### 4. Crear project-status.yaml

Amb les respostes del briefing, crea `memory/project-status.yaml`:

```yaml
metadata:
  ultima_actualitzacio: "[DATA_AVUI]"
  actualitzat_per: "Main-Agent (Initial Setup)"
  fase: "[FASE_RESPOSTA_USER]"

visio_general:
  que_es: "[DESCRIPCIO_RESPOSTA_USER]"
  objectiu: "[OBJECTIU_PRINCIPAL]"
  client: "[CLIENT_O_INTERN]"

estat_actual:
  fase: "[FASE_RESPOSTA_USER]"
  ultima_feature: "N/A (setup inicial)"
  seguent_milestone: "[MILESTONE_SI_EN_SAP]"

features:
  # Si user ha mencionat features existents, afegeix-les aquí
  # Altrament deixa buit o comenta

stack_tecnologic:
  frontend: "[FRAMEWORK_FRONTEND]"
  backend: "[RUNTIME_BACKEND]"
  database: "[DATABASE_O_CAP]"
  deploy: "[PLATFORM_DEPLOY]"

urls:
  # production: "[URL_SI_EXISTEIX]"
  # staging: "[URL_SI_EXISTEIX]"

pendents_prioritaris:
  # Si user ha mencionat tasques, afegeix-les
  # Altrament deixa buit

decisions_clau: {}
gotchas_i_issues: {}
convencions_codi: {}
historic_sessions: []
```

### 5. Personalitzar prompts/newSession.md

Edita `prompts/newSession.md` amb la informació del projecte:

```markdown
- En aquest projecte treballarem en [DESCRIPCIO_DEL_PROJECTE].
- Actúa segons les instruccions a 'agents/main-agent.yaml'
- [COMPORTAMENT_ESPECIFIC_SI_USER_HA_DEMANAT]
- Llegeix memory/project-status.yaml i memory/context.yaml
```

### 6. Personalitzar agents/main-agent.yaml (opcional)

Si l'usuari ha especificat alguna cosa particular sobre el comportament de l'agent, afegeix-ho:

```yaml
rol: Development Agent
descripcio: Agent que implementa features, resol bugs i desenvolupa el projecte utilitzant el sistema Memory per mantenir context entre sessions

# Afegeix aquí responsabilitats o notes específiques del projecte si cal
```

### 7. Inicialitzar Fitxers Buits

Crea els següents fitxers buits per començar:

**memory/full/adr.yaml:**
```yaml
# Architecture Decision Records
# Documentació completa de totes les decisions arquitectòniques del projecte

adrs:
  # Les ADRs s'afegiran amb @prompts/endSession.md quan es prenguin decisions
```

**memory/full/sessions.yaml:**
```yaml
# Sessions Log
# Històric de totes les sessions de treball significatives

sessions:
  # Les sessions s'afegiran amb @prompts/endSession.md al final de cada sessió
```

**NO crear** `memory/context.yaml` - es generarà quan executis `@prompts/compile-context.md` per primer cop.

### 8. Confirmar Instal·lació

Informa l'usuari que memsys3 s'ha configurat correctament:

```
✅ memsys3 configurat correctament!

Estructura creada:
  - memory/ (templates, viz, full/, README.md)
  - prompts/ (compile-context, endSession, mind, newSession)
  - agents/ (context-agent, main-agent)

Fitxers inicialitzats:
  - memory/project-status.yaml (amb dades del teu projecte)
  - memory/full/adr.yaml (buit, preparat per decisions)
  - memory/full/sessions.yaml (buit, preparat per sessions)

Pròxims passos:
1. Comença a desenvolupar normalment
2. Al final de la sessió: @prompts/endSession.md
3. Per compilar context: @prompts/compile-context.md
4. Per veure la "ment" dels agents: @prompts/mind.md
```

## Notes

- **No sobreescriure** si els fitxers ja existeixen (preguntar abans)
- **Personalització**: Cada projecte és únic, adapta segons les respostes
- **Flexibilitat**: Si user no sap alguna resposta, deixa placeholder o "TBD"
- **Documentació**: Recorda que memory/README.md té tota la info de com usar el sistema

---

**Comença ara el deployment de memsys3 per aquest projecte.**
