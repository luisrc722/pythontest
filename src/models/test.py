# src/models/test.py
import random
from typing import List, Optional, Dict
from .question import Question
from .result import Result
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.markup import escape
    _RICH_AVAILABLE = True
except Exception:
    _RICH_AVAILABLE = False

class Test:
    def __init__(self, title: str, questions: List[Question], formative: bool = False, rubric: Optional[dict] = None):
        self.title = title
        self.questions = list(questions)
        random.shuffle(self.questions)
        self.results = None
        self.formative = formative
        self.rubric = rubric or {}

    def run(self):
        if _RICH_AVAILABLE:
            console = Console()
            console.rule("🧩 Iniciando test")
            console.print(f"[bold]{self.title}[/bold]")
        else:
            print(f"\n🧩 Iniciando test: {self.title}\n")
        score = 0
        by_area_total = {}
        by_area_correct = {}
        by_diff_total = {}
        by_diff_correct = {}
        by_out_total: Dict[str, int] = {}
        by_out_correct: Dict[str, int] = {}
        for idx, q in enumerate(self.questions, 1):
            if _RICH_AVAILABLE:
                console.print(Panel.fit(escape(f"{idx}. {q.text}"), title=f"Pregunta {idx}"))
                for i, opt in enumerate(q.options):
                    console.print(f"   [bold]{chr(97 + i)})[/bold] {escape(str(opt))}")
            else:
                print(f"{idx}. {q.text}")
                for i, opt in enumerate(q.options):
                    print(f"   {chr(97 + i)}) {opt}")
            # Leer entrada segura: acepta a.., A.., y 1..n; reintenta si inválida
            ans_idx = None
            while True:
                if _RICH_AVAILABLE:
                    ans = Prompt.ask("👉 Tu respuesta (a, b, c... o 1..n)").strip()
                else:
                    ans = input("👉 Tu respuesta (a, b, c... o 1..n): ").strip()
                if not ans:
                    if _RICH_AVAILABLE:
                        console.print("   [yellow]Entrada vacía. Intenta de nuevo.[/yellow]")
                    else:
                        print("   Entrada vacía. Intenta de nuevo.")
                    continue
                # numérico 1..n
                if ans.isdigit():
                    n = int(ans)
                    if 1 <= n <= len(q.options):
                        ans_idx = n - 1
                        break
                # letra a..z
                ch = ans.lower()[0]
                offset = ord(ch) - 97
                if 0 <= offset < len(q.options):
                    ans_idx = offset
                    break
                if _RICH_AVAILABLE:
                    console.print("   [yellow]Entrada inválida. Elige una opción válida.[/yellow]")
                else:
                    print("   Entrada inválida. Elige una opción válida.")

            correct_now = q.is_correct(q.options[ans_idx])
            if correct_now:
                if _RICH_AVAILABLE:
                    console.print("[green]✅ Correcto[/green]")
                else:
                    print("✅ Correcto")
                score += 1
                if self.formative and q.explanation:
                    if _RICH_AVAILABLE:
                        console.print(f"   [cyan]ℹ️  Explicación:[/cyan] {escape(str(q.explanation))}")
                    else:
                        print(f"   ℹ️  Explicación: {q.explanation}")
                if not _RICH_AVAILABLE:
                    print()
            else:
                if _RICH_AVAILABLE:
                    console.print(f"[red]❌ Incorrecto.[/red] Correcta: [bold]{escape(str(q.correct))}[/bold]")
                else:
                    print(f"❌ Incorrecto. Correcta: {q.correct}")
                exp = q.explanation or f"La respuesta correcta es '{q.correct}'."
                if _RICH_AVAILABLE:
                    console.print(f"   [cyan]ℹ️  Explicación:[/cyan] {escape(str(exp))}\n")
                else:
                    print(f"   ℹ️  Explicación: {exp}\n")

            # Acumular estadísticas
            by_area_total[q.area] = by_area_total.get(q.area, 0) + 1
            by_diff_total[q.difficulty] = by_diff_total.get(q.difficulty, 0) + 1
            for out in (q.outcomes or []):
                by_out_total[out] = by_out_total.get(out, 0) + 1
                if correct_now:
                    by_out_correct[out] = by_out_correct.get(out, 0) + 1
            if correct_now:
                by_area_correct[q.area] = by_area_correct.get(q.area, 0) + 1
                by_diff_correct[q.difficulty] = by_diff_correct.get(q.difficulty, 0) + 1

        # Evaluar rúbrica si existe
        rubric_eval = None
        if self.rubric:
            try:
                from ..utils.rubric import evaluate_rubric

                ok, details = evaluate_rubric(self.rubric, len(self.questions), score, by_area_total, by_area_correct)
                rubric_eval = {"ok": ok, "details": details}
            except Exception:
                rubric_eval = None

        self.results = Result(
            self.title,
            len(self.questions),
            score,
            by_area_total=by_area_total,
            by_area_correct=by_area_correct,
            by_diff_total=by_diff_total,
            by_diff_correct=by_diff_correct,
            rubric_eval=rubric_eval,
            by_out_total=by_out_total,
            by_out_correct=by_out_correct,
        )
        self.results.show_summary()
        return self.results
