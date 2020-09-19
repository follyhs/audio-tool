#!/usr/bin/env python
#-*-coding:utf-8-*-

import jsonpointer
import json
import jsonpatch
from functools import wraps

def load_json(json_string):
    try:
        return json.loads(json_string)
    except ValueError , e:
        raise ValueError("Could not parse '%s' as JSON: %s" % (json_string, e))
def _with_json(f):
    @wraps(f)
    def wrapper(self, json_string, *args, **kwargs):
        return json.dumps(f(self, load_json(json_string), *args, **kwargs), ensure_ascii=False)
    return wrapper
#@_with_json
def get_json_value(json_string,json_pointer):
    return jsonpointer.resolve_pointer(json_string,json_pointer)


data = {'a':{'b':'e'},'c':'d'}
#_json = json.dumps(data)

print type(data)
    
d = get_json_value(data,'/a')
print d
print type(d)

_dump = json.dumps(d)
print type(_dump)
_load = json.loads(_dump)
print type(_load)
print _load

#print jsonpointer.resolve_pointer(json_dump,"")

#d = jsonpointer.resolve_pointer(json_load, '/a')
#print d
#print type(d)
