#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from pony.flask import Pony
from config import config
from gogdbcore.dbmodel import db

app = Flask(__name__)
app.config.update(config)

Pony(app)
