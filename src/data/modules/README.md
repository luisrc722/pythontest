# Módulos Educativos

Los módulos definen conjuntos de temas (leaves) y cuotas para componer exámenes por bloque.

Formatos soportados: TOML o JSON.

Claves
- `areas`: lista de leaves
- `per_leaf_min`: entero o "all" (tomar todas las preguntas disponibles)
- `overrides`: mapa leaf→mínimo (o "all")
- `difficulty_mix`: objetivos de mezcla por dificultad
- `max_total`: recorte del total tras muestrear

Ejemplo TOML: `src/data/modules/python_fundamentals.toml`
