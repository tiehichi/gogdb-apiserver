#!/usr/bin/env python
# encoding: utf-8

import datetime

def datetime2str(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def dict_safeget(dictobj, key, default, convert=None, exclude=[]):
    if key in dictobj:
        if convert == None:
            value = dictobj.get(key)
        else:
            try:
                value = convert(dictobj.get(key))
            except:
                value = default
        if value in exclude:
            return default
        else:
            return value
    else:
        return default
