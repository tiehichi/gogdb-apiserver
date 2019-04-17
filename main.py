#!/usr/bin/env python
# encoding: utf-8

from views import *
from app import app, db

db.bind(**app.config['PONY'])
db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    app.run()
