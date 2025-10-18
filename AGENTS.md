# AGENTS.md

Contexto operativo para trabajar en este repositorio. Mantén este documento alineado con el código y los datos.

## Resumen del Proyecto
- Propósito: Simulador/quiz en consola con muestreo estratificado por temas para Python (extendible a CUDA/DLI, web y data science).
- Alcance: CLI interactiva, dataset unificado en JSON, taxonomía jerárquica, mínimos por leaf (blueprint) y mezcla de dificultad.
- Estado: MVP funcional con banco base completo y tooling de validación/cobertura.

## Stack y Requisitos
- Python: 3.10+
- Gestor: pip + venv local (`.venv`)
- Dependencias: ver `requirements.txt` (incluye numpy, pytest, jupyterlab, rich, black, isort, flake8, pydantic, click, toml, inquirer, streamlit, fastapi, uvicorn, pandas, matplotlib)

## Estructura del Repositorio
- `src/` código de la app
  - `src/main.py` CLI principal (Click; `--mode [exam|formative]`, `--seed`)
  - `src/models/` Question, Test, Result (dataclasses, feedback y resumen)
  - `src/utils/` loader, sampler (estratificado), taxonomy, blueprint
  - `src/data/` questions.json (banco), taxonomy.json (índice), blueprint.json (mínimos), README.md (guía)
- `tests/` pruebas (pytest)
- `scripts/` tooling: validador, enriquecedor de explicaciones, workflow.sh
- `Makefile` atajos (install, run, validate, data-check, test, cov, fmt, lint, lab, streamlit, fastapi)
- `README.md` guía de uso/entorno; este `AGENTS.md` guía técnica
 - `docs/` documentación ampliada (quickstart, authoring, taxonomy, blueprint, rubrics, stats, troubleshooting, FAQ)

## Comandos Comunes
- Instalar deps: `make install` (o ver README para venv manual)
- Ejecutar simulador: `make run` (p.ej., `make run ARGS="--mode formative --seed 42"`)
- Generar estadísticas: `python -m src.main stats --results-dir src/data/results --reports-dir src/data/reports`
- Validar datos: `make validate` | modo estricto: `make data-check`
- Pruebas: `make test` | cobertura: `make cov`
- Formato/Lint: `make fmt && make lint`
- Jupyter: `make lab`; Streamlit: `make streamlit`; FastAPI: `make fastapi`
- Workflow completo local: `make workflow` o `bash scripts/workflow.sh`

## Configuración y Entorno
- Sin variables de entorno obligatorias.
- Config de datos: `src/data/taxonomy.json` (leaves) y `src/data/blueprint.json` (mínimos y mezcla de dificultad).
- No versionar `.venv/`. Ejecutar desde raíz, usar `python -m src.main` para imports correctos.

## Convenciones de Código
- Estilo: PEP8 + `black` + `isort` + `flake8`.
- Imports relativos dentro de `src` (usar `from .utils...` / `from ..models...`). Mantener idioma de UI en español.
- Usar dataclasses para modelos simples y typing explícito. Evitar variables de 1 letra.
- Manejo de entrada CLI robusto (argparse) y mensajes consistentes.
- No romper tests existentes; añadir tests cerca del código que cambias si aplica (pytest). No añadir frameworks nuevos sin necesidad.

## Testing
- Framework: pytest. Ejecutar `make test` antes de cambios significativos.
- Añadir pruebas unitarias para muestreo, validación y utilidades según evolucione.

## Datos y Persistencia
- Banco unificado: `src/data/questions.json`. Reglas en `src/data/README.md`.
- Cada pregunta debe incluir: `id`, `text`, `options`, `correct`, `area` (leaf exacto), `difficulty` ∈ {basica, intermedia, avanzada}. `explanation` recomendado.
- IDs estables (`py.<grupo>.<leaf>.<nnn>`). Sin duplicados. Español neutro.
- Validación obligatoria: `make data-check` (falla si algún leaf < mínimo del blueprint).
- Taxonomía: `src/data/taxonomy.json` define leaves válidos; modificarla antes de agregar nuevas áreas.
- Blueprint: `src/data/blueprint.json` define `per_leaf_min` global y `overrides` por leaf, y `difficulty_mix` objetivo.

## Flujo de Trabajo
- Proponer cambios de estructura en un issue antes de aplicarlos.
- Para nuevas features: actualizar README y este AGENTS.md si impacta el flujo o los datos.
- Mantener consistencia entre código, datos y documentación.

## Tareas Pendientes (Backlog breve)
- [ ] Modo “formativo” vs “examen” integrado (ya disponible en CLI; añadir más opciones si se requiere)
- [ ] UI opcional en Streamlit / API FastAPI (a evaluar)
- [ ] Más pruebas unitarias para utils/loader y result breakdown

## Notas para Agentes
- Respeta esta guía para todo el repo. Cambios amplios: discútelos primero.
- Prioriza soluciones simples y documenta decisiones en README/AGENTS.
- Si agregas nuevas áreas, mantén actualizados taxonomy.json, blueprint.json y valida con `make data-check`.
