# ISSUE-030: Wiki GitHub sync post-v1.0

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Issue (deuda documentación)
**Plazo:** Post-v1.0
**Fecha identificación:** 2026-05-09
**Sesión origen:** 2026-05-09 (BLUEPRINTING-001 Frente 8 Bloque 2 docs)

---

## Problema / Necesidad

Wiki GitHub en `https://github.com/iv0nis/memsys3/wiki` tiene 4 páginas creadas en sesión 2026-04-16 (release v0.21.0):
- Home (propuesta de valor)
- Prompts Reference
- Workflow
- Agents

Tras los Frentes 1-7 BLUEPRINT-001 (sesiones 2026-05-07 → 2026-05-08), el wiki probablemente está **desfasado**:
- No menciona PRINCIPLES.md (creado en Frente 1, ADR-022)
- No menciona memory.yaml (ADR-020)
- No menciona backlog/docs/ informe+plan (ADR-021)
- No menciona hook anti-leak (ADR-025)
- No menciona multi-work integration (v0.24.0)
- Posiblemente referencias `DevAgent`/`DevAI` residuales (terminología erradicada en Frente 5)
- Lista de prompts puede estar incompleta (no menciona `multi_work.md`, `commands.md` actualizado, etc.)

## Por qué deferido a post-v1.0

Frente 8 BLUEPRINT-001 ya tiene scope grande (cleanup backlog + docs/ landscape + decisiones arquitectónicas + tag v1.0.0). Wiki sync requiere:

1. Clone separate repo: `git clone https://github.com/iv0nis/memsys3.wiki.git`
2. Audit completo de las 4 páginas
3. Reescritura de secciones desfasadas
4. Commit + push al wiki repo

Estimación: 1-2h trabajo cuidadoso.

Diferirlo permite:
- Cerrar v1.0.0 en plazo razonable
- Actualizar wiki **una vez con todo consolidado** (no actualizar dos veces: ahora + tras v1.0)
- Anuncio v1.0 puede mencionar "wiki actualizada como sigue" en release notes

## Propuesta / Acciones

Tras tag v1.0.0:

1. **Clone wiki**:
   ```bash
   git clone https://github.com/iv0nis/memsys3.wiki.git
   cd memsys3.wiki
   ```

2. **Audit las 4 páginas** vs estado actual del repo:
   - Home: actualizar pitch con principios + features v1.0
   - Prompts Reference: añadir `multi_work.md`, actualizar descripciones de `actualizar.md` (pasos 6.4-6.6), `endSession.md` (paso 2.7-2.8), `compile-context.md` (Tier 3 dual folder)
   - Workflow: incluir backlog cleanup automatizado (paso 2.8 endSession)
   - Agents: añadir bloque `coordinacion_paralela` (multi-work), `memoria_usuario` (ADR-020), restricciones nuevas

3. **Páginas potenciales nuevas a crear**:
   - "Principles" — replicar PRINCIPLES.md (o link a raíz repo si GitHub renderiza desde root)
   - "Migration v0.X → v1.0" — guía si hay breaking changes (verificar)
   - "FAQ" — basada en preguntas reales tras release

4. **Sync continuo**: definir convención (¿quién edita wiki? ¿el mantenedor en cada release? ¿comunidad via PR?)

## Decisiones / Acciones

Pendiente de ejecución post-v1.0.

**Trigger**: tras `git push --tags v1.0.0` y publicación de release notes.

## Referencias

- **Origen**: BLUEPRINT-001 Frente 8 Bloque 2 docs (sesión 2026-05-09)
- **Wiki actual**: https://github.com/iv0nis/memsys3/wiki
- **Sesión wiki creación**: 2026-04-16 (release v0.21.0)
- **Items relacionados**: ISSUE-025 (link roto README — UPDATE.md ya publicado, DEVELOPMENT.md publicado en este Frente 8)
- **Frentes que afectan wiki**: 1 (PRINCIPLES.md), 4 (templates), 5 (residualidad terminología), 6 (dogfooting + hook), 7 (smoke tests + EXPLORATION-004 paso 2.7)

<!-- version: 0.1.0 -->
