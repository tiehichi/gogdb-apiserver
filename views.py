#!/usr/bin/env python
# encoding: utf-8

from app import app, db
from flask import request, redirect, jsonify
from pony.orm import *
from utilities import DictGet

@app.route('/')
def index():
    return redirect('/changes')


@app.route('/changes')
def changes():
    limit = DictGet(request.args, 'limit', 50, [int, abs], [0])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])
    summary = db.ChangeRecord.select().count()
    pages = summary / limit if summary % limit == 0 else summary / limit + 1

    records = db.ChangeRecord.select().order_by(desc(db.ChangeRecord.dateTime))[limit*(page-1):limit*page]
    rep = {'limit':limit, 'page':page, 'pages':pages, 'records':[r.to_dict() for r in records]}

    return jsonify(rep)


@app.route('/changes/<int:gameid>')
def gamechanges(gameid):
    limit = DictGet(request.args, 'limit', 20, [int, abs], [0])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])
    summary = db.ChangeRecord.select(lambda cr: cr.game.id == gameid).count()
    pages = summary / limit if summary % limit == 0 else summary / limit + 1

    records = db.ChangeRecord.select(lambda cr: cr.game.id == gameid).order_by(desc(db.ChangeRecord.dateTime))[limit*(page-1):limit*page]
    rep = {'limit':limit, 'page':page, 'pages':pages, 'records':[r.to_dict() for r in records]}

    return jsonify(rep)


@app.route('/products')
def products():
    limit = DictGet(request.args, 'limit', 20, [int, abs], [0])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])
    summary = db.GameDetail.select().count()
    pages = summary / limit if summary % limit == 0 else summary / limit + 1

    products = db.GameDetail.select().order_by(desc(db.GameDetail.lastUpdate))[limit*(page-1):limit*page]
    rep = {'limit':limit,
        'page':page,
        'pages':pages,
        'products':[product.to_dict(exclude='basePrice discount lastPriceUpdate lastDiscountUpdate changeRecord',
            with_collections=True, related_objects=True) for product in products]}

    return jsonify(rep)


@app.route('/products/<int:gameid>')
def productdetail(gameid):
    product = db.GameDetail.get(lambda pro: pro.id == gameid)
    if product:
        return jsonify(product.to_dict(exclude='basePrice discount lastPriceUpdate lastDiscountUpdate changeRecord',
            with_collections=True, related_objects=True))
    else:
        return jsonify({'id':gameid, 'error':True, 'status':404, 'message':'Product Not Found'}), 404
