# Autoría de Preguntas (agnóstico al tema)

Objetivo: redactar preguntas de calidad para cualquier materia, validadas automáticamente y fáciles de mantener.

Esquema mínimo
```
{
  "id": "py.functions.definitions.001",
  "text": "¿Qué palabra clave define una función?",
  "options": ["def", "func", "lambda", "define"],
  "correct": "def",
  "area": "functions/definitions",
  "difficulty": "basica",
  "explanation": "Las funciones se definen con 'def'."
}
```

Campos recomendados
- `id`: estable y legible (sujeto.tema.subtema.nnn)
- `text`: enunciado claro (evita ambigüedades)
- `options` (2–6): distractores plausibles
- `correct` ∈ `options`
- `area`: hoja válida en `src/data/taxonomy.json`
- `difficulty`: `basica|intermedia|avanzada`
- `explanation`: breve “por qué” (se muestra al fallar y en modo formativo)
- Opcionales: `domain` (p. ej., `python`, `anatomy`, `law`), `tags`, `cognitive_level` (Bloom), `outcomes` (LOs)

Buenas prácticas
- 4 opciones es un punto óptimo
- Evita “todas/ninguna de las anteriores”
- Mantén longitud similar en opciones
- Apoya con ejemplos simples si aportan claridad

Flujo de trabajo
Opción A (rápida, un archivo unificado)
1) Edita `src/data/questions.json`
2) Valida: `python scripts/validate_questions.py --strict-coverage`
3) Quick test: `python -m src.main --profile quick --leaves <leaf> --per-leaf 3`

Opción B (modular por leaf)
1) Divide el banco actual: `python scripts/split_questions.py`
2) Edita el archivo por leaf en `src/data/questions/<leaf>.json`
3) Empaqueta: `python scripts/bundle_questions.py` (o `make bundle`)
4) Valida: `python scripts/validate_questions.py --strict-coverage`
5) Quick test: `python -m src.main --profile quick --leaves <leaf> --per-leaf 3`

Asistente interactivo (Inquirer)
- Agrega una pregunta con guía: `python -m src.main add`
- Elige leaf, redacta, selecciona correcta; el sistema guarda en el archivo de leaf y empaqueta.

Formato modular por leaf (recomendado)
- Estructura de carpetas:
```
src/
  data/
    questions/
      functions/definitions.json
      control_flow/loops.json
      anatomy/cardiovascular.json
```
- Cada archivo `<leaf>.json` es un arreglo de objetos pregunta. Ejemplo mínimo:
```
[
  {
    "id": "py.functions.definitions.017",
    "text": "¿Qué palabra clave define una función?",
    "options": ["def", "func", "lambda", "define"],
    "correct": "def"
    // "area": "functions/definitions"  ← opcional, se infiere
  }
]
```
- Bundler e inferencia:
  - Si `area` no está presente, se infiere desde la ruta del archivo.
  - Los archivos se combinan ordenados por `area` e `id`.
- Reglas prácticas:
  - Codifica en UTF‑8; sin comas colgantes.
  - IDs únicos y estables por leaf (formato sugerido: `xx.<leaf_con_puntos>.<nnn>`).
  - Ejecuta `make bundle && make validate` después de editar.

Criterios de dificultad
- `basica`: recuerdo del concepto, 1 paso
- `intermedia`: aplicación con 2–3 pasos
- `avanzada`: matices/edge-cases, semántica fina

Cognitive level (Bloom) opcional
- `remember`, `understand`, `apply`, `analyze`, `evaluate`, `create`

Outcomes (LOs) opcional
- Lista de códigos de resultado (p. ej. `PY.FUNC.001`) para mapas curriculares
