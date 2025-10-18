# Taxonomía de Temas

La taxonomía define las “leaves” o temas atómicos del banco de preguntas.

Archivo
- `src/data/taxonomy.json`

Convenciones
- Rutas jerárquicas en minúsculas separadas por `/`: `grupo/subgrupo/tema`
- Mantén nombres estables; evita renombrar leaves sin migrar preguntas

Ejemplos
- `fundamentals/data_structures`
- `control_flow/loops`
- `functions/definitions`
- `data_science/numpy`

Agregar un tema
1) Añade el leaf a `taxonomy.json`
2) Crea preguntas en `questions.json` con `area` apuntando al nuevo leaf
3) Ajusta cobertura en `blueprint.json` si es necesario
4) Valida: `python scripts/validate_questions.py --strict-coverage`

Sugerencia
- Usa prefijos homogéneos (ej. `fundamentals`, `control_flow`, `functions`, `oop`, `data_science`, `web`, `other`).
