import sys
from pathlib import Path


# Ensure src/ is on path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_rich_escapes_brackets_in_question(capsys, monkeypatch):
    # Skip if Rich is not available
    try:
        from rich.prompt import Prompt  # noqa: F401
    except Exception:
        return

    from models.question import Question
    from models.test import Test

    q = Question(
        id="t.compr.esc.001",
        text="¿Qué crea [x*x for x in range(3)]?",
        options=["[1,4,9]", "[0,1,4]", "[0,1,4,9]", "Error"],
        correct="[0,1,4]",
        area="control_flow/comprehensions",
        difficulty="basica",
        domain="python",
        tags=[],
        source=None,
        explanation=None,
    )

    # Always answer 'b' (correct)
    from rich import prompt as rich_prompt

    monkeypatch.setattr(rich_prompt.Prompt, "ask", lambda *args, **kwargs: "b")

    exam = Test("Prueba Rich", [q], formative=False)
    exam.run()
    out = capsys.readouterr().out
    assert "[x*x for x in range(3)]" in out


def test_rich_escapes_brackets_in_explanation(capsys, monkeypatch):
    try:
        from rich.prompt import Prompt  # noqa: F401
    except Exception:
        return

    from models.question import Question
    from models.test import Test
    from rich import prompt as rich_prompt

    q = Question(
        id="t.expl.esc.001",
        text="Pregunta demo",
        options=["A", "B"],
        correct="B",
        area="demo/area",
        difficulty="basica",
        domain="python",
        tags=[],
        source=None,
        explanation="Ver [doc] para más info",
    )

    # Force wrong answer 'a' to trigger explanation
    monkeypatch.setattr(rich_prompt.Prompt, "ask", lambda *args, **kwargs: "a")

    exam = Test("Prueba Rich Expl", [q], formative=False)
    exam.run()
    out = capsys.readouterr().out
    assert "Ver [doc] para más info" in out
