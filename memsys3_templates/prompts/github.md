# GitHub - Subir cambios al repositorio

## Instrucciones

- Sube el repo a GitHub en español, sin emojis ni firmas
- Commits atómicos y descriptivos
- Añade el tag correspondiente si procede
- No subas la versión más allá de la 0.x.x hasta que sea estable
- Solo aumenta el minor si hay cambio relevante, en caso contrario aumenta el patch

## Workflow

1. Revisar cambios: `git status` y `git diff`
2. Añadir archivos: `git add .` o selectivo
3. Commit con mensaje descriptivo
4. Push a origin: `git push origin master`
5. Si procede, crear tag: `git tag v0.x.x && git push --tags`