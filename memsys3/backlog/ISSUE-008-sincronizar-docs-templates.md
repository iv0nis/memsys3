# ISSUE-008: Sincronizar cambio docs/ → memsys3/docs/ en templates

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Sincronización templates
**Plazo:** Medio plazo
**Fecha identificación:** 2026-02-04
**Contexto:** Sesión refactor arquitectónico dog-fooding

---

## Problema

Durante la sesión 2026-02-04 se movió toda la carpeta `docs/` a `memsys3/docs/` para consistencia arquitectónica (todo el dog-fooding en un solo lugar).

**Cambio realizado en memsys3/ (dog-fooding):**
```
ANTES: /mnt/c/PROYECTOS/memsys3/docs/
DESPUÉS: /mnt/c/PROYECTOS/memsys3/memsys3/docs/
```

**Problema identificado:**
Este cambio afecta a `memsys3_templates/` (producto distribuible) que debe sincronizarse:

1. **Referencias en prompts**: compile-context.md, reunion.md, etc. pueden tener rutas a `docs/`
2. **Estructura de carpetas**: memsys3_templates/ debe reflejar estructura final
3. **README.md**: Si menciona `docs/`, debe actualizarse

**Impacto:**
- Proyectos que usen memsys3 en el futuro tendrán estructura `memsys3/docs/` en lugar de `docs/` en raíz
- Mejora: documentación dog-fooding separada del proyecto usuario

---

## Análisis de Impacto

### Archivos/prompts a revisar en memsys3_templates/:

1. **memsys3_templates/prompts/reunion.md**
   - Verifica si menciona `docs/reunion/`
   - Actualizar a `memsys3/docs/reunion/`

2. **memsys3_templates/prompts/compile-context.md**
   - Verifica si menciona `docs/`
   - Actualizar referencias si existen

3. **memsys3_templates/README.md**
   - Verifica menciones de `docs/`
   - Actualizar si corresponde

4. **Estructura de carpetas**
   - Verificar si `memsys3_templates/docs/` existe
   - Si existe, moverlo a `memsys3_templates/memsys3/docs/` (crear si no existe)

### Referencias actualizadas en memsys3/ (dog-fooding):

- ✅ IMPROVEMENT-007: `docs/` → `memsys3/docs/`
- ✅ sessions.yaml: todas las referencias actualizadas (17 ocurrencias)
- ✅ project-status.yaml: todas las referencias actualizadas (5 ocurrencias)

---

## Propuesta de Solución

### Opción A: Sincronización manual completa

1. Revisar cada prompt en `memsys3_templates/prompts/`
2. Buscar todas las referencias a `docs/`
3. Actualizar a `memsys3/docs/`
4. Mover carpetas si es necesario
5. Testear deployment en proyecto limpio

### Opción B: Sincronización automática con script

Crear script que:
- Busca recursivamente `docs/` en memsys3_templates/
- Lista todas las ocurrencias
- Propone cambios (manual approval)

### Opción C: Gradual (cuando se necesite)

- Dejar como está en templates
- Actualizar cuando deploy.md/actualizar.md se ejecuten
- Documentar en DEVELOPMENT.md el cambio

---

## Decisiones / Acciones

**Pendiente:** Decidir cuándo y cómo sincronizar.

**Consideraciones:**
- No es urgente (templates siguen funcionando)
- Debe hacerse antes de próximo release importante
- Mejora arquitectónica que vale la pena propagar

**Próximos pasos:**
1. Revisar memsys3_templates/ para ver alcance real del cambio
2. Decidir Opción A, B o C
3. Ejecutar sincronización
4. Testear en deployment limpio
5. Actualizar DEVELOPMENT.md con nueva estructura

---

## Referencias

- Commit: b4e17ad "refactor: mover docs/ a memsys3/docs/ (dog-fooding consistente)"
- Sesión: 2026-02-04 "Compilación context.yaml v0.11.0 + Propuesta Extended Thinking"
- IMPROVEMENT-007: Extended Thinking compile-context
- ADR-007: Separación de meta-niveles en READMEs

---

## Notas

- Este ISSUE no bloquea desarrollo actual
- Es deuda técnica de sincronización templates ↔ dog-fooding
- Mejora arquitectónica que simplifica estructura para usuarios finales

**Última actualización:** 2026-02-04
