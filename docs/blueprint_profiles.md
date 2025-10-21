# Blueprint y Perfiles (cualquier materia)

Blueprint
- Archivo: `src/data/blueprint.json`
- Define mínimos por leaf (`per_leaf_min`), overrides por leaf y mezcla de dificultad (`difficulty_mix`).
- Puede incluir `rubric` para criterios de aprobación.

Perfiles de ejecución
- `--profile global`: usa toda la taxonomía (opcional `--exhaustive`).
- `--profile topic`: selecciona leaves específicas con `--leaves`.
- `--profile quick`: como `topic` pero con `per-leaf` menor por defecto (3).
- `--profile module`: lee un archivo TOML/JSON con áreas/cuotas personalizadas.
   - Formato del módulo: claves en nivel raíz (`areas`, `per_leaf_min`, `overrides`, `difficulty_mix`, `max_total`).

Ejemplos
- Global acotado: `python -m src.main --profile global --max-total 60`
- Global exhaustivo: `python -m src.main --profile global --exhaustive`
- Topic rápido: `python -m src.main --profile quick --leaves functions/definitions --per-leaf 3`
- Module: `python -m src.main --profile module --module-file src/data/modules/python_fundamentals.toml`

Orden del examen
- `--order random` (por defecto), `--order difficulty`, `--order area`.
