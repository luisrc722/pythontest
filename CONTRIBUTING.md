# Contribuir a este proyecto

¡Gracias por tu interés en colaborar! Este proyecto busca ser una herramienta abierta y útil para evaluaciones educativas desde nivel básico hasta avanzado.

## Cómo empezar
- Clona el repo y crea un entorno:
  - `make install` (o ver README para pasos manuales con venv)
- Verifica que todo corre localmente:
  - `make validate` y `make test`
  - `python -m src.main` para ejecutar el simulador

## Flujo de trabajo de desarrollo
- Formato y estilo: `make fmt && make lint`
- Pruebas y cobertura: `make test` y `make cov`
- Validación de datos: `make data-check` (falla si falta cobertura en algún tema)
- Documentación: consulta `docs/` (quickstart, authoring, taxonomy, blueprint, rubrics, stats)

## Agregar preguntas (banco de datos)
- Opción modular por leaf (recomendada para contribuciones):
  1. Divide (una vez): `python scripts/split_questions.py`
  2. Edita `src/data/questions/<leaf>.json`
  3. Empaqueta: `python scripts/bundle_questions.py` o `make bundle`
  4. Valida: `python scripts/validate_questions.py --strict-coverage`
- Asistente interactivo: `python -m src.main add` (requiere `inquirer`)
- Sigue las pautas de `docs/authoring.md` (esquema, dificultad, explicación, metadatos)

## Pull Requests
- Crea una rama desde `main`: `feat/...`, `fix/...`, `docs/...`
- Asegura pasar `make fmt lint test data-check`
- Describe claramente el cambio (motivo, alcance, impacto)
- Para cambios en datos, incluye una nota de cobertura (qué leaves tocaste)

## Código de conducta y seguridad
- Cumple el [Código de Conducta](CODE_OF_CONDUCT.md)
- Reporta vulnerabilidades siguiendo la [política de seguridad](SECURITY.md)

¡Gracias por contribuir! 🙌
