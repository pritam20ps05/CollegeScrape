from core import *
from auth import *
from jsonschema import ValidationError
from flask import Flask, render_template, Response, session, redirect

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
    from auth import user_login

    app.register_blueprint(api)
    app.register_blueprint(user_login)

# Page routes
@app.route('/')
@loginhandler.handleLogin(loginrequired=False)
def home(userinfo):
    return render_template('home.html', user=userinfo)

@app.route('/counsellingsearch/')
@loginhandler.handleLogin(loginrequired=True)
def counselSearch(userinfo):
    return render_template('counsellingsearch.html', user=userinfo)

@app.route('/collegesearch/')
@loginhandler.handleLogin(loginrequired=True)
def collegeSearch(userinfo):
    return render_template('underconstruction.html', user=userinfo)

@app.errorhandler(404)
@loginhandler.handleLogin(loginrequired=False)
def notfound(userinfo, e):
    return Response(render_template('404.html', user=userinfo), 404)

@app.errorhandler(CustomError)
def customerr(e):
    return {'error': e.message}, e.status_code

@app.errorhandler(ValidationError)
def notvalid(e):
    return {'error': e.message}, 400

@app.errorhandler(LoginError)
def customerr(e):
    if e.method == 'GET':
        return redirect(e.getredirecturl)
    else:
        return {'error': e.message}, 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)