# Simulador CUDA Python – NVIDIA DLI

Pequeño simulador/quiz en consola para practicar fundamentos de Python (y extensible a CUDA/NVIDIA DLI) a partir de bancos de preguntas en JSON.

Atajos de documentación
- Guía rápida: docs/quickstart.md
- Autoría (unificado/modular): docs/authoring.md
- Taxonomía: docs/taxonomy.md
- Blueprint y perfiles: docs/blueprint_profiles.md
- Rúbricas: docs/rubrics.md
- Estadísticas: docs/stats.md
- Solución de problemas: docs/troubleshooting.md
- FAQ: docs/faq.md

## Características
- Carga preguntas desde `src/data/*.json`.
- Selección aleatoria de N preguntas por ejecución.
- Interfaz de línea de comandos simple con feedback inmediato.
- Resumen de resultados y cálculo de nivel.

## Requisitos
- Python 3.10+
- Dependencias listadas en `requirements.txt`

Instalación rápida:
- Crear y activar entorno virtual (opcional): `python -m venv .venv && source .venv/bin/activate`
- Instalar dependencias: `pip install -r requirements.txt`

## Estructura
- `src/main.py`: punto de entrada de la app y política por áreas.
- `src/utils/loader.py`: carga unificada desde `src/data/questions.json` (con fallback legacy).
- `src/utils/sampler.py`: muestreo estratificado por área y dificultad.
- `src/utils/taxonomy.py`: carga y utilidades para la taxonomía jerárquica.
- `src/utils/blueprint.py`: carga la política de mínimos por leaf y mezcla de dificultad.
- `src/models/`: clases `Question`, `Test`, `Result`.
- `src/data/questions.json`: banco unificado (recomendado). Legacy: `python_basics.json`, `numpy_basics.json`, `cuda_intro.json`.
- `src/data/taxonomy.json`: Índice Maestro de temas/rutas para escalar el banco.
- `src/data/blueprint.json`: configuración de mínimos por leaf y mezcla de dificultad.
- `tests/`: pruebas.

## Entorno y Portabilidad (venv)
Para mover el proyecto y que funcione en cualquier ruta/PC, usa un entorno virtual local por carpeta. No copies/traslades el `.venv` entre máquinas: recrea el entorno e instala dependencias.

Pasos rápidos (Linux/macOS):
- Crear y activar entorno: `python3 -m venv .venv && source .venv/bin/activate`
- Actualizar pip: `python -m pip install --upgrade pip`
- Instalar dependencias (recomendado): `pip install -r requirements.txt`
- Alternativa mínima (según paquetes solicitados):
  `pip install numpy pytest pytest-cov ipywidgets jupyterlab rich black isort flake8 pydantic click toml inquirer streamlit fastapi uvicorn pandas matplotlib`

Windows (PowerShell):
- Crear: `py -3 -m venv .venv`
- Activar: `.venv\Scripts\Activate.ps1`
- Instalar: `python -m pip install --upgrade pip && pip install -r requirements.txt`

Verificación rápida del entorno:
- Ejecutar validación del banco: `python scripts/validate_questions.py`
- Correr pruebas: `pytest -q`
- Iniciar el simulador: `python -m src.main`

Notas de portabilidad:
- Ejecuta siempre los comandos desde la raíz del repo y usa `python -m src.main` para respetar imports relativos.
- No hagas commit del entorno `.venv/`. Si mueves el proyecto, recrea el entorno y reinstala.
- Las rutas de datos son relativas (`src/data/...`), por lo que no dependen del path absoluto del repo.

## Uso
Ejecutar el simulador con muestreo estratificado por áreas:

```
python -m src.main
```

Por defecto intenta `src/data/questions.json` y toma 5 por área para las áreas definidas en `AREAS_DEFAULT` dentro de `src/main.py`. Si faltan preguntas en un área, toma todas las disponibles.
El simulador avisará si detecta leaves con cobertura insuficiente y sugerirá ejecutar `make data-check` para un reporte.

Modos de ejecución:
- Modo examen (por defecto): muestra explicación solo cuando fallas.
  `python -m src.main --mode exam`
- Modo formativo: muestra explicación también cuando aciertas.
  `python -m src.main --mode formative`

Reproducibilidad: fija la semilla de aleatoriedad con `--seed`.
`python -m src.main --mode formative --seed 42`

