#!/usr/bin/env python
# encoding: utf-8

from flask.json import JSONEncoder
import datetime
import re


class GOGJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
        except TypeError:
                pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


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


def specstr_cleaner(specstr):
    if specstr:
        spec = re.compile('<[^>]*>')
        return spec.sub('', specstr)
    else:
        return specstr
