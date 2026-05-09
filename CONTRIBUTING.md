# Contributing to memsys3

Gracias por tu interés en contribuir a memsys3. Esta guía cubre el flujo básico para reportar bugs, proponer cambios y mantener la calidad del código.

Para entender la **arquitectura interna** del repositorio (estructura, dogfooting/templates split, sistema de rutas), consulta [`DEVELOPMENT.md`](DEVELOPMENT.md).

---

## Antes de empezar

1. **Lee [`PRINCIPLES.md`](memsys3_templates/PRINCIPLES.md)** — los 10 principios sistémicos invariantes que rigen memsys3 (anti-CDC, agnosticismo, una sola carpeta, etc.). Cualquier cambio debe poder justificarse desde uno de ellos.

2. **Activa los git hooks anti-leak** (protección dogfooting → distribuible, ADR-025):
   ```bash
   git config core.hooksPath .githooks
   ```
   Esto se hace una sola vez tras clonar el repo. Sin esto, los commits no validan que items de dogfooting no se filtren al scaffold distribuible.

3. **Familiarízate con la estructura** del repo: `DEVELOPMENT.md` explica la separación `memsys3_templates/` (distribuible agnóstico) vs `memsys3/` (instancia dogfooting).

---

## Cómo reportar bugs

1. Verifica que no exista un issue similar en [GitHub Issues](https://github.com/iv0nis/memsys3/issues).
2. Crea un issue nuevo con:
   - **Contexto**: qué intentabas hacer
   - **Pasos para reproducir**: comandos exactos, prompts ejecutados
   - **Comportamiento esperado vs actual**
   - **Versión de memsys3**: `cat memsys3/memory/project-status.yaml | grep memsys3_version`
   - **Modelo de IA usado**: Claude Sonnet/Opus/etc., Gemini, Codex...
   - **Contexto del sistema**: SO, terminal, otros agentes activos en paralelo

3. Si el bug ya está documentado en `memsys3/backlog/`, comenta el ID del item existente en lugar de duplicar.

---

## Cómo proponer cambios

### Workflow básico

1. **Fork** del repo en GitHub.
2. **Clone** tu fork localmente.
3. Crea una **branch** descriptiva: `git checkout -b fix/issue-NNN-descripcion-corta` o `feat/nombre-corto`.
4. **Activa los hooks** (paso 2 de "Antes de empezar").
5. Realiza tus cambios siguiendo las convenciones de abajo.
6. **Commits atómicos** — uno por cambio coherente.
7. **Push a tu fork** y abre un **Pull Request** contra `master` con descripción clara.

### Para cambios significativos

Si tu cambio afecta arquitectura, principios o el sistema de prompts/agents:

1. Abre primero un **issue de discusión** explicando el problema y la propuesta.
2. Espera feedback antes de invertir tiempo en implementación.
3. Si el cambio implica una decisión arquitectónica, considera proponer una **ADR** siguiendo el formato de `memsys3/memory/full/adr.yaml`.

---

## Convenciones de commits

### Formato

```
<tipo>(<scope opcional>): <descripción concisa>

<body opcional con detalle>

<footer opcional con refs ADR/ISSUE>
```

### Tipos

- `feat`: nueva funcionalidad
- `fix`: corrección de bug
- `docs`: cambios solo en documentación
- `refactor`: cambio de código sin alterar comportamiento
- `test`: añadir o modificar tests
- `chore`: tareas de mantenimiento (bumps de versión, cleanup)

### Reglas

- **Imperativo en español**: "añade", "corrige", "actualiza" (no "añadido", "corregido")
- **Resumen ≤72 caracteres** en la primera línea
- **Body opcional**: contexto adicional separado por línea en blanco
- **Referenciar ADR/ISSUE** cuando aplica: "(ADR-025)", "(cierra ISSUE-NNN)"

### ⚠️ Regla dura: SIN firma `Co-Authored-By:`

**NUNCA añadas `Co-Authored-By: Claude` (o cualquier modelo de IA) en tus commits.**

Esta es una convención dura del proyecto. Los commits reflejan solo autoría humana. Hay defensa en profundidad de 4 capas en `memsys3/prompts/github.md` — si trabajas con asistencia de IA, asegúrate de que los commits salgan limpios.

Verificación rápida:
```bash
git log -5 --format="%B" | grep -i "co-authored" && echo "❌ FIRMA DETECTADA" || echo "✅ OK"
```

---

## Code style

### YAML
- Indentación 2 espacios estricta
- Strings con comillas dobles: `key: "value"`
- Multiline con `|` para preservar saltos, `>` para colapsarlos

### Markdown
- **Idioma**: español (es la lingua franca del proyecto)
- **Sin emojis** salvo en headers de prompts ejecutables y badges OSS estándar
- **Estilo conciso**: el agente que lo lea consume tokens

### Bash
- **POSIX agnóstico de SO** — evita extensiones GNU-only que rompen en BSD/macOS
- Ejemplo: `sed -i 'expr' file` falla en macOS; usa `mktemp` + `cat` + `mv` para inserts agnósticos
- Quote variables: `"$VAR"` no `$VAR`
- Verifica exit codes inmediatamente (no a través de pipes que enmascaran)

### Convención general
- **Nombres de archivos**: minúsculas con guiones (`mi-archivo.md`), excepto convenciones explícitas (`README.md`, `LICENSE`, etc.)
- **Items de backlog**: `PREFIJO-NNN-descripcion-corta.md` (PREFIJO en mayúsculas: `ISSUE`, `FEATURE`, `IMPROVEMENT`, `SPEC`, `BLUEPRINT`, `EXPLORATION`)

---

## Checklist antes de commit

- [ ] He activado los hooks (`git config core.hooksPath .githooks`)
- [ ] El cambio respeta los 10 principios de `PRINCIPLES.md`
- [ ] Si es cambio de templates, he sincronizado dogfooting (`memsys3/`) con distribuible (`memsys3_templates/`)
- [ ] Mensaje de commit con prefijo correcto, en español, sin firma `Co-Authored-By:`
- [ ] Si hay decisión arquitectónica, he creado/actualizado ADR
- [ ] Si toco scripts bash, son agnósticos de SO

---

## Primer PR: test de deployment

Para validar que tu PR no rompe el flujo crítico:

1. Crea un proyecto de prueba en otro directorio: `mkdir /tmp/test-memsys3 && cd /tmp/test-memsys3`
2. Despliega tu fork:
   ```bash
   git clone https://github.com/<tu-fork>/memsys3.git memsys3_temp
   # Ejecuta manualmente el Paso 2 de memsys3_temp/memsys3_templates/prompts/deploy.md
   ```
3. Verifica el inventario canónico tras deploy (debe coincidir con ADR-023).
4. Reporta el resultado en el PR (smoke test pasa / falla).

---

## Flujo de revisión

- Los PRs se revisan en orden de llegada cuando el mantenedor está disponible.
- Cambios pequeños y bien scoped se mergean rápido. Cambios grandes pueden requerir varias iteraciones.
- Si tu PR queda sin respuesta más de 2 semanas, ping cordial al mantenedor.

---

## Recursos

- **Principios**: [`memsys3_templates/PRINCIPLES.md`](memsys3_templates/PRINCIPLES.md)
- **Arquitectura**: [`DEVELOPMENT.md`](DEVELOPMENT.md)
- **Histórico de versiones**: [`CHANGELOG.md`](CHANGELOG.md)
- **Cómo actualizar memsys3**: [`UPDATE.md`](UPDATE.md)
- **Wiki GitHub**: https://github.com/iv0nis/memsys3/wiki
- **ADRs**: `memsys3/memory/full/adr.yaml` + `adr_1.yaml`

---

## Licencia

memsys3 está bajo licencia MIT (ver [`LICENSE`](LICENSE)). Al contribuir, aceptas que tus contribuciones se distribuyan bajo los mismos términos.
