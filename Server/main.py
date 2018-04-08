# -*- coding: utf-8 -*-
# filename: main.py

import web
import os
from handle import Handle

urls = (
    '/wx', 'Handle',
)
app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

if __name__ == '__main__':
    app = web.application(urls, globals())
app.run()
