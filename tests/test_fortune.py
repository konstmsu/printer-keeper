import random
import subprocess
from datetime import datetime
from pathlib import Path

import pytest
from zoneinfo import ZoneInfo

from printer_keeper.arithmetics import ArithmeticProblemGenerator
from printer_keeper.fortune import (
    MessageGenerator,
    MessageHtmlFormatter,
    MorningFortuneGenerator,
)

random.seed(42)


def test_messages():
    messages = MessageGenerator(random_seed=0)._get_messages()
    assert len(messages) > 2
    for m in messages:
        assert len(m) > 5
        assert m[-1] in ".!"
    assert "Делу – время, потехе – час." in messages


def test_template(snapshot):
    fortune = MorningFortuneGenerator(random_seed=0).generate(
        wisdom="Кукареку!",
        problems=["1 + 1 ="],
        asof=datetime(2022, 8, 4, 6, 45, tzinfo=ZoneInfo("Asia/Singapore")),
    )
    html = MessageHtmlFormatter(random_seed=0).format(fortune)
    Path("generated.html").write_text(html, encoding="utf8")
    assert snapshot == html


def test_arithmetic_problems(snapshot):
    problems = ArithmeticProblemGenerator(random_seed=0).generate()
    assert snapshot == [p.text for p in problems]


@pytest.mark.annoying
def test_end_to_end():
    result: subprocess.CompletedProcess = subprocess.run(
        "uv run -m printer_keeper".split(),
        capture_output=True,
        text=True,
    )
    assert "Printing" in result.stderr
    result.check_returncode()
