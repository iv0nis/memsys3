# ISSUE-003: Limpiar directorio .git/ residual en memsys3/ después de deployment

**Estado:** Abierto
**Prioridad:** Baja-Media
**Tipo:** Tech debt / Limpieza
**Plazo:** Antes de próxima release (v0.9.0)
**Fecha creación:** 2025-12-11

---

## Problema

Durante el deployment (`@memsys3/prompts/deploy.md`), el workflow actual:

1. Clona memsys3 temporalmente: `git clone https://github.com/iv0nis/memsys3 memsys3_temp`
2. Copia contenido a `memsys3/`: `cp -r memsys3_temp/memsys3_templates/* memsys3/`
3. Limpia temporal: `rm -rf memsys3_temp`

**Problema:** Si durante la copia se incluye `.git/` residual en `memsys3/`, esto causa:

- ⚠️ Espacio innecesario (~1-5MB)
- ⚠️ Confusión: Dos repositorios git (proyecto + memsys3 interno)
- ⚠️ Posible conflicto si usuario hace `git add .` desde raíz
- ⚠️ No es necesario para funcionamiento de memsys3

## Evidencia

**¿El problema existe actualmente?**
- Necesita verificación: comprobar si `memsys3/.git/` existe después de deployment
- Si existe: es tech debt que debe limpiarse
- Si no existe: agregar verificación explícita en deploy.md para prevenir

## Propuesta de Solución

### Opción A: Limpieza explícita en deploy.md (Recomendada)

Agregar paso de limpieza después de copiar:

```bash
# PASO 7b: Limpiar .git residual (si existe)
if [ -d "memsys3/.git" ]; then
    echo "⚠️ Detectado .git/ residual en memsys3/, limpiando..."
    rm -rf memsys3/.git
    echo "✅ .git/ eliminado"
fi
```

**Pros:**
- Explícito y seguro
- Previene el problema
- No afecta deployment normal

**Contras:**
- Un paso adicional en deploy.md

### Opción B: Copiar solo archivos (sin .git)

Usar `rsync` o flag para excluir `.git/`:

```bash
# En lugar de: cp -r memsys3_temp/memsys3_templates/* memsys3/
rsync -av --exclude='.git' memsys3_temp/memsys3_templates/ memsys3/
```

**Pros:**
- Previene desde el origen
- Más limpio

**Contras:**
- Requiere `rsync` (puede no estar en todos los sistemas)
- Más complejo

### Opción C: Verificar y advertir (sin forzar limpieza)

Solo detectar y avisar al usuario:

```bash
if [ -d "memsys3/.git" ]; then
    echo "⚠️ WARNING: memsys3/.git/ existe. Considera eliminarlo manualmente."
fi
```

**Pros:**
- No invasivo
- Usuario decide

**Contras:**
- No resuelve automáticamente
- Puede ignorarse

## Decisión Recomendada

**Opción A** (limpieza explícita) es la mejor:
- Balance entre seguridad y automatización
- Previene el problema sin complicar deployment
- Compatible con todos los sistemas (solo usa `rm -rf`)

## Implementación

1. Modificar `memsys3_templates/prompts/deploy.md`
2. Agregar PASO 7b después de copiar archivos
3. Copiar cambio a `memsys3/prompts/deploy.md` (dog-fooding)
4. Testing: deployment en proyecto nuevo, verificar que `.git/` no existe en `memsys3/`
5. Documentar en ADR si se considera decisión arquitectónica

## Referencias

- `memsys3_templates/prompts/deploy.md` (PASO 7: Copiar estructura)
- Sesión 2025-12-11 (release v0.8.0, mejoras deployment)
- Comando global `/deploy-memsys3` (sesión 2025-12-09)

## Notas Adicionales

- Prioridad baja-media: No rompe el sistema, pero es buena práctica
- Fácil de implementar (~5 líneas código)
- Puede implementarse en próxima sesión que toque deploy.md
- Si se confirma que el problema NO existe, cerrar issue documentando que deployment ya es correcto
