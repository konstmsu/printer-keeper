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
    <p style="font-size: 5em; white-space: pre-wrap"
      ><span style='color:#1D7324'>Доброе</span> <span style='color:green'>утро</span>, <span style='color:red'>мир</span>!
<span style='color:#5A701A'>Сейчас</span> <span style='color:#96290D'>четвёртое</span> <span style='color:#77450D'>августа</span> <span style='color:#77450D'>две</span> <span style='color:blue'>тысячи</span> <span style='color:#5A701A'>двадцать</span> <span style='color:green'>второго</span> <span style='color:#1D7324'>года</span>, <span style='color:#5A701A'>шесть</span> <span style='color:#0C5174'>часов</span> <span style='color:green'>сорок</span> <span style='color:#004D46'>пять</span> <span style='color:#5C255C'>минут</span></p
    >
  </body>
</html>'''
