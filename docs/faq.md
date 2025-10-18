# Preguntas Frecuentes (FAQ)

¿Sirve para primaria/secundaria?
- Sí. Usa `--profile quick` y selecciona leaves básicas. Redacta preguntas cortas y explicaciones amigables.

¿Puedo hacer exámenes exhaustivos?
- Sí. Añade `--exhaustive` para tomar todas las preguntas de las áreas seleccionadas.

¿Cómo valido que tengo suficiente banco por tema?
- `python scripts/validate_questions.py --strict-coverage` y revisa el reporte.

¿Cómo controlo la dificultad?
- Ajusta `difficulty` en preguntas y `difficulty_mix` en el blueprint.

¿Puedo definir criterios de aprobación?
- Sí, en `blueprint.json` bajo `rubric` (umbral global y por tema). El resumen muestra APROBADO/REPROBADO.

¿Necesito internet para ejecutar?
- No, solo para instalar dependencias la primera vez.

¿Windows es compatible?
- Sí. Usa PowerShell y `py -3 -m venv .venv` para crear el entorno.

¿Puedo integrar una UI web?
- Opcional. Hay soporte para Streamlit/FastAPI en requirements; puedes construir una capa arriba sin tocar el motor.
