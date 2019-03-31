#!/usr/bin/env python
# encoding: utf-8

import datetime
import re

def datetime2str(date):
    if date == None:
        return ""
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

def specstr_cleaner(specstr):
    if specstr:
        spec = re.compile('<[^>]*>')
        return spec.sub('', specstr)
    else:
        return specstr
