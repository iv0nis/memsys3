# Deploy memsys3 - Configura el Sistema Memory per al teu Projecte

Tu (DevAgent) has de configurar memsys3 per primera vegada en aquest projecte.

## Objectiu

Desplegar l'estructura completa de memsys3 al projecte actual des de GitHub, personalitzar-la i inicialitzar-la.

## Workflow de Deployment

### Pas 1: Clonar Temporalment memsys3

L'usuari t'indicarà des de quin directori treballes. Normalment serà el directori arrel del seu projecte.

```bash
# Verificar que no hi ha deployment previ
if [ -d "memsys3" ]; then
  echo "⚠️  ERROR: memsys3/ ja existeix en aquest projecte"
  echo ""
  echo "Sembla que ja has desplegat memsys3 aquí."
  echo "Si vols reinstal·lar, renombra o elimina primer:"
  echo "  mv memsys3 memsys3_backup"
  echo "  # o"
  echo "  rm -rf memsys3"
  exit 1
fi

# Netejar memsys3_temp si existeix d'execució prèvia
if [ -d "memsys3_temp" ]; then
  echo "Netejant memsys3_temp/ d'execució prèvia..."
  rm -rf memsys3_temp
fi

# Clonar el repositori com a directori temporal
git clone https://github.com/iv0nis/memsys3 memsys3_temp
```

### Pas 2: Copiar Estructura a memsys3/

Copia TOTA l'estructura de memsys3_templates/ al directori memsys3/ del projecte:

```bash
# Crear estructura base
mkdir -p memsys3/memory/full
mkdir -p memsys3/memory/templates
mkdir -p memsys3/memory/history
mkdir -p memsys3/viz
mkdir -p memsys3/prompts
mkdir -p memsys3/agents

# Crear .gitkeep en history/ perquè es pugi a git
touch memsys3/memory/history/.gitkeep

# Copiar templates
cp memsys3_temp/memsys3_templates/memory/templates/*.yaml memsys3/memory/templates/

# Copiar visualitzador
cp -r memsys3_temp/memsys3_templates/viz/* memsys3/viz/

# Copiar prompts
cp memsys3_temp/memsys3_templates/prompts/*.md memsys3/prompts/

# Copiar agents
cp memsys3_temp/memsys3_templates/agents/*.yaml memsys3/agents/

# Copiar README
cp memsys3_temp/memsys3_templates/memory/README.md memsys3/memory/

# Crear fitxers buits memory/full/
cat > memsys3/memory/full/adr.yaml << 'EOF'
# ADR Log - [NOMBRE_PROYECTO]
# Architecture Decision Records del projecte

adrs: []
EOF

cat > memsys3/memory/full/sessions.yaml << 'EOF'
# Sessions Log - [NOMBRE_PROYECTO]
# Històric de sessions de desenvolupament

sessions: []
EOF
```

### Pas 3: Briefing amb l'Usuari

Abans de personalitzar, llegeix `memsys3/memory/templates/project-status-template.yaml` per saber quins camps necessites.

Pregunta a l'usuari:

1. **Nom del projecte**: Què estem construint?
2. **Descripció 1 línia**: Què fa el projecte?
3. **Objectiu principal**: Quin és el goal del projecte?
4. **Stack tecnològic**:
   - Frontend (framework + versió)?
   - Backend (si aplica)?
   - Deployment platform?
5. **Fase actual**: Planificació, MVP, Beta, Producció?
6. **URLs**: Producció, staging (si existeixen)?
7. **Convencions**:
   - Idioma UI?
   - Idioma variables/comentaris?

### Pas 4: Registrar Versió de memsys3

Obtén la versió i commit del repositori clonat:

```bash
cd memsys3_temp
MEMSYS3_VERSION=$(git describe --tags --always)
MEMSYS3_COMMIT=$(git log -1 --format=%h)
cd ..
```

### Pas 5: Crear project-status.yaml

Amb la info recopilada, crea `memsys3/memory/project-status.yaml`:

```yaml
# Project Status - [NOMBRE_PROYECTO]

metadata:
  ultima_actualitzacio: "[DATA_AVUI]"
  actualitzat_per: "Claude (Initial Deployment)"
  fase: "[FASE]"
  memsys3_version: "[MEMSYS3_VERSION obtinguda en Pas 4]"
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
    # Afegeix camps segons resposta usuari

  backend:
    # Si aplica

  deploy:
    platform: "[PLATFORM]"

urls:
  # production: "[URL_SI_EXISTEIX]"
  # staging: "[URL_SI_EXISTEIX]"

pendents_prioritaris:
  # Si user ha esmentat tasques, afegeix-les
  # Altrament deixa buit

decisions_clau: {}
convencions_codi: {}
historic_sessions: []
```

### Pas 6: Personalitzar prompts/newSession.md

Edita `memsys3/prompts/newSession.md` amb la informació del projecte:

```markdown
- En aquest projecte treballarem en [DESCRIPCION_DEL_PROYECTO].
- Actua segons les instruccions en '@memsys3/agents/main-agent.yaml'
- [COMPORTAMENT_ESPECÍFIC_SI_USER_HA_DEMANAT]
- Llegeix @memsys3/memory/project-status.yaml i @memsys3/memory/context.yaml
```

### Pas 7: Personalitzar agents/main-agent.yaml (opcional)

