import pymongo
from core import *
from .utils import *
from flask_mail import Mail, Message
from flask import Blueprint, request, current_app

api = Blueprint('api', __name__, url_prefix='/api')

client = pymongo.MongoClient(mongouri)
db = client.counselling
cdata_col = db.counsellingData
mail = Mail(current_app)

# API routes
@api.route('/authorize', methods=['POST'])
def authorize():
    newkey = auth.genKey()
    return {
        'key': newkey
    }

@api.route('/contactus', methods=['POST'])
@validateSchema(schema_contactus, required=['name', 'email', 'subject', 'message', 'key', 'token'])
@authorizeToken
def contactus():
    query = request.get_json()
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
@validateSchema(schema_dbquery, required=['counsellingname'])
def counselinfo():
    query = request.get_json()
    counsellinginfo = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0, 'collection': 0})
    return counsellinginfo

@api.route('/institutetypefilter', methods=['POST'])
@validateSchema(schema_dbquery, required=['counsellingname', 'roundNo', 'instts', 'key', 'token'])
@authorizeToken
def insttfilter():
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
@validateSchema(schema_dbquery, required=['counsellingname', 'roundNo', 'instts', 'insts', 'key', 'token'])
@authorizeToken
def instfilter():
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
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    apns = coun_col.distinct('Academic Program Name', db_query)
    return {
        'Academic Program Names': apns
    }
    
@api.route('/counsellingdata', methods=['POST'])
@validateSchema(schema_dbquery, required=['counsellingname', 'roundNo', 'rank', 
                                           'rankBuff', 'instts', 'insts', 'apns', 
                                           'quotas', 'sts', 'gens', 'key', 'token'])
@authorizeToken
def counseldata():
    query = request.get_json()
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
