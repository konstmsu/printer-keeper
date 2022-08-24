import logging
import os
import re
import subprocess
import tempfile
from datetime import datetime
from functools import cache
from pathlib import Path
from random import Random
from typing import List

from jinja2 import Environment, PackageLoader, select_autoescape

from .arithmetics import ArithmeticProblemGenerator
from .datetime_formatting import format_date

logger = logging.getLogger("printer_keeper")

env = Environment(
    loader=PackageLoader("printer_keeper"), autoescape=select_autoescape()
)


class MessageGenerator:
    def __init__(self, *, random_seed: int = None):
        self.rnd = Random(random_seed)

    @cache
    def _get_messages(self):
        phrases = Path(__file__).parent / "phrases.txt"
        stripped = [l.strip() for l in phrases.read_text(encoding="utf8").splitlines()]
        return [l for l in stripped if l]

    def generate(self) -> str:
        return self.rnd.choice(self._get_messages())


class MorningFortuneGenerator:
    def __init__(self, *, random_seed: int = None):
        self.rnd = Random(random_seed)

    def generate(self, *, asof: datetime, wisdom: str, problems: List[str]):
        problems_joined = "\n".join(problems)
        return f"""Ура! Доброе утро!
Сегодня у нас {format_date(asof, include_year=False)} {asof.year}.

Пословица дня:
{wisdom}

Чуть-чуть арифметики:
{problems_joined}

Хорошего дня!"""


class MessageHtmlFormatter:
    def __init__(self, *, random_seed: int = None):
        self.rnd = Random(random_seed)

    def _random_color(self):
        # TODO make random colors given contrast is high enough
        return self.rnd.choice(
            [
                "black",
                "red",
                "green",
                "blue",
                "#77450D",
                "#96290D",
                "#A82255",
                "#5C255C",
                "#5642A6",
                "#0C5174",
                "#004D46",
                "#1D7324",
                "#5A701A",
                "#866103",
                "#7A542E",
            ]
        )

    def format(self, message: str) -> str:
        def format_part(m: re.Match):
            word = m.group("word")
            if word:
                return f"<span style='color:{self._random_color()}'>{word}</span>"
            return m[0]

        parts = [
            format_part(m)
            for m in re.finditer("(?P<word>\\w+)|(?P<others>\\W+)", message)
        ]

        template = env.get_template("fortune.html")
        return template.render(parts=parts)


def main():
    html_path = Path(tempfile.mkstemp(prefix="fortune_", suffix=".html")[1])
    pdf_path = Path(tempfile.mkstemp(prefix="fortune_", suffix=".pdf")[1])

    asof = datetime.now()
    message = MessageGenerator().generate()
    arithmetic_problems = ArithmeticProblemGenerator().generate()

    logger.info("Generating fortune asof %s for %s", message, asof)
    fortune = MorningFortuneGenerator().generate(
        wisdom=message, asof=asof, problems=[p.text for p in arithmetic_problems]
    )

    logger.info("Writing HTML to %s", html_path)
    html = MessageHtmlFormatter().format(fortune)
    html_path.write_text(html, encoding="utf8")

    # Convert to PDF. Or is there an easier way to print HTML?
    logger.info("Converting to PDF in %s", pdf_path)
    subprocess.run(
        [
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "--headless",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path.absolute()}",
            str(html_path.absolute()),
        ],
        check=True,
    )

    # send to printer
    logger.info("Printing %s", pdf_path)
    os.startfile(pdf_path, "open" if os.environ.get("IGNORE_PRINT") else "print")
