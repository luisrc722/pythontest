import click
from pathlib import Path
from .utils.loader import load_questions
from .utils.sampler import sample_by_area
from .utils.taxonomy import load_taxonomy, taxonomy_leaf_topics
from .utils.blueprint import load_blueprint
from .utils.module_profile import load_module_profile
from .utils.persistence import save_attempt
from .models.test import Test

AREAS_DEFAULT = [
    # Compatibilidad legado (español) si no existe taxonomy
    "fundamentos",
    "estructuras_control",
    "funciones_alcance",
    "numpy",
    "buenas_practicas",
    "errores_comunes",
]


@click.group(invoke_without_command=True, help="Motor de Exámenes (CLI)")
@click.option("--mode", type=click.Choice(["exam", "formative"]), default="exam", show_default=True, help="Modo de ejecución (feedback)")
@click.option("--seed", type=int, default=None, help="Semilla para reproducibilidad")
@click.option("--profile", type=click.Choice(["global", "topic", "module", "quick"]), default="global", show_default=True, help="Tipo de evaluación")
@click.option("--leaves", type=str, default=None, help="Lista de leaves separadas por coma para perfil topic/quick")
@click.option("--per-leaf", type=int, default=None, help="Mínimo por leaf (sobrescribe blueprint en topic/quick)")
@click.option("--max-total", type=int, default=None, help="Máximo total de preguntas (recorte después de muestrear)")
@click.option("--module-file", type=click.Path(exists=True), default=None, help="Ruta a módulo educativo (TOML/JSON) para perfil module")
@click.option("--exhaustive/--no-exhaustive", default=False, show_default=True, help="Tomar todas las preguntas disponibles de las áreas seleccionadas")
@click.option("--order", type=click.Choice(["random", "difficulty", "area"]), default="random", show_default=True, help="Ordenar preguntas por dificultad o agrupar por área")
@click.option("--results-dir", type=click.Path(), default="src/data/results", show_default=True, help="Directorio donde guardar intentos (JSONL)")
@click.pass_context
@click.option("--questions-file", type=click.Path(exists=True), default=None, help="Ruta a un archivo questions.json alternativo")
def main(ctx, mode: str, seed: int | None, profile: str, leaves: str | None, per_leaf: int | None, max_total: int | None, module_file: str | None, exhaustive: bool, order: str, results_dir: str, questions_file: str | None):
    # Si se invoca un subcomando (ej. stats), no ejecutar el flujo de 'run'
    if ctx.invoked_subcommand is not None:
        return
    click.secho("=== Motor de Exámenes (CLI) ===", bold=True)
    all_questions = load_questions(questions_file) if questions_file else load_questions()  # intenta unificado y hace fallback

    # Política: mínimo por área y mezcla de dificultad objetivo
    default_min, overrides, difficulty_mix, rubric = load_blueprint()

    # Si hay taxonomy.json, usa sus hojas como áreas (prefijos jerárquicos)
    taxonomy = load_taxonomy()
    all_leaves = taxonomy_leaf_topics(taxonomy) if taxonomy else AREAS_DEFAULT

    # Selección de áreas y mínimos según perfil
    if profile in ("topic", "quick"):
        if not leaves:
            raise click.UsageError("Para perfil 'topic'/'quick' debes indicar --leaves=leaf1,leaf2,...")
        areas = [a.strip() for a in leaves.split(",") if a.strip()]
        if exhaustive:
            effective_min = 0
        else:
            effective_min = per_leaf if per_leaf is not None else (3 if profile == "quick" else default_min)
        per_area_min_map = {a: effective_min for a in areas}
    elif profile == "module":
        if not module_file:
            raise click.UsageError("Para perfil 'module' debes indicar --module-file=RUTA")
        areas, per_area_min_map, mix_override, max_total_from_module = load_module_profile(module_file)
        if mix_override:
            difficulty_mix = mix_override
        if max_total_from_module and not max_total:
            max_total = max_total_from_module
    else:  # global
        areas = all_leaves
        if exhaustive:
            per_area_min_map = {a: 0 for a in areas}
        else:
            per_area_min_map = {a: overrides.get(a, default_min) for a in areas}

    # Aviso si hay leaves con cobertura insuficiente
    counts = {}
    for q in all_questions:
        counts[q.area] = counts.get(q.area, 0) + 1
    deficits = [(a, counts.get(a, 0), per_area_min_map.get(a, 0)) for a in areas if counts.get(a, 0) < per_area_min_map.get(a, 0)]
    if deficits:
        print("\n⚠️  Cobertura insuficiente en algunos temas (se tomarán menos preguntas):")
        for a, have, need in deficits[:10]:
            print(f" - {a}: {have}/{need}")
        print(" Sugerencia: ejecuta 'make data-check' o 'python3 scripts/validate_questions.py --strict-coverage' para ver el reporte completo.\n")

    selection = sample_by_area(
        all_questions,
        areas=areas,
        per_area_min=per_area_min_map,
        difficulty_mix=difficulty_mix,
        seed=seed,
    )

    # Recortar a máximo total si aplica
    if max_total is not None and len(selection) > max_total:
        import random as _random
        _random.shuffle(selection)
        selection = selection[:max_total]

    # Reordenar según preferencia
    if order != "random":
        if order == "difficulty":
            diff_rank = {"basica": 0, "intermedia": 1, "avanzada": 2}
            selection = sorted(selection, key=lambda q: (diff_rank.get(q.difficulty, 1), q.area))
        elif order == "area":
            selection = sorted(selection, key=lambda q: (q.area, q.difficulty))

    # Título dinámico
    def _humanize(stem: str) -> str:
        return stem.replace("_", " ").replace("-", " ").title()

    if questions_file:
        title = f"Examen: {_humanize(Path(questions_file).stem)}"
    elif profile == "module" and module_file:
        title = f"Módulo: {_humanize(Path(module_file).stem)}"
    elif profile in ("topic", "quick") and areas:
        short = ", ".join(areas[:3]) + ("…" if len(areas) > 3 else "")
        title = f"Quiz por temas: {short}"
    else:
        title = "Examen estratificado por temas"

    if not selection:
        click.secho("No se encontraron preguntas para los parámetros seleccionados.", fg="yellow")
        click.secho("Revisa la taxonomía, blueprint/módulo o el archivo de preguntas indicado.", fg="yellow")
        return
    exam = Test(title, selection, formative=(mode == "formative"), rubric=rubric)
    result = exam.run()

    # Persistencia del intento
    meta = {
        "mode": mode,
        "seed": seed,
        "profile": profile,
        "leaves": areas,
        "per_leaf": per_leaf,
        "exhaustive": exhaustive,
        "order": order,
        "module_file": module_file,
        "max_total": max_total,
        "difficulty_mix": difficulty_mix,
        "per_area_min_map": per_area_min_map,
        "rubric": rubric,
    }
    try:
        save_attempt(result, meta, results_dir=results_dir)
    except Exception as e:
        click.secho(f"[warn] No se pudo persistir el intento: {e}", fg="yellow")



