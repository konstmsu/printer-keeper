import logging
import os
import random
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from printer_keeper.datetime_formatting import format_date

logger = logging.getLogger("printer_keeper")

env = Environment(
    loader=PackageLoader("printer_keeper"), autoescape=select_autoescape()
)


# TODO generate random colors
def generate_fortune_html(message_part: str, *, asof: datetime) -> str:
    message = f"""Ура! Доброе утро!
Сегодня у нас {format_date(asof, include_year=False)} {asof.year}.
{message_part}
Хорошего дня!"""

    def format_part(m: re.Match):
        word = m.group("word")
        if word:
            # TODO make random colors given contrast is high enough
            color = random.choice(
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
            return f"<span style='color:{color}'>{word}</span>"
        return m[0]

    parts = [
        format_part(m) for m in re.finditer("(?P<word>\\w+)|(?P<others>\\W+)", message)
    ]

    template = env.get_template("fortune.html")
    return template.render(parts=parts)


def get_messages():
    phrases = Path(__file__).parent / "phrases.txt"
    stripped = [l.strip() for l in phrases.read_text(encoding="utf8").splitlines()]
    return [l for l in stripped if l]


def main():
    html_path = Path(tempfile.mkstemp(prefix="fortune_", suffix=".html")[1])
    pdf_path = Path(tempfile.mkstemp(prefix="fortune_", suffix=".pdf")[1])

    message = random.choice(get_messages())
    asof = datetime.now()
    logger.info("Generating HTML for %s asof %s", message, asof)
    fortune = generate_fortune_html(message, asof=asof)
    logger.info("Writing HTML to %s", html_path)
    html_path.write_text(fortune, encoding="utf8")

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
    os.startfile(pdf_path, "print")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("printer_keeper.log", encoding="utf8"),
            logging.StreamHandler(),
        ],
    )

    try:
        main()
    except:
        logger.exception("Application failed")

    logger.info("Done")
