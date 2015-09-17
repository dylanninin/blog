#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blog App Entrance
version 1.0
history:
2013-6-19    dylanninin@gmail.com    init
"""

import web
from config import urls

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
