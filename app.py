from flask import Flask, render_template, Response
from jsonschema import ValidationError
from core import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secretkey
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mailusername
app.config['MAIL_PASSWORD'] = mailpassword
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

with app.app_context():
    from api import api
    app.register_blueprint(api)

# Page routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/counsellingsearch/')
def counselSearch():
    return render_template('counsellingsearch.html')

@app.route('/collegesearch/')
def collegeSearch():
    return render_template('underconstruction.html')

@app.errorhandler(404)
def notfound(e):
    return Response(render_template('404.html'), 404)

@app.errorhandler(CustomError)
def customerr(e):
    return {'error': e.message}, e.status_code

@app.errorhandler(ValidationError)
def notvalid(e):
    return {'error': e.message}, 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)