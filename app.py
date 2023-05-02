from os import environ
from flask import Flask, render_template, request, Response
import pymongo

client = pymongo.MongoClient(environ['MONGODB_URI'])
db = client.counselling
cdata_col = db.counsellingData
keydata = db.accKeys
app = Flask(__name__)


# Helper functions
def isQueryValid(query: dict, schema: dict):
    for property_name in schema:
        property_type = schema[property_name].split('|')
        isproptpresent = False
        for propt in property_type:
            if str(type(query.get(property_name))) == propt:
                isproptpresent = True
        if not isproptpresent:
            return False
    return True

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

# Page routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/counsellingsearch")
def counselSearch():
    return render_template('counsellingsearch.html')

@app.route("/collegesearch")
def collegeSearch():
    return render_template('collegesearch.html')

# API routes

@app.route("/api/counsellinginfo", methods=['POST'])
def counselinfo():
    query = request.get_json()
    counsellinginfo = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0, 'collection': 0})
    return counsellinginfo

@app.route("/api/institutetypefilter", methods=['POST'])
def insttfilter():
    schema = {
        'counsellingname': '<class \'str\'>',
        'roundNo': '<class \'int\'>',
        'instts': '<class \'list\'>'
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
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    if not (coun_data and isQueryValid(query, schema)):
        return 400
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    insts = coun_col.distinct('Institute', db_query)
    apns = coun_col.distinct('Academic Program Name', db_query)
    return {
        "Institutes": insts,
        "Academic Program Names": apns
    }

@app.route("/api/institutefilter", methods=['POST'])
def instfilter():
    schema = {
        'counsellingname': '<class \'str\'>',
        'roundNo': '<class \'int\'>',
        'instts': '<class \'list\'>',
        'insts': '<class \'list\'>'
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
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    if not (coun_data and isQueryValid(query, schema)):
        return 400
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    apns = coun_col.distinct('Academic Program Name', db_query)
    return {
        "Academic Program Names": apns
    }

@app.route("/api/authorize", methods=['POST'])
def authorize():
    key = request.get_json()['acckey']
    allowedKeys = keydata.distinct('key')
    if key in allowedKeys:
        return {
            "isValid": True,
            "error": ""
        }
    else:
        return {
            "isValid": False,
            "error": "Provided Access Key is not valid"
        }
    
@app.route("/api/counsellingdata", methods=['POST'])
def counseldata():
    schema = {
        'counsellingname': '<class \'str\'>',
        'roundNo': '<class \'int\'>', 
        'rank': '<class \'int\'>|<class \'NoneType\'>', 
        'rankBuff': '<class \'int\'>|<class \'NoneType\'>', 
        'instts': '<class \'list\'>', 
        'insts': '<class \'list\'>', 
        'apns': '<class \'list\'>', 
        'quotas': '<class \'list\'>', 
        'sts': '<class \'list\'>', 
        'gens': '<class \'list\'>', 
        'acckey': '<class \'str\'>'
    }
    allowedKeys = keydata.distinct('key')
    query = request.get_json()
    coun_data = cdata_col.find_one({'counselling': str(query.get('counsellingname'))}, {'_id': 0})
    if not (coun_data and isQueryValid(query, schema)):
        return 400
    elif str(query.get('acckey')) not in allowedKeys:
        return 403
    keydata.update_one({'key': str(query.get('acckey'))}, {'$inc': {'notu': 1}})
    coun_col = db[coun_data['collection']]
    db_query = dbQuery(query)
    counsellingdata = coun_col.find(db_query, {'_id': 0}, limit=500)
    retdat = []
    for cd in counsellingdata:
        retdat.append(cd)
    return {'data': retdat}

@app.errorhandler(404)
def not_found(e):
    return  Response(render_template("404.html"), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)