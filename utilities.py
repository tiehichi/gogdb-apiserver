#!/usr/bin/env python
# encoding: utf-8

from flask.json import JSONEncoder
import datetime, decimal
from gogdbcore.dbmodel import db


class GOGJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            encoder_table = {
                    datetime.datetime: self.datetime_encoder,
                    decimal.Decimal: self.decimal_encoder,
                    db.GameLink: self.links_encoder,
                    db.Publisher: self.publisher_encoder,
                    db.Developer: self.developer_encoder,
                    db.OS: self.os_encoder,
                    db.Feature: self.feature_encoder,
                    db.Tag: self.tag_encoder,
                    db.Localization: self.loc_encoder,
                    db.Formatter: self.formatter_encoder,
                    db.Image: self.image_encoder,
                    db.Screenshot: self.screenshot_encoder,
                    db.Video: self.video_encoder,
                    db.VideoProvider: self.videoprovider_encoder,
                    db.GameDetail: self.gamedetail_encoder,
                    }
            if type(obj) in encoder_table:
                return encoder_table[type(obj)](obj)

            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

    def datetime_encoder(self, obj):
        return obj.strftime('%Y-%m-%d %H:%M:%S')

    def decimal_encoder(self, obj):
        return str(obj)

    def links_encoder(self, obj):
        return obj.to_dict(exclude='game')

    def publisher_encoder(self, obj):
        return obj.name

    def developer_encoder(self, obj):
        return obj.name

    def os_encoder(self, obj):
        return obj.name

    def feature_encoder(self, obj):
        return obj.name

    def tag_encoder(self, obj):
        return obj.name

    def loc_encoder(self, obj):
        return obj.to_dict(exclude='game')

    def formatter_encoder(self, obj):
        return obj.formatter

    def image_encoder(self, obj):
        return obj.to_dict(exclude='game', related_objects=True, with_collections=True)

    def screenshot_encoder(self, obj):
        return obj.to_dict(exclude='id game', related_objects=True, with_collections=True)

    def video_encoder(self, obj):
        return obj.to_dict(exclude='id game', related_objects=True, with_collections=True)

    def videoprovider_encoder(self, obj):
        return obj.to_dict(exclude='videos')

    def gamedetail_encoder(self, obj):
        return obj.id


def DictGet(obj, key, default=None, converts=[], exclude=[]):
    if isinstance(obj, dict):
        value = obj.get(key, default)
        if len(converts) != 0:
            try:
                for convert in converts:
                    value = convert(value)
            except:
                value = default
        if value in exclude:
            return default
        else:
            return value
    else:
        return default

