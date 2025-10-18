# Guía Rápida

Sigue estos pasos para ejecutar un examen en cualquier equipo.

Requisitos
- Python 3.10 o superior
- Conexión opcional para instalar dependencias (una sola vez)

Instalar (Linux/macOS)
- Crear venv y activar:
  - `python3 -m venv .venv && source .venv/bin/activate`
- Instalar dependencias:
  - `pip install -r requirements.txt`

Instalar (Windows PowerShell)
- `py -3 -m venv .venv`
- `.venv\\Scripts\\Activate.ps1`
- `python -m pip install --upgrade pip && pip install -r requirements.txt`

Atajos con Make (opcional)
- `make install` (crea venv e instala)
- `make run` (ejecuta el simulador)
- `make validate` (valida el banco)

Ejecutar un quiz rápido (tema específico)
- `python -m src.main --profile quick --leaves functions/definitions --per-leaf 3 --mode formative`

Examen por módulo (bloque de temas)
- `python -m src.main --profile module --module-file src/data/modules/python_fundamentals.toml`

Examen global
- `python -m src.main --profile global --max-total 60` (acotado)
- `python -m src.main --profile global --exhaustive` (exhaustivo)

Validación de banco y cobertura
- `python scripts/validate_questions.py --strict-coverage`
- Si falta cobertura en algún tema, el simulador lo avisará al iniciar.

Consejos por nivel
- Primaria/secundaria: usa `--profile quick`, ajusta `--per-leaf` y selecciona leaves básicas.
- Universidad: usa `--profile module` o `--profile global` y considera `--exhaustive` con rúbricas.
