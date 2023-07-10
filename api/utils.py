from jsonschema import validate
from functools import wraps
from flask import request
import random, string
from core import *

schema_dbquery = {
    'type': 'object',
    'properties': {
        'counsellingname': {'type' : 'string'},
        'roundNo': {'type' : 'number'},
        'rank': { 'type': ['number', 'null'] },
        'rankBuff': { 'type': ['number', 'null'] },
        'instts': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'insts': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'apns': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'quotas': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'sts': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'gens': {
            'type': 'array',
            'items': {
                'type': 'string',
            },
        },
        'key': {'type' : 'string'},
        'token': {'type' : 'string'},
    },
    'additionalProperties': False,
}

schema_contactus = {
    'type': 'object',
    'properties': {
        'name': {'type' : 'string'},
        'email': {'type' : 'string'},
        'subject': {'type' : 'string'},
        'message': {'type' : 'string'},
        'key': {'type' : 'string'},
        'token': {'type' : 'string'},
    },
    'additionalProperties': False,
}

class Authorize():
    registeredkeys = []
    maxkeys = 100
    def genKey(self):
        newkey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))
        self.registeredkeys.append(newkey)
        if len(self.registeredkeys) > self.maxkeys:
            self.registeredkeys.pop(0)
        return newkey
    
    def hash_fnv32a(self, str, as_string=True, seed=23):
        hval = 0x811c9dc5 if seed is None else seed
        for c in str:
            hval ^= ord(c)
            hval += (hval << 13) + (hval << 11) + (hval << 17) + (hval << 7) + (hval << 24)
        if as_string:
            return f'{hval & 0xffffffff:08x}'
        return hval & 0xffffffff
    
    def isKeyValid(self, key, enckey):
        if key in self.registeredkeys:
            if enckey == self.hash_fnv32a(key):
                self.registeredkeys.remove(key)
                return
        raise TokenAuthorizationError()

class TokenAuthorizationError(CustomError):
    def __init__(self):
        super().__init__('Forbidden request, Key-Token mismatch', 403)

# Helper functions
def dbQuery(query: dict):
    dq = {
        'Round': query.get('roundNo'),
    }
    if query.get('instts') != []:
        dq['Institute Type'] = {'$in': query.get('instts')}
    if query.get('insts') != []:
        dq['Institute'] = {'$in': query.get('insts')}
    if query.get('apns') != []:
        dq['Academic Program Name'] = {'$in': query.get('apns')}
    if query.get('quotas') != []:
        dq['Quota'] = {'$in': query.get('quotas')}
    if query.get('sts') != []:
        dq['Seat Type'] = {'$in': query.get('sts')}
    if query.get('gens') != []:
        dq['Gender'] = {'$in': query.get('gens')}

    if query.get('rank'):
        rank_ul = query.get('rank')
        if query.get('rankBuff'):
            rank_ul = query.get('rank') - query.get('rankBuff')
            rank_ll = query.get('rank') + query.get('rankBuff')
            dq['Closing Rank'] = {
                '$gte': rank_ul,
                '$lte': rank_ll
            }
        else:
            dq['Closing Rank'] = {
                '$gte': rank_ul
            }
    return dq

auth = Authorize()

# Helper decorators
def validateSchema(schema: dict, required: list = []):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            schema_copy = schema.copy()
            schema_copy['required'] = required
            query = request.get_json()
            validate(query, schema=schema_copy)
            return f(*args, **kw)
        return wrapper
    return decorator

def authorizeToken(f):
    @wraps(f)
    def wrapper(*args, **kw):
        query = request.get_json()
        auth.isKeyValid(str(query.get('key')), str(query.get('token')))
        return f(*args, **kw)
    return wrapper