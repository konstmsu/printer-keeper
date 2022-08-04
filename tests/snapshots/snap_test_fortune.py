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
      ><span style='color:#004D46'>Доброе</span> <span style='color:red'>утро</span>, <span style='color:black'>мир</span>!
<span style='color:#1D7324'>Сегодня</span> <span style='color:#77450D'>четвёртое</span> <span style='color:blue'>августа</span></p
    >
  </body>
</html>'''
