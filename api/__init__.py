from flask import Blueprint, request, current_app
from flask_mail import Mail, Message
from jsonschema import validate
from errors import *
from .utils import *
from core import *
import pymongo

api = Blueprint('api', __name__, url_prefix='/api')

client = pymongo.MongoClient(mongouri)
db = client.counselling
cdata_col = db.counsellingData
mail = Mail(current_app)
auth = Authorize()

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
    validate(query, schema=schema)
    auth.isKeyValid(str(query.get('key')), str(query.get('token')))
    sname = str(query.get('name'))
    smail = str(query.get('email'))
    ssubject = str(query.get('subject'))
    smessage = str(query.get('message'))

    msg = Message(f'{sname}: {ssubject}', sender = mailusername, recipients = [mailrecipient])
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
    validate(query, schema=schema)
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
    validate(query, schema=schema)
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
    validate(query, schema=schema)
    auth.isKeyValid(str(query.get('key')), str(query.get('token')))
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    if not coun_data:
        raise CustomError('Bad request, provided counselling name does not exist', 400)
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    counsellingdata = coun_col.find(db_query, {'_id': 0})
    retdat = []
    for cd in counsellingdata:
        retdat.append(cd)
    return {'data': retdat}