Si l'usuari ha especificat alguna cosa particular sobre el comportament de l'agent, afegeix-ho:

```yaml
comportament_especific:
  [SI_USER_HA_DEMANAT]: "[INSTRUCCIO]"
```

### Pas 8: Configurar .gitignore (Excloure memsys3 de GitHub)

**IMPORTANT:** Pregunta a l'usuari si vol excloure memsys3/ de GitHub.

**Raó per excloure:**
- memsys3 conté informació específica del teu flux de treball amb IA
- Inclou sessions de treball, decisions internes, gotchas del desenvolupament
- És context local que NO ha de ser públic en el repositori
- Es regenera/actualitza constantment en cada sessió

Pregunta a l'usuari:

---

**🔒 Vols excloure memsys3/ de GitHub?**

memsys3 conté el teu context de desenvolupament local (sessions, decisions, gotchas). Aquesta informació és útil per a tu però generalment NO ha de pujar-se al repositori públic.

**Opcions:**

**A) Sí, excloure memsys3/ de git (RECOMANAT)**
- memsys3/ serà ignorat per git
- No es pujarà al repositori
- Romandrà només a la teva màquina local

⚠️ **IMPORTANT - Limitació de Claude Code:**
Si tries aquesta opció, les @ mencions NO funcionaran (ex: `@memsys3/prompts/newSession.md`).
Això és una limitació de seguretat de Claude Code amb fitxers ignorats.

**Solució/Workaround:**
En lloc d'utilitzar @ mencions, dona instruccions directes a Claude:
- ✅ **"Executa memsys3/prompts/newSession.md"**
- ✅ **"Llegeix i executa les instruccions en memsys3/prompts/compile-context.md"**
- ❌ ~~`@memsys3/prompts/newSession.md`~~ (no funcionarà)

El sistema funcionarà perfectament, només canvia la forma d'invocar els prompts.

**B) No, permetre que memsys3/ es pugi a git**
- memsys3/ s'inclourà en commits
- Es pujarà al repositori (públic o privat)
- Útil si vols compartir el context amb el teu equip
- ✅ Les @ mencions funcionaran normalment

---

**Si l'usuari tria OPCIÓ A (recomanat):**

1. Llegeix el .gitignore existent (si existeix):
   ```bash
   cat .gitignore 2>/dev/null || echo "# .gitignore no existeix, es crearà"
   ```

2. Verifica si memsys3/ ja està exclòs:
   ```bash
   grep -q "memsys3" .gitignore 2>/dev/null && echo "✅ Ja està exclòs" || echo "➕ Necessita afegir-se"
   ```

3. Si NO està exclòs, afegeix-lo al .gitignore:
   - Si .gitignore existeix → usa Edit tool per afegir al final:
     ```
     # memsys3 - Sistema de gestió de context (local only)
     memsys3/
     ```
   - Si .gitignore NO existeix → usa Write tool per crear-lo:
     ```
     # memsys3 - Sistema de gestió de context (local only)
     memsys3/
     ```

4. Verifica que funciona:
   ```bash
   git status --short | grep memsys3
   # Si no apareix res → ✅ correctament ignorat
   ```

**Si l'usuari tria OPCIÓ B:**

- No modificar .gitignore
- Informar que memsys3/ s'inclourà en commits

### Pas 9: Eliminar Clone Temporal

```bash
rm -rf memsys3_temp
```

### Pas 10: Informar a l'Usuari

Confirma que el deployment s'ha completat correctament:

```
✅ memsys3 deployment completat!

Estructura creada:
- memsys3/memory/full/ (adr.yaml, sessions.yaml inicialitzats)
- memsys3/memory/templates/ (guies permanents)
- memsys3/memory/history/ (per a Plan Contingència)
- memsys3/viz/ (visualitzador web)
- memsys3/prompts/ (newSession, endSession, compile-context, etc.)
- memsys3/agents/ (main-agent, context-agent)

Fitxers personalitzats:
- memsys3/memory/project-status.yaml
- memsys3/prompts/newSession.md

Propers passos:
1. Compila context inicial: @memsys3/prompts/compile-context.md
2. Visualitza la memòria: @memsys3/prompts/mind.md
3. Comença a treballar amb sessions: @memsys3/prompts/newSession.md

Escalabilitat automàtica:
📈 Rotació automàtica: >1800 línies → sessions_N.yaml, adr_N.yaml
📦 Plan Contingència: >150K tokens → arxivat a history/
🔍 Context compilat: màxim 2000 línies per sessió
```

## Notes Importants

- **Templates permanents**: `memory/templates/` són guies que Main-Agent consultarà durant endSession. NO els esborris.
- **Clone temporal**: memsys3_temp/ s'esborra després de copiar. És només per a deployment.
- **Personalització mínima**: Només project-status.yaml i newSession.md necessiten personalització. Resta de fitxers són agnòstics.
- **Idioma**: Pregunta a l'usuari quin idioma vol per a la interfície i el codi.

## Troubleshooting

**"git clone falla":**
- Verifica connexió a internet
- Comprova que git està instal·lat: `git --version`

**"mkdir falla":**
- Verifica que ets en el directori correcte del projecte
- Comprova permisos d'escriptura

**"Templates no es copien":**
- Verifica que memsys3_temp/ existeix
- Comprova que la ruta memsys3_temp/memsys3_templates/ té els fitxers

---

**Deployment completat. El sistema està llest per utilitzar.**