Perfiles educativos (dividir por uso)
- Global (acreditación): muestrea todas las leaves de `taxonomy.json` conforme a `blueprint.json`.
  - `python -m src.main --profile global`
  - Limitar total: `--max-total 60`
  - Exhaustivo (todas las preguntas): `--exhaustive`
- Topic / Quick (fin de tema): centra el quiz en leaves específicas.
  - `python -m src.main --profile topic --leaves functions/definitions,control_flow/loops --per-leaf 5`
  - Versión rápida: `--profile quick` usa por defecto 3 por leaf (ajustable con `--per-leaf`).
  - Exhaustivo por tema: añade `--exhaustive` para tomar todas las preguntas de esas leaves.
- Module (módulos de curso): usa un archivo TOML/JSON con áreas y cuotas.
  - `python -m src.main --profile module --module-file src/data/modules/python_fundamentals.toml`
  - En el módulo puedes usar `per_leaf_min = "all"` u overrides con "all" para evaluar todo.

Orden del examen
- `--order random` (por defecto): mezcla global.
- `--order difficulty`: ordena por dificultad creciente (útil para evaluaciones ascendentes).
- `--order area`: agrupa por leaf para bloques temáticos.

## Formato de preguntas (unificado)
Cada objeto incluye metadatos para escalar por dominios y dificultad:

```
{
  "id": "py.fund.001",
  "text": "Pregunta...",
  "options": ["A", "B", "C", "D"],
  "correct": "Texto exacto de la opción correcta",
  "area": "fundamentals/data_structures",
  "difficulty": "basica",
  "domain": "python",
  "tags": ["tipos", "int", "float"],
  "source": "opcional",
  "explanation": "opcional: breve justificación que se muestra al fallar"
  ,"cognitive_level": "remember|understand|apply|analyze|evaluate|create (opcional)"
  ,"outcomes": ["PY.FUND.001"]
}
```

## Desarrollo
- Añade/edita preguntas en `src/data/questions.json` usando rutas jerárquicas en `area` (ej. `fundamentals/data_structures`).
- Ajusta `src/data/taxonomy.json` para controlar qué temas/leaves existen y su navegación.
- Ajusta `AREAS_DEFAULT` y `per_area_min` en `src/main.py` o usa la taxonomía para generar automáticamente la lista de áreas.
- Ajusta mínimos y mezcla de dificultad en `src/data/blueprint.json` (por ejemplo, subir a 6–8 por leaf y personalizar overrides por tema).
- `tests/` incluye pruebas del muestreo estratificado.

### Validación del banco y cobertura
- Ejecuta el validador: `python3 scripts/validate_questions.py`
- Reporta cobertura por leaf vs mínimos definidos en `blueprint.json` y verifica esquema/datos (IDs duplicados, opciones, dificultades, etc.).

### Rúbricas (opcional)
- Define criterios de aprobación en `src/data/blueprint.json` bajo la clave `rubric`, por ejemplo:
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
- El resumen mostrará “APROBADO/REPROBADO” y los criterios no cumplidos.

## Herramientas incluidas (opcionales)
- Formato y estilo: `black .`, `isort .`, `flake8`.
- Jupyter: `jupyter lab` para crear notebooks de estudio con ipywidgets.
- Streamlit (si creas una UI web ligera): `streamlit run app.py`.
- FastAPI (si expones API): `uvicorn app:app --reload`.

Estas herramientas están en `requirements.txt` para que el entorno sea homogéneo en cualquier máquina.

## Makefile (atajos)
Atajos cross‑platform para tareas comunes. Ejemplos:
- Crear venv e instalar: `make install`
- Ejecutar simulador: `make run`
- Validar banco: `make validate`
- Validar y fallar si falta cobertura (CI): `make data-check`
- Workflow local (instala deps, valida estricto y ejecuta tests con cobertura): `make workflow`
- Probar y cobertura: `make test` / `make cov`
- Formatear y lint: `make fmt && make lint`
- JupyterLab: `make lab`
- Streamlit: `make streamlit` (o `make streamlit APP=mi_app.py`)
- FastAPI: `make fastapi` (o `make fastapi MODULE=app APP_OBJECT=app PORT=8000`)

Para ver todos los comandos: `make help`.

Sin Make instalado:
- Ejecuta el flujo equivalente con bash: `bash scripts/workflow.sh`