@main.command("stats")
@click.option("--results-dir", type=click.Path(exists=True), default="src/data/results", show_default=True, help="Directorio de intentos (JSONL)")
@click.option("--reports-dir", type=click.Path(), default="src/data/reports", show_default=True, help="Salida para CSV/PNG")
@click.option("--no-plots", is_flag=True, help="No generar gráficos")
def stats(results_dir: str, reports_dir: str, no_plots: bool):
    """Agrega resultados y exporta reportes CSV/PNG."""
    try:
        import pandas as pd
        import numpy as np  # noqa: F401
    except Exception as e:
        raise click.UsageError(f"Faltan dependencias para stats (pandas). Instala requirements: {e}")

    results_path = Path(results_dir) / "attempts.jsonl"
    if not results_path.exists():
        raise click.UsageError(f"No hay resultados en {results_path}. Ejecuta un examen primero.")

    df = pd.read_json(results_path, lines=True)
    out = Path(reports_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Métricas globales
    overall = pd.DataFrame({
        "attempts": [len(df)],
        "avg_score": [df["score"].mean() if not df.empty else 0],
        "avg_pct": [(df["score"] / df["total"]).mean() * 100 if not df.empty else 0],
    })
    overall.to_csv(out / "overall.csv", index=False)

    # Por área (promedio de accuracies por intento)
    def expand_accuracy(col_total, col_correct):
        rows = []
        for _, row in df.iterrows():
            totals = row.get(col_total, {}) or {}
            corrects = row.get(col_correct, {}) or {}
            for area, t in totals.items():
                if t:
                    acc = (corrects.get(area, 0) / t) * 100
                    rows.append({"area": area, "acc": acc})
        return pd.DataFrame(rows)

    by_area_df = expand_accuracy("by_area_total", "by_area_correct")
    if not by_area_df.empty:
        by_area = by_area_df.groupby("area", as_index=False)["acc"].mean().sort_values("acc", ascending=False)
        by_area.to_csv(out / "by_area.csv", index=False)

    # Por dificultad
    by_diff_df = expand_accuracy("by_diff_total", "by_diff_correct")
    if not by_diff_df.empty:
        by_diff = by_diff_df.groupby("area", as_index=False)["acc"].mean().rename(columns={"area": "difficulty"}).sort_values("acc", ascending=False)
        by_diff.to_csv(out / "by_difficulty.csv", index=False)

    # Gráficos
    if not no_plots:
        try:
            import matplotlib.pyplot as plt
        except Exception as e:
            click.secho(f"[warn] No se pudieron generar gráficos (matplotlib): {e}", fg="yellow")
        else:
            if not by_area_df.empty:
                plt.figure(figsize=(10, 5))
                agg = by_area_df.groupby("area")["acc"].mean().sort_values()
                agg.plot(kind="barh")
                plt.title("Accuracy promedio por área (%)")
                plt.xlabel("%")
                plt.tight_layout()
                plt.savefig(out / "by_area_accuracy.png")
                plt.close()
            if not by_diff_df.empty:
                plt.figure(figsize=(6, 4))
                agg = by_diff_df.groupby("area")["acc"].mean().rename(index={"basica": "básica", "intermedia": "intermedia", "avanzada": "avanzada"})
                agg.plot(kind="bar")
                plt.title("Accuracy promedio por dificultad (%)")
                plt.ylabel("%")
                plt.tight_layout()
                plt.savefig(out / "by_difficulty_accuracy.png")
                plt.close()

    click.secho(f"Reportes generados en {out}", fg="green")


@main.command("add")
@click.option("--area", type=str, default=None, help="Leaf (area) destino. Si no se indica, se muestra selector")
def add_question(area: str | None):
    """Asistente interactivo para agregar una pregunta al banco modular."""
    try:
        import inquirer  # type: ignore
    except Exception as e:
        raise click.UsageError(f"Falta 'inquirer'. Instala los requirements: {e}")

    # Cargar taxonomy para elegir área
    taxonomy = load_taxonomy()
    leaves = taxonomy_leaf_topics(taxonomy) if taxonomy else []
    if not area:
        if not leaves:
            raise click.UsageError("No hay taxonomy.json; especifica --area explícitamente (ej. functions/definitions)")
        area = inquirer.prompt([inquirer.List("area", message="Elige leaf (tema)", choices=leaves)])['area']

    # Preguntar campos básicos
    qs = [
        inquirer.Text("text", message="Enunciado de la pregunta"),
        inquirer.Checkbox("options", message="Opciones (marca en orden). Pulsa Enter cuando termines", choices=[]),
    ]
    # Usamos flujo separado para opciones por UX
    answers = {}
    answers["text"] = inquirer.prompt([inquirer.Text("text", message="Enunciado de la pregunta")])['text']
    # Capturar opciones una por una
    options = []
    while True:
        opt = inquirer.prompt([inquirer.Text("opt", message=f"Opción {len(options)+1} (vacío para terminar)")])['opt']
        if not opt:
            break
        options.append(opt)
        if len(options) >= 6:
            break
    if len(options) < 2:
        raise click.UsageError("Se requieren al menos 2 opciones")
    answers["options"] = options

    correct = inquirer.prompt([inquirer.List("correct", message="¿Cuál es la opción correcta?", choices=options)])['correct']
    difficulty = inquirer.prompt([inquirer.List("difficulty", message="Dificultad", choices=["basica","intermedia","avanzada"], default="basica")])['difficulty']
    explanation = inquirer.prompt([inquirer.Text("explanation", message="Explicación breve (opcional)")]).get('explanation')
    tags = inquirer.prompt([inquirer.Text("tags", message="Tags separados por coma (opcional)")]).get('tags')
    tags_list = [t.strip() for t in (tags or '').split(',') if t.strip()]

    # Construir ID incremental por leaf
    leaf_path = Path("src/data/questions") / (area + ".json")
    leaf_path.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if leaf_path.exists():
        try:
            existing = json.loads(leaf_path.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    # Buscar último sufijo numérico
    prefix = "py." + area.replace('/', '.') + "."
    max_n = 0
    for q in existing:
        qid = q.get('id') or ''
        if qid.startswith(prefix):
            try:
                n = int(qid.split('.')[-1])
                if n > max_n:
                    max_n = n
            except Exception:
                pass
    new_id = f"{prefix}{max_n+1:03d}"

    new_q = {
        "id": new_id,
        "text": answers["text"],
        "options": options,
        "correct": correct,
        "area": area,
        "difficulty": difficulty,
        "domain": "python",
        "tags": tags_list,
        "explanation": explanation or None,
    }

    existing.append(new_q)
    leaf_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    click.secho(f"Pregunta guardada en {leaf_path} (id: {new_id})", fg="green")
    # Reempaquetar
    try:
        from . import main as _m
        # Evitar import cíclico; invocar bundler vía script
        import subprocess, sys as _sys
        subprocess.run([_sys.executable, str(Path(__file__).resolve().parents[1] / 'scripts/bundle_questions.py')], check=True)
    except Exception as e:
        click.secho(f"[warn] No se pudo bundlear automáticamente: {e}", fg="yellow")


if __name__ == "__main__":
    main()
