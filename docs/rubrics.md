# Rúbricas de Aprobación

Permiten definir criterios de aprobación globales y por tema.

Dónde
- En `src/data/blueprint.json`, clave `rubric`.

Ejemplo
```
{
  "per_leaf_min": 6,
  "difficulty_mix": {"basica": 0.5, "intermedia": 0.35, "avanzada": 0.15},
  "rubric": {
    "global": {"min_score": 0.7},
    "per_leaf_min_pct": 0.5
  }
}
```

Interpretación
- Global: al menos 70% de aciertos totales.
- Por tema: al menos 50% en cada leaf presentado.
- El resumen indica APROBADO/REPROBADO y detalla los criterios incumplidos.

Consejos
- Ajusta los umbrales a la exigencia del curso.
- Puedes empezar solo con el global y luego añadir mínimos por leaf.
