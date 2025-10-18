# Guía para alimentar el examen

Este directorio contiene el banco de preguntas y la taxonomía usada para seleccionar preguntas de forma estratificada por temas (leaves).

Contenido clave:
- `questions.json`: banco unificado de preguntas.
- `taxonomy.json`: Índice Maestro con los temas/"leaves" válidos.
- `blueprint.json`: mínimos por leaf y mezcla de dificultad objetivo.

Esquema de una pregunta (campos y reglas)
- `id`: identificador estable. Formato sugerido: `py.<grupo>.<leaf>.<nnn>` (p.ej., `py.fundamentals.data_structures.001`).
- `text`: enunciado de la pregunta.
- `options`: lista de opciones (2–6).
- `correct`: opción correcta (debe existir en `options`).
- `area`: ruta jerárquica a un leaf de `taxonomy.json` (p.ej., `functions/definitions`). Debe coincidir exactamente con un leaf de `taxonomy.json`.
- `difficulty`: una de `basica` | `intermedia` | `avanzada`.
- `domain`: ámbito (p.ej., `python`, `numpy`, `django`, `cuda`).
- `tags`: etiquetas libres.
- `source` (opcional): referencia, autor o nota.
- `explanation` (opcional, recomendado): breve justificación que se muestra al fallar.
- `cognitive_level` (opcional): nivel de Bloom (`remember|understand|apply|analyze|evaluate|create`).
- `outcomes` (opcional): lista de códigos de resultados de aprendizaje (LOs) asociados.

Buenas prácticas al redactar
- Usa enunciados claros y sin ambigüedades.
- Asegura que `correct` esté exactamente en `options`.
- Incluye distractores plausibles (no triviales, sin trucos rebuscados).
- Mezcla niveles de dificultad por leaf.
- Evita preguntas dependientes de versiones a menos que lo indiques en `tags` o `source`.

Cómo elegir `area`
- Revisa `taxonomy.json` y elige siempre un leaf (no un grupo intermedio).
- Ejemplos válidos: `fundamentals/data_structures`, `control_flow/loops`, `functions/definitions`, `data_science/numpy`.
- Si falta un leaf que necesitas, proponlo y agrégalo a `taxonomy.json` primero.

Criterios de dificultad
- `basica`: recuerdo/concepto directo, 1 paso, sin trampas ni edge-cases.
- `intermedia`: aplicación del concepto, 2–3 pasos, puede involucrar pequeños matices (orden de evaluación, truthiness, etc.).
- `avanzada`: casos límite, semántica fina (mutabilidad, MRO, performance vectorizada), requiere experiencia práctica.

Reglas para opciones (distractores)
- 4 opciones es lo recomendado (1 correcta + 3 plausibles).
- Evita “todas/ninguna de las anteriores”.
- Mantén longitudes similares y sin pistas por formato.
- No repitas opciones ni uses sinónimos que confundan sin aportar.

Guía para `explanation`
- Estructura sugerida: Por qué es correcta + Por qué no las otras + Referencia.
- 1–3 líneas. Incluye snippet corto si aporta claridad.
- Ejemplo de estilo: “list es mutable; tuple/str/int son inmutables. Ver docs: https://docs.python.org/3/tutorial/datastructures.html”.

Flujo de contribución
1) Agrega preguntas en `questions.json` siguiendo el esquema y `taxonomy.json`.
2) Ejecuta el validador: `python3 scripts/validate_questions.py`.
3) Si hay advertencias/errores, corrígelos. Asegura cobertura ≥ mínimos del `blueprint.json`.

Ejemplo mínimo
```
{
  "id": "py.functions.definitions.001",
  "text": "¿Qué palabra clave define una función?",
  "options": ["def", "func", "lambda", "define"],
  "correct": "def",
  "area": "functions/definitions",
  "difficulty": "basica",
  "domain": "python",
  "tags": ["funciones", "def"],
  "explanation": "Las funciones se definen con 'def' según la sintaxis de Python."
}
```

Ejemplos por tema (con explanation)

