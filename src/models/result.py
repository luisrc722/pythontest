# src/models/result.py

try:
    from rich.console import Console
    from rich.table import Table
    _RICH_AVAILABLE = True
except Exception:
    _RICH_AVAILABLE = False


class Result:
    def __init__(
        self,
        title: str,
        total: int,
        score: int,
        by_area_total: dict | None = None,
        by_area_correct: dict | None = None,
        by_diff_total: dict | None = None,
        by_diff_correct: dict | None = None,
        rubric_eval: dict | None = None,
        by_out_total: dict | None = None,
        by_out_correct: dict | None = None,
    ):
        self.title = title
        self.total = total
        self.score = score
        self.by_area_total = by_area_total or {}
        self.by_area_correct = by_area_correct or {}
        self.by_diff_total = by_diff_total or {}
        self.by_diff_correct = by_diff_correct or {}
        self.rubric_eval = rubric_eval or {}
        self.by_out_total = by_out_total or {}
        self.by_out_correct = by_out_correct or {}

    def level(self):
        if self.total == 0:
            return "Sin preguntas"
        ratio = self.score / self.total
        if ratio >= 0.8:
            return "Óptimo ✅"
        elif ratio >= 0.55:
            return "Intermedio ⚙️"
        else:
            return "Básico 📘"

    def show_summary(self):
        if _RICH_AVAILABLE:
            console = Console()
            console.rule("📊 Resultados")
            console.print(f"[bold]Test:[/bold] {self.title}")
            console.print(f"[bold]Puntaje:[/bold] {self.score}/{self.total}  •  [bold]Nivel:[/bold] {self.level()}")

            if self.rubric_eval:
                verdict = self.rubric_eval.get("ok")
                details = self.rubric_eval.get("details", {})
                status = "[green]APROBADO[/green]" if verdict else "[red]REPROBADO[/red]"
                console.print(f"[bold]Veredicto:[/bold] {status}")
                if details and not verdict:
                    for k, v in details.items():
                        console.print(f" - {k}: {v}")

            if self.by_area_total:
                table = Table(title="Desglose por área")
                table.add_column("Área")
                table.add_column("Correctas")
                table.add_column("Total")
                table.add_column("%")
                for area, total in sorted(self.by_area_total.items()):
                    ok = self.by_area_correct.get(area, 0)
                    pct = (ok / total * 100) if total else 0
                    table.add_row(area, str(ok), str(total), f"{pct:.0f}%")
                console.print(table)

            if self.by_diff_total:
                table = Table(title="Desglose por dificultad")
                table.add_column("Dificultad")
                table.add_column("Correctas")
                table.add_column("Total")
                table.add_column("%")
                for diff, total in sorted(self.by_diff_total.items()):
                    ok = self.by_diff_correct.get(diff, 0)
                    pct = (ok / total * 100) if total else 0
                    table.add_row(diff, str(ok), str(total), f"{pct:.0f}%")
                console.print(table)
        else:
            print("📊 RESULTADOS:")
            print(f"  Test: {self.title}")
            print(f"  Puntaje: {self.score}/{self.total}")
            print(f"  Nivel: {self.level()}")
            if self.rubric_eval:
                verdict = self.rubric_eval.get("ok")
                details = self.rubric_eval.get("details", {})
                status = "APROBADO" if verdict else "REPROBADO"
                print(f"  Veredicto: {status}")
                if details and not verdict:
                    for k, v in details.items():
                        print(f"   - {k}: {v}")
            if self.by_area_total:
                print("\n  Desglose por área:")
                for area, total in sorted(self.by_area_total.items()):
                    ok = self.by_area_correct.get(area, 0)
                    pct = (ok / total * 100) if total else 0
                    print(f"   - {area}: {ok}/{total} ({pct:.0f}%)")
            if self.by_diff_total:
                print("\n  Desglose por dificultad:")
                for diff, total in sorted(self.by_diff_total.items()):
                    ok = self.by_diff_correct.get(diff, 0)
                    pct = (ok / total * 100) if total else 0
                    print(f"   - {diff}: {ok}/{total} ({pct:.0f}%)")
