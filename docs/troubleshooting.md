# Solución de Problemas

No se encuentra `python`/`python3`
- Verifica instalación de Python 3.10+. En Windows, usa `py -3`.

Faltan dependencias (pydantic, click, rich, ...)
- Activa venv y ejecuta: `pip install -r requirements.txt` (o `make install`).

`ModuleNotFoundError: models/utils`
- Ejecuta siempre desde la raíz y con `python -m src.main` (no `python src/main.py`).

EOF/Aborted! durante ejecución
- Ocurre si no hay más entradas al usar here-docs. En uso interactivo no pasa. Responde en vivo o aumenta líneas en el here-doc.

Validación falla (coverage insuficiente)
- Ejecuta `python scripts/validate_questions.py --strict-coverage` y completa preguntas en leaves con déficit.

Errores del bundler/split
- `[warn] No se pudo leer <archivo>.json`: JSON inválido (verifica comas, comillas y codificación UTF‑8).
- Área faltante: el bundler infiere `area` desde la ruta del archivo por leaf; verifica que la ruta sea `src/data/questions/<leaf>.json`.
- IDs duplicados: asegúrate de usar un prefijo por leaf (ej. `py.functions.definitions.XXX`) y numeración incremental.

Sin preguntas seleccionadas
- El motor mostrará un aviso si no encuentra preguntas para los parámetros; revisa taxonomía, blueprint/módulo, o `--questions-file`.

JSON malformado
- Usa un formateador/validador JSON. Revisa comas finales y comillas.

Colores extraños en terminal
- Rich respeta ANSI. Cambia a un tema de alto contraste o ejecuta en un terminal diferente.
