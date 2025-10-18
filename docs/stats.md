# Persistencia y Estadísticas

Este motor guarda cada intento y permite generar reportes agregados.

Persistencia (automática)
- Archivo: `src/data/results/attempts.jsonl` (formato JSON Lines)
- Contenido por intento:
  - timestamp, título, total, score, nivel
  - desglose: `by_area_total/correct`, `by_diff_total/correct`
  - rúbrica (si existe): `rubric.ok`, `rubric.details`
  - meta: perfil, leaves, per_leaf, exhaustive, order, seed, blueprint aplicado

Generar estadísticas
- Comando CLI: `python -m src.main stats --results-dir src/data/results --reports-dir src/data/reports`
- Requisitos: `pandas` (y `matplotlib` para gráficos opcionales)
- Salidas:
  - `overall.csv`: número de intentos, promedio de score y %
  - `by_area.csv`: accuracy promedio por tema (leaf)
  - `by_difficulty.csv`: accuracy promedio por dificultad
  - `by_area_accuracy.png`, `by_difficulty_accuracy.png` (si `matplotlib` está disponible)

Sugerencias
- Usa `--seed` para reproducibilidad cuando compares intentos.
- Versiona la carpeta `src/data/results/` si quieres conservar historial entre equipos (o exporta a CSV en `src/data/reports/`).
