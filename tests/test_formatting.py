import re
from datetime import date, datetime, timedelta

from printer_keeper.datetime_formatting import format_date, format_datetime


def test_format_day():
    assert format_date(date(2022, 7, 15), include_year=False) == "пятнадцатое июля"


def test_format_datetime():
    assert (
        format_datetime(datetime(2022, 7, 15, 6, 25))
        == "пятнадцатое июля две тысячи двадцать второго года, шесть часов двадцать пять минут"
    )
    assert (
        format_datetime(datetime(2023, 1, 1, 20, 50))
        == "первое января две тысячи двадцать третьего года, двадцать часов пятьдесят минут"
    )
    assert (
        format_datetime(datetime(2023, 9, 29, 1, 31))
        == "двадцать девятое сентября две тысячи двадцать третьего года, один час тридцать одна минута"
    )
    for i in range(1000):
        dt = datetime(2022, 1, 1, 13, 45) + timedelta(days=i, minutes=i)
        res = format_datetime(dt)
        assert re.search("двадцать второго|двадцать третьего|двадцать четвёртого", res)
        assert re.search(
            "января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря",
            res,
        )
        assert re.search("года", res)
        assert re.search("час|часов|часа", res)
        assert re.search("минут", res)


def test_format_regressions(snapshot):
    for i in range(1000):
        dt = datetime(2024, 1, 1, 6, 0) + timedelta(days=i, minutes=i)
        res = format_datetime(dt)
        assert snapshot == res
