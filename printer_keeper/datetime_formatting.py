from datetime import date, datetime
from typing import Literal


def format_date(d: date, *, include_year: bool) -> str:
    def year():
        if d.year == 2022:
            return "две тысячи двадцать второго"
        if d.year == 2023:
            return "две тысячи двадцать третьего"
        if d.year == 2024:
            return "две тысячи двадцать четвёртого"
        if d.year == 2025:
            return "две тысячи двадцать пятого"
        if d.year == 2026:
            return "две тысячи двадцать шестого"
        # TODO make generic
        raise NotImplementedError

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
