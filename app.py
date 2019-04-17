#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from pony.flask import Pony
from config import config
from gogdbcore.dbmodel import db
from utilities import GOGJSONEncoder

app = Flask(__name__)
app.config.update(config)
app.json_encoder = GOGJSONEncoder

Pony(app)
