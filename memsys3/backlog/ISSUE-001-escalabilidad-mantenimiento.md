# ISSUE-001: Escalabilidad del Mantenimiento y Sincronización

**Estado:** Abierto
**Prioridad:** Media
**Tipo:** Tech Debt / Escalabilidad
**Plazo:** Medio plazo (evitar estancamiento futuro)
**Fecha identificación:** 2025-11-03
**Contexto:** Sesión de correcciones FASE 3 traducción catalán→español

---

## 📋 Problema

memsys3 tiene un **problema de escalabilidad en el mantenimiento** causado por:

1. **Falta de verificación automatizada** de consistencia
2. **Sincronización manual propensa a errores** entre múltiples archivos
3. **Sin "single source of truth"** para metadatos compartidos (versión, límites, estructura)

### Síntomas Observados

#### 1. Fallo FASE 3 Traducción

**Contexto:** Otra instancia reportó "Sistema 100% español, 0 resultados catalán"

**Realidad:** Había 200+ líneas con catalán residual

**Causa raíz:**
- Comando grep incompleto (solo buscaba palabras con acentos específicos)
- No había tests automatizados para validar
- Verificación manual exhaustiva requirió 2+ horas adicionales

**Impacto:** Ciclo de trabajo ineficiente (ejecutar → reportar completado → re-verificar → encontrar errores → re-ejecutar)

#### 2. Desincronización de Versión

**Observado en auditoría:**
- `README.md` línea 225: "Versión: 1.0"
- `project-status.yaml`: "fase: Development v1.3"

**Causa:** Versión hardcodeada en múltiples lugares, sin mecanismo de sincronización

**Impacto:** Cambiar versión requiere búsqueda manual en todos los archivos

#### 3. Desincronización de Estructura

**Observado en auditoría:**
- `README.md` mostraba `viz/` dentro de `memory/`
- Realidad: `viz/` está en raíz de `memsys3_templates/`

**Causa:** Árbol de directorios duplicado manualmente en README

**Impacto:** Reestructuraciones requieren actualizar representaciones textuales manualmente

---

## 🎯 Alcance del Problema

### Áreas Afectadas

1. **Metadatos Duplicados**
   - Versión: README.md, project-status.yaml, posiblemente otros
   - Límites técnicos: mencionados en 4 READMEs + ADRs + código
   - Rutas de archivos: hardcodeadas en prompts, READMEs, DEVELOPMENT.md

2. **Referencias Cruzadas**
   - Gotchas documentados en sessions → extraídos por Context Agent
   - Workflows descritos en múltiples READMEs
   - Conceptos clave (rotación, contingencia) explicados en varios lugares

3. **Estructuras Representadas**
   - Árbol de directorios en README.md (texto plano)
   - Estructura real del filesystem
   - Sin generación automática

4. **Validaciones de Calidad**
   - Idioma (catalán vs español)
   - Sintaxis YAML
   - Consistencia de metadatos
   - Sincronización memsys3/ ↔ memsys3_templates/

### Proyección a Futuro

**Si el proyecto crece:**
- Más archivos → más puntos de sincronización manual
- Más contributors → mayor probabilidad de inconsistencias
- Más conceptos compartidos → mayor superficie de error
- **Mantenimiento escala linealmente** con tamaño del proyecto

**Operaciones costosas actualmente:**
- Cambio de versión global
- Reestructuración de archivos
- Traducción o cambios masivos de contenido
- Actualización de conceptos compartidos
- Validación de consistencia completa

---

## 💡 Posibles Aproximaciones (No Soluciones Definitivas)

### Opción 1: Tests Automatizados Mínimos

**Descripción:** GitHub Actions que validen consistencia básica en cada PR/push

**Pros:**
- Detecta errores antes de merge
- No requiere setup local de developers
- Escalable (corre automáticamente)

**Contras:**
- Requiere definir qué validar exactamente
- Añade complejidad al repo (workflows, scripts)
- Solo valida, no corrige automáticamente

**Ejemplos de tests:**
```yaml
# .github/workflows/quality.yml
- name: Verificar idioma español
  run: |
    if grep -r "però\|això\|només" memsys3/ --include="*.yaml" --exclude-dir="docs"; then
      echo "Catalán encontrado"
      exit 1
    fi

- name: Verificar sintaxis YAML
  run: python -m yaml memsys3/**/*.yaml

- name: Verificar versión consistente
  run: |
    VERSION_README=$(grep "Versión:" README.md | cut -d' ' -f2)
    VERSION_STATUS=$(grep "fase:" memsys3/memory/project-status.yaml)
    # Comparar...
```

### Opción 2: Single Source of Truth para Metadatos

**Descripción:** Archivo único `metadata.yaml` con info compartida, referencias automáticas

**Pros:**
- Un solo lugar para actualizar
- Referencias automáticas eliminan duplicación
- Claro qué es "oficial"

**Contras:**
- Requiere mecanismo de "inyección" en archivos
- Complejidad adicional (¿script pre-commit? ¿compilación?)
- memsys3 no tiene runtime, complicado implementar

**Ejemplo conceptual:**
```yaml
# metadata.yaml
version: "1.3"
limits:
  context_yaml_lines: 2000
  rotation_threshold: 1800
  contingency_tokens: 150000

# README.md (generado)
**Versión**: {{ metadata.version }}
```

### Opción 3: Scripts de Verificación Pre-commit

**Descripción:** Git hooks locales que validen antes de commit

**Pros:**
- Detecta errores antes de push
- Flexible (cualquier validación)

**Contras:**
- Requiere setup local de cada developer
- Fácil de bypasear (--no-verify)
- No ayuda con contributors ocasionales

### Opción 4: Documentación de "Puntos Calientes"

