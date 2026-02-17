# FEATURE-008: Soporte multilenguaje (i18n) de memsys3

**Estado:** Propuesto
**Prioridad:** Baja
**Tipo:** Feature / Internacionalización
**Plazo:** Long-term
**Fecha identificación:** 2026-02-17

---

## Problema / Necesidad

memsys3 está actualmente desarrollado en español. Se intentó una versión catalana (`actualizar_cat.md`) pero no funcionó bien. El objetivo a largo plazo es hacer memsys3 verdaderamente multilenguaje.

## Propuesta

1. **Traducir código al inglés**: variables, keys YAML, nombres de campos internos (ej: `visio_general`, `estat_actual`, `seguent_milestone` → `overview`, `current_state`, `next_milestone`)
2. **Sistema i18n para prompts**: templates de prompts adaptables al idioma del proyecto
3. **Inglés como base canónica**: memsys3 en inglés como fuente, con traducciones opcionales

## Contexto

- El intento de sincronización catalán (branch `catalan` en GitHub + `actualizar_cat.md`) fue descartado
- El Paso 3 del deploy ya pregunta idioma UI/código al usuario, pero esa info no se propaga bien
- Fix urgente previo: asegurar que `newSession.md` incluya instrucción de idioma (ver project-status siguiente_milestone)

## Referencias

- `prompts/actualizar_cat.md` - intento previo (descartado)
- `memsys3/docs/archivo/` - documentación del proceso de traducción catalán
