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


class App(web.application):
    def run(self, port=8080, *middlewares):
        func = self.wsgifunc(*middlewares)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


if __name__ == "__main__":
    app = App(urls, globals())
    app.run(web.config.port)
