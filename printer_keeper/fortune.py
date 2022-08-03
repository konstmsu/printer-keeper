import random
from typing import Literal
from jinja2 import Environment, PackageLoader, select_autoescape
import re
from pathlib import Path
import os
import subprocess
from datetime import datetime

env = Environment(
    loader=PackageLoader("printer_keeper"), autoescape=select_autoescape()
)


def format_datetime(dt: datetime) -> str:
    def year():
        if dt.year == 2022:
            return "две тысячи двадцать второго"
        if dt.year == 2023:
            return "две тысячи двадцать третьего"
        if dt.year == 2024:
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
        f"{days[dt.day-1]} {months[dt.month-1]}",
        f"{year()} года,",
        f"{number(dt.hour, gender='male')} {inflect('час', dt.hour)}",
        f"{number(dt.minute, gender='female')} {inflect('минута', dt.minute)}",
    ]
    return " ".join(parts)


# TODO generate random phrase and colors
def generate_fortune_html(message_part: str, *, asof: datetime) -> str:
    message = f"{message_part}\nСейчас {format_datetime(asof)}"

    def format_part(m: re.Match):
        word = m.group("word")
        if word:
            color = random.choice(
                [
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


if __name__ == "__main__":
    html_path = Path("tmp/fortune.html")
    pdf_path = Path("tmp/fortune.pdf")

    html_path.parent.mkdir(parents=True, exist_ok=True)

    # cleanup
    html_path.unlink(missing_ok=True)
    pdf_path.unlink(missing_ok=True)

    fortune = generate_fortune_html("Доброе утро, прекрасный мир!", asof=datetime.now())
    html_path.write_text(fortune, encoding="utf8")

    # Convert to PDF. Or is there an easier way to print HTML?
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
    os.startfile(pdf_path, "print")
