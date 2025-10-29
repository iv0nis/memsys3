# End Session - Documenta la Sessió Actual

Tu (DevAgent) has de documentar aquesta sessió de treball al sistema Memory del projecte.

## Objectiu

Registrar què s'ha fet durant aquesta sessió perquè el pròxim DevAgent tingui context complet.

## Workflow

### 1. Recopilar Evidències Objectives

Recull evidències de què s'ha fet:

```bash
# Git (si disponible)
git status && git diff --stat && git log --oneline -5

# Fitxers modificats (ajusta -mmin segons durada sessió)
find . -type f -mmin -180 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*'

# Bash history
history | tail -30
```

**Notes:** Aquestes evidències són opcionals però recomanades. Si alguna falla, continua amb el teu context intern.

### 2. Auto-analitzar la Sessió

Identifica:
- **Features/Tasques**: Què has implementat, bugs resolts, refactorings
- **Problemes Resolts**: Obstacles trobats i com els has solucionat
- **Decisions Preses**: Decisions tècniques o arquitectòniques (importants → ADR)
- **Tech afegida/eliminada**: Dependencies, tools i per què
- **Deployments**: URLs, serveis desplegats
- **Pròxims Passos**: Què queda pendent

### 3. Comprovar Rotacions Automàtiques

**Sessions.yaml:**
```bash
wc -l memsys3/memory/full/sessions.yaml
# Si > 1800 línies:
ls memsys3/memory/full/sessions_*.yaml 2>/dev/null  # Trobar proper número
cp memsys3/memory/full/sessions.yaml memsys3/memory/full/sessions_N.yaml  # Copiar
wc -l memsys3/memory/full/sessions_N.yaml  # Verificar
# Crear nou sessions.yaml amb header YAML buit
```

**adr.yaml:**
```bash
wc -l memsys3/memory/full/adr.yaml
# Si > 1800 línies: mateix procés → adr_N.yaml
```

**Rotació = Copia segura + Verificació + Nou fitxer buit**

### 4. Documentar

**A. Afegir Sessió a `memsys3/memory/full/sessions.yaml`:**
- Afegir al PRINCIPI de l'array `sessions:`
- Usar `memsys3/memory/templates/sessions-template.yaml` com a guia
- ID i data: YYYY-MM-DD d'avui
- Títol descriptiu i concís
- Sigues complet però evita detalls massa granulars

**B. Crear ADRs si cal (a `memsys3/memory/full/adr.yaml`):**

Només si has pres **decisions arquitectòniques importants**:
- Triar llibreria/framework en lloc d'un altre
- Canviar arquitectura del sistema
- Decidir patró de disseny
- Canviar stack tecnològic

**NO crear ADR per:**
- Canvis cosmètics (colors, padding)
- Validacions de formularis
- Bugs menors
- Refactorings de funcions

Si crees ADR:
1. Comprovar rotació adr.yaml (pas 3)
2. Usar `memsys3/memory/templates/adr-template.yaml`
3. Linkear ADR des de sessió (camp `adr_relacionada`)

**C. Actualitzar `memsys3/memory/project-status.yaml`:**
- `metadata.ultima_actualitzacio`: Data d'avui
- `metadata.actualitzat_per`: "Claude (Session [Títol])"
- `estat_actual.ultima_feature`: Si has completat feature
- `features`: Canviar `estat: operatiu` si s'ha completat
- `historic_sessions`: Afegir entrada resumida
- `pendents_prioritaris`: Actualitzar segons pròxims passos

### 5. Informar l'Usuari

Resum breu de què s'ha documentat:

```
✅ Sessió documentada a memsys3/memory/full/sessions.yaml
✅ [N] ADRs creades (si n'hi ha)
✅ memsys3/memory/project-status.yaml actualitzat
✅ Rotació feta (si calia): sessions.yaml → sessions_N.yaml

Highlights de la sessió:
- [Feature principal implementada]
- [Problema crític resolt]
- [Decisió arquitectònica presa]

Pròxims passos: [Top 2-3 tasques pendents]
```

## Notes Importants

- **Format YAML**: Indentació estricta (2 espais), usa `|` per multiline
- **Consistència**: Segueix estil de sessions/ADRs anteriors
- **NO preguntar**: Assumeix que la documentació és correcta (pregunta només si falta context crític)
- **Context Agent**: No et preocupis per tokens aquí, ell filtrarà després
- **Rotació automàtica**: Preserva SEMPRE les dades (sessions_N.yaml, adr_N.yaml)

---

**Comença ara la documentació de la sessió actual.**
