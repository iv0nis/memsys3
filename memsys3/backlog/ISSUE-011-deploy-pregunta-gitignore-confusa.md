# ISSUE-011: Pregunta .gitignore en deploy es confusa para el usuario

**Estado**: Abierto
**Prioridad**: Media
**Tipo**: Bug / UX
**Plazo**: Corto plazo
**Fecha creación**: 2026-02-17

---

## Problema

En `deploy.md` PASO 8, la pregunta sobre si excluir `memsys3/` del `.gitignore` está planteada de forma confusa. El usuario debe entender implicaciones técnicas (@ mentions, privacidad) antes de poder decidir.

La pregunta actual presenta demasiado contexto técnico antes de la decisión, cuando la decisión en sí es simple: **¿quieres que memsys3 sea privado o compartido?**

---

## Propuesta de Solución

Simplificar el briefing de PASO 8 a una pregunta directa:

```
¿Quieres excluir memsys3/ del repositorio git?
- Sí (privado): el contexto del proyecto no se sube a GitHub
- No (compartido): el contexto se versiona y otros colaboradores lo ven
```

Sin mencionar @ mentions ni detalles técnicos en la pregunta inicial. Si el usuario elige "Sí", entonces avisar brevemente del workaround para @ mentions.

---

## Referencias

- Prompt afectado: `memsys3_templates/prompts/deploy.md` (PASO 8)
- ADR relacionada: ADR-010 (decisión sobre .gitignore en deployment)
- Sesión donde se detectó: 2026-02-06 (deployment BusinessHub)