## Documentación ampliada
- Guía rápida: `docs/quickstart.md`
- Autoría de preguntas: `docs/authoring.md`
- Taxonomía (temas): `docs/taxonomy.md`
- Blueprint y Perfiles: `docs/blueprint_profiles.md`
- Rúbricas de aprobación: `docs/rubrics.md`
- Accesibilidad e i18n: `docs/accessibility_i18n.md`
- Solución de problemas: `docs/troubleshooting.md`
- Preguntas frecuentes: `docs/faq.md`
- Estadísticas y persistencia: `docs/stats.md`

## Edición modular del banco
- Unificado: edita `src/data/questions.json` y valida.
- Modular por leaf: trabaja en `src/data/questions/<leaf>.json` (mismo esquema) y empaqueta:
  - Dividir banco actual: `python scripts/split_questions.py`
  - Empaquetar todo: `python scripts/bundle_questions.py` o `make bundle`
  - Validar: `python scripts/validate_questions.py --strict-coverage`
- Asistente interactivo: `python -m src.main add` (requiere `inquirer`)

## Contribución, Conducta, Seguridad y Licencia
- Contribuir: lee `CONTRIBUTING.md`
- Código de conducta: `CODE_OF_CONDUCT.md`
- Seguridad (reporte de vulnerabilidades): `SECURITY.md`
- Licencia: MIT (ver `LICENSE`)

## Persistencia y Estadísticas
- Cada intento se guarda en `src/data/results/attempts.jsonl` con metadatos (perfil, seed, mezcla, desglose por área/dificultad y veredicto de rúbrica si existe).
- Genera reportes con: `python -m src.main stats --results-dir src/data/results --reports-dir src/data/reports`
  - Exporta `overall.csv`, `by_area.csv`, `by_difficulty.csv` y gráficos PNG (si `matplotlib` está disponible).
  - Desactiva gráficos con `--no-plots`.

## Roadmap y uso de herramientas
Esta es la hoja de ruta para aprovechar el entorno venv y las herramientas instaladas.

- Fase 1 — UX de consola + validación fuerte (COMPLETADA)
  - Pydantic: valida el esquema de preguntas al cargarlas (opciones, correcta, dificultad, normalización).
  - Click: CLI con opciones `--mode` y `--seed` manteniendo compatibilidad con `python -m src.main`.
  - Rich: salida coloreada de preguntas/feedback y resumen en tablas.

- Fase 2 — Persistencia + analítica
  - Guardar intentos en `data/results/*.jsonl` con breakdown y seed.
  - Pandas/Numpy: métricas agregadas; Matplotlib: gráficos simples.
  - Comando `stats` para exportes (CSV/PNG) y reporte en consola (Rich).

- Fase 3 — Curaduría y UI
  - JupyterLab + ipywidgets: notebook para editar/validar preguntas por leaf.
  - Streamlit: UI web ligera del examen (selección de áreas, modo formativo).

- Fase 4 — API
  - FastAPI + Uvicorn: endpoints para muestrear exámenes y registrar resultados.

Configuración y estilo
- pyproject.toml (opcional): centralizar config de black/isort/flake8/pytest si se desea.

## Notas y próximos pasos
- Hay un archivo `AGENTS.md` con convenciones y contexto para colaborar.
- Mejoras recientes:
  - Se corrigió el modelo `Question` y se unificó el cargador de datos.
  - Se agregó muestreo estratificado por área/dificultad.
  - Se agregó soporte para taxonomía jerárquica (`src/data/taxonomy.json`).
  - Pendiente: completar el banco unificado `src/data/questions.json` con suficientes preguntas por leaf y ampliar tests.

## Índice Maestro sugerido (taxonomía)
La taxonomía base se define en `src/data/taxonomy.json` y propone rutas como:

- Fundamentals: `fundamentals/data_structures`, `fundamentals/operators`, `fundamentals/variables`
- Control Flow: `control_flow/conditionals`, `control_flow/loops`, `control_flow/comprehensions`
- Functions: `functions/definitions`, `functions/decorators`, `functions/generators`, `functions/async`
- OOP: `oop/classes`, `oop/inheritance`, `oop/magic_methods`
- Data Science: `data_science/numpy`, `data_science/pandas`, `data_science/visualization`
- Web: `web/flask`, `web/django`, `web/fastapi`
- Courses: `courses/cuda_python_course`
- Other: `modules_packages`, `exceptions`, `file_io`, `testing`, `async_programming`, `best_practices`

Puedes ampliar esta lista y establecer mínimos deseados por leaf ajustando `per_area_min` en `src/main.py`. Cuando el banco crezca, considera subirlo a 6–8.
