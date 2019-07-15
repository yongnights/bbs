#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
from apps.common import bp as common_bp
import config
from exts import db,mail,alidayu
from flask_wtf import CSRFProtect


app = Flask(__name__)

#def create_app():

app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
alidayu.init_app(app)

CSRFProtect(app)
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)
app.register_blueprint(ueditor_bp)

#    return app

#app = create_app()

if __name__ == '__main__':
    app.run()
