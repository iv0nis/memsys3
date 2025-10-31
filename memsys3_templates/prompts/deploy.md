# Deploy memsys3 - Configura el Sistema Memory per al teu Projecte

Tu (DevAgent) has de configurar memsys3 per primer cop en aquest projecte.

## Objectiu

Desplegar l'estructura completa de memsys3 al projecte actual des de GitHub, personalitzar-la i inicialitzar-la.

## Workflow de Deployment

### Pas 1: Clonar Temporalment memsys3

El usuari t'indicarà des de quin directori treballes. Normalment serà el directori arrel del seu projecte.

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

# Crear .gitkeep en history/ para que se suba a git
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

### Pas 4: Crear project-status.yaml

Amb la info recopilada, crea `memsys3/memory/project-status.yaml`:

```yaml
# Project Status - [NOMBRE_PROYECTO]

metadata:
  ultima_actualitzacio: "[DATA_AVUI]"
  actualitzat_per: "Claude (Initial Deployment)"
  fase: "[FASE]"

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
  # Si user ha mencionat tasques, afegeix-les
  # Altrament deixa buit

decisions_clau: {}
convencions_codi: {}
historic_sessions: []
```

### Pas 5: Personalitzar prompts/newSession.md

Edita `memsys3/prompts/newSession.md` amb la informació del projecte:

```markdown
- En aquest projecte treballarem en [DESCRIPCIO_DEL_PROJECTE].
- Actúa segons les instruccions a '@memsys3/agents/main-agent.yaml'
- [COMPORTAMENT_ESPECIFIC_SI_USER_HA_DEMANAT]
- Llegeix @memsys3/memory/project-status.yaml i @memsys3/memory/context.yaml
```

### Pas 6: Personalitzar agents/main-agent.yaml (opcional)

Si l'usuari ha especificat alguna cosa particular sobre el comportament de l'agent, afegeix-ho:

```yaml
comportament_especific:
  [SI_USER_HA_DEMANAT]: "[INSTRUCCIO]"
```

### Pas 7: Eliminar Clone Temporal

```bash
rm -rf memsys3_temp
```

### Pas 8: Informar l'Usuari

Confirma que el deployment s'ha completat correctament:

```
✅ memsys3 deployment completat!

Estructura creada:
- memsys3/memory/full/ (adr.yaml, sessions.yaml inicialitzats)
- memsys3/memory/templates/ (guies permanents)
- memsys3/memory/history/ (per Plan Contingencia)
- memsys3/viz/ (visualitzador web)
- memsys3/prompts/ (newSession, endSession, compile-context, etc.)
- memsys3/agents/ (main-agent, context-agent)

Fitxers personalitzats:
- memsys3/memory/project-status.yaml
- memsys3/prompts/newSession.md

Pròxims passos:
1. Compila context inicial: @memsys3/prompts/compile-context.md
2. Visualitza la memòria: @memsys3/prompts/mind.md
3. Comença a treballar amb sessions: @memsys3/prompts/newSession.md

Escalabilitat automàtica:
📈 Rotació automàtica: >1800 línies → sessions_N.yaml, adr_N.yaml
📦 Plan Contingencia: >150K tokens → archivado a history/
🔍 Context compilat: màxim 2000 línies per sessió
```

## Notes Importants

- **Templates permanents**: `memory/templates/` són guies que Main-Agent consultarà durant endSession. NO els esborris.
- **Clone temporal**: memsys3_temp/ s'esborra després de copiar. És només per deployment.
- **Personalització mínima**: Només project-status.yaml i newSession.md necessiten personalització. Resta de fitxers són agnòstics.
- **Idioma**: Pregunta a l'usuari quin idioma vol per la interfície i el codi.

## Troubleshooting

**"git clone falla":**
- Verifica connexió a internet
- Comprova que git està instal·lat: `git --version`

**"mkdir falla":**
- Verifica que estàs al directori correcte del projecte
- Comprova permisos d'escriptura

**"Templates no es copien":**
- Verifica que memsys3_temp/ existeix
- Comprova que la ruta memsys3_temp/memsys3_templates/ té els fitxers

---

**Deployment completat. El sistema està llest per usar.**