Fundamentals / Data Structures
```
{
  "id": "py.fundamentals.data_structures.010",
  "text": "¿Cuál de las siguientes es una estructura mutable?",
  "options": ["tuple", "list", "str", "int"],
  "correct": "list",
  "area": "fundamentals/data_structures",
  "difficulty": "basica",
  "domain": "python",
  "tags": ["mutabilidad"],
  "explanation": "list es mutable; tuple, str e int son inmutables. Ver: docs de estructuras de datos de Python."
}
```

Control Flow / Loops
```
{
  "id": "py.control_flow.loops.010",
  "text": "¿Qué hace 'continue' dentro de un bucle?",
  "options": ["Termina el bucle", "Salta a la siguiente iteración", "Reinicia el bucle", "No hace nada"],
  "correct": "Salta a la siguiente iteración",
  "area": "control_flow/loops",
  "difficulty": "basica",
  "domain": "python",
  "tags": ["continue"],
  "explanation": "continue omite el resto del bloque actual y pasa a la próxima iteración del bucle."
}
```

Functions / Definitions
```
{
  "id": "py.functions.definitions.010",
  "text": "¿Qué sucede con parámetros por defecto mutables?",
  "options": ["Se evalúan en cada llamada", "Se comparten entre llamadas", "No son válidos", "Se convierten a inmutables"],
  "correct": "Se comparten entre llamadas",
  "area": "functions/definitions",
  "difficulty": "avanzada",
  "domain": "python",
  "tags": ["default mutable args"],
  "explanation": "Los valores por defecto se crean una vez al definir la función; si son mutables, su estado persiste entre invocaciones."
}
```

Data Science / NumPy
```
{
  "id": "py.data_science.numpy.010",
  "text": "¿Qué es broadcasting en NumPy?",
  "options": ["Paralelismo", "Reglas para operar con formas distintas", "Compilación JIT", "Serialización"],
  "correct": "Reglas para operar con formas distintas",
  "area": "data_science/numpy",
  "difficulty": "intermedia",
  "domain": "numpy",
  "tags": ["broadcasting"],
  "explanation": "Broadcasting expande arrays con dimensiones compatibles sin copiarlos para permitir operaciones vectorizadas."
}
```

OOP / Classes
```
{
  "id": "py.oop.classes.010",
  "text": "¿Cuál es el primer parámetro de un método de instancia?",
  "options": ["self", "cls", "this", "obj"],
  "correct": "self",
  "area": "oop/classes",
  "difficulty": "basica",
  "domain": "python",
  "tags": ["self"],
  "explanation": "Por convención, el primer parámetro de métodos de instancia se llama 'self' y referencia a la instancia."
}
```

Web / Flask
```
{
  "id": "py.web.flask.010",
  "text": "¿Cómo se define una ruta en Flask?",
  "options": ["@app.route", "app.get", "route()", "@route"],
  "correct": "@app.route",
  "area": "web/flask",
  "difficulty": "basica",
  "domain": "flask",
  "tags": ["route"],
  "explanation": "El decorador @app.route asocia una URL a una función de vista en Flask."
}
```

Other / Exceptions
```
{
  "id": "py.other.exceptions.010",
  "text": "¿Qué bloque se ejecuta siempre?",
  "options": ["except", "finally", "else", "retry"],
  "correct": "finally",
  "area": "other/exceptions",
  "difficulty": "intermedia",
  "domain": "python",
  "tags": ["try except"],
  "explanation": "El bloque 'finally' se ejecuta siempre, se lance o no una excepción, útil para liberar recursos."
}
```

Checklist de calidad antes de subir
- id único y estable (sin reciclar numeración).
- area coincide con un leaf de taxonomy.json.
- correct ∈ options; entre 4–5 opciones preferido.
- difficulty ∈ {basica, intermedia, avanzada}.
- Si usas `cognitive_level`, que pertenezca a Bloom (arriba).
- Si usas `outcomes`, que sea lista de strings (p.ej., `PY.FUNC.001`).
- explanation incluida y útil (cuando aplique).
- Ejecutado: `python3 scripts/validate_questions.py` sin errores.

Comandos útiles
- Validar: `python3 scripts/validate_questions.py`
- Ejecutar examen: `python3 -m src.main`

Convenciones de estilo
- Español neutro, preguntas con tilde y puntuación.
- Código mínimo y legible en snippets (si usas). Envuelve en ``` para bloques.
- Evita tecnicismos innecesarios cuando no aportan al objetivo.
