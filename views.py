#!/usr/bin/env python
# encoding: utf-8

from app import app, db
from flask import request, redirect
from pony.orm import *
import json, utilities

@app.route('/')
def index():
    return redirect('/changes')

@app.route('/changes')
def changes():
    limit = utilities.dict_safeget(request.args, 'limit', 50, convert=int, exclude=[0])
    page = utilities.dict_safeget(request.args, 'page', 1, convert=int, exclude=[0])
    summary = db.ChangeRecord.select().count()
    pages = summary / limit if summary % limit == 0 else summary / limit + 1

    records = db.ChangeRecord.select().order_by(desc(db.ChangeRecord.dateTime))[limit*(page-1):limit*page]
    rep = {'limit':limit, 'page':page, 'pages':pages, 'records':[r.to_dict() for r in records]}
    for r in rep['records']:
        r['dateTime'] = utilities.datetime2str(r['dateTime'])

    return json.dumps(rep)
