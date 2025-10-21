# Módulos Educativos

Los módulos definen conjuntos de temas (leaves) y cuotas para componer exámenes por bloque.

Formatos soportados: TOML o JSON (claves a nivel raíz).

Claves (top‑level)
- `areas`: lista de leaves (ej.: `functions/definitions`)
- `per_leaf_min`: entero o "all" (tomar todas las preguntas disponibles)
- `overrides`: mapa leaf→mínimo (o "all")
- `difficulty_mix`: objetivos de mezcla por dificultad
- `max_total`: recorte del total tras muestrear

Ejemplo TOML
```
areas = [
  "fundamentals/data_structures",
  "fundamentals/operators",
  "functions/definitions",
]

per_leaf_min = 4

[overrides]
"functions/definitions" = 5

[difficulty_mix]
basica = 0.6
intermedia = 0.3
avanzada = 0.1

max_total = 24
```
