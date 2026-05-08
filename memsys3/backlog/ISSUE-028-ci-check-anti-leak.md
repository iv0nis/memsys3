# ISSUE-028: CI check anti-leak (cuando se establezca pipeline)

**Estado:** Abierto
**Prioridad:** Baja
**Tipo:** Tech debt / DevOps
**Plazo:** Cuando se establezca pipeline CI en el repo
**Fecha identificación:** 2026-05-08
**Origen:** ADR-025 (alternativas descartadas → "CI check pospuesto")

---

## Problema / Necesidad

ADR-025 estableció un protocolo anti-leak en dos capas:

1. **Capa 1**: hook `pre-commit` en `.githooks/pre-commit` (defensa local).
2. **Capa 2**: auditoría en `comprobar_alineamiento.md` (defensa periódica manual).

Ambas capas son **locales al dev**. Limitaciones:

- Un PR de un contributor externo puede introducir leak antes de que el maintainer audite.
- `--no-verify` permite saltarse el hook (escape válido pero peligroso).
- Si un dev no ejecuta `git config core.hooksPath .githooks`, el hook NO está activo.

Actualmente el repo memsys3 NO tiene pipeline CI activo. Cuando se establezca uno (GitHub Actions u otro), conviene añadir un check que ejecute la misma lógica del hook contra cada push/PR.

## Propuesta / Opciones

### Opción A — GitHub Action (recomendada cuando llegue el momento)

Workflow en `.github/workflows/anti-leak.yml`:

```yaml
name: Anti-leak templates/backlog
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify no leaks in memsys3_templates/backlog/
        run: |
          set -e
          LEAKS=$(find memsys3_templates/backlog -maxdepth 1 -type f -name '[A-Z]*-[0-9]*-*.md' || true)
          if [ -n "$LEAKS" ]; then
            echo "❌ ANTI-LEAK (ADR-025): items de backlog en distribuible:"
            echo "$LEAKS"
            exit 1
          fi
          # También vetar items en cualquier subdir de memsys3_templates/
          OTHER=$(find memsys3_templates -name '[A-Z]*-[0-9]*-*.md' -type f || true)
          if [ -n "$OTHER" ]; then
            echo "❌ ANTI-LEAK: items de backlog encontrados en memsys3_templates/:"
            echo "$OTHER"
            exit 1
          fi
          echo "✅ Sin leaks"
```

**Pros**:
- Defensa al PR/push, atrapa contributors externos antes del merge.
- Funciona aunque el dev no tenga `core.hooksPath` configurado.
- Funciona aunque el dev haya usado `--no-verify` localmente.

**Contras**:
- Requiere que GitHub Actions esté habilitado en el repo.
- Latencia (segundos) vs hook local (instantáneo).

### Opción B — Reutilizar el hook como script invocable

Refactorizar `.githooks/pre-commit` en un script reutilizable + el hook como wrapper. La GHA invocaría el mismo script, garantizando una sola fuente de verdad.

**Pros**: DRY, mantenimiento único.
**Contras**: Refactor adicional, complejidad inicial. Hacer en su momento si el script crece.

## Decisiones / Acciones

- [ ] Esperar a que se establezca pipeline CI en el repo (puede no ocurrir si memsys3 nunca recibe contributors externos)
- [ ] Implementar Opción A (workflow GHA) cuando aplique
- [ ] Considerar Opción B si el script anti-leak crece más allá de ~30 líneas

## Referencias

- **ADR origen**: ADR-025 (estrategia dogfooting versionado, alternativas descartadas → "CI check")
- **Mecanismo local**: `.githooks/pre-commit` + bloque PASO 6.5 en `memsys3/prompts-dev/comprobar_alineamiento.md`
- **Incidente que motiva la cadena**: IMPROVEMENT-008 (resuelto en BLUEPRINT-001 Frente 3)
- **Item paralelo similar**: ISSUE-022 (hook pre-commit anti-firma) — podría compartir infraestructura `.githooks/`