**Descripción:** Lista en DEVELOPMENT.md de qué sincronizar manualmente en cada tipo de cambio

**Pros:**
- Simple, sin código adicional
- Claro para contributors
- Bajo overhead

**Contras:**
- Sigue siendo manual
- Depende de que contributors lean y sigan
- No escala bien con complejidad

**Ejemplo:**
```markdown
# docs/DEVELOPMENT.md - Checklist de Sincronización

## Al cambiar versión:
- [ ] README.md línea 225
- [ ] project-status.yaml campo "fase"
- [ ] Verificar menciones en otros docs/

## Al reestructurar archivos:
- [ ] Actualizar árbol en README.md
- [ ] Verificar rutas en prompts/
- [ ] Actualizar DEVELOPMENT.md
```

### Opción 5: Reducir Duplicación Donde Sea Posible

**Descripción:** Eliminar representaciones duplicadas que se pueden generar

**Pros:**
- Menos superficie de error
- Menos que sincronizar manualmente

**Contras:**
- No siempre posible (algunos duplicados son necesarios)
- Requiere decisiones arquitectónicas

**Ejemplos:**
- ¿Árbol de directorios generado por script desde filesystem real?
- ¿Versión leída programáticamente en tests?
- ¿Referencias a límites centralizadas?

---

## 🤔 Consideraciones de Diseño

### Naturaleza de memsys3

memsys3 es un **sistema basado en archivos** sin runtime ni compilación:
- No hay "build step" donde generar archivos
- No hay servidor que inyecte metadatos
- Archivos se copian directamente en deployment
- Diseñado para ser simple y portable

### Balance Simplicidad vs Automatización

**Agregar mucha automatización tiene costos:**
- Complejidad del repo (más archivos, scripts, workflows)
- Curva de aprendizaje para contributors
- Dependencias externas (GitHub Actions, Python, etc.)
- Mantenimiento del tooling mismo

**Pero NO agregar automatización tiene costos:**
- Mantenimiento manual intensivo
- Alto riesgo de errores humanos
- No escala con crecimiento del proyecto
- Freno a la evolución (miedo a cambios grandes)

### Pregunta Clave

**¿Cuánto mantenimiento manual es aceptable para memsys3?**

- Si es un proyecto personal/pequeño: tal vez documentación de puntos calientes es suficiente
- Si se espera que crezca/tenga contributors: tests automatizados básicos son necesarios
- Si se vuelve crítico para proyectos grandes: mayor automatización justificada

---

## 📊 Propuesta Incremental (Sugerencia)

### Fase 1: Quick Wins (Esfuerzo: Bajo)

1. **Documentar puntos calientes** en DEVELOPMENT.md
   - Checklist de qué sincronizar en cada tipo de cambio
   - Lista de metadatos duplicados y sus ubicaciones

2. **Script de verificación básico** (local, opcional)
   ```bash
   # scripts/verify.sh
   # Verifica idioma, sintaxis YAML, etc.
   # Contributors pueden correr manualmente
   ```

3. **Marcar áreas propensas a error** en código
   ```yaml
   # README.md
   **Versión**: 1.3  # SYNC: project-status.yaml
   ```

### Fase 2: Automatización Básica (Esfuerzo: Medio)

4. **GitHub Actions para validación**
   - Idioma (grep catalán)
   - Sintaxis YAML (yamllint)
   - Opcionalmente: versión consistente

5. **Pre-commit hooks recomendados**
   - Documentar en DEVELOPMENT.md
   - Proveer script opcional

### Fase 3: Reducción de Duplicación (Esfuerzo: Alto)

6. **Evaluar qué duplicación se puede eliminar**
   - ¿Árbol de directorios generado?
   - ¿Metadatos centralizados?
   - Requiere decisión arquitectónica (potencial ADR)

7. **Implementar según sea necesario**
   - Solo si el proyecto crece lo suficiente
   - Solo si el dolor de mantenimiento justifica la complejidad

---

## 🎯 Acciones Inmediatas Sugeridas

1. **Documentar como gotcha** en sesión actual
   - Tipo: "arquitectura"
   - Criticidad: "media" (no bloquea trabajo actual, pero frena escalabilidad)
   - Solución: "Por definir - evaluar opciones en ISSUE-001"

2. **Discutir prioridad** con stakeholders
   - ¿Cuánto espera crecer el proyecto?
   - ¿Cuántos contributors se esperan?
   - ¿Cuál es el apetito por complejidad adicional?

3. **Implementar Fase 1** (documentación)
   - Bajo esfuerzo, alto valor
   - No añade complejidad técnica
   - Puede hacerse ahora mismo

4. **Evaluar Fase 2** (tests básicos)
   - Decidir qué tests aportan más valor
   - Implementar solo lo esencial
   - Puede posponerse si proyecto no crece

---

## 📚 Referencias

- **Sesión:** 2025-11-03 (correcciones FASE 3)
- **Commits relacionados:**
  - 6d7b631: Correcciones FASE 3 (detectó el problema)
  - 5cf651c: Correcciones auditoría (desincronización versión/estructura)
- **Documentos:**
  - docs/archivo/REPORTE-FALLO-VERIFICACION-FASE3.md
  - docs/archivo/AUDITORIA-DOCUMENTACION-COMPLETADA.md

---

## 🏷️ Etiquetas

`tech-debt` `escalabilidad` `mantenimiento` `automatización` `testing` `medio-plazo`

---

## 💬 Notas

Este documento es un **problem statement**, no una solución definitiva. El objetivo es:
1. Capturar el problema claramente
2. Explorar opciones posibles
3. Facilitar decisión informada sobre qué hacer

**No hay urgencia inmediata**, pero ignorar este problema hará que el mantenimiento sea cada vez más costoso conforme el proyecto crezca.
