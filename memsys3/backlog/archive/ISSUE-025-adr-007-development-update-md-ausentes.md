# ISSUE-025: README.md raíz linkea `docs/UPDATE.md` y `docs/DEVELOPMENT.md` que no existen en raíz repo

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Issue (link roto + brecha ADR-007)
**Plazo:** Antes de release v1.0 (Frente 8)
**Fecha identificación:** 2026-05-07
**Origen:** Auditoría BLUEPRINT-001 Frente 2 — verificación ADR-007.

---

## Problema

ADR-007 (Separación de meta-niveles en READMEs) define cuatro READMEs por audiencia:

1. `README.md` raíz — descubrimiento del repo (existe).
2. `memsys3_templates/README.md` — sistema desplegado (existe).
3. `docs/DEVELOPMENT.md` — contribuidores de memsys3.
4. `docs/UPDATE.md` — quien actualiza memsys3.

Estado actual:

- `docs/DEVELOPMENT.md` y `docs/UPDATE.md` **NO existen en raíz repo** (raíz `docs/` solo contiene `comunidad/` y `reports/`).
- Sí existen en `memsys3/docs/` (dogfooding) pero esa ruta no se publica.
- `README.md` raíz **línea 217** referencia explícitamente `docs/UPDATE.md` → **link roto público**.

## Discusión sobre ubicación correcta

ADR-007 indica que estos archivos son para **audiencias del repo** (contribuidores y upgraders), no para usuarios desplegados. Por tanto:

- ✅ Lugar correcto: **raíz repo** (`docs/DEVELOPMENT.md`, `docs/UPDATE.md`).
- ❌ NO en `memsys3_templates/docs/` (eso sería para usuarios que ya desplegaron).

## Causa probable

Durante refactors anteriores (sesión 2026-02-04 movió `docs/` → `memsys3/docs/`), los archivos quedaron solo en dogfooding sin que se sincronizara una copia "publicable" a raíz repo.

## Acción propuesta

1. Decidir contenido canónico de `docs/DEVELOPMENT.md` y `docs/UPDATE.md` para audiencia pública (no leak de dogfooting).
2. Crear ambos en raíz `docs/`.
3. Verificar que README.md:217 link funciona.
4. Considerar si el contenido se deriva de los actuales `memsys3/docs/DEVELOPMENT.md` y `memsys3/docs/UPDATE.md` (probablemente sí, con limpieza de referencias internas al dogfooting).

## Impacto en release v1.0

Medio. Link roto en README público es mala impresión para usuarios externos descubriendo el repo. Debe resolverse antes de tagear v1.0.0. Encaja naturalmente en **Frente 8** (Comunicación + tag v1.0.0) del BLUEPRINT-001.

## Referencias

- Auditoría: `memsys3/backlog/docs/informe_BLUEPRINT-001-auditoria.md` §4.1
- ADR origen: ADR-007 en `memsys3/memory/full/adr.yaml`
- Link roto: `README.md:217`
