# ISSUE-014: Formato fecha reuniones debería ser YYYYMMDD

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Mejora / Consistencia
**Fecha identificación:** 2026-02-20

---

## Problema / Necesidad

El formato actual de naming de archivos de reuniones es `DDMMYY_N.md` (ej: `200226_5.md`), lo que causa:
- Ordenación incorrecta en el filesystem (ordena por día, no por fecha real)
- Ambigüedad: `200226` puede leerse como día 20, mes 02, año 26 o de otras formas
- Inconsistente con el estándar ISO 8601 usado en el resto de memsys3 (fechas en YAML van como `YYYY-MM-DD`)

## Comportamiento esperado

Formato `YYYYMMDD_N.md` (ej: `20260220_5.md`):
- Ordena correctamente por fecha en cualquier filesystem
- Sin ambigüedad
- Consistente con ISO 8601

## Impacto

- Cambiar documentación en `meet.md` (Protocolo común, sección Naming)
- Los archivos existentes en `docs/meets/` quedan con el formato antiguo (no hace falta renombrarlos retroactivamente)

## Referencias

- Archivos actuales: `200226_1.md` ... `200226_5.md`, `170226_1.md`, etc.
- `meet.md` sección "Naming y ubicación del archivo"
