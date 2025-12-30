# ISSUE-006: Backups de memsys3 deben estar SIEMPRE en .gitignore

**Estado:** Abierto
**Prioridad:** Alta
**Tipo:** Bug / Risk de Seguridad
**Plazo:** Inmediato
**Fecha identificación:** 2025-12-30

---

## Problema / Necesidad

Durante actualización de memsys3 se crea un backup (ej: `memsys3_backup_20251222_202326/`). El comportamiento actual respecto a .gitignore es inconsistente y peligroso:

**Escenario A: memsys3/ en .gitignore (Opción A recomendada en deploy.md PASO 8)**
- ✅ memsys3/ ignorado
- ✅ Backup también ignorado (por regla general de Git: si padre ignorado, hijos también)
- Resultado: OK

**Escenario B: memsys3/ NO en .gitignore (Opción B en deploy.md PASO 8)**
- ❌ memsys3/ versionado
- ❌ Backup NO ignorado → se versiona en git
- Resultado: **PROBLEMA CRÍTICO**

**Consecuencias del Escenario B:**
1. Backups (potencialmente múltiples) se suben a git
2. Backups contienen datos sensibles (sessions, decisiones, gotchas)
3. Inflado innecesario del repositorio (duplicación de datos)
4. Confusión: ¿cuál es la carpeta correcta? ¿memsys3/ o memsys3_backup_*/?
5. Si proyecto es público, backups privados quedan expuestos

**Caso real confirmado:**
- **Proyecto:** Taller Colomer
- **Situación:** memsys3/ en .gitignore → backup también ignorado (OK por ahora)
- **Riesgo:** Otros proyectos con memsys3/ versionado subirán backups sin darse cuenta

---

## Análisis

**Problema raíz:**
Los backups de memsys3 NO están explícitamente excluidos en .gitignore. Su inclusión/exclusión depende indirectamente de si memsys3/ está ignorado.

**Filosofía correcta:**
**Backups son SIEMPRE temporales** → NUNCA deben versionarse → Deben estar SIEMPRE en .gitignore, independientemente de si memsys3/ está versionado o no.

**Comparación con otros sistemas:**
- node_modules/ → .gitignore
- .env → .gitignore
- *.log → .gitignore
- **memsys3_backup_*/ → DEBE estar en .gitignore**

---

## Propuesta / Opciones

### Opción A: Agregar regla automática a .gitignore (RECOMENDADA)

Durante deploy.md y actualizar.md, SIEMPRE agregar:

```bash
# Agregar a .gitignore (si no existe ya)
grep -q "memsys3_backup_" .gitignore 2>/dev/null || echo "memsys3_backup_*/" >> .gitignore
```

**Pros:**
- Protección automática
- No requiere intervención del usuario
- Consistente con filosofía de seguridad
- Previene subida accidental de datos sensibles

**Contras:**
- Modifica .gitignore del usuario sin preguntar (mitigable: informar claramente)

### Opción B: Preguntar al usuario si agregar regla

```
⚠️ Los backups de memsys3 (memsys3_backup_*/) no están en .gitignore.
¿Agregar regla automáticamente? (Recomendado)

A) Sí, agregar a .gitignore (RECOMENDADO)
B) No, gestionar manualmente
```

**Pros:**
- Usuario decide
- Transparente

**Contras:**
- Usuario puede elegir mal (no agregar → riesgo)
- Requiere interacción adicional

### Opción C: Crear backups en directorio temporal externo

Crear backups en `/tmp/` o `~/.memsys3_backups/` en lugar de junto a memsys3/:

```bash
mkdir -p ~/.memsys3_backups/
cp -r memsys3 ~/.memsys3_backups/memsys3_backup_$(date +%Y%m%d_%H%M%S)
```

**Pros:**
- No contamina repositorio
- Separación clara backup vs proyecto

**Contras:**
- Usuario puede olvidar dónde están backups
- Limpieza menos obvia (no visibles en proyecto)
- Complejidad adicional de gestión

---

## Decisiones / Acciones

**Decisión:** Implementar **Opción A** (agregar regla automática)

**Justificación:**
- Backups NUNCA deben versionarse (filosofía universal)
- Protección automática es mejor que depender del usuario
- Consistente con PASO 8 deploy.md (consulta .gitignore para privacidad)

**Implementación:**

1. **deploy.md PASO 8:** Después de consultar si excluir memsys3/, SIEMPRE agregar:
   ```bash
   # Proteger backups (SIEMPRE ignorados, independiente de memsys3/)
   grep -q "memsys3_backup_" .gitignore 2>/dev/null || echo "memsys3_backup_*/" >> .gitignore
   echo "✅ Backups de memsys3 protegidos en .gitignore"
   ```

2. **actualizar.md PASO 5:** Antes de crear backup, agregar misma protección:
   ```bash
   # Proteger backups antes de crear
   grep -q "memsys3_backup_" .gitignore 2>/dev/null || echo "memsys3_backup_*/" >> .gitignore

   # Crear backup
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   cp -r memsys3 memsys3_backup_$TIMESTAMP
   ```

3. **Verificación post-fix:**
   - Testear en proyecto con memsys3/ versionado → verificar backup ignorado
   - Testear en proyecto con memsys3/ ignorado → verificar backup ignorado
   - Ambos casos: `git status` no debe mostrar memsys3_backup_*/

---

## Referencias

- **Prompt afectado:** `memsys3/prompts/actualizar.md` (PASO 5), `memsys3/prompts/deploy.md` (PASO 8)
- **Caso real:** Taller Colomer (memsys3/ ignorado → backup ignorado, OK)
- **Riesgo:** Proyectos con memsys3/ versionado (Opción B) subirán backups sin darse cuenta
- **Conversación:** Sesión 2025-12-30, detección durante discusión pre-endSession

---

## Notas Adicionales

**Prevención de aliases problemáticos:**
El usuario menciona: "no hay riesgos de hacer aliases en prompts de backup"
- Confirmado: @ mentions NO funcionan con archivos ignorados (limitación Claude Code)
- Si memsys3_backup_*/ está ignorado, no se puede hacer @memsys3_backup_*/
- Esto es BUENO: evita referencias accidentales a backups temporales

**Filosofía memsys3:**
- Datos sensibles (sessions, decisiones, gotchas) deben protegerse
- Backups son TEMPORALES, no contenido del proyecto
- .gitignore es primera línea de defensa contra subidas accidentales

**Relacionado:**
- deploy.md PASO 8: consulta .gitignore para excluir memsys3/ (privacidad)
- Esta issue complementa: backups SIEMPRE privados, independiente de memsys3/

**Testing requerido:**
- [ ] Desplegar memsys3 con Opción A (excluir) → verificar backup ignorado
- [ ] Desplegar memsys3 con Opción B (incluir) → verificar backup ignorado
- [ ] Actualizar memsys3 existente → verificar backup ignorado
- [ ] Verificar que .gitignore contiene "memsys3_backup_*/" después de deploy/actualizar
