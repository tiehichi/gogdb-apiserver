#!/usr/bin/env python
# encoding: utf-8

from app import app, db
from flask import request, redirect, jsonify
from pony.orm import *
from utilities import DictGet

@app.route('/')
def index():
    return redirect('/changes/')


@app.route('/changes')
@app.route('/changes/')
def changes():
    limit = DictGet(request.args, 'limit', 50, [int, abs])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])

    records = db.ChangeRecord.select()
    summary = records.count()

    if limit != 0:
        pages = summary / limit if summary % limit == 0 else summary / limit + 1
        records = records.order_by(desc(db.ChangeRecord.dateTime))[limit*(page-1):limit*page]
    else:
        pages = 1

    rep = {'count':summary, 'limit':limit, 'page':page, 'pages':pages, 'records':[r.to_dict() for r in records]}

    return jsonify(rep)


@app.route('/changes/<int:gameid>')
@app.route('/changes/<int:gameid>/')
def gamechanges(gameid):
    limit = DictGet(request.args, 'limit', 20, [int, abs])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])
    records = db.ChangeRecord.select(lambda cr: cr.game.id == gameid)
    summary = records.count()

    if limit != 0:
        pages = summary / limit if summary % limit == 0 else summary / limit + 1
        records = records.order_by(desc(db.ChangeRecord.dateTime))[limit*(page-1):limit*page]
    else:
        pages = 1

    rep = {'count':summary, 'limit':limit, 'page':page, 'pages':pages, 'records':[r.to_dict() for r in records]}

    return jsonify(rep)

@app.route('/products')
@app.route('/products/')
def products():
    limit = DictGet(request.args, 'limit', 20, [int, abs])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])
    query = DictGet(request.args, 'query', '')

    if query == '':
        summary = db.GameDetail.select().count()
        prods = db.GameDetail.select().order_by(desc(db.GameDetail.lastUpdate))

    else:
        prods = select(prod for prod in db.GameDetail).where(lambda prod: query.lower() in prod.title.lower() or query.lower() in str(prod.id))
        summary = prods.count()

    if limit != 0:
        pages = summary / limit if summary % limit == 0 else summary / limit + 1
        prods = prods[limit*(page-1):limit*page]
    else:
        pages = 1

    rep = {'count':summary,
        'limit':limit,
        'page':page,
        'pages':pages,
        'products':[prod.to_dict(exclude='basePrice discount lastPriceUpdate lastDiscountUpdate changeRecord',
            with_collections=True, related_objects=True) for prod in prods]}

    return jsonify(rep)


@app.route('/products/<int:gameid>')
@app.route('/products/<int:gameid>/')
def productdetail(gameid):
    product = db.GameDetail.get(lambda pro: pro.id == gameid)
    if product:
        return jsonify(product.to_dict(exclude='basePrice discount lastPriceUpdate lastDiscountUpdate changeRecord',
            with_collections=True, related_objects=True))
    else:
        return jsonify({'id':gameid, 'error':True, 'status':404, 'message':'Product Not Found'}), 404


@app.route('/price/<int:gameid>')
@app.route('/price/<int:gameid>/')
def baseprice(gameid):
    limit = DictGet(request.args, 'limit', 50, [int, abs])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])

    price = db.BasePrice.select(lambda p: p.game.id == gameid)
    if not price:
        return jsonify({'id':gameid, 'error':True, 'status':404, 'message':'Product Not Found'}), 404

    ccode = request.args.get('countryCode', '')

    if ccode == '':

        summary = price.count()

        if limit != 0:
            pages = summary / limit if summary % limit == 0 else summary / limit + 1
            price = price[limit*(page-1):limit*page]
        else:
            pages = 1

        rep = {'count':summary,
                'limit':limit,
                'page':page,
                'pages':pages,
                'baseprice':[p.to_dict(exclude='game') for p in price]
                }
    else:
        price = price.where(lambda p: p.country == ccode.upper())

        if not price:
            return jsonify({'id':gameid, 'error':True, 'status':404, 'message':'Country Code Not Found'}), 404

        rep = price.first().to_dict(exclude='game')

    return jsonify(rep)


@app.route('/discount/<int:gameid>')
@app.route('/discount/<int:gameid>/')
def discount(gameid):
    limit = DictGet(request.args, 'limit', 50, [int, abs])
    page = DictGet(request.args, 'page', 1, [int, abs], [0])

    dis = db.Discount.select(lambda d: d.game.id == gameid).order_by(desc(db.Discount.dateTime))
    if not dis:
        return jsonify({'id':gameid, 'error':True, 'status':404, 'message':'Product Not Found'}), 404

    summary = dis.count()

    if limit != 0:
        pages = summary / limit if summary % limit == 0 else summary / limit + 1
        dis = dis[limit*(page-1):limit*page]
    else:
        pages = 1

    rep = {'count':summary,
            'limit':limit,
            'page':page,
            'pages':pages,
            'discount':[d.to_dict(exclude='game') for d in dis]
            }
    return jsonify(rep)
