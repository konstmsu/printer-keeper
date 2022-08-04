import random
import tempfile
from typing import Literal
from jinja2 import Environment, PackageLoader, select_autoescape
import re
from pathlib import Path
import os
import subprocess
from datetime import datetime, date
import logging

logger = logging.getLogger("printer_keeper")

env = Environment(
    loader=PackageLoader("printer_keeper"), autoescape=select_autoescape()
)


def format_date(d: date, *, include_year: bool) -> str:
    def year():
        if d.year == 2022:
            return "две тысячи двадцать второго"
        if d.year == 2023:
            return "две тысячи двадцать третьего"
        if d.year == 2024:
            return "две тысячи двадцать четвёртого"
        # TODO make generic
        raise NotImplemented()

    months = [
        "января",
        "февраля",
        "марта",
        "апреля",
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        "ноября",
        "декабря",
    ]
    days = [
        "первое",
        "второе",
        "третье",
        "четвёртое",
        "пятое",
        "шестое",
        "седьмое",
        "восьмое",
        "девятое",
        "десятое",
        "одиннадцатое",
        "двенадцатое",
        "тринадцатое",
        "четырнадцатое",
        "пятнадцатое",
        "шестнадцатое",
        "семнадцатое",
        "восемнадцатое",
        "девятнадцатое",
        "двадцатое",
        "двадцать первое",
        "двадцать второе",
        "двадцать третье",
        "двадцать четвёртое",
        "двадцать пятое",
        "двадцать шестое",
        "двадцать седьмое",
        "двадцать восьмое",
        "двадцать девятое",
        "тридцатое",
        "тридцать первое",
    ]

    parts = [days[d.day - 1], months[d.month - 1]]

    if include_year:
        parts.append(f"{year()} года")

    return " ".join(parts)


def format_datetime(dt: datetime) -> str:
    simple_numbers = [
        "ноль",
        ("один", "одна"),
        ("два", "две"),
        "три",
        "четыре",
        "пять",
        "шесть",
        "семь",
        "восемь",
        "девять",
        "десять",
        "одиннадцать",
        "двенадцать",
        "тринадцать",
        "четырнадцать",
        "пятнадцать",
        "шестнадцать",
        "семнадцать",
        "восемнадцать",
        "девятнадцать",
    ]
    tens = [
        "двадцать",
        "тридцать",
        "сорок",
        "пятьдесят",
        "шестьдесят",
        "семьдесят",
        "восемьдесят",
        "девяноста",
    ]

    def number(v: int, *, gender: Literal["male", "female"]) -> str:
        gender_index = {"male": 0, "female": 1}[gender]
        if v in [1, 2]:
            return simple_numbers[v][gender_index]
        if 3 <= v < 20:
            return simple_numbers[v]
        if v < 100:
            t = tens[v // 10 - 2]
            if v % 10 == 0:
                return t
            d = number(v % 10, gender=gender)
            return f"{t} {d}"
        return str(v)

    def inflect(word: str, count: int) -> str:
        if 5 <= count % 100 <= 20:
            c = 2
        elif count % 10 == 1:
            c = 0
        elif count % 10 in [2, 3, 4]:
            c = 1
        else:
            c = 2

        words = [("час", "часа", "часов"), ("минута", "минуты", "минут")]
        for forms in words:
            if word == forms[0]:
                return forms[c]
        return word

    parts = [
        format_date(dt.date(), include_year=True) + ",",
        f"{number(dt.hour, gender='male')} {inflect('час', dt.hour)}",
        f"{number(dt.minute, gender='female')} {inflect('минута', dt.minute)}",
    ]
    return " ".join(parts)


# TODO generate random phrase and colors
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
    return [l.strip() for l in phrases.read_text(encoding="utf8").splitlines()]


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
