#!/usr/bin/python
# -*- coding: utf-8 -*-
def _init():
    global _global_dict
    _global_dict = {}
def set(name, value):
    _global_dict[name] = value
def sets(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if isinstance(v,int):
                _global_dict[k] = v 
def get(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue
