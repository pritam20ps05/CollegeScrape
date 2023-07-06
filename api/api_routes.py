from flask import Blueprint, request, current_app
from jsonschema import validate, ValidationError
from flask_mail import Mail, Message
import pymongo, random, string

from os import environ

api = Blueprint('api', __name__, url_prefix='/api')

client = pymongo.MongoClient(environ['MONGODB_URI'])
db = client.counselling
cdata_col = db.counsellingData
mail = Mail(current_app)

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
                return True
        return False

auth = Authorize()

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


# API routes
@api.route('/contactus', methods=['POST'])
def contactus():
    schema = {
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
    query = request.get_json()
    schema['minProperties'] = len(schema['properties'].keys())
    try:
        validate(query, schema=schema)
    except ValidationError as e:
        return {'error': e.message}, 400
    iskeyvalid = auth.isKeyValid(str(query.get('key')), str(query.get('token')))
    if not iskeyvalid:
        return {'error': 'Forbidden request, Key-Token mismatch'}, 403
    
    sname = str(query.get('name'))
    smail = str(query.get('email'))
    ssubject = str(query.get('subject'))
    smessage = str(query.get('message'))

    msg = Message(f'{sname}: {ssubject}', sender = environ['MAIL_USERNAME'], recipients = [environ['MAIL_RECIPIENT']])
    msg.body = f'Mail: {smail}\n\n{smessage}'
    mail.send(msg)
    return {
        'message': 'Your query has been successfully submited'
    }

@api.route('/counsellinginfo', methods=['POST'])
def counselinfo():
    query = request.get_json()
    counsellinginfo = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0, 'collection': 0})
    return counsellinginfo

@api.route('/institutetypefilter', methods=['POST'])
def insttfilter():
    schema = {
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
        },
        'additionalProperties': False,
    }
    query = request.get_json()
    qe = {
        'rank': None, 
        'rankBuff': None, 
        'insts': [], 
        'apns': [], 
        'quotas': [], 
        'sts': [], 
        'gens': []
    }
    query.update(qe)
    schema['minProperties'] = len(schema['properties'].keys())
    try:
        validate(query, schema=schema)
    except ValidationError as e:
        return {'error': e.message}, 400
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    insts = coun_col.distinct('Institute', db_query)
    apns = coun_col.distinct('Academic Program Name', db_query)
    return {
        'Institutes': insts,
        'Academic Program Names': apns
    }

@api.route('/institutefilter', methods=['POST'])
def instfilter():
    schema = {
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
        },
        'additionalProperties': False,
    }
    query = request.get_json()
    qe = {
        'rank': None, 
        'rankBuff': None, 
        'apns': [], 
        'quotas': [], 
        'sts': [], 
        'gens': []
    }
    query.update(qe)
    schema['minProperties'] = len(schema['properties'].keys())
    try:
        validate(query, schema=schema)
    except ValidationError as e:
        return {'error': e.message}, 400
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    apns = coun_col.distinct('Academic Program Name', db_query)
    return {
        'Academic Program Names': apns
    }

@api.route('/authorize', methods=['POST'])
def authorize():
    newkey = auth.genKey()
    return {
        'key': newkey
    }
    
@api.route('/counsellingdata', methods=['POST'])
def counseldata():
    schema = {
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
    query = request.get_json()
    schema['minProperties'] = len(schema['properties'].keys())
    try:
        validate(query, schema=schema)
    except ValidationError as e:
        return {'error': e.message}, 400
    iskeyvalid = auth.isKeyValid(str(query.get('key')), str(query.get('token')))
    if not iskeyvalid:
        return {'error': 'Forbidden request, Key-Token mismatch'}, 403
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    if not coun_data:
        return {'error': 'Bad request, provided counselling name does not exist'}, 400
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    counsellingdata = coun_col.find(db_query, {'_id': 0})
    retdat = []
    for cd in counsellingdata:
        retdat.append(cd)
    return {'data': retdat}
