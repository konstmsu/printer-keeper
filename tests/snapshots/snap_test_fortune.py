# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_arithmetic_problems 1'] = [
    '13 + 32 = ',
    '13 + 18 = ',
    '38 - 19 = ',
    '24 - 6 = ',
    '9 * 8 = ',
    '3 * 4 = ',
    '81 / 9 = ',
    '56 / 8 = '
]

snapshots['test_template 1'] = '''<html>
  <head>
    <title>Доброе Утро!</title>
  </head>
  <body>
    <p style="font-size: 2.2em; white-space: pre-wrap"
      ><span style='color:#866103'>Ура</span>! <span style='color:#A82255'>Доброе</span> <span style='color:#5A701A'>утро</span>!
<span style='color:#7A542E'>Сегодня</span> <span style='color:#A82255'>у</span> <span style='color:black'>нас</span> <span style='color:#77450D'>четвёртое</span> <span style='color:#5642A6'>августа</span> <span style='color:#5C255C'>2022</span>.

<span style='color:#A82255'>Пословица</span> <span style='color:#7A542E'>дня</span>:
<span style='color:#5A701A'>Кукареку</span>!

<span style='color:#866103'>Чуть</span>-<span style='color:#77450D'>чуть</span> <span style='color:#5C255C'>арифметики</span>:
□   <span style='color:#96290D'>1</span> + <span style='color:#0C5174'>1</span> =
<span style='color:#7A542E'>Правильно</span>:    <span style='color:#7A542E'>из</span> <span style='color:blue'>1</span>

<span style='color:#5642A6'>Хорошего</span> <span style='color:green'>дня</span>!</p
    >
  </body>
</html>'''
