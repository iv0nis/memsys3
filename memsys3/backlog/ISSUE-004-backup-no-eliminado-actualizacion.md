# ISSUE-004: Backup no eliminado tras actualización de memsys3

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Tech Debt / Limpieza
**Plazo:** Corto plazo
**Fecha identificación:** 2025-12-16

---

## Problema / Necesidad

El comando de actualización de memsys3 (`@memsys3/prompts/actualizar.md`) genera un backup del deployment anterior, pero **NO lo elimina** al finalizar el proceso exitoso.

**Comportamiento actual:**
- Actualización ejecutada correctamente
- Backup creado (probablemente en algún directorio temporal o con sufijo `_backup`)
- Backup permanece en el sistema después de validación exitosa

**Comportamiento esperado:**
- Si actualización es exitosa → eliminar backup automáticamente
- Si actualización falla → mantener backup para rollback

**Consecuencia:**
- Acumulación de archivos residuales
- Usuario debe limpiar manualmente
- No está claro si es seguro borrar el backup

---

## Análisis Requerido

Pendiente de investigación en próxima sesión:

1. **¿Dónde se genera el backup?**
   - Ruta exacta del backup creado
   - Naming pattern (sufijo, timestamp, etc.)

2. **¿Por qué no se borra?**
   - Revisar código de `actualizar.md`
   - ¿Falta paso de limpieza?
   - ¿Es intencional para debugging?

3. **¿Cuándo debe borrarse?**
   - Opción A: Inmediatamente tras validación exitosa
   - Opción B: Pregunta al usuario si conservar
   - Opción C: Mantener N días y luego borrar

---

## Propuesta / Opciones

### Opción A: Limpieza Automática con Confirmación
```
1. Backup creado → memsys3_backup_YYYYMMDD/
2. Actualización ejecutada
3. Validaciones OK
4. Pregunta: "¿Eliminar backup? (s/n)"
5. Si sí → rm -rf memsys3_backup_YYYYMMDD/
```

**Pros:** Usuario decide, seguro
**Contras:** Requiere interacción adicional

### Opción B: Limpieza Automática Siempre
```
1. Backup creado
2. Actualización ejecutada
3. Validaciones OK
4. Eliminar backup automáticamente
```

**Pros:** Sin intervención manual, limpio
**Contras:** Si hay problema tardío, backup ya borrado

### Opción C: Mantener con TTL
```
1. Backup creado con timestamp
2. Al ejecutar próxima actualización → borrar backups >7 días
```

**Pros:** Permite rollback en ventana razonable
**Contras:** Más complejo, acumula backups temporalmente

---

## Decisiones / Acciones

**Pendiente de análisis.**

Próxima sesión:
1. Ejecutar `actualizar.md` y observar exactamente qué backup crea
2. Revisar código de actualizar.md para encontrar paso de backup
3. Verificar si hay paso de limpieza comentado/omitido
4. Proponer fix según hallazgos

---

## Referencias

- **Prompt:** `memsys3/prompts/actualizar.md`
- **Observación:** Sesión testing /actualizar-memsys3 (2025-12-15)
- **Contexto:** Testing exitoso en proyecto UOC (v0.6.1→v0.8.1)
- **Git:** Posible relación con directorio `.git` residual (ver ISSUE-003)

---

## Notas Adicionales

- Posiblemente relacionado con ISSUE-003 (limpiar .git residual)
- Ambos issues son sobre residuos post-deployment/actualización
- Considerar limpieza unificada en ambos prompts (deploy.md + actualizar.md)
