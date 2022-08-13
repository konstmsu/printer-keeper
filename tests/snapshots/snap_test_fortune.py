# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_template 1'] = '''<html>
  <head>
    <title>Доброе Утро!</title>
  </head>
  <body>
    <p style="font-size: 4em; white-space: pre-wrap"
      ><span style='color:#004D46'>Ура</span>! <span style='color:red'>Доброе</span> <span style='color:black'>утро</span>!
<span style='color:#1D7324'>Сегодня</span> <span style='color:#77450D'>у</span> <span style='color:blue'>нас</span> <span style='color:blue'>четвёртое</span> <span style='color:green'>августа</span> <span style='color:#1D7324'>2022</span>.
<span style='color:red'>Кукареку</span>!
<span style='color:#004D46'>Хорошего</span> <span style='color:#1D7324'>дня</span>!</p
    >
  </body>
</html>'''
